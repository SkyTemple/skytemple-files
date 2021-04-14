"""Testing script for ExplorerScript."""
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
import asyncio
import logging
import os
import signal
import sys
import time
import traceback
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock
from typing import List, Tuple

from ndspy.rom import NintendoDSRom

from explorerscript.source_map_visualizer import SourceMapVisualizer
from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.common.script_util import load_script_files, SCRIPT_DIR
from skytemple_files.common.util import get_rom_folder, get_files_from_rom_with_extension
from skytemple_files.script.ssb.dbg.export_ssb_test import export_ssb_as_txt
from skytemple_files.script.ssb.flow import SsbFlow
from skytemple_files.script.ssb.handler import SsbHandler
from skytemple_files.script.ssb.script_compiler import ScriptCompiler


def print_table_row(r1, r2, r3, r4, r5, r6, r7):
    print(f"{r1:>15} {r2:>15} {r3:>15} {r4:>15} {r5:>15} {r6:>15} {r7:>15}")


rom_lock = Lock()
times_lock = Lock()
poison_lock = Lock()
poison_container = [False]
loop = asyncio.get_event_loop()
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


async def main(executor):
    output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
    os.makedirs(output_dir, exist_ok=True)

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us_unpatched.nds'))

    script_info = load_script_files(get_rom_folder(rom, SCRIPT_DIR))

    # total, opening. decompiling, parsing, compiling, serializing
    times: List[Tuple[float, float, float, float, float, float]] = []

    static_data = Pmd2XmlReader.load_default(for_version='EoS_NA')
    awaitables = []
    for i, file_name in enumerate(get_files_from_rom_with_extension(rom, 'ssb')):
        # TODO: Those scripts fail for JP.
        if file_name in ['SCRIPT/D42P21A/enter23.ssb', 
                         'SCRIPT/D73P11A/us0303.ssb',
                         'SCRIPT/D73P11A/us0305.ssb',
                         'SCRIPT/D73P11A/us2003.ssb',
                         'SCRIPT/D73P11A/us2005.ssb',
                         'SCRIPT/D73P11A/us2103.ssb',
                         'SCRIPT/D73P11A/us2105.ssb',
                         'SCRIPT/D73P11A/us2203.ssb',
                         'SCRIPT/D73P11A/us2205.ssb',
                         'SCRIPT/D73P11A/us2303.ssb',
                         'SCRIPT/D73P11A/us2305.ssb']:
            continue
        # Run multiple in parallel with asyncio executors.
        awaitables.append(loop.run_in_executor(
            executor,
            process_single,

            file_name, times, static_data, output_dir, rom
        ))

    pending = awaitables
    while len(pending) > 0:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        # to raise exceptions of tasks back to main loop:
        for fut in done:
            try:
                fut.result()
            except Exception:
                loop.stop()
                with poison_lock:
                    poison_container[0] = True
                raise

    times_structured = list(zip(*times))

    print_table_row("", "TOTAL", "OPENING", "DECOMPILING", "PARSING", "COMPILING", "SERIALIZING")
    print_table_row(*(["==========="] * 7))
    print_table_row("TOTAL:", *[round(sum(t), 2) for t in times_structured])
    print_table_row("AVG:", *[round(sum(t) / len(t), 2) for t in times_structured])
    print_table_row("MAX:", *[round(max(t), 2) for t in times_structured])
    print_table_row("MIN:", *[round(min(t), 2) for t in times_structured])

    #rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_all_scripts_replaced.nds'))


def process_single(file_name, times, static_data, output_dir, rom):
    if poison_container[0]:
        return
    print(file_name)

    out_file_name = os.path.join(output_dir, file_name.replace('.ssb', '.exps'))
    os.makedirs(os.path.dirname(out_file_name), exist_ok=True)

    try:

        with rom_lock:
            time_before = time.time()
            bin_before = rom.getFileByName(file_name)
            time_opening = time.time()
        ssb_before = SsbHandler.deserialize(bin_before, static_data)
        explorer_script, source_map_before = ssb_before.to_explorerscript()
        time_decompiling = time.time()
        ssb_script, _ = ssb_before.to_ssb_script()
        time_decompiling_ssb_script = time.time()

        for pos_mark in source_map_before.get_position_marks__direct():
            print(pos_mark)

        with open(out_file_name, 'w') as f:
            f.write(explorer_script)

        # Test the compiling and writing, by compiling the model, writing it to binary, and then loading it again,
        # and checking the generated ssb script.
        compiler = ScriptCompiler(static_data)
        time_parsing = 0

        def callback_after_parsing():
            nonlocal time_parsing
            time_parsing = time.time()

        ssb_after, source_map_after = compiler.compile_explorerscript(explorer_script, file_name, callback_after_parsing)
        time_compiling = time.time()

        bin_after = SsbHandler.serialize(ssb_after, static_data)
        time_serializing = time.time()

        ssb_after = SsbHandler.deserialize(bin_after, static_data)
        ssb_script_after_compiling_and_decompiling, _ = ssb_after.to_ssb_script()

        """
        dir_for_scripts_sm = os.path.join(output_dir, 'exps_export_test', 'source_maps')
        dir_for_scripts_before = os.path.join(output_dir, 'exps_export_test', 'before')
        dir_for_scripts_after = os.path.join(output_dir, 'exps_export_test', 'after')
        os.makedirs(dir_for_scripts_before, exist_ok=True)
        os.makedirs(dir_for_scripts_after, exist_ok=True)
        os.makedirs(dir_for_scripts_sm, exist_ok=True)
        with open(os.path.join(dir_for_scripts_before, file_name.replace('/', '_') + '.ssbs'), 'w') as f:
            f.write(ssb_script)
        with open(os.path.join(dir_for_scripts_after, file_name.replace('/', '_') + '.ssbs'), 'w') as f:
            f.write(ssb_script_after_compiling_and_decompiling)

        explorer_script_after_compiling_and_decompiling, source_map_after_cd = ssb_after.to_explorerscript()

        with open(os.path.join(dir_for_scripts_before, file_name.replace('/', '_') + '.exps'), 'w') as f:
            f.write(explorer_script)
        with open(os.path.join(dir_for_scripts_after, file_name.replace('/', '_') + '.exps'), 'w') as f:
            f.write(explorer_script_after_compiling_and_decompiling)
        """

        # Run flow check
        ssb_flow_before = SsbFlow(ssb_before, static_data)
        ssb_flow_after = SsbFlow(ssb_after, static_data)

        """
        ssb_flow_before.to_dot(os.path.join(dir_for_scripts_before, file_name.replace('/', '_') + '.flow'))
        ssb_flow_after.to_dot(os.path.join(dir_for_scripts_after, file_name.replace('/', '_') + '.flow'))
        """

        ssb_flow_before.assert_equal(ssb_flow_after)

        """
        # Output source maps
        with open(os.path.join(dir_for_scripts_sm, file_name.replace('/', '_') + '_after_decompile.sm.exps'), 'w') as f:
            f.write(SourceMapVisualizer(explorer_script, source_map_before).write())
        with open(os.path.join(dir_for_scripts_sm, file_name.replace('/', '_') + '_after_compile.sm.exps'), 'w') as f:
            f.write(SourceMapVisualizer(explorer_script, source_map_after).write())

        with open(os.path.join(dir_for_scripts_before, file_name.replace('/', '_') + '.ssb_txt'), 'w') as f:
            f.write(export_ssb_as_txt(ssb_before))
        with open(os.path.join(dir_for_scripts_after, file_name.replace('/', '_') + '.ssb_txt'), 'w') as f:
            f.write(export_ssb_as_txt(ssb_after))
        """

        with rom_lock:
            rom.setFileByName(file_name, bin_after)

        with times_lock:
            times.append((
                time_serializing - time_before,  # total
                time_opening - time_before,  # opening.
                time_decompiling - time_opening,  # decompiling,
                time_parsing - time_decompiling_ssb_script,  # parsing,
                time_compiling - time_parsing,  # compiling,
                time_serializing - time_compiling,  # serializing
            ))
    except BaseException as ex:
        raise RuntimeError(f"Error for {file_name}.") from ex


def handle_exception(loop, context):
    # context["message"] will always be there; but context["exception"] may not
    print(f"Exception while converting.", file=sys.stderr)
    if "exception" in context:
        ex = context["exception"]
        print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)), file=sys.stderr)
    else:
        print(f"AsyncIO fatal error: {context['message']}", file=sys.stderr)
    loop.stop()


if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=max(2, os.cpu_count() - 2))
    loop.set_exception_handler(handle_exception)
    try:
        loop.run_until_complete(main(executor))
    finally:
        loop.close()
        executor.shutdown()
