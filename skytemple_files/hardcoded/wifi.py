#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
from skytemple_files.common.util import read_uintle, write_uintle


class HardcodedWifi:
    @staticmethod
    def get_nas_nintendowifi_net_pubkey(ov00: bytes, config: Pmd2Data) -> bytes:
        block1 = config.binaries['overlay/overlay_0000.bin'].blocks['nas.nintendowifi.net-Pubkey1']
        block2 = config.binaries['overlay/overlay_0000.bin'].blocks['nas.nintendowifi.net-Pubkey2']
        assert ov00[block1.begin:block1.end] == ov00[block2.begin:block2.end]
        return ov00[block1.begin:block1.end]

    @staticmethod
    def set_nas_nintendowifi_net_pubkey(key: bytes, ov00: bytearray, config: Pmd2Data) -> None:
        block1 = config.binaries['overlay/overlay_0000.bin'].blocks['nas.nintendowifi.net-Pubkey1']
        block2 = config.binaries['overlay/overlay_0000.bin'].blocks['nas.nintendowifi.net-Pubkey2']

        if len(key) != block1.end - block1.begin:
            raise ValueError(f"The public key must be exactly {block1.end - block1.begin} bytes long. Pad if needed.")

        ov00[block1.begin:block1.end] = key
        ov00[block2.begin:block2.end] = key
