"""Testing script for SsbScript."""
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
import time
from typing import List, Tuple

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.common.script_util import load_script_files, SCRIPT_DIR
from skytemple_files.common.util import get_rom_folder, get_files_from_rom_with_extension
from skytemple_files.script.ssb.handler import SsbHandler
from skytemple_files.script.ssb.script_compiler import ScriptCompiler


def print_table_row(r1, r2, r3, r4, r5, r6, r7):
    print(f"{r1:>15} {r2:>15} {r3:>15} {r4:>15} {r5:>15} {r6:>15} {r7:>15}")


def main():
    output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
    os.makedirs(output_dir, exist_ok=True)

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

    script_info = load_script_files(get_rom_folder(rom, SCRIPT_DIR))

    # total, opening. decompiling, parsing, compiling, serializing
    times: List[Tuple[float, float, float, float, float, float]] = []

    for i, file_name in enumerate(get_files_from_rom_with_extension(rom, 'ssb')):
        print(file_name)

        out_file_name = os.path.join(output_dir, file_name.replace('/', '_') + '.ssbs')

        time_before = time.time()
        bin_before = rom.getFileByName(file_name)
        time_opening = time.time()
        ssb_before = SsbHandler.deserialize(bin_before)
        ssb_script, source_map_before = ssb_before.to_ssb_script()
        time_decompiling = time.time()

        for pos_mark in source_map_before.get_position_marks__direct():
            print(pos_mark)

        with open(out_file_name, 'w') as f:
            f.write(ssb_script)

        # Test the compiling and writing, by compiling the model, writing it to binary, and then loading it again,
        # and checking the generated ssb script.
        compiler = ScriptCompiler(Pmd2XmlReader.load_default())
        time_parsing = 0
        def callback_after_parsing():
            nonlocal time_parsing
            time_parsing = time.time()
        ssb_after, source_map_after = compiler.compile_ssbscript(ssb_script, callback_after_parsing)
        time_compiling = time.time()

        bin_after = SsbHandler.serialize(ssb_after)
        time_serializing = time.time()
        ssb_after_after = SsbHandler.deserialize(bin_after)
        ssb_script_after = ssb_after_after.to_ssb_script()[0]

        with open('/tmp/diff1.ssb', 'w') as f:
            f.write(ssb_script)

        with open('/tmp/diff2.ssb', 'w') as f:
            f.write(ssb_script_after)

        assert(ssb_script == ssb_script_after)
        assert(source_map_before == source_map_after)

        times.append((
            time_serializing - time_before,  # total
            time_opening - time_before,  # opening.
            time_decompiling - time_opening,  # decompiling,
            time_parsing - time_decompiling,  # parsing,
            time_compiling - time_parsing,  # compiling,
            time_serializing - time_compiling,  # serializing
        ))

    times_structured = list(zip(*times))

    print_table_row("", "TOTAL", "OPENING", "DECOMPILING", "PARSING", "COMPILING", "SERIALIZING")
    print_table_row(*(["==========="] * 7))
    print_table_row("TOTAL:", *[round(sum(t), 2) for t in times_structured])
    print_table_row("AVG:", *[round(sum(t) / len(t), 2) for t in times_structured])
    print_table_row("MAX:", *[round(max(t), 2) for t in times_structured])
    print_table_row("MIN:", *[round(min(t), 2) for t in times_structured])


if __name__ == '__main__':
    main()
