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
from typing import Callable

from ndspy.fnt import Folder
from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import get_resources_dir
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler
from skytemple_files.common.util import _
OV_FILE_IDX = 36
OV_FILE_PATH = os.path.join(get_resources_dir(), 'patches', 'asm_patches', 'end_asm_mods', 'src', 'overlay_0036.bin')


class ExtraSpacePatch(AbstractPatchHandler):

    @property
    def name(self) -> str:
        return 'ExtraSpace'

    @property
    def description(self) -> str:
        return _("This patch adds a new overlay 36 to the game, which is loaded at address 0x023A7080 and provides extra space for patches to place code and data in.")

    @property
    def author(self) -> str:
        return 'End45'

    @property
    def version(self) -> str:
        return '0.1.0'

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.UTILITY

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        return 36 in rom.loadArm9Overlays([36])

    def apply(self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):

        # Put the overlay file into the ROM
        folder: Folder = rom.filenames
        folder_first_file_id = folder.firstID
        assert folder_first_file_id == OV_FILE_IDX, "The overlay already exists or the ROM FAT is an unexpected state."
        with open(OV_FILE_PATH, 'rb') as f:
            rom.files.insert(OV_FILE_IDX, f.read())

        def recursive_increment_folder_start_idx(rfolder: Folder, if_bigger_than):
            if rfolder.firstID > if_bigger_than:
                rfolder.firstID += 1
            for _, sfolder in rfolder.folders:
                recursive_increment_folder_start_idx(sfolder, if_bigger_than)

        recursive_increment_folder_start_idx(rom.filenames, folder_first_file_id - 1)

        apply()

    def unapply(self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data):
        raise NotImplementedError()
