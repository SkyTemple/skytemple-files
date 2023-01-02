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

import os
import shutil
import subprocess
import sys
import tempfile

from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.util import (
    get_resources_dir,
    open_utf8,
    set_rw_permission_folder,
)
from skytemple_files.patch.arm_patcher import ArmipsNotInstalledError, PatchError
from skytemple_files.user_error import make_user_err

ASM_ENTRYPOINT_FN = "__main.asm"
OUT_BIN = "code_out.bin"


class ArmipsImporter:
    # TODO: Can probably merge that with the base patcher...
    def assemble(self, patch_asm: str):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copytree(
                os.path.join(
                    get_resources_dir(), "patches", "asm_patches", "eos_move_effects"
                ),
                tmp,
                dirs_exist_ok=True,
                symlinks=True,
            )

            set_rw_permission_folder(tmp)

            # Write final asm file
            with open_utf8(os.path.join(tmp, ASM_ENTRYPOINT_FN), "w") as file:
                file.write(patch_asm)

            # Run armips
            try:
                prefix = ""
                # Under Windows, try to load from SkyTemple _resources dir first.
                if sys.platform.startswith("win") and os.path.exists(
                    os.path.join(get_resources_dir(), "armips.exe")
                ):
                    prefix = os.path.join(get_resources_dir(), "")
                exec_name = os.getenv("SKYTEMPLE_ARMIPS_EXEC", f"{prefix}armips")
                result = subprocess.Popen(
                    [exec_name, ASM_ENTRYPOINT_FN],
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

            if retcode != 0:
                raise make_user_err(
                    PatchError,
                    _("ARMIPS reported an error while applying the patch."),
                    str(result.stdout.read(), "utf-8"),  # type: ignore
                    str(result.stderr.read(), "utf-8")  # type: ignore
                    if result.stderr
                    else "",
                )

            out_bin_path = os.path.join(tmp, OUT_BIN)
            if not os.path.exists(out_bin_path):
                raise ValueError(
                    f(_("The armips source file did not create a {OUT_BIN}."))
                )
            with open(out_bin_path, "rb") as file:
                return file.read()
