#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.import math

import math
import os
import glob
from enum import Enum

from PIL import Image
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED
from tempfile import TemporaryDirectory

from skytemple_files.common.util import simple_quant
from skytemple_files.common.xml_util import prettify
from skytemple_files.graphics.chara_wan.model import WanFile, SequenceFrame, FrameOffset, AnimStat, ImgPiece, \
    MetaFramePiece, MINUS_FRAME, DEBUG_PRINT, DIM_TABLE, TEX_SIZE
import skytemple_files.graphics.chara_wan.utils as exUtils
import skytemple_files.graphics.chara_wan.wan_utils as exWanUtils


DRAW_CENTER_X = 0
DRAW_CENTER_Y = -4

MAX_ANIMS = 44

ANIM_ORDER = [0, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20,
              21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43]


class FlipMode(Enum):
    # Image is unique / new
    NONE = 0
    # Image is an exact copy of another image
    COPY = 1
    # Image is a flipped copy of another image
    FLIP = 2


def ImportSheets(inDir, strict=False):

    if DEBUG_PRINT:
        if not os.path.isdir(os.path.join(inDir, '_pieces_in')):
            os.makedirs(os.path.join(inDir, '_pieces_in'))
        if not os.path.isdir(os.path.join(inDir, '_frames_in')):
            os.makedirs(os.path.join(inDir, '_frames_in'))

    anim_stats = {}
    anim_names = {}
    tree = ET.parse(os.path.join(inDir, 'AnimData.xml'))
    root = tree.getroot()
    sdwSize = int(root.find('ShadowSize').text)
    if sdwSize < 0 or sdwSize > 2:
        raise ValueError("Invalid shadow size: {0}".format(sdwSize))
    anims_node = root.find('Anims')
    for anim_node in anims_node.iter('Anim'):
        name = anim_node.find('Name').text
        index = -1
        index_node = anim_node.find('Index')
        if index_node is not None:
            index = int(index_node.text)
        backref_node = anim_node.find('CopyOf')
        if backref_node is not None:
            backref = backref_node.text
            anim_stat = AnimStat(index, name, None, backref)
        else:
            frame_width = anim_node.find('FrameWidth')
            frame_height = anim_node.find('FrameHeight')
            anim_stat = AnimStat(index, name, (int(frame_width.text), int(frame_height.text)), None)

            rush_frame = anim_node.find('RushFrame')
            if rush_frame is not None:
                anim_stat.rushFrame = int(rush_frame.text)
            hit_frame = anim_node.find('HitFrame')
            if hit_frame is not None:
                anim_stat.hitFrame = int(hit_frame.text)
            return_frame = anim_node.find('ReturnFrame')
            if return_frame is not None:
                anim_stat.returnFrame = int(return_frame.text)

            durations_node = anim_node.find('Durations')
            for dur_node in durations_node.iter('Duration'):
                duration = int(dur_node.text)
                anim_stat.durations.append(duration)

            anim_names[name.lower()] = index
            if index == -1 and strict:
                raise ValueError("{0} has its own sheet and does not have an index!".format(name))

        if index > -1:
            if index in anim_stats:
                raise ValueError("{0} and {1} both have the an index of {2}!".format(anim_stats[index].name, name, index))
            anim_stats[index] = anim_stat

    copy_indices = {}
    for idx in anim_stats:
        stat = anim_stats[idx]
        if stat.backref is not None:
            back_idx = anim_names[stat.backref.lower()]
            if back_idx not in copy_indices:
                copy_indices[back_idx] = []
            copy_indices[back_idx].append(idx)

    # read all sheets
    extra_sheets = []
    anim_sheets = {}
    for filepath in glob.glob(os.path.join(inDir, '*-Anim.png')):
        _, file = os.path.split(filepath)
        anim_parts = file.split('-')
        anim_name = anim_parts[0]
        if anim_name.lower() not in anim_names:
            extra_sheets.append(anim_name)
        else:
            index = anim_names[anim_name.lower()]
            del anim_names[anim_name.lower()]

            anim_img = Image.open(os.path.join(inDir, anim_name + '-Anim.png')).convert("RGBA")
            offset_img = Image.open(os.path.join(inDir, anim_name + '-Offsets.png')).convert("RGBA")
            shadow_img = Image.open(os.path.join(inDir, anim_name + '-Shadow.png')).convert("RGBA")

            anim_sheets[index] = (anim_img, offset_img, shadow_img, anim_name)

    # raise warning if there exist anim stats without anims, or anims without anim stats
    if len(anim_names) > 0:
        orphans = []
        for k in anim_names:
            orphans.append(k)
        raise ValueError("Xml found with no sheet: {0}".format(', '.join(orphans)))
    if len(extra_sheets) > 0:
        raise ValueError("Sheet found with no xml: {0}".format(', '.join(extra_sheets)))

    animGroupData = []
    frames = []
    frameToSequence = []
    for idx in range(MAX_ANIMS):
        if idx in anim_sheets:
            anim_img, offset_img, shadow_img, anim_name = anim_sheets[idx]
            tileSize = anim_stats[idx].size
            durations = anim_stats[idx].durations

            # check against inconsistent sizing
            if anim_img.size != offset_img.size or anim_img.size != shadow_img.size:
                raise ValueError("Anim, Offset, and Shadow sheets for {0} must be the same size!".format(anim_name))

            if anim_img.size[0] % tileSize[0] != 0 or anim_img.size[1] % tileSize[1] != 0:
                raise ValueError("Sheet for {4} is {0}x{1} pixels and is not divisible by {2}x{3} in xml!".format(
                    anim_img.size[0], anim_img.size[1], tileSize[0], tileSize[1], anim_name))

            total_frames = anim_img.size[0] // tileSize[0]
            # check against inconsistent duration counts
            if total_frames != len(durations):
                raise ValueError("Number of frames in {0} does not match count of durations ({1}) specified in xml!".format(anim_name, len(durations)))

            if anim_stats[idx].rushFrame >= len(durations):
                raise ValueError("RushFrame of {0} is greater than the number of frames ({1}) in {2}!".format(anim_stats[idx].rushFrame, len(durations), anim_name))
            if anim_stats[idx].hitFrame >= len(durations):
                raise ValueError("HitFrame of {0} is greater than the number of frames ({1}) in {2}!".format(anim_stats[idx].hitFrame, len(durations), anim_name))
            if anim_stats[idx].returnFrame >= len(durations):
                raise ValueError("ReturnFrame of {0} is greater than the number of frames ({1}) in {2}!".format(anim_stats[idx].returnFrame, len(durations), anim_name))

            group = []
            total_dirs = anim_img.size[1] // tileSize[1]
            for dir in range(8):
                if dir >= total_dirs:
                    break
                sequence = []
                for jj in range(anim_img.size[0] // tileSize[0]):
                    rel_center = (tileSize[0] // 2 - DRAW_CENTER_X, tileSize[1] // 2 - DRAW_CENTER_Y)
                    tile_rect = (jj * tileSize[0], dir * tileSize[1], tileSize[0], tileSize[1])
                    tile_bounds = (tile_rect[0], tile_rect[1], tile_rect[0] + tile_rect[2], tile_rect[1] + tile_rect[3])
                    bounds = exUtils.getCoveredBounds(anim_img, tile_bounds)
                    emptyBounds = False
                    if bounds[0] >= bounds[2]:
                        bounds = (rel_center[0], rel_center[1], rel_center[0]+1, rel_center[1]+1)
                        emptyBounds = True
                    rect = (bounds[0], bounds[1], bounds[2] - bounds[0], bounds[3] - bounds[1])
                    abs_bounds = exUtils.addToBounds(bounds, (tile_rect[0], tile_rect[1]))
                    frame_tex = anim_img.crop(abs_bounds)

                    shadow_offset = exUtils.getOffsetFromRGB(shadow_img, tile_bounds, False, False, False, False, True)
                    frame_offset = exUtils.getOffsetFromRGB(offset_img, tile_bounds, True, True, True, True, False)
                    offsets = FrameOffset(None, None, None, None)
                    if frame_offset[2] is None:
                        # raise warning if there's missing shadow or offsets
                        if strict:
                            raise ValueError("No frame offset found in frame {0} for {1}".format((jj, dir), anim_name))
                        offsets = FrameOffset(rel_center, rel_center, rel_center, rel_center)
                    else:
                        offsets.center = frame_offset[2]
                        if frame_offset[0] is None:
                            offsets.head = frame_offset[2]
                        else:
                            offsets.head = frame_offset[0]
                        offsets.lhand = frame_offset[1]
                        offsets.rhand = frame_offset[3]
                    offsets.AddLoc((-rect[0], -rect[1]))

                    shadow = rel_center
                    if shadow_offset[4] is not None:
                        shadow = shadow_offset[4]
                    elif strict:
                        raise ValueError("No shadow offset found in frame {0} for {1}".format((jj, dir), anim_name))
                    shadow_diff = exUtils.addLoc(shadow, rect, True)
                    shadow = exUtils.addLoc(shadow, rel_center, True)

                    if emptyBounds and shadow_offset[4] is None and frame_offset[2] is None:
                        continue

                    frames.append((frame_tex, offsets, shadow_diff))
                    frame = SequenceFrame(-1, durations[jj], 0, shadow, shadow)
                    if anim_stats[idx].rushFrame == jj:
                        frame.SetRushPoint(True)
                    if anim_stats[idx].hitFrame == jj:
                        frame.SetHitPoint(True)
                    if anim_stats[idx].returnFrame == jj:
                        frame.SetReturnPoint(True)

                    sequence.append(frame)
                    frameToSequence.append((idx, dir, jj))

                group.append(sequence)

            animGroupData.append(group)
        else:
            animGroupData.append([])

    # get all unique frames and map them to the animations
    # same with shadows and offsets
    frame_map = [None] * len(frames)
    final_frames = []
    mapDuplicateImportImgs(frames, final_frames, frame_map)

    # center the frame based on shadow placements
    reverse_frame_map = {}
    for idx, mapping in enumerate(frame_map):
        dest = mapping[0]
        if dest not in reverse_frame_map:
            reverse_frame_map[dest] = []
        reverse_frame_map[dest].append(idx)

    for key in reverse_frame_map:
        shadow_diffs = []
        for start in reverse_frame_map[key]:
            new_diff = frames[start][2]
            shadow_diffs.append(new_diff)
        # choose the mode?  median? as the true offset
        freq = {}
        for diff in shadow_diffs:
            if diff not in freq:
                freq[diff] = 0
            freq[diff] += 1
        chosen_diff = shadow_diffs[0]
        for diff in freq:
            if freq[diff] > freq[chosen_diff]:
                chosen_diff = diff
        # now that we have our chosen diff
        # set the frame in final_frames to the chosen diff
        final_frames[key] = (final_frames[key][0], final_frames[key][1], chosen_diff, final_frames[key][3], final_frames[key][4])
        # and then set the diff mapping to their shadow diff - chosen diff
        for start in reverse_frame_map[key]:
            frame_map[start] = (frame_map[start][0], exUtils.addLoc(chosen_diff, frames[start][2], True))
        # now, the frame will treat chosenDiff as its center
        # and all diffs will be applied to the offsets of the currently created animGroups

    # final_frames is now a list of unique graphics where flips are treated as separate but refer to the originals
    # now, create metaframes and image data
    # palette is needed first.  get palette data

    # use tilequant to modify all anim images at once and force to 16 colors or less (including transparent)
    # first, generate an image containing all frames in final_frames

    max_width = 0
    max_height = 0
    for frame in final_frames:
        frame_tex = frame[0]
        max_width = max(max_width, frame_tex.size[0])
        max_height = max(max_height, frame_tex.size[1])

    max_width = exUtils.roundUpToMult(max_width, 2)
    max_height = exUtils.roundUpToMult(max_height, 2)

    max_tiles = int(math.ceil(math.sqrt(len(final_frames))))
    combinedImg = Image.new('RGBA', (max_tiles * max_width, max_tiles * max_height), (0, 0, 0, 0))

    crop_bounds = []
    for idx, frame in enumerate(final_frames):
        frame_tex = frame[0]
        round_width = exUtils.roundUpToMult(frame_tex.size[0], 2)
        round_height = exUtils.roundUpToMult(frame_tex.size[1], 2)
        tile_pos = (idx % max_tiles * max_width, idx // max_tiles * max_height)
        paste_bounds = (tile_pos[0] + (max_width - round_width) // 2,
                        tile_pos[1] + (max_height - round_height) // 2,
                        tile_pos[0] + (max_width - round_width) // 2 + frame_tex.size[0],
                        tile_pos[1] + (max_height - round_height) // 2 + frame_tex.size[1])
        crop_bounds.append(paste_bounds)
        combinedImg.paste(frame_tex, paste_bounds, frame_tex)

    colors = combinedImg.getcolors()

    if strict and len(colors) > 16:
        raise ValueError("Number of (nontransparent) colors over 15: {0}".format(len(colors)))

    transparent = (0, 127, 151, 255)
    foundTrans = True
    while foundTrans:
        foundTrans = False
        for count, color in colors:
            if color == transparent:
                transparent = (0, 127, transparent[3] - 1, 255)
                foundTrans = True
                break

    datas = combinedImg.getdata()
    return_datas = []
    for idx in range(len(datas)):
        if datas[idx][3] == 0:
            return_datas.append(transparent)
        else:
            return_datas.append(datas[idx])
    combinedImg.putdata(return_datas)

    # TODO: wan can actually handle more than 16 colors so long as a single image piece itself only has 16 colors
    # to actually allow over 16 colors, an algorithm would be needed to get the color list for every individual frame
    # and then combine the color lists such that there are as few distinct palettes as possible
    # and that no palettes have over 16 colors (transparency included)

    # then, run through simple_quant
    reducedImg = simple_quant(combinedImg).convert("RGBA")

    datas = reducedImg.getdata()
    for idx in range(len(datas)):
        if return_datas[idx] != transparent:
            return_datas[idx] = datas[idx]
    reducedImg.putdata(return_datas)

    palette = reducedImg.getcolors()
    palette_map = {}
    singlePalette = []
    for count, rgba in palette:
        palette_map[rgba] = len(singlePalette)
        singlePalette.append(rgba)

        # transparent is always 0
        if rgba == transparent:
            prev_zero = singlePalette[0]
            singlePalette[0] = rgba
            singlePalette[-1] = prev_zero
            palette_map[prev_zero] = palette_map[rgba]
            palette_map[rgba] = 0

    # then, cut up the image and return to the original final_frames
    for idx in range(len(final_frames)):
        frame_tex, offsets, shadow_diff, flip, flip_mode = final_frames[idx]
        frame_tex = reducedImg.crop(crop_bounds[idx])
        final_frames[idx] = (frame_tex, offsets, shadow_diff, flip, flip_mode)

    while len(singlePalette) < 16:
        singlePalette.append((32, 169, 32, 255))
        singlePalette.append((65, 117, 100, 255))
        singlePalette.append((105, 110, 111, 255))
        singlePalette.append((32, 50, 48, 255))
        singlePalette.append((50, 49, 32, 255))
        while len(singlePalette) > 16:
            singlePalette.pop()

    # create imgData, metaframe data, and offset data
    imgData = []
    frameData = []
    offsetData = []
    for idx, frame in enumerate(final_frames):
        if DEBUG_PRINT:
            frame[0].save(os.path.join(inDir, '_frames_in', 'F-' + format(idx, '02d') + '.png'))

        shadow_diff = frame[2]
        flip = frame[3]
        if flip > -1:
            flipped_frame = frameData[flip]
            addFlippedImgData(frame[4], frameData, flipped_frame, final_frames[flip], frame)
        else:
            # will append to imgData and frameData
            addImgData(imgData, frameData, palette_map, transparent, frame)
        offsets = frame[1]
        offsets.AddLoc((-shadow_diff[0], -shadow_diff[1]))
        offsetData.append(offsets)


    # apply the mappings to the animations, correcting the frame indices and shadow offsets
    for idx, frame in enumerate(frames):
        frame_seq_mapping = frameToSequence[idx]
        group = animGroupData[frame_seq_mapping[0]]
        sequence = group[frame_seq_mapping[1]]
        animFrame = sequence[frame_seq_mapping[2]]
        mapFrame = frame_map[idx]
        animFrame.frameIndex = mapFrame[0]
        shadow_diff = mapFrame[1]
        animFrame.offset = exUtils.addLoc(animFrame.offset, shadow_diff)

    for idx in copy_indices:
        copies = copy_indices[idx]
        for copy_idx in copies:
            animGroupData[copy_idx] = exWanUtils.duplicateAnimGroup(animGroupData[idx])

    wan = WanFile()
    wan.imgData = imgData
    wan.frameData = frameData
    wan.animGroupData = animGroupData
    wan.offsetData = offsetData
    wan.customPalette = [singlePalette]
    wan.sdwSize = sdwSize
    # return the wan file
    return wan


def ImportSheetsFromZip(zipFile, strict=False):
    with TemporaryDirectory() as tmp_dir:
        with ZipFile(zipFile, 'r') as zipObj:
            zipObj.extractall(tmp_dir)
        wan = ImportSheets(tmp_dir, strict)
    return wan


def ExportSheets(outDir, sdwImg, wan, anim_name_map):


    if not os.path.isdir(outDir):
        os.makedirs(outDir)

    if DEBUG_PRINT:
        if not os.path.isdir(os.path.join(outDir, '_pieces')):
            os.makedirs(os.path.join(outDir, '_pieces'))
        if not os.path.isdir(os.path.join(outDir, '_frames')):
            os.makedirs(os.path.join(outDir, '_frames'))

    anim_stats = []
    maxFrameBounds = (10000, 10000, -10000, -10000)
    # get max bounds across all frames
    for idx, metaFrame in enumerate(wan.frameData):
        for mt_idx, metaFramePiece in enumerate(metaFrame):
            # update bounds based on image
            fBounds = metaFramePiece.GetBounds()
            maxFrameBounds = exUtils.combineExtents(maxFrameBounds, fBounds)

        # update bounds based on offsets
        offset = wan.offsetData[idx]
        maxFrameBounds = exUtils.combineExtents(maxFrameBounds, offset.GetBounds())

    # round up to nearest x8
    maxFrameBounds = exUtils.centerBounds(maxFrameBounds, (DRAW_CENTER_X, DRAW_CENTER_Y))
    maxFrameBounds = exUtils.roundUpBox(maxFrameBounds)

    # create all frames, and visual representation of offsets tied to each frame
    frames = []
    offsets = []
    frames_bounds_tight = []
    piece_imgs = {}
    for idx, metaFrame in enumerate(wan.frameData):
        has_minus = False
        draw_queue = []
        for mt_idx, metaFramePiece in enumerate(metaFrame):
            # create the piece
            parent_idx = MINUS_FRAME
            if metaFramePiece.imgIndex == MINUS_FRAME:
                has_minus = True
                prev_idx = mt_idx - 1
                while metaFrame[prev_idx].imgIndex == MINUS_FRAME or metaFrame[
                    prev_idx].getTileNum() != metaFramePiece.getTileNum():
                    prev_idx = prev_idx - 1
                parent_idx = metaFrame[prev_idx].imgIndex
            else:
                parent_idx = metaFramePiece.imgIndex

            if parent_idx in piece_imgs:
                img = piece_imgs[parent_idx]
            else:
                img = metaFramePiece.GeneratePiece(wan.imgData, wan.customPalette, parent_idx)
                piece_imgs[parent_idx] = img
            draw_queue.append((img, metaFramePiece))

        # create an image to represent the full metaFrameGroup
        groupImg = Image.new('RGBA', (maxFrameBounds[2] - maxFrameBounds[0], maxFrameBounds[3] - maxFrameBounds[1]),
                             (0, 0, 0, 0))
        while len(draw_queue) > 0:
            img, metaFramePiece = draw_queue.pop()
            metaFramePiece.DrawOn(groupImg, img, (maxFrameBounds[0], maxFrameBounds[1]))
        if DEBUG_PRINT:
            groupImg.save(os.path.join(outDir, '_frames', 'F-' + format(idx, '02d') + '.png'))
        frames.append(groupImg)

        # create an image for particle offsets
        particleImg = Image.new('RGBA', (maxFrameBounds[2] - maxFrameBounds[0], maxFrameBounds[3] - maxFrameBounds[1]),
                                (0, 0, 0, 0))
        offset = wan.offsetData[idx]
        offset.DrawOn(particleImg, (maxFrameBounds[0], maxFrameBounds[1]))
        if DEBUG_PRINT:
            particleImg.save(os.path.join(outDir, '_frames', 'F-' + format(idx, '02d') + '-Offsets.png'))
        offsets.append(particleImg)

        # create a tighter bounds representation of the frame, down to the pixel
        frame_rect = exUtils.getCoveredBounds(groupImg)
        frame_rect = exUtils.addToBounds(frame_rect, maxFrameBounds)
        frame_rect = exUtils.combineExtents(frame_rect, offset.GetBounds())
        frames_bounds_tight.append(frame_rect)

    if DEBUG_PRINT:
        for piece_idx in piece_imgs:
            img = piece_imgs[piece_idx]
            img.save(os.path.join(outDir, '_pieces', 'P-' + format(piece_idx, '03d') + '.png'))

    # get max bounds for all animations
    groupBounds = []
    shadow_rect = (sdwImg.size[0] // -2, sdwImg.size[1] // -2, sdwImg.size[0] // 2, sdwImg.size[1] // 2)
    shadow_rect_tight = exUtils.getCoveredBounds(sdwImg)
    shadow_rect_tight = exUtils.addToBounds(shadow_rect_tight, shadow_rect)
    for idx, animGroup in enumerate(wan.animGroupData):

        maxBounds = (10000, 10000, -10000, -10000)
        for g_idx, singleAnim in enumerate(animGroup):
            for a_idx, animFrame in enumerate(singleAnim):
                frame_rect = frames_bounds_tight[animFrame.frameIndex]
                frameBounds = exUtils.addToBounds(frame_rect, animFrame.offset)
                maxBounds = exUtils.combineExtents(maxBounds, frameBounds)
                shadowBounds = exUtils.addToBounds(shadow_rect_tight, animFrame.shadow)
                maxBounds = exUtils.combineExtents(maxBounds, shadowBounds)
        # round up to nearest x8
        maxBounds = exUtils.centerBounds(maxBounds, (DRAW_CENTER_X, DRAW_CENTER_Y))
        maxBounds = exUtils.roundUpBox(maxBounds)
        groupBounds.append(maxBounds)

    # create animations
    for idx, animGroup in enumerate(wan.animGroupData):
        animsPerGroup = len(animGroup)
        # some groups may be empty
        if animsPerGroup == 0:
            continue

        if idx >= len(anim_name_map) or anim_name_map[idx][0] == '':
            raise ValueError("Animation #{0} needs a name!".format(idx))

        dupe_idx = -1
        for cmp_idx in ANIM_ORDER:
            if cmp_idx == idx:
                break
            cmp_group = wan.animGroupData[cmp_idx]
            if exWanUtils.animGroupsEqual(animGroup, cmp_group):
                dupe_idx = cmp_idx
                break

        if dupe_idx > -1:
            anim_stats.append(AnimStat(idx, anim_name_map[idx][0], None, anim_name_map[dupe_idx][0]))
            for extra_idx in range(1, len(anim_name_map[idx])):
                anim_stats.append(AnimStat(-1, anim_name_map[idx][extra_idx], None, anim_name_map[dupe_idx][0]))
            continue

        maxBounds = groupBounds[idx]
        maxSize = (maxBounds[2] - maxBounds[0], maxBounds[3] - maxBounds[1])
        new_stat = AnimStat(idx, anim_name_map[idx][0], maxSize, None)

        framesPerAnim = 0
        for g_idx, singleAnim in enumerate(animGroup):
            framesPerAnim = max(framesPerAnim, len(singleAnim))

        animImg = Image.new('RGBA', (maxSize[0] * framesPerAnim, maxSize[1] * animsPerGroup), (0, 0, 0, 0))
        particleImg = Image.new('RGBA', (maxSize[0] * framesPerAnim, maxSize[1] * animsPerGroup), (0, 0, 0, 0))
        shadowImg = Image.new('RGBA', (maxSize[0] * framesPerAnim, maxSize[1] * animsPerGroup), (0, 0, 0, 0))
        for g_idx, singleAnim in enumerate(animGroup):
            for a_idx, animFrame in enumerate(singleAnim):
                if a_idx >= len(new_stat.durations):
                    new_stat.durations.append(animFrame.duration)
                if animFrame.IsRushPoint():
                    new_stat.rushFrame = a_idx
                if animFrame.IsHitPoint():
                    new_stat.hitFrame = a_idx
                if animFrame.IsReturnPoint():
                    new_stat.returnFrame = a_idx

                frameImg = frames[animFrame.frameIndex]
                tilePos = (a_idx * maxSize[0], g_idx * maxSize[1])
                pastePos = (tilePos[0] - maxBounds[0] + maxFrameBounds[0] + animFrame.offset[0],
                            tilePos[1] - maxBounds[1] + maxFrameBounds[1] + animFrame.offset[1])
                animImg.paste(frameImg, pastePos, frameImg)
                offsetImg = offsets[animFrame.frameIndex]
                particleImg.paste(offsetImg, pastePos, offsetImg)

                shadowBounds = exUtils.addToBounds(shadow_rect, animFrame.shadow)
                shadowPastePos = (tilePos[0] - maxBounds[0] + shadowBounds[0],
                                  tilePos[1] - maxBounds[1] + shadowBounds[1])
                shadowImg.paste(sdwImg, shadowPastePos, sdwImg)
        animImg.save(os.path.join(outDir, new_stat.name + '-Anim.png'))
        particleImg.save(os.path.join(outDir, new_stat.name + '-Offsets.png'))
        shadowImg.save(os.path.join(outDir, new_stat.name + '-Shadow.png'))

        for extra_idx in range(1, len(anim_name_map[idx])):
            anim_stats.append(AnimStat(-1, anim_name_map[idx][extra_idx], None, anim_name_map[idx][0]))
        anim_stats.append(new_stat)

    # export the xml
    root = ET.Element("AnimData")
    shadow_node = ET.SubElement(root, "ShadowSize")
    shadow_node.text = str(wan.sdwSize)

    anims_node = ET.SubElement(root, "Anims")
    for stat in anim_stats:
        anim_node = ET.SubElement(anims_node, "Anim")
        name_node = ET.SubElement(anim_node, "Name")
        name_node.text = stat.name
        if stat.index > -1:
            index_node = ET.SubElement(anim_node, "Index")
            index_node.text = str(stat.index)
        if stat.backref is not None:
            backref_node = ET.SubElement(anim_node, "CopyOf")
            backref_node.text = stat.backref
        else:
            frame_width = ET.SubElement(anim_node, "FrameWidth")
            frame_width.text = str(stat.size[0])
            frame_height = ET.SubElement(anim_node, "FrameHeight")
            frame_height.text = str(stat.size[1])
            if stat.rushFrame > -1:
                rush_frame = ET.SubElement(anim_node, "RushFrame")
                rush_frame.text = str(stat.rushFrame)
            if stat.hitFrame > -1:
                hit_frame = ET.SubElement(anim_node, "HitFrame")
                hit_frame.text = str(stat.hitFrame)
            if stat.returnFrame > -1:
                return_frame = ET.SubElement(anim_node, "ReturnFrame")
                return_frame.text = str(stat.returnFrame)
            durations_node = ET.SubElement(anim_node, "Durations")
            for duration in stat.durations:
                dur_node = ET.SubElement(durations_node, "Duration")
                dur_node.text = str(duration)

    with open(os.path.join(outDir, 'AnimData.xml'), 'w') as f:
        f.write(prettify(root))


def ExportSheetsAsZip(zipFile, sdwImg, wan, anim_name_map):
    with TemporaryDirectory() as tmp_dir:
        ExportSheets(tmp_dir, sdwImg, wan, anim_name_map)
        with ZipFile(zipFile, 'w') as ZipObj:
            abs_src = os.path.abspath(tmp_dir)
            for dirname, subdirs, files in os.walk(tmp_dir):
                for filename in files:
                    # Avoid absolute path creation
                    absname = os.path.abspath(os.path.join(dirname, filename))
                    arcname = absname[len(abs_src) + 1:]
                    ZipObj.write(absname, arcname)


def mapDuplicateImportImgs(imgs, final_imgs, img_map):
    for idx, img in enumerate(imgs):
        dupe = False
        flip = -1
        flip_mode = FlipMode.NONE
        for final_idx, final_img in enumerate(final_imgs):
            imgs_equal = exUtils.imgsEqual(final_img[0], img[0])
            # if offsets are not synchronized, they are counted as different
            if imgs_equal:
                imgs_equal = exUtils.offsetsEqual(final_img[1], img[1], img[0].size[0])
                if imgs_equal:
                    img_map[idx] = (final_idx, (0, 0))
                    dupe = True
                    break
                else:
                    flip_mode = FlipMode.COPY
                    flip = final_idx
            else:
                imgs_flip = exUtils.imgsEqual(final_img[0], img[0], True)
                if imgs_flip:
                    imgs_flip = exUtils.offsetsEqual(final_img[1], img[1], img[0].size[0], True)
                if imgs_flip:
                    flip_mode = FlipMode.FLIP
                    flip = final_idx

        if not dupe:
            img_map[idx] = (len(final_imgs), (0, 0))
            final_imgs.append((img[0], img[1], img[2], flip, flip_mode))


def addFlippedImgData(flipMode: FlipMode, frameData, metaFrame, old_frame, new_frame):
    x_border = old_frame[2][0]
    newMetaFrame = []
    for piece in metaFrame:
        newPiece = MetaFramePiece(piece.imgIndex, piece.attr0, piece.attr1, piece.attr2)
        if flipMode == FlipMode.FLIP:
            newPiece.setHFlip(True)
            # move the piece in the reflected position.
            range = newPiece.GetBounds()
            endX = range[2]
            origEndX = x_border + endX
            flipStartX = -origEndX + old_frame[0].size[0]
            newX = flipStartX - x_border
            newPiece.setXOffset(newX)
        newMetaFrame.append(newPiece)

    # regardless of flip, the center point may be treated differently between frames.  correct it.
    point_diff = exUtils.addLoc(new_frame[2], old_frame[2], True)
    # add it to all metaframe components
    for piece in newMetaFrame:
        new_offset = (piece.getXOffset() - point_diff[0], piece.getYOffset() - point_diff[1])
        piece.setXOffset(new_offset[0])
        piece.setYOffset(new_offset[1])
    frameData.append(newMetaFrame)


def addImgData(imgData, frameData, palette_map, transparent, frame):
    img = frame[0]
    pt_zero = frame[2]
    # chop the frames into images and metaframes - need psy's algorithm for this
    piece_locs = chopImgToPieceLocs(img, transparent)

    metaFrame = []
    # create new metaframe piece data from the pieces
    cur_tile = 0
    for idx, piece_loc in enumerate(piece_locs):
        piece = piece_loc[0]
        loc = piece_loc[1]
        metaFramePiece = MetaFramePiece(len(imgData) + idx, 0, 0, 0)
        # set coordinates
        result_loc = exUtils.addLoc(loc, pt_zero, True)
        metaFramePiece.setXOffset(result_loc[0])
        metaFramePiece.setYOffset(result_loc[1])
        # set dimensions
        block_size = (piece.size[0] // TEX_SIZE, piece.size[1] // TEX_SIZE)
        res_type = DIM_TABLE.index(block_size)
        metaFramePiece.setResolutionType(res_type)
        # set RnS parameter - always true when not disabled; when reading in we are never disabled
        metaFramePiece.setRotAndScalingOn(True)
        # set tile index
        metaFramePiece.setTileNum(cur_tile)
        # priority is ALWAYS 3
        metaFramePiece.setPriority(3)
        # set last if this is the last
        if idx == len(piece_locs) - 1:
            metaFramePiece.setIsLast(True)

        metaFrame.append(metaFramePiece)
        # increase tile index
        blocks_occupied = max(1, block_size[0] * block_size[1] // 4)
        cur_tile += blocks_occupied
    frameData.append(metaFrame)

    # add each piece
    for piece, _ in piece_locs:
        imgStrip = convertPieceToImgStrip(piece, palette_map)
        imgData.append(imgStrip)

def convertPieceToImgStrip(piece, palette_map):
    imgPx = []
    datas = piece.getdata()
    for yy in range(0, piece.size[1], TEX_SIZE):
        for xx in range(0, piece.size[0], TEX_SIZE):
            for py in range(TEX_SIZE):
                for px in range(TEX_SIZE):
                    imgPos = (xx + px, yy + py)
                    color = datas[imgPos[1] * piece.size[0] + imgPos[0]]
                    color_idx = palette_map[color]
                    imgPx.append(color_idx)
    # merge 4bpp pixels into single bytes
    imgPx4bpp = []
    for px_idx in range(0, len(imgPx), 2):
        px_low = imgPx[px_idx]
        px_hi = imgPx[px_idx + 1]
        px = px_hi * 16 + px_low
        imgPx4bpp.append(px)
    # chop into zeroes and strips
    strips = []
    cur_strip = []
    prevZero = None
    for block in range(0, len(imgPx4bpp), 32):
        allZero = True
        for idx in range(32):
            if imgPx4bpp[block + idx] != 0:
                allZero = False
                break
        if allZero != prevZero:
            strips.append(cur_strip)
            cur_strip = []
        cur_strip.extend(imgPx4bpp[block:block + 32])
        prevZero = allZero
    # add the pending strip
    strips.append(cur_strip)
    # remove the definitively empty strip
    strips.pop(0)
    imgStrip = ImgPiece()
    imgStrip.imgPx = strips
    return imgStrip

def chopImgToPieceLocs(img, transparent):
    chopped_imgs = []
    smallest_dim = 3
    for idx, dim in enumerate(DIM_TABLE):
        if img.size[0] <= dim[0] * TEX_SIZE and img.size[1] <= dim[1] * TEX_SIZE:
            if dim[0] * dim[1] < DIM_TABLE[smallest_dim][0] * DIM_TABLE[smallest_dim][1]:
                smallest_dim = idx
    if img.size[0] > 8 * TEX_SIZE or img.size[1] > 8 * TEX_SIZE:
        roundUp = (exUtils.roundUpToMult(img.size[0], TEX_SIZE), exUtils.roundUpToMult(img.size[1], TEX_SIZE))
        fullImg = Image.new('RGBA', roundUp, transparent)
        fullImg.paste(img, (0, 0), img)

        yy = 0
        total_size = 0
        while yy < roundUp[1]:
            addy = TEX_SIZE * 4
            while yy + addy > roundUp[1]:
                addy //= 2
            xx = 0
            while xx < roundUp[0]:
                addx = TEX_SIZE * 4
                while xx + addx > roundUp[0]:
                    addx //= 2
                bounds = (xx, yy, xx + addx, yy + addy)
                cutImg = fullImg.crop(bounds)
                chopped_imgs.append((cutImg, (xx,yy)))
                total_size += max(1, addx * addy // TEX_SIZE // TEX_SIZE // 4)
                xx += addx
            yy += addy

        # print("Size: {0}".format(total_size))
    else:
        newWidth = DIM_TABLE[smallest_dim][0] * TEX_SIZE
        newHeight = DIM_TABLE[smallest_dim][1] * TEX_SIZE
        newImg = Image.new('RGBA', (newWidth, newHeight), transparent)
        newImg.paste(img, (0, 0), img)
        chopped_imgs.append((newImg, (0, 0)))
    return chopped_imgs

