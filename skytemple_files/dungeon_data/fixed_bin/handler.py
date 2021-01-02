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
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.dungeon_data.fixed_bin.model import FixedBin

from skytemple_files.dungeon_data.fixed_bin.writer import FixedBinWriter


class FixedBinHandler(DataHandler[FixedBin]):
    """
    Deals with Sir0 wrapped models by default (assumes they are Sir0 wrapped).
    Use the deserialize_raw / serialize_raw methods to work with the unwrapped models instead.
    """
    @classmethod
    def deserialize(cls, data: bytes, static_data: Pmd2Data, **kwargs) -> 'FixedBin':
        from skytemple_files.common.types.file_types import FileType
        return FileType.SIR0.unwrap_obj(FileType.SIR0.deserialize(data), FixedBin, static_data)

    @classmethod
    def serialize(cls, data: 'FixedBin', **kwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        return FileType.SIR0.serialize(FileType.SIR0.wrap_obj(data))

    @classmethod
    def deserialize_raw(cls, data: bytes, **kwargs) -> 'FixedBin':
        return FixedBin(data)

    @classmethod
    def serialize_raw(cls, data: 'FixedBin', **kwargs) -> bytes:
        return FixedBinWriter(data).write()[0]
