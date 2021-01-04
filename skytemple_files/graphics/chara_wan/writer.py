import sys
import os
import glob
from PIL import Image
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from chara_wan.model import WanFile, SequenceFrame, MetaFramePiece, FrameOffset, AnimStat, ImgPiece, \
    MINUS_FRAME, DIM_TABLE, TEX_SIZE
import chara_wan.utils as exUtils




DRAW_CENTER_X = 0
DRAW_CENTER_Y = -4

MAX_ANIMS = 44

ANIM_ORDER = [0, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20, \
              21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43]

DEBUG_PRINT = False






def ExportWan(out_file, wan):
    out_file.write(b'\x53\x49\x52\x30')
    sir0_ptrs = [4, 8]
    # 4- WAN header ptr
    write_ptr(out_file, 0, sir0_ptrs)
    # 8 - SIR0 pointer list ptr
    write_ptr(out_file, 0, sir0_ptrs)
    # 12 - zeroes
    out_file.write((0).to_bytes(4, 'little'))
    # Metaframes
    ptrMetaFrames = []
    for metaFrame in wan.frameData:
        ptrMetaFrames.append(out_file.tell())
        for piece in metaFrame:
            out_file.write(piece.imgIndex.to_bytes(2, 'little', signed=True))
            out_file.write((0).to_bytes(2, 'little'))
            out_file.write((piece.attr0).to_bytes(2, 'little'))
            out_file.write((piece.attr1).to_bytes(2, 'little'))
            out_file.write((piece.attr2).to_bytes(2, 'little'))

    # animation sequences
    animSeqPtrList = []
    for anim_group in wan.animGroupData:
        groupSequencesPtrs = []
        for sequence in anim_group:
            groupSequencesPtrs.append(out_file.tell())
            for animFrame in sequence:
                out_file.write(animFrame.duration.to_bytes(1, 'little'))
                out_file.write(animFrame.flag.to_bytes(1, 'little'))
                out_file.write(animFrame.frameIndex.to_bytes(2, 'little'))
                out_file.write(animFrame.offset[0].to_bytes(2, 'little', signed=True))
                out_file.write(animFrame.offset[1].to_bytes(2, 'little', signed=True))
                out_file.write(animFrame.shadow[0].to_bytes(2, 'little', signed=True))
                out_file.write(animFrame.shadow[1].to_bytes(2, 'little', signed=True))
            # write a null
            out_file.write((0).to_bytes(12, 'little'))
        if len(anim_group) > 0:
            while len(groupSequencesPtrs) < 8:
                groupSequencesPtrs.append(groupSequencesPtrs[-1])
        animSeqPtrList.append(groupSequencesPtrs)

    padUntilDiv(out_file, b'\xAA', 4)

    # img data
    ptrImgs = []
    for img in wan.imgData:
        zSort = img.zSort
        imgTable = []
        # write pixel data
        for pxStrip in img.imgPx:
            hasNonZero = False
            for px in pxStrip:
                if px > 0:
                    hasNonZero = True
                    break
            if hasNonZero:
                imgTable.append((out_file.tell(), len(pxStrip)))
                for px in pxStrip:
                    out_file.write(px.to_bytes(1, 'little'))
            else:
                imgTable.append((0, len(pxStrip)))

        ptrImgs.append(out_file.tell())
        for img_write in imgTable:
            # pixelSource
            write_ptr(out_file, img_write[0], sir0_ptrs)
            # amt
            out_file.write(img_write[1].to_bytes(2, 'little'))
            # unk#14
            out_file.write((0).to_bytes(2, 'little'))
            # unk#2
            out_file.write(zSort.to_bytes(4, 'little'))
        out_file.write((0).to_bytes(12, 'little'))

    # palette data
    ptrPaletteDataBlock = out_file.tell()
    nbColorsPerRow = 0
    for palette_row in wan.customPalette:
        if len(palette_row) > 1:
            nbColorsPerRow = len(palette_row)
        for palette in palette_row:
            # R
            out_file.write(palette[0].to_bytes(1, 'little'))
            # G
            out_file.write(palette[1].to_bytes(1, 'little'))
            # B
            out_file.write(palette[2].to_bytes(1, 'little'))
            # X
            out_file.write(b'\x80')
    # palette info
    ptrPaletteInfo = out_file.tell()
    write_ptr(out_file, ptrPaletteDataBlock, sir0_ptrs)
    # Unk#3
    out_file.write((0).to_bytes(2, 'little'))
    # colors per row
    out_file.write(nbColorsPerRow.to_bytes(2, 'little'))
    # Unk#4
    out_file.write((0).to_bytes(2, 'little'))
    # Unk#5
    out_file.write((255).to_bytes(2, 'little'))
    # 4 bytes of zeroes indicating end of palette info?
    out_file.write((0).to_bytes(4, 'little'))

    # Metaframes ref table
    ptrMetaFramesRefTable = out_file.tell()
    for metaframe_ptr in ptrMetaFrames:
        write_ptr(out_file, metaframe_ptr, sir0_ptrs)

    # Particle offsets table
    ptrOffsetsTable = out_file.tell()
    for offset in wan.offsetData:
        out_file.write(offset.head[0].to_bytes(2, 'little', signed=True))
        out_file.write(offset.head[1].to_bytes(2, 'little', signed=True))
        out_file.write(offset.lhand[0].to_bytes(2, 'little', signed=True))
        out_file.write(offset.lhand[1].to_bytes(2, 'little', signed=True))
        out_file.write(offset.rhand[0].to_bytes(2, 'little', signed=True))
        out_file.write(offset.rhand[1].to_bytes(2, 'little', signed=True))
        out_file.write(offset.center[0].to_bytes(2, 'little', signed=True))
        out_file.write(offset.center[1].to_bytes(2, 'little', signed=True))

    # AnimSequenceTable
    animGroupSequencePtrs = []
    for groupSequencesPtrs in animSeqPtrList:
        animGroupSequencePtrs.append(out_file.tell())
        for animSeqPtr in groupSequencesPtrs:
            write_ptr(out_file, animSeqPtr, sir0_ptrs)
        if len(groupSequencesPtrs) == 0:
            out_file.write((0).to_bytes(4, 'little'))

    # AnimGroupTable
    ptrAnimGroupTable = out_file.tell()
    for idx, groupSequencesPtrs in enumerate(animSeqPtrList):
        groupPtr = animGroupSequencePtrs[idx]
        if len(groupSequencesPtrs) == 0:
            groupPtr = 0
        # location of the first sequence in the group
        write_ptr(out_file, groupPtr, sir0_ptrs)
        # number of sequences in group
        out_file.write(len(groupSequencesPtrs).to_bytes(2, 'little'))
        # Unk#16
        out_file.write((0).to_bytes(2, 'little'))

    # Image Data Table
    ptrImageDataTable = out_file.tell()
    for img_ptr in ptrImgs:
        write_ptr(out_file, img_ptr, sir0_ptrs)

    # compute max block space
    max_blocks = 0
    for idx, metaFrame in enumerate(wan.frameData):
        cur_tile = 0
        for piece in metaFrame:
            if piece.imgIndex != MINUS_FRAME:
                twidth, theight = DIM_TABLE[piece.getResolutionType()]
                blocks_occupied = max(1, twidth * theight // 4)
                cur_tile += blocks_occupied
        max_blocks = max(max_blocks, cur_tile)

    # AnimInfo
    ptrAnimInfo = out_file.tell()
    write_ptr(out_file, ptrMetaFramesRefTable, sir0_ptrs)
    write_ptr(out_file, ptrOffsetsTable, sir0_ptrs)
    write_ptr(out_file, ptrAnimGroupTable, sir0_ptrs)
    out_file.write(len(animSeqPtrList).to_bytes(2, 'little'))
    # Unk#6
    out_file.write(max_blocks.to_bytes(2, 'little'))
    # Unk#7
    out_file.write((0).to_bytes(2, 'little'))
    # Unk#8
    out_file.write((0).to_bytes(2, 'little'))
    # Unk#9
    out_file.write((0).to_bytes(2, 'little'))
    # Unk#10
    out_file.write((0).to_bytes(2, 'little'))

    # Image Data Info
    ptrImageDataInfo = out_file.tell()
    write_ptr(out_file, ptrImageDataTable, sir0_ptrs)
    write_ptr(out_file, ptrPaletteInfo, sir0_ptrs)
    # Unk#13
    out_file.write((0).to_bytes(2, 'little'))
    # Is256ColorSpr - never
    out_file.write((0).to_bytes(2, 'little'))
    # Unk#11
    if len(ptrImgs) > 0:
        out_file.write((1).to_bytes(2, 'little'))
    else:
        out_file.write((0).to_bytes(2, 'little'))
    # nbImgs
    out_file.write(len(ptrImgs).to_bytes(2, 'little'))

    # WAN header
    ptrWAN = out_file.tell()
    write_ptr(out_file, ptrAnimInfo, sir0_ptrs)
    write_ptr(out_file, ptrImageDataInfo, sir0_ptrs)
    # img type - always 1 for character sprites
    out_file.write((1).to_bytes(2, 'little'))
    # Unk#12
    out_file.write((0).to_bytes(2, 'little'))

    # fill with AA until divisible by 16
    padUntilDiv(out_file, b'\xAA', 16)

    # sir0 pointers
    ptrSir0 = out_file.tell()
    for idx, offset in enumerate(sir0_ptrs):
        offset_to_encode = offset
        if idx > 0:
            offset_to_encode -= sir0_ptrs[idx - 1]
        # This tells the loop whether it needs to encode null bytes, if at least one higher byte was non-zero
        has_higher_non_zero = False
        # Encode every bytes of the 4 bytes integer we have to
        for i in range(4, 0, -1):
            currentbyte = (offset_to_encode >> (7 * (i - 1))) & 0x7F
            # the lowest byte to encode is special
            if i == 1:
                # If its the last byte to append, leave the highest bit to 0 !
                out_file.write(currentbyte.to_bytes(1, 'little'))
            elif currentbyte != 0 or has_higher_non_zero:
                # if any bytes but the lowest one! If not null OR if we have encoded a higher non-null byte before!
                out_file.write((currentbyte | 0x80).to_bytes(1, 'little'))
                has_higher_non_zero = True
    # null terminate the sir0 header list
    out_file.write(b'\x00')

    # fill with AA until divisible by 16
    padUntilDiv(out_file, b'\xAA', 16)

    out_file.seek(4)
    out_file.write(ptrWAN.to_bytes(4, 'little'))
    out_file.write(ptrSir0.to_bytes(4, 'little'))


# This will accurately load all sir0 found in m_ground, m_attack, and monster.bin with a few exceptions:
# m_ground_0546_0xb01840.wan - Armaldo.  Metaframe Unk#0 is a nonzero
# m_ground_0587_0xbd0a10.wan - Latios.  Unknown difference
# monster_0433_0x3dd1c0.sir0 - Giratina Origin.  Extra zeroes after file end.
# monster_0438_0x3ec6d0.sir0 - Shaymin Sky.  Extra zeroes after file end.
def ImportWan(in_file):

    wan = WanFile([], [], [], [], [])
    wan.customPalette = []
    # Read SIR0 Header: ptr to WAN header
    in_file.seek(4)
    ptrWAN = int.from_bytes(in_file.read(4), 'little')

    # Read WAN header: ptr to AnimInfo, ptr to ImageDataInfo
    in_file.seek(ptrWAN)
    ptrAnimInfo = int.from_bytes(in_file.read(4), 'little')
    ptrImageDataInfo = int.from_bytes(in_file.read(4), 'little')
    if ptrAnimInfo == 0 or ptrImageDataInfo == 0:
        raise Exception('  Null pointer in Wan Header!')
    imgType = int.from_bytes(in_file.read(2), 'little')
    if imgType != 1:
        raise Exception('  Not a chara!')

    updateUnusedStats([], 'Unk#12', int.from_bytes(in_file.read(2), 'little'))

    # Read ImageDataInfo: ptr to ImageDataTable block, ptr to PaletteInfo, NbImgs, print Unk#13 and Is256ColorSpr
    in_file.seek(ptrImageDataInfo)
    ptrImageDataTable = int.from_bytes(in_file.read(4), 'little')
    ptrPaletteInfo = int.from_bytes(in_file.read(4), 'little')
    if ptrImageDataTable == 0 or ptrPaletteInfo == 0:
        raise Exception('  Null pointer in Image Data Info!')
    # Unk#13 - ALWAYS 0
    int.from_bytes(in_file.read(2), 'little')
    # Is256ColorSpr - ALWAYS 0
    int.from_bytes(in_file.read(2), 'little')
    # Unk#11 - ALWAYS 1 unless completely empty?
    updateUnusedStats([], 'Unk#11', int.from_bytes(in_file.read(2), 'little'))
    nbImgs = int.from_bytes(in_file.read(2), 'little')
    # print('  NbImgs:' + str(nbImgs))

    # Read PaletteInfo: ptr to PaletteDataBlock, print NbColorsPerRow and All unknowns
    in_file.seek(ptrPaletteInfo)
    ptrPaletteDataBlock = int.from_bytes(in_file.read(4), 'little')
    # Unk#3 - ALWAYS 0
    int.from_bytes(in_file.read(2), 'little')
    nbColorsPerRow = max(1, int.from_bytes(in_file.read(2), 'little'))
    # Unk#4 - ALWAYS 0
    int.from_bytes(in_file.read(2), 'little')
    # Unk#5 - ALWAYS 255
    int.from_bytes(in_file.read(2), 'little')

    # Read PaletteDataBlock: Save contents
    in_file.seek(ptrPaletteDataBlock)
    wan.customPalette = []
    totalColors = (ptrPaletteInfo - ptrPaletteDataBlock) // 4
    totalPalettes = totalColors // nbColorsPerRow
    for ii in range(totalPalettes):
        palette = []
        for jj in range(nbColorsPerRow):
            red = int.from_bytes(in_file.read(1), 'little')
            blue = int.from_bytes(in_file.read(1), 'little')
            green = int.from_bytes(in_file.read(1), 'little')
            in_file.read(1)
            palette.append((red, blue, green, 255))
        wan.customPalette.append(palette)

    ##Read ImageDataTable: list of all ptr to CompressedImages (use the Nb of images variable to know when to stop)
    in_file.seek(ptrImageDataTable)
    ptrImgs = []
    for img in range(nbImgs):
        ptrImgs.append(int.from_bytes(in_file.read(4), 'little'))

    ##Read CompTable: Read all Image data and assemble; add byte arrays into a list.
    wan.imgData = []  ##one continuous list of bytes
    for ptrImg in ptrImgs:
        in_file.seek(ptrImg)
        imgPiece = ImgPiece()
        imgPiece.imgPx = []
        ##Read pixels or zero padding.
        while True:
            ptrPixSrc = int.from_bytes(in_file.read(4), 'little')
            amt = int.from_bytes(in_file.read(2), 'little')
            # amt is ALWAYS a multiple of 32.  values 1-31 x 32 have been observed
            if ptrPixSrc == 0 and amt == 0:
                break
            # Unk#14 - ALWAYS 0
            int.from_bytes(in_file.read(2), 'little')
            # z-sort is always consistent for a full image strip
            imgPiece.zSort = int.from_bytes(in_file.read(4), 'little')

            pxStrip = []
            if ptrPixSrc == 0:
                for zero in range(amt):
                    pxStrip.append(0)
            else:
                ptrCurrent = in_file.tell()
                in_file.seek(ptrPixSrc)
                for pix in range(amt):
                    pxStrip.append(int.from_bytes(in_file.read(1), 'little'))
                in_file.seek(ptrCurrent)
            imgPiece.imgPx.append(pxStrip)
        wan.imgData.append(imgPiece)

    ##Read AnimInfo: ptr to MetaFramesRefTable, ptr to AnimGroupTable
    in_file.seek(ptrAnimInfo)
    ptrMetaFramesRefTable = int.from_bytes(in_file.read(4), 'little')
    ptrOffsetsTable = int.from_bytes(in_file.read(4), 'little')
    ptrAnimGroupTable = int.from_bytes(in_file.read(4), 'little')
    nbAnimGroups = int.from_bytes(in_file.read(2), 'little')
    # Unk#6 - Max number of blocks that a frame takes
    int.from_bytes(in_file.read(2), 'little')
    # Unk#7 - ALWAYS 0
    int.from_bytes(in_file.read(2), 'little')
    # Unk#8 - ALWAYS 0
    int.from_bytes(in_file.read(2), 'little')
    # Unk#9 - ALWAYS 0
    int.from_bytes(in_file.read(2), 'little')
    # Unk#10 - ALWAYS 0
    int.from_bytes(in_file.read(2), 'little')
    # get ptr to AnimSequenceTable
    in_file.seek(ptrAnimGroupTable)
    ptrAnimGroups = []
    for ptrAnimSeq in range(nbAnimGroups):
        ##read the location
        animLoc = int.from_bytes(in_file.read(4), 'little')
        ##read the length
        animLength = int.from_bytes(in_file.read(2), 'little')
        # Unk#16 - ALWAYS 0
        int.from_bytes(in_file.read(2), 'little')
        ##save curlocation
        curLocation = in_file.tell()
        ##go to seq location
        in_file.seek(animLoc)
        ptrAnims = []
        for ii in range(animLength):
            ##read all anims
            animPtr = int.from_bytes(in_file.read(4), 'little')
            ptrAnims.append(animPtr)
        ptrAnimGroups.append(ptrAnims)
        in_file.seek(curLocation)

    if ptrOffsetsTable == 0:
        raise Exception("Zero Offset")

    ptrFramesRefTableEnd = ptrOffsetsTable

    # Read MetaFramesRefTable: list of all ptr to Meta Frames
    # stop when reached particleOffsetsTable
    # or on AnimSequenceTable, if the above is zero
    in_file.seek(ptrMetaFramesRefTable)
    ptrMetaFrames = []
    while in_file.tell() < ptrFramesRefTableEnd:
        ptrMetaFrames.append(int.from_bytes(in_file.read(4), 'little'))
    # print('  NbMetaframes:' + str(len(ptrMetaFrames)))

    ##Read MetaFrames: for each meta frame group, read until "end of meta frame group" bit is reached.
    wan.frameData = []
    for idx, ptrMetaFrame in enumerate(ptrMetaFrames):
        in_file.seek(ptrMetaFrame)
        metaFrameData = []
        while True:
            imgIndex = int.from_bytes(in_file.read(2), 'little', signed=True)
            # Unk#0 - ALWAYS 0 EXCEPT for just ONE official sprite:
            # m_ground,0546,Unk#0,171,0,2560
            int.from_bytes(in_file.read(2), 'little')
            attr0 = int.from_bytes(in_file.read(2), 'little')
            attr1 = int.from_bytes(in_file.read(2), 'little')
            attr2 = int.from_bytes(in_file.read(2), 'little')
            newFramePiece = MetaFramePiece(imgIndex, attr0, attr1, attr2)

            # values of interest:
            # resolution y
            # color palette mode - ALWAYS 0
            # mosaic mode - ALWAYS 0
            # obj mode - ALWAYS Normal
            # obj disable -
            updateUnusedStats([str(len(wan.frameData)), str(len(metaFrameData))],
                              'MFDisabled', int(newFramePiece.isDisabled()))
            # rotation and scaling - ALWAYS 1 when DISABLE is 0
            # Y offset

            # resolution x
            # flip vertical
            # flip horizontal
            # last frame
            # unused - leave 0
            # X offset

            # palette - this will be autocalculated
            # priority - ALWAYS 3
            # tileindex - ALWAYS follows the rules of memory placement: 4 blocks = +1 index.  1 block min

            ##document the used config
            metaFrameData.append(newFramePiece)
            if newFramePiece.isLast():
                break

        wan.frameData.append(metaFrameData)

    in_file.seek(ptrOffsetsTable)
    wan.offsetData = []
    for offset_idx in range(len(ptrMetaFrames)):
        headX = int.from_bytes(in_file.read(2), 'little', signed=True)
        headY = int.from_bytes(in_file.read(2), 'little', signed=True)
        lhandX = int.from_bytes(in_file.read(2), 'little', signed=True)
        lhandY = int.from_bytes(in_file.read(2), 'little', signed=True)
        rhandX = int.from_bytes(in_file.read(2), 'little', signed=True)
        rhandY = int.from_bytes(in_file.read(2), 'little', signed=True)
        centerX = int.from_bytes(in_file.read(2), 'little', signed=True)
        centerY = int.from_bytes(in_file.read(2), 'little', signed=True)
        wan.offsetData.append(FrameOffset((headX, headY), (lhandX, lhandY), (rhandX, rhandY), (centerX, centerY)))

    ##read all anim pointers
    wan.animGroupData = []
    for ptrAnimGroup in ptrAnimGroups:
        animGroup = []
        for a_idx, ptrAnim in enumerate(ptrAnimGroup):
            # if repeating the same pointer, it's the same animation. skip
            if a_idx > 0 and ptrAnim == ptrAnimGroup[a_idx - 1]:
                continue
            in_file.seek(ptrAnim)
            animSequence = []
            while True:
                frameDur = int.from_bytes(in_file.read(1), 'little')
                flag = int.from_bytes(in_file.read(1), 'little')
                frameIndex = int.from_bytes(in_file.read(2), 'little')
                sprOffX = int.from_bytes(in_file.read(2), 'little', signed=True)
                sprOffY = int.from_bytes(in_file.read(2), 'little', signed=True)
                sdwOffX = int.from_bytes(in_file.read(2), 'little', signed=True)
                sdwOffY = int.from_bytes(in_file.read(2), 'little', signed=True)
                if frameDur == 0:
                    break
                else:
                    animSequence.append(SequenceFrame(frameIndex, frameDur, flag,
                                                    (sprOffX, sprOffY), (sdwOffX, sdwOffY)))
            animGroup.append(animSequence)
        wan.animGroupData.append(animGroup)

    return wan


def ImportSheets(inDir):

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
            if index > -1:
                anim_stats[index] = AnimStat(index, name, None, backref)
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

            if index > -1:
                anim_stats[index] = anim_stat
            anim_names[name.lower()] = index

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
        anim_name = anim_parts[0].lower()
        if anim_name not in anim_names:
            extra_sheets.append(anim_name)
        else:
            index = anim_names[anim_name]
            del anim_names[anim_name]

            anim_img = Image.open(os.path.join(inDir, anim_name + '-Anim.png')).convert("RGBA")
            offset_img = Image.open(os.path.join(inDir, anim_name + '-Offsets.png')).convert("RGBA")
            shadow_img = Image.open(os.path.join(inDir, anim_name + '-Shadow.png')).convert("RGBA")

            anim_sheets[index] = (anim_img, offset_img, shadow_img)

    # raise warning if there exist anim stats without anims, or anims without anim stats
    if len(anim_names) > 0:
        orphans = []
        for k in anim_names:
            orphans.append(k)
        raise Exception("Xml found with no sheet: {0}".format(', '.join(orphans)))
    if len(extra_sheets) > 0:
        raise Exception("Sheet found with no xml: {0}".format(', '.join(extra_sheets)))

    animGroupData = []
    frames = []
    frameToSequence = []
    for idx in range(MAX_ANIMS):
        if idx in anim_sheets:
            anim_img, offset_img, shadow_img = anim_sheets[idx]
            # TODO: raise warning if there's missing shadow or offsets
            tileSize = anim_stats[idx].size
            durations = anim_stats[idx].durations

            # TODO: check against inconsistent sizing
            # TODO: check against inconsistent duration counts
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
                        # warn about no offset for this frame, probably?
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
        final_frames[key] = (final_frames[key][0], final_frames[key][1], chosen_diff, final_frames[key][3])
        # and then set the diff mapping to their shadow diff - chosen diff
        for start in reverse_frame_map[key]:
            frame_map[start] = (frame_map[start][0], exUtils.addLoc(chosen_diff, frames[start][2], True))
        # now, the frame will treat chosenDiff as its center
        # and all diffs will be applied to the offsets of the currently created animGroups

    # final_frames is now a list of unique graphics where flips are treated as separate but refer to the originals
    # now, create metaframes and image data
    # palette is needed first.  get palette data
    palette_map = {}
    for frame in final_frames:
        tex = frame[0]
        exUtils.addToPalette(palette_map, tex)

    singlePalette = []
    # add transparent at the START
    singlePalette.append((0, 0, 0, 0))
    for color in palette_map:
        palette_map[color] = len(singlePalette)
        singlePalette.append(color)
    palette_map[(0, 0, 0, 0)] = 0
    # raise warning if over the palette limit
    if len(singlePalette) > 16:
        raise Exception("Number of (nontransparent) colors over 15: {0}".format(len(singlePalette)))
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
            addFlippedImgData(frameData, flipped_frame, final_frames[flip], frame)
        else:
            # will append to imgData and frameData
            addImgData(imgData, frameData, palette_map, frame)
        offsets = frame[1]
        offsets.AddLoc((-shadow_diff[0], -shadow_diff[1]))
        offsetData.append(offsets)

    # adjust transparent color to a substitute color
    transparent = (0, 127, 151, 255)
    foundTrans = True
    while foundTrans:
        foundTrans = False
        for color in singlePalette:
            if color == transparent:
                transparent = (0, 127, transparent[3] - 1, 255)
                foundTrans = True
                break
    singlePalette[0] = transparent

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
            animGroupData[copy_idx] = duplicateAnimGroup(animGroupData[idx])

    wan = WanFile(imgData, frameData, animGroupData, offsetData, [singlePalette])
    wan.sdwSize = sdwSize
    # return the wan file
    return wan


def ExportSheets(outDir, sdwImg, effectData, anim_name_map):
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
    for idx, metaFrame in enumerate(effectData.frameData):
        for mt_idx, metaFramePiece in enumerate(metaFrame):
            # update bounds based on image
            fBounds = metaFramePiece.GetBounds()
            maxFrameBounds = exUtils.combineExtents(maxFrameBounds, fBounds)

        # update bounds based on offsets
        offset = effectData.offsetData[idx]
        maxFrameBounds = exUtils.combineExtents(maxFrameBounds, offset.GetBounds())

    # round up to nearest x8
    maxFrameBounds = exUtils.centerBounds(maxFrameBounds, (DRAW_CENTER_X, DRAW_CENTER_Y))
    maxFrameBounds = exUtils.roundUpBox(maxFrameBounds)

    # create all frames, and visual representation of offsets tied to each frame
    frames = []
    offsets = []
    frames_bounds_tight = []
    piece_imgs = {}
    for idx, metaFrame in enumerate(effectData.frameData):
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
                img = metaFramePiece.GeneratePiece(effectData.imgData, effectData.customPalette, parent_idx)
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
        offset = effectData.offsetData[idx]
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
    for idx, animGroup in enumerate(effectData.animGroupData):
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
    for idx, animGroup in enumerate(effectData.animGroupData):
        animsPerGroup = len(animGroup)
        # some groups may be empty
        if animsPerGroup == 0:
            continue

        dupe_idx = -1
        for cmp_idx in ANIM_ORDER:
            if cmp_idx == idx:
                break
            cmp_group = effectData.animGroupData[cmp_idx]
            if animGroupsEqual(animGroup, cmp_group):
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
    shadow_node.text = str(effectData.sdwSize)

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
        f.write(minidom.parseString(ET.tostring(root)).toprettyxml(indent="\t"))



def MergeWan(wan_files):

    # custom palettes are always the same
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
    for ii in range(MAX_ANIMS):
        animGroupData.append([])
        for wan in wan_files:
            if ii < len(wan.animGroupData) and len(wan.animGroupData[ii]) > 0:
                animGroupData[ii] = wan.animGroupData[ii]

    return WanFile(imgData, frameData, animGroupData, offsetData, customPalette)


def SplitWan(wan, anim_presence):
    wan_files = []
    for anim_list in anim_presence:

        animGroupData = []
        for anim_idx, anim_group in enumerate(anim_list):
            if not anim_group:
                animGroupData.append([])
            elif anim_idx < len(wan.animGroupData):
                new_anim = duplicateAnimGroup(wan.animGroupData[anim_idx])
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

        new_wan = WanFile(imgData, frameData, animGroupData, offsetData, wan.customPalette)
        wan_files.append(new_wan)
    return wan_files









def padUntilDiv(out_file, bt, div):
    fill = div - out_file.tell() % div
    if fill != div:
        for ii in range(fill):
            out_file.write(bt)


def updateUnusedStats(log_params, name, val):
    #stats.append([log_params[0], log_params[1], name, log_params[2:], val])
    if DEBUG_PRINT and val != 0:
        print('  ' + name + ':' + str(val))

def write_ptr(out_file, value, sir0_ptrs):
    if value > 0:
        sir0_ptrs.append(out_file.tell())
    out_file.write(value.to_bytes(4, 'little'))


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
                    frameData.append(duplicateMetaFrame(inputFrameData[frame_idx]))
                    offsetData.append(duplicateOffset(inputOffsetData[frame_idx]))
                frame.frameIndex = frame_map[frame_idx]

def transferStrippedImgData(inputImgData, imgData, frameData):
    img_map = {}
    for metaFrame in frameData:
        for piece in metaFrame:
            piece_idx = piece.imgIndex
            if piece_idx not in img_map:
                img_map[piece_idx] = len(imgData)
                imgData.append(duplicateImgData(inputImgData[piece_idx]))
            piece.imgIndex = img_map[piece_idx]


def addFlippedImgData(frameData, metaFrame, old_frame, new_frame):
    x_border = old_frame[2][0]
    newMetaFrame = []
    for piece in metaFrame:
        newPiece = MetaFramePiece(piece.imgIndex, piece.attr0, piece.attr1, piece.attr2)
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


def addImgData(imgData, frameData, palette_map, frame):
    img = frame[0]
    pt_zero = frame[2]
    # chop the frames into images and metaframes - need psy's algorithm for this
    piece_locs = chopImgToPieceLocs(img)

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

def chopImgToPieceLocs(img):
    chopped_imgs = []
    smallest_dim = 3
    for idx, dim in enumerate(DIM_TABLE):
        if img.size[0] <= dim[0] * TEX_SIZE and img.size[1] <= dim[1] * TEX_SIZE:
            if dim[0] * dim[1] < DIM_TABLE[smallest_dim][0] * DIM_TABLE[smallest_dim][1]:
                smallest_dim = idx
    if img.size[0] > 8 * TEX_SIZE or img.size[1] > 8 * TEX_SIZE:
        roundUp = (exUtils.roundUpToMult(img.size[0], TEX_SIZE), exUtils.roundUpToMult(img.size[1], TEX_SIZE))
        fullImg = Image.new('RGBA', roundUp, (0, 0, 0, 0))
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



        print("Size: {0}".format(total_size))
    else:
        newWidth = DIM_TABLE[smallest_dim][0] * TEX_SIZE
        newHeight = DIM_TABLE[smallest_dim][1] * TEX_SIZE
        newImg = Image.new('RGBA', (newWidth, newHeight), (0, 0, 0, 0))
        newImg.paste(img, (0, 0), img)
        chopped_imgs.append((newImg, (0, 0)))
    return chopped_imgs



def animGroupsEqual(anim1, anim2):
    if len(anim1) != len(anim2):
        return False

    anims_equal = True
    # perform a check to see if they're equal
    for anim_idx in range(len(anim1)):
        if len(anim1[anim_idx]) != len(anim2[anim_idx]):
            anims_equal = False
            break

        for frame_idx in range(len(anim1[anim_idx])):
            frame1 = anim1[anim_idx][frame_idx]
            frame2 = anim2[anim_idx][frame_idx]

            if frame1.frameIndex != frame2.frameIndex or frame1.duration != frame2.duration \
                    or frame1.offset != frame2.offset or frame1.shadow != frame2.shadow:
                anims_equal = False
                break
        if not anims_equal:
            break
    return anims_equal


def duplicateAnimGroup(anim):
    new_group = []
    for anim_seq in anim:
        new_seq = []
        for frame in anim_seq:
            new_frame = SequenceFrame(frame.frameIndex, frame.duration, frame.flag, frame.offset, frame.shadow)
            new_frame.SetRushPoint(frame.IsRushPoint())
            new_seq.append(new_frame)
        new_group.append(new_seq)
    return new_group

def duplicateMetaFrame(frame):
    new_frame = []
    for piece in frame:
        new_piece = MetaFramePiece(piece.imgIndex, piece.attr0, piece.attr1, piece.attr2)
        new_frame.append(new_piece)
    return new_frame


def duplicateOffset(offset):
    return FrameOffset(offset.head, offset.lhand, offset.rhand, offset.center)

def duplicateImgData(imgStrip):
    new_img = ImgPiece()
    new_img.zSort = imgStrip.zSort
    for strip in imgStrip.imgPx:
        new_strip = strip.copy()
        new_img.imgPx.append(new_strip)

    return new_img

def mapDuplicateImportImgs(imgs, final_imgs, img_map):
    for idx, img in enumerate(imgs):
        dupe = False
        flip = -1
        for final_idx, final_img in enumerate(final_imgs):
            imgs_equal = exUtils.imgsEqual(final_img[0], img[0])
            # if offsets are not synchronized, they are counted as different
            if imgs_equal:
                imgs_equal = offsetsEqual(final_img[1], img[1], img[0].size[0])
            if imgs_equal:
                img_map[idx] = (final_idx, (0, 0))
                dupe = True
                break
            imgs_flip = exUtils.imgsEqual(final_img[0], img[0], True)
            if imgs_flip:
                imgs_flip = offsetsEqual(final_img[1], img[1], img[0].size[0], True)
            if imgs_flip:
                flip = final_idx

        if not dupe:
            img_map[idx] = (len(final_imgs), (0, 0))
            final_imgs.append((img[0], img[1], img[2], flip))

def offsetsEqual(offset1, offset2, imgWidth, flip=False):
    if flip:
        center = (imgWidth - offset2.center[0] - 1, offset2.center[1])
        head = (imgWidth - offset2.head[0] - 1, offset2.head[1])
        lhand = (imgWidth - offset2.lhand[0] - 1, offset2.lhand[1])
        rhand = (imgWidth - offset2.rhand[0] - 1, offset2.rhand[1])
    else:
        center = offset2.center
        head = offset2.head
        lhand = offset2.lhand
        rhand = offset2.rhand

    if offset1.center != center:
        return False
    if offset1.head != head:
        return False
    if offset1.lhand != lhand:
        return False
    if offset1.rhand != rhand:
        return False
    return True
