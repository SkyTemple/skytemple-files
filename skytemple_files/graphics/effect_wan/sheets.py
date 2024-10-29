#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
# mypy: ignore-errors

from __future__ import annotations

import os
import shutil

from PIL import Image

from skytemple_files.graphics.effect_wan.model import (
    DEBUG_PRINT,
    TEX_SIZE,
)

CENTER_X = 256
CENTER_Y = 508


def ExportSheets(outDir, wan):
    if not os.path.isdir(outDir):
        os.makedirs(outDir)

    if wan.imgType == 3:
        img = GenerateAtlas(wan.imgData, wan.customPalette, 0)
        if img is not None:
            img.save(os.path.join(outDir, "Atlas.png"))
    else:
        for passNum in range(1, 4):
            ExportEffectStep(outDir, wan, passNum)


def GenerateAtlas(imgData, inPalette, paletteIndex):
    imgPx = []
    for img in imgData.imageLists:
        # flatten the list to include all strips
        for pxStrip in img:
            for px in pxStrip:
                imgPx.append(px)

    band_width = imgData.atlasX
    band_height = imgData.atlasY
    widthInTex = 1
    heightInTex = max((len(imgPx) // (band_width * band_height) - 1) // widthInTex, 0) + 1

    newImg = Image.new("RGBA", (widthInTex * band_width, heightInTex * band_height), (0, 0, 0, 0))
    datas = [(0, 0, 0, 0)] * (widthInTex * band_width * heightInTex * band_height)
    for yy in range(heightInTex):
        for xx in range(widthInTex):
            texPosition = (yy * widthInTex + xx) * band_width * band_height
            if texPosition < len(imgPx):
                ##iterate the elements of the block and assign pixels
                for py in range(band_height):
                    for px in range(band_width):
                        if texPosition + py * band_width + px < len(imgPx):
                            paletteElement = imgPx[texPosition + py * band_width + px]
                            if paletteElement == 0:
                                color = (0, 0, 0, 0)
                            else:
                                color = inPalette[paletteIndex][paletteElement]
                            imgPosition = (xx * band_width + px, yy * band_height + py)
                            datas[imgPosition[1] * widthInTex * band_width + imgPosition[0]] = color
    newImg.putdata(datas)
    return newImg


def ExportEffectStep(outDir, effectData, passNum):
    ##note: these operations never remove
    if passNum == 1:
        ##step 1: create the pieces
        ##place in /_pieces/ folder
        if not os.path.isdir(os.path.join(outDir, "_pieces")):
            os.makedirs(os.path.join(outDir, "_pieces"))
        ##with the name of [chunk index]-[original palette]
        for metaFrameData in effectData.frameData:
            for useConfig in metaFrameData:
                img = GeneratePiece(
                    effectData.is256Color,
                    effectData.imgData,
                    effectData.customPalette,
                    useConfig.paletteIndex,
                    useConfig.blockOffset,
                    useConfig.res[0],
                    useConfig.res[1],
                )
                if img is not None:
                    img.save(
                        os.path.join(
                            outDir,
                            "_pieces",
                            "P-"
                            + format(useConfig.blockOffset, "02d")
                            + "-"
                            + format(useConfig.paletteIndex, "02d")
                            + ".png",
                        )
                    )

        ##users may want to group pieces together
        for ii in range(4):
            if not os.path.isdir(os.path.join(outDir, "_pieces", "group_" + str(ii + 1))):
                os.makedirs(os.path.join(outDir, "_pieces", "group_" + str(ii + 1)))

        for imgDir in os.listdir(os.path.join(outDir, "_pieces")):
            if os.path.isdir(os.path.join(outDir, "_pieces", imgDir)):
                groupIndex = imgDir.split("_")[1]
                for imgFile in os.listdir(os.path.join(outDir, "_pieces", imgDir)):
                    pieceInfo = os.path.splitext(imgFile)[0].split("-")
                    blockOffset = int(pieceInfo[1])
                    paletteIndex = int(pieceInfo[2])
                    refConfig = None
                    for metaFrameData in effectData.frameData:
                        for useConfig in metaFrameData:
                            if useConfig.blockOffset == blockOffset:
                                refConfig = useConfig
                    img = GeneratePiece(
                        effectData.is256Color,
                        effectData.imgData,
                        effectData.customPalette,
                        paletteIndex,
                        blockOffset,
                        refConfig.res[0],
                        refConfig.res[1],
                    )
                    if img is not None:
                        suffix = ""
                        if len(pieceInfo) > 3:
                            suffix = "-^"
                        img.save(
                            os.path.join(
                                outDir,
                                "_pieces",
                                imgDir,
                                "P-" + format(blockOffset, "02d") + "-" + format(paletteIndex, "02d") + suffix + ".png",
                            )
                        )
        ##users may want to inspect for recolor chains
    elif passNum == 2:
        ##step 2: create the frame pieces
        ##place in /_pieces_frames/
        if not os.path.isdir(os.path.join(outDir, "_pieces_frames")):
            os.makedirs(os.path.join(outDir, "_pieces_frames"))

        ##find the minimum box across all frames
        minBox = (10000, 10000, -1, -1)
        for metaFrameData in effectData.frameData:
            for useConfig in metaFrameData:
                newRect = GetPieceRect(effectData, useConfig)
                if newRect is not None:
                    minBox = CombineExtents(minBox, newRect)
        ##don't need to worry if all frames contain only one piece!

        ##frame size will be adjusted amongst all metaframes in an effect
        minBox = roundUpBox(minBox)
        for frameIndex in range(len(effectData.frameData)):
            metaFrameData = effectData.frameData[frameIndex]
            for pieceIndex in range(len(metaFrameData)):
                useConfig = metaFrameData[pieceIndex]
                ##do not print the frame if the piece it uses is not in the outDir
                singleConfig = [useConfig]
                ##use the name of [metaframe index]-[piece index][^ if this needs to stay in the back]
                img = GenerateFrame(effectData, singleConfig, minBox)
                if img is not None:
                    suffix = ""
                    if not useConfig.front:
                        suffix = "-^"
                    img.save(
                        os.path.join(
                            outDir,
                            "_pieces_frames",
                            "F-" + format(frameIndex, "02d") + "-" + format(pieceIndex, "02d") + suffix + ".png",
                        )
                    )

        ##users may want to separate an animation into layers
        ##add group_1 to group_4 for categorization
        ##also, for all folders that have images in them,
        ##recreate the frame pieces of those image names
        for ii in range(4):
            if not os.path.isdir(os.path.join(outDir, "_pieces_frames", "group_" + str(ii + 1))):
                os.makedirs(os.path.join(outDir, "_pieces_frames", "group_" + str(ii + 1)))

        for imgDir in os.listdir(os.path.join(outDir, "_pieces_frames")):
            if os.path.isdir(os.path.join(outDir, "_pieces_frames", imgDir)):
                groupIndex = imgDir.split("_")[1]
                for imgFile in os.listdir(os.path.join(outDir, "_pieces_frames", imgDir)):
                    pieceInfo = os.path.splitext(imgFile)[0].split("-")
                    frameIndex = int(pieceInfo[1])
                    pieceIndex = int(pieceInfo[2])
                    useConfig = effectData.frameData[frameIndex][pieceIndex]
                    ##do not print the frame if the piece it uses is not in the outDir
                    singleConfig = [useConfig]
                    ##use the name of [metaframe index]-[piece index][^ if this needs to stay in the back]
                    img = GenerateFrame(effectData, singleConfig, minBox)
                    if img is not None:
                        suffix = ""
                        if not useConfig.front:
                            suffix = "-^"
                        img.save(
                            os.path.join(
                                outDir,
                                "_pieces_frames",
                                imgDir,
                                "F-" + format(frameIndex, "02d") + "-" + format(pieceIndex, "02d") + suffix + ".png",
                            )
                        )

        ##copy only the actual palette,
        # so that an organizer would have an easier time sorting
    elif passNum == 3:
        ##step 3: create the anim
        ##first, measure the frame dimensions given all the metaframes

        ##maps metaframeIndex-pieceIndex to list of groups
        groupConfig = {}
        totalGroups = 1
        ##maps group to list of palettes
        ##no palette signifies to use natural colors
        groupPaletteConfig = {}
        groupPaletteConfig[0] = []
        ##check the metaframe piece organization in the folder corresponding to the referenced metaframe
        ##create full compiled frames from each grouped subfolder in pass3/[inIndex]/[frameIndex]/
        for imgDir in os.listdir(os.path.join(outDir, "_pieces_frames")):
            if os.path.isdir(os.path.join(outDir, "_pieces_frames", imgDir)):
                totalGroups = totalGroups + 1
                groupIndex = imgDir.split("_")[1]
                groupPaletteConfig[int(groupIndex)] = []
                for img in os.listdir(os.path.join(outDir, "_pieces_frames", imgDir)):
                    pieceInfo = os.path.splitext(img)[0].split("-")
                    if pieceInfo[0] == "P":  ##if it's a piece, it denotes a recolor request
                        groupPaletteConfig[int(groupIndex)].append(int(pieceInfo[2]))
                    else:
                        pairKey = (int(pieceInfo[1]), int(pieceInfo[2]))
                        if pairKey not in groupConfig:
                            groupConfig[pairKey] = []
                        groupConfig[pairKey].append(int(groupIndex))
            else:  ##frames not added in a group will be considered group0
                pieceInfo = os.path.splitext(imgDir)[0].split("-")
                if pieceInfo[0] == "P":  ##if it's a piece, it denotes a recolor request
                    groupPaletteConfig[0].append(int(pieceInfo[2]))
                else:
                    pairKey = (int(pieceInfo[1]), int(pieceInfo[2]))
                    if pairKey not in groupConfig:
                        groupConfig[pairKey] = []
                    groupConfig[pairKey].append(0)

        for animIndex in range(len(effectData.animData)):
            animData = effectData.animData[animIndex]
            ##create a number of lists equal to the number of groups
            animPieceCollection = []
            for group in range(totalGroups):
                animPieceCollection.append([])

            for animFrame in animData:
                ##for each frame of the animation, get the metaframe
                ##create a number of lists equal to the number of groups
                framePieceCollection = []
                for group in range(totalGroups):
                    framePieceCollection.append([])

                if animFrame.frmIndex < len(effectData.frameData):
                    for pieceIndex in range(len(effectData.frameData[animFrame.frmIndex])):
                        if (animFrame.frmIndex, pieceIndex) in groupConfig:
                            ##for each piece of the metaframe,
                            ##check each group for its presence
                            useConfig = effectData.frameData[animFrame.frmIndex][pieceIndex]
                            for group in groupConfig[(animFrame.frmIndex, pieceIndex)]:
                                ##if found, add that piece to that list
                                framePieceCollection[group].insert(0, useConfig)

                ##then go through each list, and if it's not empty, add it to the higher list
                for group in range(totalGroups):
                    if len(framePieceCollection[group]) > 0:
                        animPieceCollection[group].append(framePieceCollection[group])

            ##go through each list
            for layerIndex in range(len(animPieceCollection)):
                anim = animPieceCollection[layerIndex]
                if len(anim) > 0:
                    ##check to see if dual-sided
                    backSided = False
                    frontSided = False
                    ##get the minBox for each anim
                    minBox = (10000, 10000, -1, -1)
                    for frame in anim:
                        for useConfig in frame:
                            if useConfig.front:
                                frontSided = True
                            else:
                                backSided = True
                            newRect = GetPieceRect(effectData, useConfig)
                            if newRect is not None:
                                minBox = CombineExtents(minBox, newRect)

                    minBox = roundUpBox(minBox)
                    minSize = (minBox[2] - minBox[0], minBox[3] - minBox[1])
                    maxDim = max(minSize[0], minSize[1])
                    minBox = (
                        minBox[0] + (minSize[0] - maxDim) // 2,
                        minBox[1] + (minSize[1] - maxDim) // 2,
                        minBox[0] + (minSize[0] + maxDim) // 2,
                        minBox[1] + (minSize[1] + maxDim) // 2,
                    )

                    if len(groupPaletteConfig[layerIndex]) > 0:
                        for recolorIndex in groupPaletteConfig[layerIndex]:
                            ##go through each frame
                            printedFrames = []
                            backFrames = []
                            frontFrames = []
                            for frame in anim:
                                ##create the frame from the list of useConfigs
                                recolorFrame = []
                                for useConfig in frame:
                                    newConfig = useConfig.Clone()
                                    newConfig.paletteIndex = recolorIndex
                                    recolorFrame.append(newConfig)
                                imgFrame = GenerateFrame(effectData, recolorFrame, minBox)
                                if imgFrame is not None:
                                    printedFrames.append(imgFrame)
                                    if backSided and frontSided:
                                        backList = []
                                        frontList = []
                                        for useConfig in recolorFrame:
                                            if useConfig.front:
                                                frontList.append(useConfig)
                                            else:
                                                backList.append(useConfig)
                                        imgBack = GenerateFrame(effectData, backList, minBox)
                                        if imgBack == None:
                                            imgBack = Image.new(
                                                "RGBA", (minBox[2] - minBox[0], minBox[3] - minBox[1]), (0, 0, 0, 0)
                                            )
                                        backFrames.append(imgBack)
                                        imgFront = GenerateFrame(effectData, frontList, minBox)
                                        if imgFront == None:
                                            imgFront = Image.new(
                                                "RGBA", (minBox[2] - minBox[0], minBox[3] - minBox[1]), (0, 0, 0, 0)
                                            )
                                        frontFrames.append(imgFront)

                            ##sort them into groups according to
                            ##place in base directory
                            ##with the name template of A-[anim_sequence]-[layer]-[recolor index]
                            printedAnim = CombineFramesIntoAnim(printedFrames)
                            printedAnim.save(
                                os.path.join(
                                    outDir,
                                    "A-"
                                    + format(animIndex, "02d")
                                    + "-"
                                    + format(layerIndex, "02d")
                                    + "-"
                                    + format(recolorIndex, "02d")
                                    + ".png",
                                )
                            )

                            if backSided and frontSided:
                                backAnim = CombineFramesIntoAnim(backFrames)
                                backAnim.save(
                                    os.path.join(
                                        outDir,
                                        "A-"
                                        + format(animIndex, "02d")
                                        + "-"
                                        + format(layerIndex, "02d")
                                        + "-"
                                        + format(recolorIndex, "02d")
                                        + "-B"
                                        + ".png",
                                    )
                                )

                                frontAnim = CombineFramesIntoAnim(frontFrames)
                                frontAnim.save(
                                    os.path.join(
                                        outDir,
                                        "A-"
                                        + format(animIndex, "02d")
                                        + "-"
                                        + format(layerIndex, "02d")
                                        + "-"
                                        + format(recolorIndex, "02d")
                                        + "-F"
                                        + ".png",
                                    )
                                )
                    else:
                        ##go through each frame
                        printedFrames = []
                        backFrames = []
                        frontFrames = []
                        for frame in anim:
                            ##create the frame from the list of useConfigs
                            imgFrame = GenerateFrame(effectData, frame, minBox)
                            if imgFrame is not None:
                                printedFrames.append(imgFrame)
                                if backSided and frontSided:
                                    backList = []
                                    frontList = []
                                    for useConfig in frame:
                                        if useConfig.front:
                                            frontList.append(useConfig)
                                        else:
                                            backList.append(useConfig)
                                    imgBack = GenerateFrame(effectData, backList, minBox)
                                    if imgBack == None:
                                        imgBack = Image.new(
                                            "RGBA", (minBox[2] - minBox[0], minBox[3] - minBox[1]), (0, 0, 0, 0)
                                        )
                                    backFrames.append(imgBack)
                                    imgFront = GenerateFrame(effectData, frontList, minBox)
                                    if imgFront == None:
                                        imgFront = Image.new(
                                            "RGBA", (minBox[2] - minBox[0], minBox[3] - minBox[1]), (0, 0, 0, 0)
                                        )
                                    frontFrames.append(imgFront)

                        ##sort them into groups according to
                        ##place in base directory
                        ##with the name template of A-[anim_sequence]-[layer]-[recolor index]
                        printedAnim = CombineFramesIntoAnim(printedFrames)
                        printedAnim.save(
                            os.path.join(
                                outDir,
                                "A-" + format(animIndex, "02d") + "-" + format(layerIndex, "02d") + "-N" + ".png",
                            )
                        )

                        if backSided and frontSided:
                            backAnim = CombineFramesIntoAnim(backFrames)
                            backAnim.save(
                                os.path.join(
                                    outDir,
                                    "A-" + format(animIndex, "02d") + "-" + format(layerIndex, "02d") + "-N-B" + ".png",
                                )
                            )

                            frontAnim = CombineFramesIntoAnim(frontFrames)
                            frontAnim.save(
                                os.path.join(
                                    outDir,
                                    "A-" + format(animIndex, "02d") + "-" + format(layerIndex, "02d") + "-N-F" + ".png",
                                )
                            )

        ##combine all piece groups
        for imgDir in os.listdir(os.path.join(outDir, "_pieces")):
            if os.path.isdir(os.path.join(outDir, "_pieces", imgDir)):
                groupIndex = imgDir.split("_")[1]
                img_list = []
                maxBox = (0, 0)
                for imgFile in os.listdir(os.path.join(outDir, "_pieces", imgDir)):
                    img = Image.open(os.path.join(outDir, "_pieces", imgDir, imgFile))
                    img_list.append(img)
                    maxBox = (max(img.size[0], maxBox[0]), max(img.size[1], maxBox[1]))

                maxBox = (RoundUpToMult(maxBox[0], 8), RoundUpToMult(maxBox[1], 8))
                maxBox = (max(maxBox[0], maxBox[1]), max(maxBox[0], maxBox[1]))
                for img_index in range(len(img_list)):
                    imgNew = Image.new("RGBA", maxBox, (0, 0, 0, 0))
                    imgNew.paste(
                        img_list[img_index],
                        (
                            (maxBox[0] - img_list[img_index].size[0]) // 2,
                            (maxBox[1] - img_list[img_index].size[1]) // 2,
                        ),
                        img_list[img_index],
                    )
                    img_list[img_index] = imgNew

                if len(img_list):
                    printedPieces = CombineFramesIntoAnim(img_list)
                    printedPieces.save(os.path.join(outDir, "S-" + format(int(groupIndex), "02d") + ".png"))

        ##combine all piece groups
        for imgDir in os.listdir(os.path.join(outDir, "_pieces")):
            if os.path.isdir(os.path.join(outDir, "_pieces", imgDir)):
                groupIndex = imgDir.split("_")[1]
                img_list = []
                maxBox = (0, 0)
                for imgFile in os.listdir(os.path.join(outDir, "_pieces", imgDir)):
                    img = Image.open(os.path.join(outDir, "_pieces", imgDir, imgFile))
                    img_list.append(img)
                    maxBox = (max(img.size[0], maxBox[0]), max(img.size[1], maxBox[1]))

                maxBox = (RoundUpToMult(maxBox[0], 8), RoundUpToMult(maxBox[1], 8))
                maxBox = (max(maxBox[0], maxBox[1]), max(maxBox[0], maxBox[1]))
                for img_index in range(len(img_list)):
                    imgNew = Image.new("RGBA", maxBox, (0, 0, 0, 0))
                    imgNew.paste(
                        img_list[img_index],
                        (
                            (maxBox[0] - img_list[img_index].size[0]) // 2,
                            (maxBox[1] - img_list[img_index].size[1]) // 2,
                        ),
                        img_list[img_index],
                    )
                    img_list[img_index] = imgNew

                if len(img_list):
                    printedPieces = CombineFramesIntoAnim(img_list)
                    printedPieces.save(os.path.join(outDir, "S-" + format(int(groupIndex), "02d") + ".png"))

        if not DEBUG_PRINT:
            shutil.rmtree(os.path.join(outDir, "_pieces"))
            shutil.rmtree(os.path.join(outDir, "_pieces_frames"))

        ##create a number of images equal to the number of groups
        ##with dimensions equal to the number of frames * measured frame dimensions
        ##for each frame of the animation, get the metaframe
        ##for each piece of the metaframe,
        ##check each group for its presence
        ##if it's found, draw it on the corresponding image in the corresponding frame position


def GeneratePiece(is256Color, imgData, inPalette, paletteIndex, blockOffset, width, height):
    if imgData is None:
        newImg = Image.new(
            "RGBA",
            (width * TEX_SIZE, height * TEX_SIZE),
            (128 * (blockOffset // 9 % 3), 128 * (blockOffset // 3 % 3), 128 * (blockOffset % 3), 255),
        )
        return newImg

    ##creates a tex piece out of the imgdata, with the specified piece index and dimensions
    newImg = Image.new("RGBA", (width * TEX_SIZE, height * TEX_SIZE), (0, 0, 0, 0))
    datas = [(0, 0, 0, 0)] * (width * TEX_SIZE * height * TEX_SIZE)

    noTrans = False

    if is256Color:
        bytePos = blockOffset * 2 * TEX_SIZE * TEX_SIZE
        imgPx = None
        curByte = 0
        for imgPx0 in imgData.imageLists:
            flatImgPx0 = []
            for pxStrip in imgPx0:
                for px in pxStrip:
                    flatImgPx0.append(px)
            if curByte == bytePos:
                imgPx = flatImgPx0
                break
            curByte += len(flatImgPx0)

            # blocks are always in units of 128 bytes
            # is a given flatImgPx0 is not a multiple of 128, round up to that multiple of 128
            while curByte % (2 * TEX_SIZE * TEX_SIZE) != 0:
                curByte += 64

        for yy in range(height):
            for xx in range(width):
                blockIndex = yy * width + xx
                texPosition = blockIndex * TEX_SIZE * TEX_SIZE

                if texPosition < len(imgPx):
                    for py in range(TEX_SIZE):
                        for px in range(TEX_SIZE):
                            paletteElement = imgPx[texPosition + py * TEX_SIZE + px]
                            ##print('palette:' + str(paletteIndex) + ' element:' + str(paletteElement))
                            if paletteElement == 0:
                                color = (0, 0, 0, 0)
                            else:
                                color = inPalette[paletteIndex][paletteElement]

                            if color[3] > 0:
                                noTrans = True
                            imgPosition = (xx * TEX_SIZE + px, yy * TEX_SIZE + py)
                            datas[imgPosition[1] * width * TEX_SIZE + imgPosition[0]] = color

    else:
        imgPx0 = imgData.imageLists[blockOffset]
        imgPx = []
        # flatten the list to include all strips
        for pxStrip in imgPx0:
            for px in pxStrip:
                imgPx.append(px)

        for yy in range(height):
            for xx in range(width):
                blockIndex = yy * width + xx
                texPosition = blockIndex * TEX_SIZE * TEX_SIZE

                for py in range(TEX_SIZE):
                    for px in range(TEX_SIZE):
                        paletteElement = imgPx[texPosition + py * TEX_SIZE + px]
                        ##print('palette:' + str(paletteIndex) + ' element:' + str(paletteElement))
                        if paletteElement == 0:
                            color = (0, 0, 0, 0)
                        else:
                            color = inPalette[paletteIndex][paletteElement]

                        if color[3] > 0:
                            noTrans = True
                        imgPosition = (xx * TEX_SIZE + px, yy * TEX_SIZE + py)
                        datas[imgPosition[1] * width * TEX_SIZE + imgPosition[0]] = color

    newImg.putdata(datas)

    ##DO NOT EXPORT BLANK TEXTURES
    if noTrans:
        return newImg
    return None


def GetPieceRect(effectData, useConfig):
    imgPiece = GeneratePiece(
        effectData.is256Color,
        effectData.imgData,
        effectData.customPalette,
        useConfig.paletteIndex,
        useConfig.blockOffset,
        useConfig.res[0],
        useConfig.res[1],
    )
    if imgPiece == None:
        return None
    box = getCoveredRect(imgPiece, useConfig.hFlip, useConfig.vFlip)
    return (
        box[0] + useConfig.offset[0],
        box[1] + useConfig.offset[1],
        box[2] + useConfig.offset[0],
        box[3] + useConfig.offset[1],
    )


def GenerateFrame(effectData, metaFrameData, minBox):
    drewSomething = False

    newImg = Image.new("RGBA", (minBox[2] - minBox[0], minBox[3] - minBox[1]), (0, 0, 0, 0))
    for useConfig in metaFrameData:
        imgPiece = GeneratePiece(
            effectData.is256Color,
            effectData.imgData,
            effectData.customPalette,
            useConfig.paletteIndex,
            useConfig.blockOffset,
            useConfig.res[0],
            useConfig.res[1],
        )
        if imgPiece is not None:
            useConfig.DrawOn(newImg, imgPiece, (minBox[0], minBox[1]))
            drewSomething = True
    if drewSomething:
        return newImg
    else:
        return None


def CombineFramesIntoAnim(img_list):
    ##combines all frames into a horizontal animation sheet
    ##ASSUMES ALL IMGS ARE THE SAME SIZE
    size = img_list[0].size
    imgNew = Image.new("RGBA", (size[0] * len(img_list), size[1]), (0, 0, 0, 0))
    for img_index in range(len(img_list)):
        imgNew.paste(img_list[img_index], (size[0] * img_index, 0), img_list[img_index])
    return imgNew


def getCoveredRect(inImg, hFlip=False, vFlip=False):
    minX, minY = inImg.size
    maxX = -1
    maxY = -1

    srcData = inImg.getdata()
    for i in range(0, inImg.size[0]):
        for j in range(0, inImg.size[1]):
            trans_i = i
            if hFlip:
                trans_i = inImg.size[0] - i - 1
            trans_j = j
            if vFlip:
                trans_j = inImg.size[1] - j - 1
            color = srcData[trans_i + trans_j * inImg.size[0]]
            if color[3] != 0:
                if i < minX:
                    minX = i
                if i > maxX:
                    maxX = i
                if j < minY:
                    minY = j
                if j > maxY:
                    maxY = j
    return (minX, minY, maxX + 1, maxY + 1)


def roundUpBox(minBox):
    ##print(str(minBox))
    width = max(CENTER_X - minBox[0], minBox[2] - CENTER_X) * 2
    height = minBox[3] - minBox[1]
    newWidth = RoundUpToMult(width, 8)
    newHeight = RoundUpToMult(height, 8)
    startX = CENTER_X - newWidth // 2
    startY = minBox[1] + (height - newHeight) // 2
    return (startX, startY, startX + newWidth, startY + newHeight)


def CombineExtents(extent1, extent2):
    return (
        min(extent1[0], extent2[0]),
        min(extent1[1], extent2[1]),
        max(extent1[2], extent2[2]),
        max(extent1[3], extent2[3]),
    )


def RoundUpToMult(inInt, inMult):
    subInt = inInt - 1
    div = subInt // inMult
    return (div + 1) * inMult
