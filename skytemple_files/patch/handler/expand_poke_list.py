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

from typing import Callable, List

from ndspy.rom import NintendoDSRom
from range_typed_integers import u16_checked, u8

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.data import (
    GAME_REGION_EU,
    GAME_REGION_US,
    GAME_VERSION_EOS,
    Pmd2Data,
)
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import (
    normalize_string,
    get_files_from_rom_with_extension,
    read_u16,
    get_binary_from_rom,
    read_u32,
    set_binary_in_rom,
)
from skytemple_files.compression_container.pkdpx.handler import PkdpxHandler
from skytemple_files.container.bin_pack.handler import BinPackHandler
from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.data.level_bin_entry.model import LEVEL_BIN_ENTRY_LEVEL_LEN
from skytemple_files.data.md.handler import MdHandler
from skytemple_files.data.md.protocol import Gender
from skytemple_files.data.md_evo import MEVO_ENTRY_LENGTH, MEVO_STATS_LENGTH
from skytemple_files.data.md_evo.handler import MdEvoHandler
from skytemple_files.data.md_evo.model import MdEvoEntry, MdEvoStats
from skytemple_files.data.str.handler import StrHandler
from skytemple_files.data.tbl_talk.handler import TblTalkHandler
from skytemple_files.data.val_list.handler import ValListHandler
from skytemple_files.data.waza_p.handler import WazaPHandler
from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler
from skytemple_files.graphics.kao import SUBENTRIES
from skytemple_files.graphics.kao.handler import KaoHandler
from skytemple_files.hardcoded.dungeons import DungeonDefinition, HardcodedDungeons
from skytemple_files.hardcoded.fixed_floor import HardcodedFixedFloorTables
from skytemple_files.patch.category import PatchCategory
from skytemple_files.patch.handler.abstract import AbstractPatchHandler, DependantPatch

NUM_PREVIOUS_ENTRIES = 600
NUM_PREVIOUS_MD_MAX = 1155

DOJO_DUNGEONS_FIRST = u8(0xB4)
DOJO_DUNGEONS_LAST = u8(0xBF)
DOJO_MAPPA_ENTRY = u8(0x35)

PATCH_CHECK_ADDR_APPLIED_US = 0x5449C
PATCH_CHECK_ADDR_APPLIED_EU = 0x54818
PATCH_CHECK_INSTR_APPLIED = 0x00000483

US_TABLE_SF = 0xA3D14
EU_TABLE_SF = 0xA4314
JP_TABLE_SF = 0x0
US_TABLE_MF = 0xA3DAC
EU_TABLE_MF = 0xA43AC
JP_TABLE_MF = 0x0
US_TABLE_SP = 0x39B4
EU_TABLE_SP = 0x39A8
JP_TABLE_SP = 0x0
TABLE_SP_SIZE = 0xD8

US_NEW_PKMN_STR_REGION = 0x4814
US_NEW_CAT_STR_REGION = 0x5014
US_FILE_ASSOC = {"MESSAGE/text_e.str": ("BALANCE/st_m2n_j.bin", "BALANCE/st_n2m_j.bin")}
EU_NEW_PKMN_STR_REGION = 0x4833
EU_NEW_CAT_STR_REGION = 0x5033
EU_FILE_ASSOC = {
    "MESSAGE/text_e.str": ("BALANCE/st_m2n_e.bin", "BALANCE/st_n2m_e.bin"),
    "MESSAGE/text_f.str": ("BALANCE/st_m2n_f.bin", "BALANCE/st_n2m_f.bin"),
    "MESSAGE/text_g.str": ("BALANCE/st_m2n_g.bin", "BALANCE/st_n2m_g.bin"),
    "MESSAGE/text_i.str": ("BALANCE/st_m2n_i.bin", "BALANCE/st_n2m_i.bin"),
    "MESSAGE/text_s.str": ("BALANCE/st_m2n_s.bin", "BALANCE/st_n2m_s.bin"),
}
NUM_NEW_ENTRIES = 2048

DUMMY_PKMN = 553
DUMMY_LS = 150  # Using Mewtwo's learnset, as it's supposed to be one of the biggest
DUMMY_PERSONALITY = 0x20  # Using Dialga's personality


class ExpandPokeListPatchHandler(AbstractPatchHandler, DependantPatch):
    @property
    def name(self) -> str:
        return "ExpandPokeList"

    @property
    def description(self) -> str:
        return _(
            """Expand the pokemon entries allowed to 2048, and makes all the entries independent.
Needs ChangeEvoSystem, ExternalizeWazaFile, ExternalizeMappaFile patches to work.
It is strongly recommended to fix any dungeon error before applying this patch,
and to save a backup of your ROM before applying this."""
        )

    @property
    def author(self) -> str:
        return "Anonymous"

    @property
    def version(self) -> str:
        return "-1.0.0"

    @property
    def category(self) -> PatchCategory:
        return PatchCategory.IMPROVEMENT_TWEAK

    def depends_on(self) -> List[str]:
        return ["ChangeEvoSystem", "ExternalizeWazaFile", "ExternalizeMappaFile"]

    def is_applied(self, rom: NintendoDSRom, config: Pmd2Data) -> bool:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                return (
                    read_u32(rom.arm9, PATCH_CHECK_ADDR_APPLIED_US)
                    != PATCH_CHECK_INSTR_APPLIED
                )
            if config.game_region == GAME_REGION_EU:
                return (
                    read_u32(rom.arm9, PATCH_CHECK_ADDR_APPLIED_EU)
                    != PATCH_CHECK_INSTR_APPLIED
                )
        raise NotImplementedError()

    def apply(
        self, apply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        if config.game_version == GAME_VERSION_EOS:
            if config.game_region == GAME_REGION_US:
                new_pkmn_str_region = US_NEW_PKMN_STR_REGION
                new_cat_str_region = US_NEW_CAT_STR_REGION
                file_assoc = US_FILE_ASSOC
                table_sf = US_TABLE_SF
                table_mf = US_TABLE_MF
                table_sp = US_TABLE_SP
            if config.game_region == GAME_REGION_EU:
                new_pkmn_str_region = EU_NEW_PKMN_STR_REGION
                new_cat_str_region = EU_NEW_CAT_STR_REGION
                file_assoc = EU_FILE_ASSOC
                table_sf = EU_TABLE_SF
                table_mf = EU_TABLE_MF
                table_sp = EU_TABLE_SP
        if not self.is_applied(rom, config):
            bincfg = config.bin_sections.arm9
            binary = bytearray(get_binary_from_rom(rom, bincfg))

            # Apply the patch
            for filename in get_files_from_rom_with_extension(rom, "str"):
                bin_before = rom.getFileByName(filename)
                strings = StrHandler.deserialize(
                    bin_before, string_encoding=config.string_encoding
                )
                block = config.string_index_data.string_blocks["Pokemon Names"]
                monsters = strings.strings[block.begin : block.end]
                strings.strings[block.begin : block.end] = [""] * (
                    block.end - block.begin
                )
                block = config.string_index_data.string_blocks["Pokemon Categories"]
                cats = strings.strings[block.begin : block.end]
                strings.strings[block.begin : block.end] = [""] * (
                    block.end - block.begin
                )
                for x in range(NUM_NEW_ENTRIES):
                    if x < NUM_PREVIOUS_ENTRIES * 2:
                        str_pkmn = monsters[x % NUM_PREVIOUS_ENTRIES]
                    else:
                        str_pkmn = "DmyPk%04d" % x
                    if len(strings.strings) <= new_pkmn_str_region + x - 1:
                        strings.strings.append(str_pkmn)
                    else:
                        strings.strings[new_pkmn_str_region + x - 1] = str_pkmn
                for x in range(NUM_NEW_ENTRIES):
                    if x < NUM_PREVIOUS_ENTRIES * 2:
                        str_cat = cats[x % NUM_PREVIOUS_ENTRIES]
                    else:
                        str_cat = "DmyCa%04d" % x
                    if len(strings.strings) <= new_cat_str_region + x - 1:
                        strings.strings.append(str_cat)
                    else:
                        strings.strings[new_cat_str_region + x - 1] = str_cat
                bin_after = StrHandler.serialize(strings)
                rom.setFileByName(filename, bin_after)

                sorted_list = list(
                    enumerate(
                        strings.strings[
                            new_pkmn_str_region
                            - 1 : new_pkmn_str_region
                            - 1
                            + NUM_NEW_ENTRIES
                        ]
                    )
                )
                sorted_list.sort(key=lambda x: normalize_string(x[1]))
                sorted_list2 = [x[0] for x in sorted_list]
                inv_sorted_list = [
                    sorted_list2.index(i) for i in range(NUM_NEW_ENTRIES)
                ]
                m2n_model = ValListHandler.deserialize(
                    rom.getFileByName(file_assoc[filename][0])
                )
                m2n_model.set_list(inv_sorted_list)
                rom.setFileByName(
                    file_assoc[filename][0], ValListHandler.serialize(m2n_model)
                )
                n2m_model = ValListHandler.deserialize(
                    rom.getFileByName(file_assoc[filename][1])
                )
                n2m_model.set_list(sorted_list2)
                rom.setFileByName(
                    file_assoc[filename][1], ValListHandler.serialize(n2m_model)
                )

            # Expand kao file
            kao_bin = rom.getFileByName("FONT/kaomado.kao")
            kao_model = KaoHandler.deserialize(kao_bin)
            kao_model.expand(NUM_NEW_ENTRIES - 1)
            for i in range(NUM_PREVIOUS_ENTRIES - 1):
                for j in range(SUBENTRIES):
                    a = kao_model.get(i, j)
                    b = kao_model.get(i + NUM_PREVIOUS_ENTRIES, j)
                    if b is None and a is not None:
                        kao_model.set(i + NUM_PREVIOUS_ENTRIES, j, a)
            rom.setFileByName("FONT/kaomado.kao", KaoHandler.serialize(kao_model))

            # Expand tbl_talk
            tlk_bin = rom.getFileByName("MESSAGE/tbl_talk.tlk")
            tlk_model = TblTalkHandler.deserialize(tlk_bin)
            while tlk_model.get_nb_monsters() < NUM_NEW_ENTRIES:
                tlk_model.add_monster_personality(DUMMY_PERSONALITY)
            rom.setFileByName(
                "MESSAGE/tbl_talk.tlk", TblTalkHandler.serialize(tlk_model)
            )

            # Add monsters
            md_bin = rom.getFileByName("BALANCE/monster.md")
            md_model = MdHandler.deserialize(md_bin)
            new_entries = list(md_model.entries)
            while len(new_entries) < NUM_NEW_ENTRIES:
                new_entries.append(
                    FileType.MD.get_entry_model_cls().new_empty(
                        u16_checked(len(new_entries))
                    )
                )
            for i in range(NUM_PREVIOUS_ENTRIES):
                new_entries[i].entid = i
                if new_entries[NUM_PREVIOUS_ENTRIES + i].gender == Gender.INVALID.value:
                    new_entries[NUM_PREVIOUS_ENTRIES + i].entid = (
                        NUM_PREVIOUS_ENTRIES + i
                    )
                else:
                    new_entries[NUM_PREVIOUS_ENTRIES + i].entid = i
            block2 = bincfg.data.MONSTER_SPRITE_DATA
            data = (
                binary[block2.address : block2.address + block2.length]
                + binary[block2.address : block2.address + block2.length]
            )
            data += b"\x00\x00" * (NUM_NEW_ENTRIES - (len(data) // 2))
            for i in range(0, len(data), 2):
                new_entries[i // 2].unk17 = data[i]
                new_entries[i // 2].unk18 = data[i + 1]
                new_entries[i // 2].bitfield1_0 = False
                new_entries[i // 2].bitfield1_1 = False
                new_entries[i // 2].bitfield1_2 = False
                new_entries[i // 2].bitfield1_3 = False

            x = table_sf
            while read_u16(rom.arm9, x) != 0:
                pkmn_id = read_u16(rom.arm9, x)
                new_entries[
                    pkmn_id
                ].bitfield1_3 = True  # pylint: disable=invalid-sequence-index
                if (
                    new_entries[NUM_PREVIOUS_ENTRIES + pkmn_id].gender
                    != Gender.INVALID.value
                ):
                    new_entries[NUM_PREVIOUS_ENTRIES + pkmn_id].bitfield1_3 = True
                x += 2
            x = table_mf
            while read_u16(rom.arm9, x) != 0:
                pkmn_id = read_u16(rom.arm9, x)
                new_entries[
                    pkmn_id
                ].bitfield1_2 = True  # pylint: disable=invalid-sequence-index
                if (
                    new_entries[NUM_PREVIOUS_ENTRIES + pkmn_id].gender
                    != Gender.INVALID.value
                ):
                    new_entries[NUM_PREVIOUS_ENTRIES + pkmn_id].bitfield1_2 = True
                x += 2
            ov19 = rom.loadArm9Overlays([19])[19].data
            for x in range(table_sp, table_sp + TABLE_SP_SIZE, 2):
                pkmn_id = read_u16(ov19, x)
                new_entries[
                    pkmn_id
                ].bitfield1_1 = True  # pylint: disable=invalid-sequence-index
                new_entries[
                    pkmn_id
                ].bitfield1_0 = True  # pylint: disable=invalid-sequence-index
                if new_entries[NUM_PREVIOUS_ENTRIES + pkmn_id].gender != Gender.INVALID:
                    new_entries[NUM_PREVIOUS_ENTRIES + pkmn_id].bitfield1_1 = True
                    new_entries[NUM_PREVIOUS_ENTRIES + pkmn_id].bitfield1_0 = True

            md_model.entries = new_entries
            rom.setFileByName("BALANCE/monster.md", MdHandler.serialize(md_model))

            # Edit Mappa bin
            mappa_bin = rom.getFileByName("BALANCE/mappa_s.bin")
            mappa_model = MappaBinHandler.deserialize(mappa_bin)
            dl = HardcodedDungeons.get_dungeon_list(bytes(rom.arm9), config)
            # Handle Dojos
            start_floor = 0
            for x in range(DOJO_DUNGEONS_FIRST, DOJO_DUNGEONS_LAST - 2):
                dl.append(
                    DungeonDefinition(u8(5), DOJO_MAPPA_ENTRY, u8(start_floor), u8(0))
                )
                start_floor += 5
            dl.append(
                DungeonDefinition(u8(1), DOJO_MAPPA_ENTRY, u8(start_floor), u8(0))
            )
            start_floor += 1
            dl.append(
                DungeonDefinition(u8(0x30), DOJO_MAPPA_ENTRY, u8(start_floor), u8(0))
            )
            start_floor += 0x30
            for dungeon in dl:
                for f in range(
                    dungeon.start_after + 1,
                    dungeon.start_after + dungeon.number_floors,
                    2,
                ):
                    try:
                        for entry in mappa_model.floor_lists[dungeon.mappa_index][
                            f
                        ].monsters:
                            if (
                                entry.md_index != DUMMY_PKMN
                                and entry.md_index < NUM_PREVIOUS_ENTRIES
                                and entry.md_index + NUM_PREVIOUS_ENTRIES
                                < len(md_model.entries)
                                and md_model.entries[
                                    entry.md_index + NUM_PREVIOUS_ENTRIES
                                ].gender
                                != Gender.INVALID.value
                            ):
                                entry.md_index += NUM_PREVIOUS_ENTRIES
                    except:
                        print(f"{dungeon.mappa_index}, {f} is not valid.")
            rom.setFileByName(
                "BALANCE/mappa_s.bin", MappaBinHandler.serialize(mappa_model)
            )

            # Add moves
            waza_p_bin = rom.getFileByName("BALANCE/waza_p.bin")
            waza_p_model = WazaPHandler.deserialize(waza_p_bin)
            while len(waza_p_model.learnsets) < NUM_PREVIOUS_ENTRIES:
                waza_p_model.learnsets.append(
                    waza_p_model.learnsets[DUMMY_LS]
                )  # Max Moveset
            for new_moveset in waza_p_model.learnsets:
                waza_p_model.learnsets.append(new_moveset)
            while len(waza_p_model.learnsets) < NUM_NEW_ENTRIES:
                waza_p_model.learnsets.append(
                    waza_p_model.learnsets[DUMMY_LS]
                )  # Max Moveset
            rom.setFileByName(
                "BALANCE/waza_p.bin", WazaPHandler.serialize(waza_p_model)
            )

            # Add moves 2
            waza_p_bin = rom.getFileByName("BALANCE/waza_p2.bin")
            waza_p_model = WazaPHandler.deserialize(waza_p_bin)
            while len(waza_p_model.learnsets) < NUM_PREVIOUS_ENTRIES:
                waza_p_model.learnsets.append(
                    waza_p_model.learnsets[DUMMY_LS]
                )  # Max Moveset
            for new_moveset in waza_p_model.learnsets:
                waza_p_model.learnsets.append(new_moveset)
            while len(waza_p_model.learnsets) < NUM_NEW_ENTRIES:
                waza_p_model.learnsets.append(
                    waza_p_model.learnsets[DUMMY_LS]
                )  # Max Moveset
            rom.setFileByName(
                "BALANCE/waza_p2.bin", WazaPHandler.serialize(waza_p_model)
            )

            # Add levels
            level_bin = rom.getFileByName("BALANCE/m_level.bin")
            level_model = BinPackHandler.deserialize(level_bin)
            while len(level_model.get_files_bytes()) < NUM_PREVIOUS_ENTRIES:
                new_bytes_unpacked = bytes(LEVEL_BIN_ENTRY_LEVEL_LEN * 100)
                new_bytes_pkdpx = PkdpxHandler.serialize(
                    PkdpxHandler.compress(new_bytes_unpacked)
                )
                new_bytes = Sir0Handler.serialize(Sir0Handler.wrap(new_bytes_pkdpx, []))
                level_model.append(new_bytes)  # Empty Levelup data
            for i in range(NUM_PREVIOUS_ENTRIES):
                level_model.append(level_model[i])
            while len(level_model.get_files_bytes()) < NUM_NEW_ENTRIES:
                new_bytes_unpacked = bytes(LEVEL_BIN_ENTRY_LEVEL_LEN * 100)
                new_bytes_pkdpx = PkdpxHandler.serialize(
                    PkdpxHandler.compress(new_bytes_unpacked)
                )
                new_bytes = Sir0Handler.serialize(Sir0Handler.wrap(new_bytes_pkdpx, []))
                level_model.append(new_bytes)  # Empty Levelup data
            rom.setFileByName(
                "BALANCE/m_level.bin", BinPackHandler.serialize(level_model)
            )

            # Add evolutions
            evo_bin = rom.getFileByName("BALANCE/md_evo.bin")
            evo_model = MdEvoHandler.deserialize(evo_bin)
            while len(evo_model.evo_entries) < NUM_NEW_ENTRIES:
                evo_model.evo_entries.append(MdEvoEntry(bytearray(MEVO_ENTRY_LENGTH)))
            while len(evo_model.evo_stats) < NUM_NEW_ENTRIES:
                evo_model.evo_stats.append(MdEvoStats(bytearray(MEVO_STATS_LENGTH)))
            rom.setFileByName("BALANCE/md_evo.bin", MdEvoHandler.serialize(evo_model))

            # Fixed floors
            ov29 = config.bin_sections.overlay29
            ov29bin = bytearray(get_binary_from_rom(rom, ov29))
            monster_list = HardcodedFixedFloorTables.get_monster_spawn_list(
                ov29bin, config
            )
            for m in monster_list:
                if m.md_idx >= NUM_PREVIOUS_MD_MAX:
                    m.md_idx += NUM_NEW_ENTRIES - NUM_PREVIOUS_MD_MAX  # type: ignore
            HardcodedFixedFloorTables.set_monster_spawn_list(
                ov29bin, monster_list, config
            )
            set_binary_in_rom(rom, ov29, bytes(ov29bin))
        try:
            apply()
        except RuntimeError as ex:
            raise ex

    def unapply(
        self, unapply: Callable[[], None], rom: NintendoDSRom, config: Pmd2Data
    ) -> None:
        raise NotImplementedError()
