#  Copyright 2020-2025 SkyTemple Contributors
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

from skytemple_files.graphics.effect_screen.model import TEX_SIZE


def ExportSheets(outDir, effectData, includeAlpha):
    if not os.path.isdir(outDir):
        os.makedirs(outDir)

    for frameIndex, frame in enumerate(effectData.animData):
        img = GenerateScreenFrame(effectData.imgData, frame, effectData.customPalette, includeAlpha)
        img.save(os.path.join(outDir, "F-" + format(frameIndex, "02d") + ".png"))


def GenerateScreenFrame(imgData, frame, inPalette, includeAlpha):
    screen_width = 256
    screen_height = 160

    newImg = Image.new("RGBA", (screen_width, screen_height), (0, 0, 0, 0))

    curBlockIdx = 0
    for screenPiece in frame.pieces:
        if screenPiece.skip:
            curBlockIdx += screenPiece.index
        else:
            alpha = 255
            if includeAlpha:
                alpha = frame.alpha // 256
            piece = GenerateScreenPiece(imgData, screenPiece, inPalette, alpha)
            if screenPiece.flipX:
                piece = piece.transpose(Image.FLIP_LEFT_RIGHT)
            if screenPiece.flipY:
                piece = piece.transpose(Image.FLIP_TOP_BOTTOM)

            blockX = curBlockIdx % 33
            blockY = curBlockIdx // 33
            newImg.paste(piece, (blockX * TEX_SIZE, blockY * TEX_SIZE), piece)
            curBlockIdx += 1

    return newImg


def GenerateScreenPiece(imgData, screenPiece, inPalette, alpha):
    newImg = Image.new("RGBA", (TEX_SIZE, TEX_SIZE), (0, 0, 0, 0))
    datas = [(0, 0, 0, 0)] * (TEX_SIZE * TEX_SIZE)

    texPosition = screenPiece.index * TEX_SIZE * TEX_SIZE
    ##iterate the elements of the block and assign pixels
    for py in range(TEX_SIZE):
        for px in range(TEX_SIZE):
            paletteElement = imgData[texPosition + py * TEX_SIZE + px]
            if paletteElement == 0:
                color = (0, 0, 0, 0)
            else:
                color = inPalette[0][paletteElement]
                color = (color[0], color[1], color[2], alpha)
            datas[py * TEX_SIZE + px] = color

    newImg.putdata(datas)
    return newImg
