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
import shutil
import subprocess
import tempfile
from typing import Dict

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Patch, Pmd2Binary
from skytemple_files.common.util import get_binary_from_rom_ppmdu, set_binary_in_rom_ppmdu, open_utf8

ASM_ENTRYPOINT_FN = '__main.asm'


class PatchError(RuntimeError):
    def __init__(self, message: str, error_out: str):
        self.message = message
        self.error_out = error_out

    def __str__(self):
        return self.message + '\n' + self.error_out


class ArmipsNotInstalledError(RuntimeError):
    pass



class ArmPatcher:
    def __init__(self, rom: NintendoDSRom):
        self.rom = rom

    def apply(self, patch: Pmd2Patch, binaries: Dict[str, Pmd2Binary], patch_file_dir: str, stub_path: str):
        try:
            with tempfile.TemporaryDirectory() as tmp:
                shutil.copytree(patch_file_dir, tmp, dirs_exist_ok=True)

                # Build ASM file to run
                asm_entrypoint = ''

                # First read in  stub
                with open(os.path.join(tmp, stub_path)) as f:
                    asm_entrypoint += f.read() + '\n'

                # Then include other includes
                for include in patch.includes:
                    asm_entrypoint += f'.include "{os.path.join(tmp, include.filename)}"\n'

                # Build binary blocks
                for open_bin in patch.open_bins:
                    binary = binaries[open_bin.filepath]
                    binary_path = os.path.join(tmp, open_bin.filepath)
                    os.makedirs(os.path.dirname(binary_path), exist_ok=True)
                    # Write binary to tmp dir
                    with open(binary_path, 'wb') as f:
                        f.write(get_binary_from_rom_ppmdu(self.rom, binary))
                    asm_entrypoint += f'.open "{binary_path}", "{binary_path}_out.bin", 0x{binary.loadaddress:0x}\n'
                    for include in open_bin.includes:
                        asm_entrypoint += f'.include "{os.path.join(tmp, include.filename)}"\n'
                    asm_entrypoint += '.close\n'

                # Write final asm file
                with open_utf8(os.path.join(tmp, ASM_ENTRYPOINT_FN), 'w') as f:
                    f.write(asm_entrypoint)

                # Run armips
                original_cwd = os.getcwd()
                os.chdir(tmp)
                try:
                    result = subprocess.Popen(["armips", ASM_ENTRYPOINT_FN],
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT)
                    retcode = result.wait()
                except FileNotFoundError as ex:
                    raise ArmipsNotInstalledError("ARMIPS could not be found. Make sure, that "
                                                  "'armips' is inside your system's PATH.") from ex
                # Restore cwd
                os.chdir(original_cwd)

                if retcode != 0:
                    raise PatchError("ARMIPS reported an error while applying the patch.",
                                     str(result.stdout.read(), 'utf-8'))

                # Load the binaries back into the ROM
                for open_bin in patch.open_bins:
                    binary = binaries[open_bin.filepath]
                    binary_path = os.path.join(tmp, open_bin.filepath)
                    with open(binary_path + '_out.bin', 'rb') as f:
                        set_binary_in_rom_ppmdu(self.rom, binary, f.read())

        except (PatchError, ArmipsNotInstalledError):
            raise
        except BaseException as ex:
            raise RuntimeError("Error while applying the patch") from ex
