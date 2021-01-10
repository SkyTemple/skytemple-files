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
from xml.dom import minidom
from xml.etree.ElementTree import Element

from xml.etree import ElementTree

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_ppmdu_config_for_rom
from skytemple_files.common.xml_util import prettify
from skytemple_files.container.bin_pack.model import BinPack
from skytemple_files.data.md.model import NUM_ENTITIES, Md
from skytemple_files.data.monster_xml import monster_xml_export, monster_xml_import
from skytemple_files.data.waza_p.model import WazaP
from skytemple_files.graphics.kao.model import Kao, SUBENTRIES

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
os.makedirs(output_dir, exist_ok=True)

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
config = get_ppmdu_config_for_rom(rom)

def write_xml(xml, fn):
    with open(os.path.join(output_dir, fn), 'w') as f:
        f.write(prettify(xml))


md: Md = FileType.MD.deserialize(rom.getFileByName('BALANCE/monster.md'))
waza_p: WazaP = FileType.WAZA_P.deserialize(rom.getFileByName('BALANCE/waza_p.bin'))
waza_p2: WazaP = FileType.WAZA_P.deserialize(rom.getFileByName('BALANCE/waza_p2.bin'))
level_bin: BinPack = FileType.BIN_PACK.deserialize(rom.getFileByName('BALANCE/m_level.bin'))
kao: Kao = FileType.KAO.deserialize(rom.getFileByName('FONT/kaomado.kao'))
languages = {}
for lang in config.string_index_data.languages:
    languages[lang.name] = FileType.STR.deserialize(rom.getFileByName('MESSAGE/' + lang.filename))


for md_base_index in range(0, NUM_ENTITIES):
    md_gender1 = None
    md_gender2 = None
    names = None
    moveset = None
    moveset2 = None
    stats = None
    portraits = None
    portraits2 = None

    md_gender1 = md.entries[md_base_index]
    if NUM_ENTITIES + md_base_index < len(md.entries):
        md_gender2 = md.entries[NUM_ENTITIES + md_base_index]

    string_id = config.string_index_data.string_blocks['Pokemon Names'].begin + md_base_index
    cat_string_id = config.string_index_data.string_blocks['Pokemon Categories'].begin + md_base_index
    names = {}
    for lang_name, lang_model in languages.items():
        names[lang_name] = (lang_model.strings[string_id], lang_model.strings[cat_string_id])

    if md_base_index < len(waza_p.learnsets):
        moveset = waza_p.learnsets[md_base_index]

    if md_base_index < len(waza_p2.learnsets):
        moveset2 = waza_p2.learnsets[md_base_index]

    stat_id = md_base_index - 1
    if stat_id > -1 and stat_id < len(level_bin):
        stats = FileType.LEVEL_BIN_ENTRY.deserialize(
            FileType.COMMON_AT.deserialize(FileType.SIR0.deserialize(level_bin[stat_id]).content).decompress()
        )

    if stat_id > -1 and stat_id < kao.toc_len:
        portraits = []
        for kao_i in range(0, SUBENTRIES):
            portraits.append(kao.get(stat_id, kao_i))

    if stat_id > -1 and NUM_ENTITIES + stat_id < kao.toc_len:
        portraits2 = []
        for kao_i in range(0, SUBENTRIES):
            portraits2.append(kao.get(NUM_ENTITIES + stat_id, kao_i))
    
    xml = monster_xml_export(
        config.game_version, md_gender1, md_gender2,
        names,
        moveset, moveset2,
        stats, portraits, portraits2
    )
    fn = f'{md_base_index:04}_{languages["English"].strings[string_id].replace("?", "_")}.xml'
    print(fn)
    write_xml(xml, fn)


# try to replace Bulbasaur data with Charmanders
charmander_xml = ElementTree.parse(os.path.join(output_dir, '0004_Charmander.xml')).getroot()

#config.game_version
md_gender1 = md.entries[1]
md_gender2 = md.entries[601]
names = {}
string_id = config.string_index_data.string_blocks['Pokemon Names'].begin + 1
cat_string_id = config.string_index_data.string_blocks['Pokemon Categories'].begin + 1
for lang_name, lang_model in languages.items():
    names[lang_name] = (lang_model.strings[string_id], lang_model.strings[cat_string_id])
moveset = waza_p.learnsets[1]
moveset2 = waza_p.learnsets[1]
stats = FileType.LEVEL_BIN_ENTRY.deserialize(
    FileType.COMMON_AT.deserialize(FileType.SIR0.deserialize(level_bin[0]).content).decompress()
)
portraits = []
for kao_i in range(0, SUBENTRIES):
    portraits.append(kao.get(0, kao_i))
portraits2 = []
for kao_i in range(0, SUBENTRIES):
    portraits2.append(kao.get(600, kao_i))

# IMPORT CHARMANDER
assert monster_xml_import(
    charmander_xml,
    md_gender1, md_gender2,
    names,
    moveset, moveset2,
    stats, portraits, portraits2
) == config.game_version

bulbasaur_xml = monster_xml_export(
        config.game_version, md_gender1, md_gender2,
        names,
        moveset, moveset2,
        stats, portraits, portraits2
    )
write_xml(bulbasaur_xml, 'bulbasaur_but_actually_charmander.xml')

with open(os.path.join(output_dir, '0004_Charmander.xml')) as f_char:
    with open(os.path.join(output_dir, 'bulbasaur_but_actually_charmander.xml')) as f_bulba:
        assert f_char.read() == f_bulba.read()
