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

from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler
from skytemple_files.dungeon_data.mappa_g_bin.handler import MappaGBinHandler
from skytemple_files.dungeon_data.mappa_g_bin.mappa_converter import convert_mappa_to_mappag

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

mappag_bin = rom.getFileByName('BALANCE/mappa_gs.bin')
mappa_g = MappaGBinHandler.deserialize(mappag_bin)

mappa_bin = rom.getFileByName('BALANCE/mappa_s.bin')
mappa = MappaBinHandler.deserialize(mappa_bin)

assert mappa_g == convert_mappa_to_mappag(mappa)
