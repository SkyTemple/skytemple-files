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

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.graphics.zmappat.model import ZMappaT
from skytemple_files.graphics.zmappat.writer import ZMappaTWriter


class ZMappaTHandler(DataHandler[ZMappaT]):
    """
    Deals with Sir0 wrapped models by default (assumes they are Sir0 wrapped).
    Use the deserialize_raw / serialize_raw methods to work with the unwrapped models instead.
    """

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> ZMappaT:
        from skytemple_files.common.types.file_types import FileType

        return FileType.SIR0.unwrap_obj(FileType.SIR0.deserialize(data), ZMappaT)

    @classmethod
    def serialize(cls, data: ZMappaT, **kwargs: OptionalKwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType

        return FileType.SIR0.serialize(FileType.SIR0.wrap_obj(data))

    @classmethod
    def new(
        cls, img: list[Image.Image], mask: list[Image.Image], minimized=False
    ) -> ZMappaT:
        zmappat = ZMappaT(None, 0)
        if minimized:
            zmappat.from_pil_minimized(img, mask)
        else:
            zmappat.from_pil(img, mask)
        return zmappat

    @classmethod
    def deserialize_raw(cls, data: bytes, **kwargs) -> ZMappaT:
        return ZMappaT(data, 0)

    @classmethod
    def serialize_raw(cls, data: ZMappaT, **kwargs: OptionalKwargs) -> bytes:
        return ZMappaTWriter(data).write()[0]
