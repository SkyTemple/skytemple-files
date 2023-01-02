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
# mypy: ignore-errors
from __future__ import annotations

import sys

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_ppmdu_config_for_rom
from skytemple_files.hardcoded.iq import IqGroupsSkills

COMPRESSED_GROUPS = bytearray(
    [
        0x8E,
        0x91,
        0xF2,
        0x8D,
        0x60,
        0x00,
        0x40,
        0x42,
        0x0E,  # Group A
        0x8E,
        0x81,
        0xFA,
        0x49,
        0x41,
        0x40,
        0x9C,
        0x40,
        0x04,  # Group B
        0x8E,
        0x03,
        0xD2,
        0x01,
        0x34,
        0x91,
        0x03,
        0x99,
        0x04,  # Group C
        0xAC,
        0x41,
        0xFC,
        0xA5,
        0x80,
        0x49,
        0x01,
        0x90,
        0x01,  # Group D
        0x9C,
        0x85,
        0xD1,
        0x01,
        0xB9,
        0xA0,
        0xB4,
        0x01,
        0x00,  # Group E
        0x8E,
        0x99,
        0xD4,
        0xB5,
        0x40,
        0x72,
        0x00,
        0x02,
        0x04,  # Group F
        0xAC,
        0x43,
        0xDC,
        0x95,
        0x00,
        0x0A,
        0x60,
        0x18,
        0x03,  # Group G
        0xAC,
        0x95,
        0xD4,
        0x49,
        0x41,
        0x20,
        0xB8,
        0x01,
        0x01,  # Group H
        0x8C,
        0x01,
        0xD0,
        0x01,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,  # Unused group 1
        0x8C,
        0x01,
        0xD0,
        0x01,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,  # Unused group 2
        0xAC,
        0x93,
        0xD4,
        0xA1,
        0x34,
        0x81,
        0xA0,
        0x14,
        0x00,  # Group I
        0x9C,
        0xA9,
        0xD1,
        0x85,
        0x18,
        0x62,
        0x01,
        0x12,
        0x02,  # Group J
        0x8C,
        0x01,
        0xD0,
        0x01,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,  # Unused group 3
        0x8C,
        0x01,
        0xD0,
        0x01,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,  # Unused group 4
        0x8C,
        0x01,
        0xD0,
        0x01,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,  # Unused group 5
        0x8C,
        0x01,
        0xD0,
        0x01,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)  # Unused group 6


def main():
    rom_path = sys.argv[1]
    rom = NintendoDSRom.fromFile(rom_path)
    config = get_ppmdu_config_for_rom(rom)
    block_compressed = config.binaries["arm9.bin"].symbols["CompressedIqGroupsSkills"]
    arm9 = rom.arm9

    groups = IqGroupsSkills.read_uncompressed(arm9, config)
    IqGroupsSkills.write_compressed(arm9, groups, config)

    assert arm9[block_compressed.begin : block_compressed.end] == COMPRESSED_GROUPS

    groups2 = IqGroupsSkills.read_compressed(arm9, config)
    for i in range(len(groups)):
        assert sorted(groups[i]) == sorted(groups2[i])


if __name__ == "__main__":
    main()
