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
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.

try:
    from PIL import Image
except ImportError:
    from pil import Image

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.wte.model import Wte, WteImageType
from skytemple_files.graphics.wte.writer import WteWriter


class WteHandler(DataHandler[Wte]):
    """
    Deals with Sir0 wrapped models by default (assumes they are Sir0 wrapped).
    Use the deserialize_raw / serialize_raw methods to work with the unwrapped models instead.
    """

    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> 'Wte':
        from skytemple_files.common.types.file_types import FileType
        return FileType.SIR0.unwrap_obj(FileType.SIR0.deserialize(data), Wte)

    @classmethod
    def serialize(cls, data: 'Wte', **kwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        return FileType.SIR0.serialize(FileType.SIR0.wrap_obj(data))

    @classmethod
    def new(cls, img: Image.Image, img_type: WteImageType, discard_palette: bool) -> Wte:
        wte = Wte(None, 0)
        wte.from_pil(img, img_type, discard_palette)
        return wte

    @classmethod
    def deserialize_raw(cls, data: bytes, **kwargs) -> 'Wte':
        return Wte(data)

    @classmethod
    def serialize_raw(cls, data: 'Wte', **kwargs) -> bytes:
        return WteWriter(data).write()[0]
