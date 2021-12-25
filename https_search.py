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
from ndspy.rom import NintendoDSRom
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu, read_var_length_string, \
    set_binary_in_rom_ppmdu, get_files_from_rom_with_extension


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


rom = NintendoDSRom.fromFile("/home/marco/dev/skytemple/skytemple/CLEAN_ROM/pmdsky.nds")
ppmdu = get_ppmdu_config_for_rom(rom)

ov00 = get_binary_from_rom_ppmdu(rom, ppmdu.binaries['overlay/overlay_0000.bin'])

for x in find_all(ov00, b"https://"):
    _, string = read_var_length_string(ov00, x, "ascii")
    new_string = bytearray(len(string))
    string = string.replace('https://', 'http://')
    new_string[0:len(string)] = bytes(string, 'ascii')
    ov00[x:x+len(new_string)] = new_string

for x in find_all(ov00, b"nintendowifi.net"):
    ov00[x:x+len(b"nintendowifi.net")] = b"wc.skytemple.org"

with open('/tmp/ov00.bin', 'wb') as f:
    f.write(ov00)

set_binary_in_rom_ppmdu(rom, ppmdu.binaries['overlay/overlay_0000.bin'], ov00)

for fn in get_files_from_rom_with_extension(rom, 'ssb'):
    ssb = FileType.SSB.deserialize(rom.getFileByName(fn), ppmdu)
    for rtn in ssb.routine_ops:
        for op in rtn:
            if op.op_code.name == 'BranchDebug':
                print(op)
                op.params[0] = 1 if op.params[0] == 0 else 0
    rom.setFileByName(fn, FileType.SSB.serialize(ssb, ppmdu))

rom.saveToFile("/home/marco/dev/skytemple/skytemple/skyworkcopy_edit.nds")
