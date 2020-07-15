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
from xml.dom import minidom
from xml.etree import ElementTree

from ndspy.rom import NintendoDSRom

from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler
from skytemple_files.dungeon_data.mappa_bin.model import MappaBin

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
os.makedirs(output_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))

mappa_bin = rom.getFileByName('BALANCE/mappa_s.bin')
mappa = MappaBinHandler.deserialize(mappa_bin)
assert mappa == MappaBinHandler.deserialize(mappa_bin)


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


xml = mappa.to_xml()
with open(os.path.join(output_dir, 'floors.xml'), 'w') as f:
    f.write(prettify(xml))

assert mappa == MappaBin.from_xml(xml)
