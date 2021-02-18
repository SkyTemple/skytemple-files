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
from typing import Callable

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.patch.handler.abstract import AbstractPatchHandler


class ExtraSpacePatch(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'ExtraSpace'

    @property
    def description(self) -> str:
        return "This patch adds a new overlay 36 to the game, which is loaded at address 0x023A7080 and provides extra space for patches to place code and data in."

    @property
    def author(self) -> str:
        return 'End45'

    @property
    def version(self) -> str:
        return '0.1.0'

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        # TODO
        raise NotImplementedError()

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        # Apply the patch
        apply()

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
