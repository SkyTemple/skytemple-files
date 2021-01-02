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
from skytemple_files.container.bin_pack.model import BinPack
from skytemple_files.container.bin_pack.writer import BinPackWriter


class BinPackHandler(DataHandler[BinPack]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> BinPack:
        return BinPack(data)

    @classmethod
    def serialize(cls, data: BinPack, fixed_header_len=0, **kwargs) -> bytes:
        """
        Serialize the bin pack.

        If fixed_header_len is set, the first sub file is placed at exactly this position,
        the header is padded until then. For the three files in the MONSTER/ directory,
        this must be 0x1300.
        """
        return BinPackWriter(data, fixed_header_len).write()
