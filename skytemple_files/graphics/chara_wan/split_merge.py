#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.

import skytemple_files.graphics.chara_wan.wan_utils as exWanUtils
from skytemple_files.graphics.chara_wan.model import WanFile, MINUS_FRAME


def MergeWan(wan_files):

    # custom palettes are always the same
    sdwSize = wan_files[0].sdwSize
    customPalette = wan_files[0].customPalette
    # merge all pieces and remap the frames that reference them
    imgData = []
    for wan in wan_files:
        mapImgData(wan.imgData, imgData, wan.frameData)

    # merge all frames and remap the animations that reference them
    frameData = []
    offsetData = []
    for wan in wan_files:
        mapFrameData(wan.frameData, frameData, wan.offsetData, offsetData, wan.animGroupData)

    # merge all anim groups - if multiple sources have an anim on the same index, choose any.
    # theyre proven all the same
    animGroupData = []
    max_anims = 0
    for wan in wan_files:
        max_anims = max(max_anims, len(wan.animGroupData))

    for ii in range(max_anims):
        animGroupData.append([])
        for wan in wan_files:
            if ii < len(wan.animGroupData) and len(wan.animGroupData[ii]) > 0:
                animGroupData[ii] = wan.animGroupData[ii]

    wan = WanFile()
    wan.imgData = imgData
    wan.frameData = frameData
    wan.animGroupData = animGroupData
    wan.offsetData = offsetData
    wan.customPalette = customPalette
    wan.sdwSize = sdwSize
    return wan


def SplitWan(wan, anim_presence):
    wan_files = []
    for anim_list in anim_presence:

        animGroupData = []
        for anim_idx, anim_group in enumerate(anim_list):
            if not anim_group:
                animGroupData.append([])
            elif anim_idx < len(wan.animGroupData):
                new_anim = exWanUtils.duplicateAnimGroup(wan.animGroupData[anim_idx])
                animGroupData.append(new_anim)
            else:
                animGroupData.append([])
        frameData = []
        offsetData = []
        # adds only necessary frames to frameData, and remaps frame references in animGroupData
        # offset data included
        transferStrippedFrameData(wan.frameData, frameData, wan.offsetData, offsetData, animGroupData)
        # add only necessary pieces to imgData, and remaps the image piece references in frameData
        imgData = []
        transferStrippedImgData(wan.imgData, imgData, frameData)

        new_wan = WanFile()
        new_wan.imgData = imgData
        new_wan.frameData = frameData
        new_wan.animGroupData = animGroupData
        new_wan.offsetData = offsetData
        new_wan.customPalette = wan.customPalette
        new_wan.sdwSize = wan.sdwSize
        wan_files.append(new_wan)
    return wan_files


def mapImgData(inputImgData, imgData, frameData):
    mapping = {}
    for idx, img in enumerate(inputImgData):
        dupe_idx = -1
        for check_idx, check_img in enumerate(imgData):
            imgs_equal = True
            # perform a check to see if they're equal
            if len(img.imgPx) == len(check_img.imgPx):
                for ii in range(len(img.imgPx)):
                    if len(img.imgPx[ii]) == len(check_img.imgPx[ii]):
                        for jj in range(len(img.imgPx[ii])):
                            if img.imgPx[ii][jj] != check_img.imgPx[ii][jj]:
                                imgs_equal = False
                                break
                    else:
                        imgs_equal = False

                    if not imgs_equal:
                        break
            else:
                imgs_equal = False

            if imgs_equal:
                dupe_idx = check_idx
                break
        if dupe_idx > -1:
            mapping[idx] = dupe_idx
        else:
            mapping[idx] = len(imgData)
            imgData.append(img)

    for frame in frameData:
        for piece in frame:
            if piece.imgIndex != MINUS_FRAME:
                piece.imgIndex = mapping[piece.imgIndex]


def mapFrameData(inputFrameData, frameData, inputOffsetData, offsetData, animGroupData):
    mapping = {}
    for idx, frame in enumerate(inputFrameData):
        dupe_idx = -1
        for check_idx, check_frame in enumerate(frameData):
            frames_equal = True

            # perform a check to see if they're equal
            if len(frame) == len(check_frame):
                for ii in range(len(frame)):
                    if frame[ii].imgIndex != check_frame[ii].imgIndex or frame[ii].attr0 != check_frame[ii].attr0 \
                            or frame[ii].attr1 != check_frame[ii].attr1 or frame[ii].attr2 != check_frame[ii].attr2:
                        frames_equal = False
                        break
            else:
                frames_equal = False

            if frames_equal:
                dupe_idx = check_idx
                break
        if dupe_idx > -1:
            mapping[idx] = dupe_idx
        else:
            mapping[idx] = len(frameData)
            frameData.append(frame)
            offsetData.append(inputOffsetData[idx])

    for animGroup in animGroupData:
        for anim in animGroup:
            for animFrame in anim:
                animFrame.frameIndex = mapping[animFrame.frameIndex]


def transferStrippedFrameData(inputFrameData, frameData, inputOffsetData, offsetData, animGroupData):
    frame_map = {}
    for anim_group in animGroupData:
        for anim_seq in anim_group:
            for frame in anim_seq:
                frame_idx = frame.frameIndex
                if frame_idx not in frame_map:
                    frame_map[frame_idx] = len(frameData)
                    frameData.append(exWanUtils.duplicateMetaFrame(inputFrameData[frame_idx]))
                    offsetData.append(exWanUtils.duplicateOffset(inputOffsetData[frame_idx]))
                frame.frameIndex = frame_map[frame_idx]

def transferStrippedImgData(inputImgData, imgData, frameData):
    img_map = {}
    for metaFrame in frameData:
        for piece in metaFrame:
            piece_idx = piece.imgIndex
            if piece_idx not in img_map:
                img_map[piece_idx] = len(imgData)
                imgData.append(exWanUtils.duplicateImgData(inputImgData[piece_idx]))
            piece.imgIndex = img_map[piece_idx]
