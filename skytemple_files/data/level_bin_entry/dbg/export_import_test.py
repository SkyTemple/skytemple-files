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
import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
m_level_bin = rom.getFileByName('BALANCE/m_level.bin')
m_level = FileType.BIN_PACK.deserialize(m_level_bin)

all_level_ups = []
all_level_ups_bin_decompressed = []

# Collect all level up data
for entry_bin in m_level:
    entry_bin_sir0 = FileType.SIR0.deserialize(entry_bin)
    entry_bin_unpacked = FileType.COMMON_AT.deserialize(entry_bin_sir0.content)
    entry_bin_decompressed = entry_bin_unpacked.decompress()
    all_level_ups_bin_decompressed.append(entry_bin_decompressed)
    entry = FileType.LEVEL_BIN_ENTRY.deserialize(entry_bin_decompressed)
    all_level_ups.append(entry)

#print(all_level_ups)

# Convert the entries back to bytes
new_bytes_for_entries = []
for i, entry in enumerate(all_level_ups):
    new_bytes_unpacked = FileType.LEVEL_BIN_ENTRY.serialize(entry)
    new_bytes_at = FileType.COMMON_AT.serialize(FileType.COMMON_AT.compress(new_bytes_unpacked))
    new_bytes = FileType.SIR0.wrap(new_bytes_at, [])
    # Compare!
    new_bytes_for_entries.append(new_bytes)
    assert all_level_ups_bin_decompressed[i] == new_bytes_unpacked
