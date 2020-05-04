"""Testing script for ExplorerScript."""
#  Copyright 2020 Parakoopa
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

        out_file_name = os.path.join(output_dir, file_name.replace('/', '_') + '.exps')

        time_before = time.time()
        bin_before = rom.getFileByName(file_name)
        time_opening = time.time()
        ssb_before = SsbHandler.deserialize(bin_before)
        explorer_script, source_map_before = ssb_before.to_explorerscript()
        ssb_script, _ = ssb_before.to_ssb_script()
        time_decompiling = time.time()

        for pos_mark in source_map_before.position_marks:
            print(pos_mark)

        with open(out_file_name, 'w') as f:
            f.write(explorer_script)

        # Test the compiling and writing, by compiling the model, writing it to binary, and then loading it again,
        # and checking the generated ssb script.
        compiler = ScriptCompiler(Pmd2XmlReader.load_default())
        time_parsing = 0
        def callback_after_parsing():
            nonlocal time_parsing
            time_parsing = time.time()
        ssb_after, source_map_after = compiler.compile_explorerscript(explorer_script, callback_after_parsing)
        time_compiling = time.time()

        bin_after = SsbHandler.serialize(ssb_after)
        time_serializing = time.time()

        ssb_after = SsbHandler.deserialize(bin_after)
        ssb_script_after_compiling_and_decompiling, _ = ssb_after.to_ssb_script()

        dir_for_scripts_before = os.path.join(output_dir, 'exps_export_test', 'before')
        dir_for_scripts_after = os.path.join(output_dir, 'exps_export_test', 'after')
        os.makedirs(dir_for_scripts_before, exist_ok=True)
        os.makedirs(dir_for_scripts_after, exist_ok=True)
        with open(os.path.join(dir_for_scripts_before, file_name.replace('/', '_') + '.ssbs'), 'w') as f:
            f.write(ssb_script)
        with open(os.path.join(dir_for_scripts_after, file_name.replace('/', '_') + '.ssbs'), 'w') as f:
            f.write(ssb_script_after_compiling_and_decompiling)

        explorer_script_after_compiling_and_decompiling, source_map_after_cd = ssb_after.to_explorerscript()

        with open(os.path.join(dir_for_scripts_before, file_name.replace('/', '_') + '.exps'), 'w') as f:
            f.write(explorer_script)
        with open(os.path.join(dir_for_scripts_after, file_name.replace('/', '_') + '.exps'), 'w') as f:
            f.write(explorer_script_after_compiling_and_decompiling)

        # todo: assert(len(list(source_map_before)) == len(list(source_map_after)) == len(list(source_map_after_cd)))
        # todo: assert(SsbFlow(ssb_before) == SsbFlow(ssb_after))

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
