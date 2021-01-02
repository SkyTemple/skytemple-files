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
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    from pil import Image, ImageDraw, ImageFont
from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.common.script_util import load_script_files, SCRIPT_DIR
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_rom_folder, create_file_in_rom, read_uintle, write_uintle
from skytemple_files.script.ssa_sse_sss.actor import SsaActor
from skytemple_files.script.ssa_sse_sss.dbg.export_draw_maps import draw_maps_main
from skytemple_files.script.ssa_sse_sss.event import SsaEvent
from skytemple_files.script.ssa_sse_sss.handler import SsaHandler
from skytemple_files.script.ssa_sse_sss.object import SsaObject
from skytemple_files.script.ssa_sse_sss.position import SsaPosition

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

def main():
    os.makedirs(output_dir, exist_ok=True)

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))

    bin_before = rom.getFileByName('SCRIPT/G01P01A/enter.sse')
    ssa_before = SsaHandler.deserialize(bin_before)
    data = Pmd2XmlReader.load_default()
    scriptdata = data.script_data

    ssa_before.layer_list[0].objects = [
                                 # TODO: 5=Width, 1=Height!
        SsaObject(scriptdata, 6, 5, 1, SsaPosition(scriptdata, 44, 24, 0, 0, scriptdata.directions__by_name['Down'].id), 10, -1)
    ]

    # Write NPC types
    npc_table_start = data.binaries['arm9.bin'].blocks['Entities'].begin
    NPC_TABLE_ENTRY_LEN = 0x0c
    # uint16: type, uint16: entid, uint32: pointer to name, unk3, unk4

    # Shaymin NPC_SHEIMI 534 / V02P06A
    ent_id__shaymin = scriptdata.level_entities__by_name['NPC_SHEIMI'].id
    print(read_uintle(rom.arm9, npc_table_start + ent_id__shaymin * NPC_TABLE_ENTRY_LEN + 0x02, 2))
    write_uintle(rom.arm9, 534, npc_table_start + ent_id__shaymin * NPC_TABLE_ENTRY_LEN + 0x02, 2)
    # Elekid NPC_SHEIMI1 266 / V02P07A
    ent_id__elekid = scriptdata.level_entities__by_name['NPC_SHEIMI1'].id
    print(read_uintle(rom.arm9, npc_table_start + ent_id__elekid * NPC_TABLE_ENTRY_LEN + 0x02, 2))
    write_uintle(rom.arm9, 266, npc_table_start + ent_id__elekid * NPC_TABLE_ENTRY_LEN + 0x02, 2)
    # Piplup NPC_SHEIMI2 428 / V03P01A
    ent_id__piplup = scriptdata.level_entities__by_name['NPC_SHEIMI2'].id
    print(read_uintle(rom.arm9, npc_table_start + ent_id__piplup * NPC_TABLE_ENTRY_LEN + 0x02, 2))
    write_uintle(rom.arm9, 428, npc_table_start + ent_id__piplup * NPC_TABLE_ENTRY_LEN + 0x02, 2)
    # Meowth NPC_SHEIMI3 52 / V03P02A
    ent_id__meowth = scriptdata.level_entities__by_name['NPC_SHEIMI3'].id
    print(read_uintle(rom.arm9, npc_table_start + ent_id__meowth * NPC_TABLE_ENTRY_LEN + 0x02, 2))
    write_uintle(rom.arm9, 52, npc_table_start + ent_id__meowth * NPC_TABLE_ENTRY_LEN + 0x02, 2)
    # Buneary NPC_SHEIMI4 469 / V03P03A
    ent_id__buneary = scriptdata.level_entities__by_name['NPC_SHEIMI4'].id
    print(read_uintle(rom.arm9, npc_table_start + ent_id__buneary * NPC_TABLE_ENTRY_LEN + 0x02, 2))
    write_uintle(rom.arm9, 469, npc_table_start + ent_id__buneary * NPC_TABLE_ENTRY_LEN + 0x02, 2)

    ssa_before.layer_list[0].actors = [
        SsaActor(scriptdata, ent_id__shaymin,
                 SsaPosition(scriptdata, 14, 24, 2, 0, scriptdata.directions__by_name['Down'].id), 5, -1),
        SsaActor(scriptdata, ent_id__elekid,
                 SsaPosition(scriptdata, 20, 24, 2, 0, scriptdata.directions__by_name['Down'].id), 6, -1),
        SsaActor(scriptdata, ent_id__piplup,
                 SsaPosition(scriptdata, 26, 24, 2, 0, scriptdata.directions__by_name['Down'].id), 7, -1),
        SsaActor(scriptdata, ent_id__meowth,
                 SsaPosition(scriptdata, 32, 24, 2, 0, scriptdata.directions__by_name['Down'].id), 8, -1),
        SsaActor(scriptdata, ent_id__buneary,
                 SsaPosition(scriptdata, 38, 24, 2, 0, scriptdata.directions__by_name['Down'].id), 9, -1),
        # Mimikyu NPC_PUKURIN 40 / V03P04A
        # Litten NPC_ZUBATTO 41 / V04P02A
        # Zorua NPC_DIGUDA 50  / V03P13A
    ]
    ssa_before.layer_list[0].events = [
        SsaEvent(6, 2, 1, 0, SsaPosition(scriptdata, 27, 0, 0, 0, None), 65535),
        SsaEvent(6, 2, 2, 0, SsaPosition(scriptdata, 27, 49, 0, 0, None), 65535),
    ]

    # Exit Guild
    ssa_before.layer_list[1].actors = [
        SsaActor(scriptdata, 0, SsaPosition(scriptdata, 29, 7, 2, 0, scriptdata.directions__by_name['Down'].id), -1, -1),
        SsaActor(scriptdata, 10, SsaPosition(scriptdata, 29, 4, 2, 0, scriptdata.directions__by_name['Down'].id), -1, -1)
    ]

    # Exit Town
    ssa_before.layer_list[2].actors = [
        SsaActor(scriptdata, 0, SsaPosition(scriptdata, 29, 44, 2, 0, scriptdata.directions__by_name['Up'].id), -1, -1),
        SsaActor(scriptdata, 10, SsaPosition(scriptdata, 29, 47, 2, 0, scriptdata.directions__by_name['Up'].id), -1, -1)
    ]

    # Create scripts, if don't exist
    tpl_ssb = rom.getFileByName('SCRIPT/G01P01A/enter01.ssb')
    try:
        rom.getFileByName('SCRIPT/G01P01A/enter05.ssb')
    except ValueError:
        create_file_in_rom(rom, 'SCRIPT/G01P01A/enter05.ssb', tpl_ssb)
    try:
        rom.getFileByName('SCRIPT/G01P01A/enter06.ssb')
    except ValueError:
        create_file_in_rom(rom, 'SCRIPT/G01P01A/enter06.ssb', tpl_ssb)
    try:
        rom.getFileByName('SCRIPT/G01P01A/enter07.ssb')
    except ValueError:
        create_file_in_rom(rom, 'SCRIPT/G01P01A/enter07.ssb', tpl_ssb)
    try:
        rom.getFileByName('SCRIPT/G01P01A/enter08.ssb')
    except ValueError:
        create_file_in_rom(rom, 'SCRIPT/G01P01A/enter08.ssb', tpl_ssb)
    try:
        rom.getFileByName('SCRIPT/G01P01A/enter09.ssb')
    except ValueError:
        create_file_in_rom(rom, 'SCRIPT/G01P01A/enter09.ssb', tpl_ssb)
    try:
        rom.getFileByName('SCRIPT/G01P01A/enter10.ssb')
    except ValueError:
        create_file_in_rom(rom, 'SCRIPT/G01P01A/enter10.ssb', tpl_ssb)

    bin_after = SsaHandler.serialize(ssa_before)
    rom.setFileByName('SCRIPT/G01P01A/enter.sse', bin_after)
    rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))

    draw_maps_main()


if __name__ == '__main__':
    main()
