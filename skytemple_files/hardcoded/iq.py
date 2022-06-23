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
from __future__ import annotations

from itertools import chain

from range_typed_integers import u8_checked, u16_checked

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import *

IQ_GAINS_TABLES = {
    False: (18, 2),
    True: (25, 1)
}
IQ_SKILL_ENTRY_LEN = 4
IQ_SKILL_RESTR_ENTRY_LEN = 2
IQ_GROUP_LIST_LEN = 25
IQ_GROUP_COMPRESSED_LIST_LEN = 9


class IqSkill:
    iq_required: i32
    restriction_group: i16

    def __init__(self, iq_required: i32, restriction_group: i16):
        # 0x0000270F (9999) = Unused skill
        # 0xFFFFFFFF = Default IQ skill that all the groups have
        self.iq_required = iq_required
        self.restriction_group = restriction_group

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IqSkill):
            return False
        return self.iq_required == other.iq_required and self.restriction_group == other.restriction_group


class HardcodedIq:
    @staticmethod
    def get_min_iq_for_exclusive_move_user(arm9: bytes, config: Pmd2Data) -> u16:
        block = config.binaries['arm9.bin'].symbols['MinIqExclusiveMoveUser']
        return read_u16(arm9, block.begin)

    @staticmethod
    def set_min_iq_for_exclusive_move_user(value: u16, arm9: bytearray, config: Pmd2Data) -> None:
        block = config.binaries['arm9.bin'].symbols['MinIqExclusiveMoveUser']
        write_u16(arm9, value, block.begin)

    @staticmethod
    def get_min_iq_for_item_master(arm9: bytes, config: Pmd2Data) -> u16:
        block = config.binaries['arm9.bin'].symbols['MinIqItemMaster']
        return read_u16(arm9, block.begin)

    @staticmethod
    def set_min_iq_for_item_master(value: u16, arm9: bytearray, config: Pmd2Data) -> None:
        block = config.binaries['arm9.bin'].symbols['MinIqItemMaster']
        write_u16(arm9, value, block.begin)

    @staticmethod
    def get_intimidator_chance(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.binaries['overlay/overlay_0010.bin'].symbols['IntimidatorChance']
        return read_u16(ov10, block.begin)

    @staticmethod
    def set_intimidator_chance(value: u16, ov10: bytearray, config: Pmd2Data) -> None:
        block = config.binaries['overlay/overlay_0010.bin'].symbols['IntimidatorChance']
        write_u16(ov10, value, block.begin)

    @staticmethod
    def get_gummi_iq_gains(arm9: bytes, config: Pmd2Data, add_types_patch_applied: bool) -> List[List[int]]:
        dim, byte_size = IQ_GAINS_TABLES[add_types_patch_applied]
        block = config.binaries['arm9.bin'].symbols['IqGummiGain']
        lst = []
        for y in range(0, dim):
            row: List[int] = []
            lst.append(row)
            for x in range(0, dim):
                row.append(read_dynamic(arm9, block.begin + ((y * dim) + x) * byte_size, length=byte_size, big_endian=False, signed=False))
        return lst

    @staticmethod
    def set_gummi_iq_gains(value: List[List[int]], arm9: bytearray, config: Pmd2Data, add_types_patch_applied: bool) -> None:
        dim, byte_size = IQ_GAINS_TABLES[add_types_patch_applied]
        block = config.binaries['arm9.bin'].symbols['IqGummiGain']
        lst_flattened = list(chain.from_iterable(value))
        if len(lst_flattened) != dim * dim:
            raise ValueError("IQ gain table does not match ROM size")
        if byte_size == 1:
            for i, b in enumerate(lst_flattened):
                write_u8(arm9, u8_checked(b), block.begin + i * byte_size)
        else:
            for i, b in enumerate(lst_flattened):
                write_u16(arm9, u16_checked(b), block.begin + i * byte_size)

    @staticmethod
    def get_gummi_belly_heal(arm9: bytes, config: Pmd2Data, add_types_patch_applied: bool) -> List[List[int]]:
        dim, byte_size = IQ_GAINS_TABLES[add_types_patch_applied]
        block = config.binaries['arm9.bin'].symbols['GummiBellyHeal']
        lst = []
        for y in range(0, dim):
            row: List[int] = []
            lst.append(row)
            for x in range(0, dim):
                row.append(read_dynamic(
                    arm9, block.begin + ((y * dim) + x) * byte_size, length=byte_size, big_endian=False, signed=False
                ))
        return lst

    @staticmethod
    def set_gummi_belly_heal(value: List[List[int]], arm9: bytearray, config: Pmd2Data, add_types_patch_applied: bool) -> None:
        dim, byte_size = IQ_GAINS_TABLES[add_types_patch_applied]
        block = config.binaries['arm9.bin'].symbols['GummiBellyHeal']
        lst_flattened = list(chain.from_iterable(value))
        if len(lst_flattened) != dim * dim:
            raise ValueError("IQ gain table does not match ROM size")
        if byte_size == 1:
            for i, b in enumerate(lst_flattened):
                write_u8(arm9, u8_checked(b), block.begin + i * byte_size)
        else:
            for i, b in enumerate(lst_flattened):
                write_u16(arm9, u16_checked(b), block.begin + i * byte_size)

    @staticmethod
    def get_wonder_gummi_gain(arm9: bytes, config: Pmd2Data) -> u8:
        block = config.binaries['arm9.bin'].symbols['WonderGummiIqGain']
        return read_u8(arm9, block.begin)

    @staticmethod
    def set_wonder_gummi_gain(value: u8, arm9: bytearray, config: Pmd2Data) -> None:
        block = config.binaries['arm9.bin'].symbols['WonderGummiIqGain']
        write_u8(arm9, value, block.begin)

    @staticmethod
    def get_juice_bar_nectar_gain(arm9: bytes, config: Pmd2Data) -> u8:
        block = config.binaries['arm9.bin'].symbols['JuiceBarNectarIqGain']
        return read_u8(arm9, block.begin)

    @staticmethod
    def set_juice_bar_nectar_gain(value: u8, arm9: bytearray, config: Pmd2Data) -> None:
        block = config.binaries['arm9.bin'].symbols['JuiceBarNectarIqGain']
        write_u8(arm9, value, block.begin)

    @staticmethod
    def get_nectar_gain(ov29: bytes, config: Pmd2Data) -> u8:
        block = config.binaries['overlay/overlay_0029.bin'].symbols['NectarIqGain']
        return read_u8(ov29, block.begin)

    @staticmethod
    def set_nectar_gain(value: u8, ov29: bytearray, config: Pmd2Data) -> None:
        block = config.binaries['overlay/overlay_0029.bin'].symbols['NectarIqGain']
        write_u8(ov29, value, block.begin)

    @staticmethod
    def get_iq_skills(arm9bin: bytes, config: Pmd2Data) -> List[IqSkill]:
        block = config.binaries['arm9.bin'].symbols['IqSkills']
        block_restr = config.binaries['arm9.bin'].symbols['IqSkillRestrictions']
        assert (block.end - block.begin) // IQ_SKILL_ENTRY_LEN == (block_restr.end - block_restr.begin) // IQ_SKILL_RESTR_ENTRY_LEN
        lst = []
        for i in range(0, (block.end - block.begin) // IQ_SKILL_ENTRY_LEN):
            lst.append(IqSkill(
                read_i32(arm9bin, block.begin + (i * IQ_SKILL_ENTRY_LEN)),
                read_i16(arm9bin, block_restr.begin + (i * IQ_SKILL_RESTR_ENTRY_LEN))
            ))
        return lst

    @staticmethod
    def set_iq_skills(value: List[IqSkill], arm9bin: bytearray, config: Pmd2Data) -> None:
        block = config.binaries['arm9.bin'].symbols['IqSkills']
        block_restr = config.binaries['arm9.bin'].symbols['IqSkillRestrictions']
        assert (block.end - block.begin) // IQ_SKILL_ENTRY_LEN == (block_restr.end - block_restr.begin) // IQ_SKILL_RESTR_ENTRY_LEN
        expected_length = int((block.end - block.begin) / IQ_SKILL_ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            arm9bin[
                block.begin + i * IQ_SKILL_ENTRY_LEN:block.begin + (i + 1) * IQ_SKILL_ENTRY_LEN
            ] = entry.iq_required.to_bytes(IQ_SKILL_ENTRY_LEN, byteorder='little', signed=True)
            arm9bin[
                block_restr.begin + i * IQ_SKILL_RESTR_ENTRY_LEN:block_restr.begin + (i + 1) * IQ_SKILL_RESTR_ENTRY_LEN
            ] = entry.restriction_group.to_bytes(IQ_SKILL_RESTR_ENTRY_LEN, byteorder='little', signed=True)


class IqGroupsSkills:
    @staticmethod
    def read_uncompressed(arm9: bytes, config: Pmd2Data) -> List[List[u8]]:
        block = config.binaries['arm9.bin'].symbols['IqGroupsSkills']
        ret = []
        for i in range(block.begin, block.end, IQ_GROUP_LIST_LEN):
            skill_list = []
            for j in range(0, IQ_GROUP_LIST_LEN):
                current_skill = arm9[i + j]
                if current_skill == 0xFF:
                    break
                skill_list.append(u8(int(current_skill)))
            ret.append(skill_list)
        return ret

    @staticmethod
    def read_compressed(arm9: bytes, config: Pmd2Data) -> List[List[u8]]:
        block = config.binaries['arm9.bin'].symbols['CompressedIqGroupsSkills']
        ret = []
        for i in range(block.begin, block.end, IQ_GROUP_COMPRESSED_LIST_LEN):
            skill_list = []
            for j in range(0, IQ_GROUP_COMPRESSED_LIST_LEN):
                current_byte = arm9[i + j]
                for k in range(0, 8):
                    if current_byte & 1 << k != 0:
                        skill_list.append(u8(j * 8 + k))
            ret.append(skill_list)
        return ret

    @staticmethod
    def write_compressed(arm9: bytearray, data: List[List[u8]], config: Pmd2Data) -> None:
        block = config.binaries['arm9.bin'].symbols['CompressedIqGroupsSkills']
        expected_length = int((block.end - block.begin) / IQ_GROUP_COMPRESSED_LIST_LEN)
        if len(data) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")

        for i, group in enumerate(data):
            group_offset = block.begin + i * IQ_GROUP_COMPRESSED_LIST_LEN
            # Clear current group before writing anything
            arm9[group_offset:group_offset + IQ_GROUP_COMPRESSED_LIST_LEN] = [0] * IQ_GROUP_COMPRESSED_LIST_LEN

            for skill in group:
                byte = skill >> 3
                bit = skill & 7
                skill_offset = group_offset + byte
                arm9[skill_offset] = arm9[skill_offset] | 1 << bit
