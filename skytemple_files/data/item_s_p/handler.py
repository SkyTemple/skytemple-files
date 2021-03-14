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

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.data.item_s_p.model import ItemSP
from skytemple_files.data.item_s_p.writer import ItemSPWriter


class ItemSPHandler(DataHandler[ItemSP]):
    """
    Deals with Sir0 wrapped models by default (assumes they are Sir0 wrapped).
    Use the deserialize_raw / serialize_raw methods to work with the unwrapped models instead.
    """
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> 'ItemSP':
        from skytemple_files.common.types.file_types import FileType
        return FileType.SIR0.unwrap_obj(FileType.SIR0.deserialize(data), ItemSP)

    @classmethod
    def serialize(cls, data: 'ItemSP', **kwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        return FileType.SIR0.serialize(FileType.SIR0.wrap_obj(data))

    @classmethod
    def deserialize_raw(cls, data: bytes, **kwargs) -> 'ItemSP':
        return ItemSP(data)

    @classmethod
    def serialize_raw(cls, data: 'ItemSP', **kwargs) -> bytes:
        return ItemSPWriter(data).write()[0]
