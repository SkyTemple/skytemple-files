#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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
from __future__ import annotations

import typing
from typing import Optional, Tuple, Union

from PIL import Image

from skytemple_files.user_error import UserValueError

Point = Tuple[int, int]
Bounds = Tuple[int, int, int, int]
PointLike = Union[Point, Bounds]


class MultipleOffsetError(UserValueError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def centerBounds(bounds: Bounds, center: Bounds) -> Bounds:
    minX = min(bounds[0] - center[0], center[0] - bounds[2])
    minY = min(bounds[1] - center[1], center[1] - bounds[3])

    maxX = max(center[0] - bounds[0], bounds[2] - center[0])
    maxY = max(center[1] - bounds[1], bounds[3] - center[1])
    return addToBounds((minX, minY, maxX, maxY), center, False)


def roundUpBox(minBox: Bounds) -> Bounds:
    width = minBox[2] - minBox[0]
    height = minBox[3] - minBox[1]
    newWidth = roundUpToMult(width, 8)
    newHeight = roundUpToMult(height, 8)
    startX = minBox[0] + (width - newWidth) // 2
    startY = minBox[1] + (height - newHeight) // 2
    return startX, startY, startX + newWidth, startY + newHeight


def addToBounds(bounds: Bounds, add: PointLike, sub: bool = False) -> Bounds:
    mult = 1
    if sub:
        mult = -1
    return (
        bounds[0] + add[0] * mult,
        bounds[1] + add[1] * mult,
        bounds[2] + add[0] * mult,
        bounds[3] + add[1] * mult,
    )


def addLoc(loc1: Bounds, loc2: Bounds, sub: bool = False) -> Point:
    mult = 1
    if sub:
        mult = -1
    return (loc1[0] + loc2[0] * mult, loc1[1] + loc2[1] * mult)


def getCoveredBounds(inImg: Image.Image, max_box: Optional[Bounds] = None) -> Bounds:
    if max_box is None:
        max_box = (0, 0, inImg.size[0], inImg.size[1])
    minX, minY = inImg.size
    maxX = -1
    maxY = -1
    datas = inImg.getdata()
    for i in range(max_box[0], max_box[2]):
        for j in range(max_box[1], max_box[3]):
            if datas[i + j * inImg.size[0]][3] != 0:
                if i < minX:
                    minX = i
                if i > maxX:
                    maxX = i
                if j < minY:
                    minY = j
                if j > maxY:
                    maxY = j
    abs_bounds = (minX, minY, maxX + 1, maxY + 1)
    return addToBounds(abs_bounds, (max_box[0], max_box[1]), True)


@typing.no_type_check
def addToPalette(palette, img) -> None:
    data = img.getdata()
    for color in data:
        if color[3] == 255:
            palette[color] = True


@typing.no_type_check
def getOffsetFromRGB(img, bounds, black, r, g, b, white):
    datas = img.getdata()
    results = [None] * 5
    for i in range(bounds[0], bounds[2]):
        for j in range(bounds[1], bounds[3]):
            color = datas[i + j * img.size[0]]
            if color[3] == 255:
                if black and color[0] == 0 and color[1] == 0 and color[2] == 0:
                    if results[0] is None:
                        results[0] = (i - bounds[0], j - bounds[1])
                    else:
                        raise MultipleOffsetError("Multiple black pixels found!")
                if r and color[0] == 255:
                    if results[1] is None:
                        results[1] = (i - bounds[0], j - bounds[1])
                    else:
                        raise MultipleOffsetError("Multiple red pixels found!")
                if g and color[1] == 255:
                    if results[2] is None:
                        results[2] = (i - bounds[0], j - bounds[1])
                    else:
                        raise MultipleOffsetError("Multiple green pixels found!")
                if b and color[2] == 255:
                    if results[3] is None:
                        results[3] = (i - bounds[0], j - bounds[1])
                    else:
                        raise MultipleOffsetError("Multiple blue pixels found!")
                if white and color[0] == 255 and color[1] == 255 and color[2] == 255:
                    if results[4] is None:
                        results[4] = (i - bounds[0], j - bounds[1])
                    else:
                        raise MultipleOffsetError("Multiple white pixels found!")
    return results


def combineExtents(extent1: Bounds, extent2: Bounds) -> Bounds:
    return (
        min(extent1[0], extent2[0]),
        min(extent1[1], extent2[1]),
        max(extent1[2], extent2[2]),
        max(extent1[3], extent2[3]),
    )


def roundUpToMult(inInt: int, inMult: int) -> int:
    subInt = inInt - 1
    div = subInt // inMult
    return (div + 1) * inMult


def imgsEqual(img1: Image.Image, img2: Image.Image, flip: bool = False) -> bool:
    if img1.size[0] != img2.size[0] or img1.size[1] != img2.size[1]:
        return False
    data_1 = img1.getdata()
    data_2 = img2.getdata()
    for xx in range(img1.size[0]):
        for yy in range(img1.size[1]):
            idx1 = xx + yy * img1.size[0]
            x2 = xx
            if flip:
                x2 = img1.size[0] - 1 - xx
            idx2 = x2 + yy * img1.size[0]
            if data_1[idx1] != data_2[idx2]:
                return False

    return True


@typing.no_type_check
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
