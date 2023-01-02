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
from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Dict, Union

from ndspy.rom import NintendoDSRom
from pmdsky_debug_py.protocol import SectionProtocol

from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.ppmdu_config.data import Pmd2Patch, Pmd2SimplePatch
from skytemple_files.common.util import (
    get_binary_from_rom,
    get_resources_dir,
    open_utf8,
    set_binary_in_rom,
    set_rw_permission_folder,
)
from skytemple_files.patch.handler.extra_space import OV_FILE_PATH
from skytemple_files.user_error import make_user_err

ASM_ENTRYPOINT_FN = "__main.asm"
Y9_BIN = "y9.bin"
logger = logging.getLogger(__name__)
EXPR_OVERLAY_PATH = re.compile(r"overlay/overlay_(\d+).bin")


class PatchError(RuntimeError):
    def __init__(self, message: str, error_out: str, error_err: str):
        self.message = message
        self.error_out = error_out
        self.error_err = error_err

    def __str__(self):
        return self.message + "\n" + self.error_out + "\n" + self.error_err


class ArmipsNotInstalledError(RuntimeError):
    pass


class ArmPatcher:
    def __init__(self, rom: NintendoDSRom):
        self.rom = rom

    def apply(
        self,
        patch: Union[Pmd2Patch, Pmd2SimplePatch],
        binaries: Dict[str, SectionProtocol],
        patch_file_dir: str,
        stub_path: str,
        game_id: str,
        parameter_values: Dict[str, Union[int, str]],
    ):
        with tempfile.TemporaryDirectory() as tmp:
            try:
                shutil.copytree(patch_file_dir, tmp, symlinks=True, dirs_exist_ok=True)

                set_rw_permission_folder(tmp)

                # Build ASM file to run
                asm_entrypoint = ""

                # First read in  stub
                with open(os.path.join(tmp, stub_path)) as fi:
                    asm_entrypoint += fi.read() + "\n"

                if isinstance(patch, Pmd2SimplePatch):
                    for replace in patch.string_replacements:
                        fn = os.path.join(tmp, replace.filename)
                        game = None
                        for game_candidate in replace.games:
                            if game_candidate.game_id == game_id:
                                game = game_candidate
                        if game is not None:
                            with open_utf8(os.path.join(tmp, fn), "r") as fi:
                                new_content = replace.regexp.sub(
                                    game.replace, fi.read()
                                )
                            with open_utf8(os.path.join(tmp, fn), "w") as fi:
                                fi.write(new_content)

                    # If it's a simple patch just output and re-import all binaries.
                    for binary_name, binary in binaries.items():
                        binary_path = binary_name_to_path(tmp, binary_name)
                        # Write binary to tmp dir
                        with open(binary_path, "wb") as fib:
                            try:
                                fib.write(get_binary_from_rom(self.rom, binary))
                            except ValueError as err:
                                if (
                                    binary_name == "overlay36"
                                    and patch.id == "ExtraSpace"
                                ):
                                    # SPECIAL CASE for ExtraSpace patch, the overlay hasn't been added to the overlay
                                    # table yet so get_binary_from_rom() fails.
                                    with open(OV_FILE_PATH, "rb") as ovfib:
                                        fib.write(ovfib.read())
                                else:
                                    raise err
                    # For simple patches we also output the overlay table as y9.bin:
                    binary_path = os.path.join(tmp, Y9_BIN)
                    # Write binary to tmp dir
                    with open(binary_path, "wb") as fib:
                        fib.write(self.rom.arm9OverlayTable)

                # Then include other includes
                for include in patch.includes:
                    asm_entrypoint += (
                        f'.include "{os.path.join(tmp, include.filename)}"\n'
                    )

                # Build binary blocks
                if isinstance(patch, Pmd2Patch):
                    for open_bin in patch.open_bins:
                        binary = binaries[binary_path_to_name(open_bin.filepath)]
                        binary_path = os.path.join(
                            tmp, open_bin.filepath.split("/")[-1]
                        )
                        os.makedirs(os.path.dirname(binary_path), exist_ok=True)
                        # Write binary to tmp dir
                        with open(binary_path, "wb") as fib:
                            fib.write(get_binary_from_rom(self.rom, binary))
                        asm_entrypoint += (
                            f'.open "{binary_path}", 0x{binary.loadaddress:0x}\n'
                        )
                        for include in open_bin.includes:
                            asm_entrypoint += (
                                f'.include "{os.path.join(tmp, include.filename)}"\n'
                            )
                        asm_entrypoint += ".close\n"

                # Write final asm file
                with open_utf8(os.path.join(tmp, ASM_ENTRYPOINT_FN), "w") as fi:
                    fi.write(asm_entrypoint)

                # Build parameters for equ
                parameters = []
                for param_name, param_value in parameter_values.items():
                    parameters += [
                        "-equ",
                        param_name,
                        f'"{param_value}"'
                        if isinstance(param_value, str)
                        else str(param_value),
                    ]

                # Run armips
                try:
                    prefix = ""
                    # Under Windows, try to load from SkyTemple _resources dir first.
                    if sys.platform.startswith("win") and os.path.exists(
                        os.path.join(get_resources_dir(), "armips.exe")
                    ):
                        prefix = os.path.join(get_resources_dir(), "")
                    exec_name = os.getenv("SKYTEMPLE_ARMIPS_EXEC", f"{prefix}armips")
                    cmd_line = [exec_name, ASM_ENTRYPOINT_FN] + parameters
                    if os.getenv("SKYTEMPLE_DEBUG_ARMIPS_OUTPUT", False):
                        print("ARMIPS CMDLINE:")
                        print(cmd_line)
                    result = subprocess.Popen(
                        cmd_line,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        cwd=tmp,
                    )
                    retcode = result.wait()
                except FileNotFoundError as ex:
                    raise make_user_err(
                        ArmipsNotInstalledError,
                        _(
                            "ARMIPS could not be found. Make sure, that "
                            "'armips' is inside your system's PATH."
                        ),
                    ) from ex

                if os.getenv("SKYTEMPLE_DEBUG_ARMIPS_OUTPUT", False):
                    print("ARMIPS OUTPUT:")
                    if result is not None:
                        print(str(result.stdout.read(), "utf-8"))  # type: ignore
                        print(str(result.stderr.read(), "utf-8") if result.stderr else "")  # type: ignore

                if retcode != 0:
                    raise make_user_err(
                        PatchError,
                        _("ARMIPS reported an error while applying the patch."),
                        str(result.stdout.read(), "utf-8"),  # type: ignore
                        str(result.stderr.read(), "utf-8")  # type: ignore
                        if result.stderr
                        else "",
                    )

                # Load the binaries back into the ROM
                opened_binaries = {}
                if isinstance(patch, Pmd2SimplePatch):
                    # Read in all binaries again
                    opened_binaries = binaries
                    # Also read in arm9OverlayTable
                    binary_path = os.path.join(tmp, Y9_BIN)
                    with open(binary_path, "rb") as fib:
                        self.rom.arm9OverlayTable = fib.read()
                else:
                    # Read opened binaries again
                    for open_bin in patch.open_bins:
                        binary_name = binary_path_to_name(open_bin.filepath)
                        opened_binaries[binary_name] = binaries[binary_name]
                for binary_name, binary in opened_binaries.items():
                    binary_path = binary_name_to_path(tmp, binary_name)
                    with open(binary_path, "rb") as fib:
                        set_binary_in_rom(self.rom, binary, fib.read())

            except (PatchError, ArmipsNotInstalledError):
                raise
            except BaseException as ex:
                raise RuntimeError(f(_("Error while applying the patch: {ex}"))) from ex


def binary_name_to_path(tmp_path: str, binary_name: str) -> str:
    """For compatibility with ppmdu binary names (prior SkyTemple 1.4)"""
    if binary_name.startswith("overlay"):
        binary_name = "overlay_" + f"{int(binary_name[7:]):04}"
    return os.path.join(tmp_path, binary_name + ".bin")


def binary_path_to_name(path: str) -> str:
    """For compatibility with ppmdu binary names (prior SkyTemple 1.4)"""
    matches = EXPR_OVERLAY_PATH.match(path)
    if matches is not None:
        return f"overlay{int(matches.group(1))}"
    else:
        return path.replace(".bin", "")
