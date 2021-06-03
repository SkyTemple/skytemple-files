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

from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu
from skytemple_files.hardcoded.fixed_floor import HardcodedFixedFloorTables
from skytemple_files.hardcoded.icon_banner import IconBanner

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
out_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

banner = IconBanner(rom)
print(banner.title_english)
os.makedirs(out_dir, exist_ok=True)
banner.icon.to_pil().save(os.path.join(out_dir, 'banner.png'))
