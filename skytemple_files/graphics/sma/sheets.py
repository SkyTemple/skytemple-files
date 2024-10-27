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

from PIL import Image

from skytemple_files.graphics.sma.model import TEX_SIZE


def ExportSheets(outDir, effectData, paletteIndex):
    if not os.path.isdir(outDir):
        os.makedirs(outDir)

    for anim_idx, statusEffectAnim in enumerate(effectData.animData):
        if statusEffectAnim.blockWidth == 0:
            continue
        frames = []
        for idx in range(statusEffectAnim.frameCount):
            frameImg = GenerateStatusFrame(
                effectData.imgData,
                effectData.customPalette,
                paletteIndex,
                statusEffectAnim.byteOffset,
                statusEffectAnim.blockWidth,
                statusEffectAnim.blockHeight,
            )
            frames.append(frameImg)
        animImg = CombineFramesIntoAnim(frames)
        animImg.save(os.path.join(outDir, "A-" + format(anim_idx, "02d") + "-" + format(paletteIndex, "02d") + ".png"))


def GenerateStatusFrame(imgData, inPalette, paletteIndex, byteOffset, width, height):
    ##creates a tex piece out of the imgdata, with the specified piece index and dimensions
    newImg = Image.new("RGBA", (width * TEX_SIZE, height * TEX_SIZE), (0, 0, 0, 0))
    datas = [(0, 0, 0, 0)] * (width * TEX_SIZE * height * TEX_SIZE)

    lengthPixels = TEX_SIZE * TEX_SIZE * width * height
    imgPx = []
    # flatten the list to include all strips
    for nn in range(lengthPixels):
        imgPx.append(imgData[byteOffset * 2 + nn])

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

                    imgPosition = (xx * TEX_SIZE + px, yy * TEX_SIZE + py)
                    datas[imgPosition[1] * width * TEX_SIZE + imgPosition[0]] = color
    newImg.putdata(datas)
    return newImg


def CombineFramesIntoAnim(img_list):
    ##combines all frames into a horizontal animation sheet
    ##ASSUMES ALL IMGS ARE THE SAME SIZE
    size = img_list[0].size
    imgNew = Image.new("RGBA", (size[0] * len(img_list), size[1]), (0, 0, 0, 0))
    for img_index in range(len(img_list)):
        imgNew.paste(img_list[img_index], (size[0] * img_index, 0), img_list[img_index])
    return imgNew
