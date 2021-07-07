"""
Debugging an issue with a certain ssb script decompilation.
First string is decompiled incorrectly at the time of writing.
See: https://canary.discord.com/channels/710190644152369162/712343169399914518/861731221432303676
"""
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
from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.common.types.file_types import FileType

FAULTY_SSB_BYTES = b'\x01\x00\x03\x00<\x00\x0f\x00\x15\x00\x00\x00;\x00\x01\x00\x05\x00\x01\x00\x00\x00\xa4\x00\x00\x00\x00\x00\x05\x00\x9e\x00\x00\x00\xaa\x00\x01\x00\x02\x00d\x00\x01\x00\x16\x00d\x00\x02\x009\x00\x87\x009\x00\xa4\x00\x00\x00\x00\x00\x05\x00\xae\x00\x03\x00\x96\x00\x80\x00\x03\x00\x04\x00\x02\x00\xea\x00\x00\x00\x1e\x00\xdb\x00\x01\x00\x1e\x00)\x00\x11\x00\x07\x000\x00\x8d\x00\x03\x00\x00\x00\x87\x003\x00\x8d\x00\x13\x00\x00\x00\x9d\x006\x00\x8d\x00\xff\x7f\x00\x00\x82\x00\x88\x00\x00\x00\x08\x00(Do I need to prepare more?)\x00\x00&\x00,\x003\x00(No.)\x00(Yes.)\x00 ...I think we can go.\x00'

ssb = FileType.SSB.deserialize(FAULTY_SSB_BYTES, static_data=Pmd2XmlReader.load_default('EoS_NA'))

print(str(ssb._header))
print(f"number_of_routines: {len(ssb.routine_info)}")
print(f"constants: {ssb.constants}")
print(f"strings: {ssb.strings}")
print(str(ssb.routine_info))
print("=== RAW ==")
lines = []
for i, ops in enumerate(ssb.routine_ops):
    lines.append(f">>> Routine {i}:")
    op_cursor = 0
    for op in ops:
        lines.append(f"{op.offset:10x}: ({op.op_code.id:3}) {op.op_code.name:45} - {op.params}")
        op_cursor += 2 + len(op.params) * 2
print('\n'.join(lines))

print("=== PREPARED FOR ES DECOMPILATION ==")
lines = []
for i, ops in enumerate(ssb.get_filled_routine_ops()):
    lines.append(f">>> Routine {i}:")
    op_cursor = 0
    for op in ops:
        lines.append(f"{op.offset:10x}: ({op.op_code.id:3}) {op.op_code.name:45} - [{', '.join([str(x) for x in op.params])}]")
        op_cursor += 2 + len(op.params) * 2
print('\n'.join(lines))
