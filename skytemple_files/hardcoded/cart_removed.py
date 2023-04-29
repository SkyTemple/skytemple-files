"""Module for editing hardcoded data regarding the cartridge removed image."""
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

from PIL import Image

from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import iter_bytes
from skytemple_files.compression_container.common_at.handler import (
    CommonAtHandler,
    CommonAtType,
)

IMG_WIDTH = 256
IMG_HEIGHT = 96


class HardcodedCartRemoved:
    @staticmethod
    def get_cart_removed_data(arm9: bytes, config: Pmd2Data) -> Image.Image:
        """
        Gets the cartridge removed data
        """
        block = config.bin_sections.arm9.data.CART_REMOVED_IMG_DATA
        data = arm9[block.address : block.address + block.length]
        img_data = CommonAtHandler.deserialize(data).decompress()
        raw_data = []
        for l, h in iter_bytes(img_data, 2):
            v = l + h * 256
            raw_data.append((v % 32) * 8)
            raw_data.append(((v >> 5) % 32) * 8)
            raw_data.append(((v >> 10) % 32) * 8)
        return Image.frombytes(
            mode="RGB", size=(IMG_WIDTH, IMG_HEIGHT), data=bytes(raw_data)
        )

    @staticmethod
    def set_cart_removed_data(
        img: Image.Image, arm9: bytearray, config: Pmd2Data
    ) -> None:
        """
        Sets the cartridge removed data
        """
        if img.width != IMG_WIDTH and img.height != IMG_HEIGHT:
            raise AttributeError(
                f(_("The image must have dimensions {IMG_WIDTH}x{IMG_HEIGHT}."))
            )
        block = config.bin_sections.arm9.data.CART_REMOVED_IMG_DATA
        img = img.convert("RGB")
        raw_data = img.tobytes()
        img_data = []
        for r, g, b in iter_bytes(raw_data, 3):
            v = (r // 8) + ((g // 8) << 5) + ((b // 8) << 10)
            img_data.append(v % 256)
            img_data.append(v // 256)
        data = CommonAtHandler.serialize(
            CommonAtHandler.compress(bytes(img_data), [CommonAtType.AT3PX])
        )
        assert block.length is not None
        if len(data) > block.length:
            raise AttributeError(
                f(
                    _(
                        "This image must be compressed better to fit in the arm9 ({len(data)} > {block.end-block.address})."
                    )
                )
            )
        arm9[block.address : block.address + block.length] = data + bytes(
            block.length - len(data)
        )
