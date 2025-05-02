"""
Export ExplorerScript in the ROM provided.
Usage: python3 export_ssb.py ROM_NAME
The files will be exported in the current directory (sub-directory SCRIPT).
Required packages (pip install):
- skytemple-files
- tqdm
"""

#  Copyright 2022 Capypara and the SkyTemple Contributors
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

import asyncio
import logging
import os
import sys
import traceback
import warnings
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock

from ndspy.rom import NintendoDSRom
from tqdm import tqdm

from skytemple_files.common.util import (
    get_files_from_rom_with_extension,
    get_ppmdu_config_for_rom,
)
from skytemple_files.script.ssb.handler import SsbHandler

poison_container = [False]
loop = asyncio.get_event_loop_policy().get_event_loop()


progress_lock = Lock()
poison_lock = Lock()


async def main(executor, rom_file):
    rom = NintendoDSRom.fromFile(rom_file)

    static_data = get_ppmdu_config_for_rom(rom)
    awaitables = []
    for i, file_name in enumerate(get_files_from_rom_with_extension(rom, "ssb")):
        # Run multiple in parallel with asyncio executors.
        awaitables.append(loop.run_in_executor(executor, process_single, file_name, static_data, rom))

    print("Exporting scripts...")
    pending = awaitables
    with tqdm(total=len(pending)) as pbar:
        while len(pending) > 0:
            len_pending_before = len(pending)
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            pbar.update(len_pending_before - len(pending))
            # to raise exceptions of tasks back to main loop:
            for fut in done:
                try:
                    fut.result()
                except Exception:
                    loop.stop()
                    with poison_lock:
                        poison_container[0] = True
                    raise

    print("Done!")


def process_single(file_name, static_data, rom):
    if poison_container[0]:
        return

    out_file_name = os.path.join(os.getcwd(), file_name.replace(".ssb", ".exps"))
    os.makedirs(os.path.dirname(out_file_name), exist_ok=True)

    try:
        ssbbin = rom.getFileByName(file_name)
        ssb = SsbHandler.deserialize(ssbbin, static_data)
        explorer_script, _ = ssb.to_explorerscript()

        with open(out_file_name, "w", encoding="utf-8") as f:
            f.write(explorer_script)
    except BaseException as ex:
        raise RuntimeError(f"Error for {file_name}.") from ex


def handle_exception(loop, context):
    # context["message"] will always be there; but context["exception"] may not
    print(f"Exception while converting.", file=sys.stderr)
    if "exception" in context:
        ex = context["exception"]
        print(
            "".join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)),
            file=sys.stderr,
        )
    else:
        print(f"AsyncIO fatal error: {context['message']}", file=sys.stderr)
    loop.stop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a ROM name.", file=sys.stderr)
        exit(1)
    if not os.path.exists(sys.argv[1]):
        print(f"ROM {sys.argv[1]} not found.", file=sys.stderr)
        exit(1)

    logging.basicConfig(level=logging.ERROR)
    warnings.filterwarnings("ignore")

    executor = ThreadPoolExecutor(max_workers=max(2, os.cpu_count() - 2))
    loop.set_exception_handler(handle_exception)
    try:
        loop.run_until_complete(main(executor, sys.argv[1]))
    finally:
        loop.close()
        executor.shutdown()
