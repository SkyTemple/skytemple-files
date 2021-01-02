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
from skytemple_files.container.bin_pack.writer import BinPackWriter
from skytemple_files.container.dungeon_bin.model import DungeonBinPack


class DungeonBinHandler(DataHandler[DungeonBinPack]):
    @classmethod
    def deserialize(cls, data: bytes, static_data: Pmd2Data, **kwargs) -> DungeonBinPack:
        return DungeonBinPack(data, static_data.dungeon_data.dungeon_bin_files)

    @classmethod
    def serialize(cls, data: DungeonBinPack, **kwargs) -> bytes:
        """
        Serialize the bin pack.
        """
        data.serialize_subfiles()
        return BinPackWriter(data, 0).write()
