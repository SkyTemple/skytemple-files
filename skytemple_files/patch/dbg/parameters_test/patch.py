#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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
from typing import Callable

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.patch.errors import PatchNotConfiguredError
from skytemple_files.patch.handler.abstract import AbstractPatchHandler


class PatchHandler(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'ParametersTest'

    @property
    def description(self) -> str:
        return "Tests patch parameters."

    @property
    def author(self) -> str:
        return 'End45'

    @property
    def version(self) -> str:
        return '0.1.0'

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        return False

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        print("DEBUGGING PATCH PARAMETERS:")
        self._debug("int_param")
        self._debug("int_param2")
        self._debug("int_param3")
        self._debug("select_param")
        self._debug("string_param")
        try:
            self._debug("doesntexist")
        except PatchNotConfiguredError:
            pass
        else:
            assert False, "Quering a non-existent variable must raise an error."
        # Apply the patch
        apply()

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data) -> None:
        raise NotImplementedError()

    def _debug(self, name: str):
        val = self.get_parameter(name)
        print(name, type(val), val)
