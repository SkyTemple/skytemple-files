"""Checks, that models can be imported again"""
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

from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin_before = rom.getFileByName('MAP_BG/bg_list.dat')
bg_list = BgListDatHandler.deserialize(bin_before)

bin_after = BgListDatHandler.serialize(bg_list)

assert bin_after == bin_before

rom.setFileByName('MAP_BG/bg_list.dat', bin_after)

rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))