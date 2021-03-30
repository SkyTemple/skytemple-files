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
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Dict, Union

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Patch, Pmd2Binary, Pmd2SimplePatch
from skytemple_files.common.util import get_binary_from_rom_ppmdu, set_binary_in_rom_ppmdu, open_utf8, get_resources_dir
from skytemple_files.common.i18n_util import f, _

ASM_ENTRYPOINT_FN = '__main.asm'
Y9_BIN = 'y9.bin'
logger = logging.getLogger(__name__)


class PatchError(RuntimeError):
    def __init__(self, message: str, error_out: str, error_err: str):
        self.message = message
        self.error_out = error_out
        self.error_err = error_err

    def __str__(self):
        return self.message + '\n' + self.error_out + '\n' + self.error_err


class ArmipsNotInstalledError(RuntimeError):
    pass


class ArmPatcher:
    def __init__(self, rom: NintendoDSRom):
        self.rom = rom

    def apply(self, patch: Union[Pmd2Patch, Pmd2SimplePatch],
              binaries: Dict[str, Pmd2Binary], patch_file_dir: str, stub_path: str, game_id: str):
        with tempfile.TemporaryDirectory() as tmp:
            try:
                shutil.copytree(patch_file_dir, tmp, dirs_exist_ok=True)

                # Build ASM file to run
                asm_entrypoint = ''

                # First read in  stub
                with open(os.path.join(tmp, stub_path)) as f:
                    asm_entrypoint += f.read() + '\n'

                if isinstance(patch, Pmd2SimplePatch):
                    for replace in patch.string_replacements:
                        fn = os.path.join(tmp, replace.filename)
                        game = None
                        for game_candidate in replace.games:
                            if game_candidate.game_id == game_id:
                                game = game_candidate
                        if game is not None:
                            with open(os.path.join(tmp, fn), 'r') as f:
                                new_content = replace.regexp.sub(game.replace, f.read())
                            with open(os.path.join(tmp, fn), 'w') as f:
                                f.write(new_content)

                    # If it's a simple patch just output and re-import all binaries.
                    for binary_name, binary in binaries.items():
                        binary_path = os.path.join(tmp, binary_name.split('/')[-1])
                        # Write binary to tmp dir
                        with open(binary_path, 'wb') as f:
                            try:
                                f.write(get_binary_from_rom_ppmdu(self.rom, binary))
                            except ValueError as err:
                                if binary_name.split('/')[-1] == 'overlay_0036.bin':
                                    continue  # We ignore if End's extra overlay is missing.
                                raise err
                    # For simple patches we also output the overlay table as y9.bin:
                    binary_path = os.path.join(tmp, Y9_BIN)
                    # Write binary to tmp dir
                    with open(binary_path, 'wb') as f:
                        f.write(self.rom.arm9OverlayTable)

                # Then include other includes
                for include in patch.includes:
                    asm_entrypoint += f'.include "{os.path.join(tmp, include.filename)}"\n'

                # Build binary blocks
                if isinstance(patch, Pmd2Patch):
                    for open_bin in patch.open_bins:
                        binary = binaries[open_bin.filepath]
                        binary_path = os.path.join(tmp, open_bin.filepath.split('/')[-1])
                        os.makedirs(os.path.dirname(binary_path), exist_ok=True)
                        # Write binary to tmp dir
                        with open(binary_path, 'wb') as f:
                            f.write(get_binary_from_rom_ppmdu(self.rom, binary))
                        asm_entrypoint += f'.open "{binary_path}", 0x{binary.loadaddress:0x}\n'
                        for include in open_bin.includes:
                            asm_entrypoint += f'.include "{os.path.join(tmp, include.filename)}"\n'
                        asm_entrypoint += '.close\n'

                # Write final asm file
                with open_utf8(os.path.join(tmp, ASM_ENTRYPOINT_FN), 'w') as f:
                    f.write(asm_entrypoint)

                # Run armips
                try:
                    prefix = ""
                    # Under Windows, try to load from SkyTemple _resources dir first.
                    if sys.platform.startswith('win') and os.path.exists(os.path.join(get_resources_dir(), 'armips.exe')):
                        prefix = os.path.join(get_resources_dir(), '')
                    exec_name = os.getenv('SKYTEMPLE_ARMIPS_EXEC', f'{prefix}armips')
                    result = subprocess.Popen([exec_name, ASM_ENTRYPOINT_FN],
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT,
                                              cwd=tmp
                                              )
                    retcode = result.wait()
                except FileNotFoundError as ex:
                    raise ArmipsNotInstalledError(_("ARMIPS could not be found. Make sure, that "
                                                    "'armips' is inside your system's PATH.")) from ex

                if retcode != 0:

                    logger.warning("Failed applying an armips patch. Debugging information follow.")
                    logger.warning("Tmp dir name: " + tmp)
                    logger.warning("Patch dir name: " + patch_file_dir)
                    contents = "???"
                    try:
                        lsresult = subprocess.Popen(['ls', '-la', tmp],
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT)
                        lsresult.wait()
                        contents = str(lsresult.stdout.read(), 'utf-8')
                    except BaseException:
                        pass
                    logger.warning("Contents of dir:\n" + contents)
                    stdout = "???"
                    try:
                        stdout = str(result.stdout.read(), 'utf-8')
                    except BaseException:
                        pass
                    logger.warning("Stdout:\n" + stdout)

                    raise PatchError(_("ARMIPS reported an error while applying the patch."),
                                     str(result.stdout.read(), 'utf-8'), str(result.stderr.read(), 'utf-8') if result.stderr else '')

                # Load the binaries back into the ROM
                opened_binaries = {}
                if isinstance(patch, Pmd2SimplePatch):
                    # Read in all binaries again
                    opened_binaries = binaries
                    # Also read in arm9OverlayTable
                    binary_path = os.path.join(tmp, Y9_BIN)
                    with open(binary_path, 'rb') as f:
                        self.rom.arm9OverlayTable = f.read()
                else:
                    # Read opened binaries again
                    for open_bin in patch.open_bins:
                        opened_binaries[open_bin.filepath] = binaries[open_bin.filepath]
                for binary_name, binary in opened_binaries.items():
                    binary_path = os.path.join(tmp, binary_name.split('/')[-1])
                    with open(binary_path, 'rb') as f:
                        try:
                            set_binary_in_rom_ppmdu(self.rom, binary, f.read())
                        except ValueError as err:
                            if binary_name.split('/')[-1] == 'overlay_0036.bin':
                                continue  # We ignore if End's extra overlay is missing.
                            raise err

            except (PatchError, ArmipsNotInstalledError):
                raise
            except BaseException as ex:
                raise RuntimeError(f(_("Error while applying the patch: {ex}"))) from ex
