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

from itertools import chain
from typing import List

from range_typed_integers import u8_checked, u16_checked, i32, i16, u16, u8

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import (
    read_i32,
    read_u8,
    read_i16,
    read_u16,
    write_u16,
    read_dynamic,
    write_u8,
)

IQ_GAINS_TABLES = {False: (18, 2), True: (25, 1)}
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
        return (
            self.iq_required == other.iq_required
            and self.restriction_group == other.restriction_group
        )


class HardcodedIq:
    @staticmethod
    def get_min_iq_for_exclusive_move_user(arm9: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.arm9.data.MIN_IQ_EXCLUSIVE_MOVE_USER
        return read_u16(arm9, block.address)

    @staticmethod
    def set_min_iq_for_exclusive_move_user(
        value: u16, arm9: bytearray, config: Pmd2Data
    ) -> None:
        block = config.bin_sections.arm9.data.MIN_IQ_EXCLUSIVE_MOVE_USER
        write_u16(arm9, value, block.address)

    @staticmethod
    def get_min_iq_for_item_master(arm9: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.arm9.data.MIN_IQ_ITEM_MASTER
        return read_u16(arm9, block.address)

    @staticmethod
    def set_min_iq_for_item_master(
        value: u16, arm9: bytearray, config: Pmd2Data
    ) -> None:
        block = config.bin_sections.arm9.data.MIN_IQ_ITEM_MASTER
        write_u16(arm9, value, block.address)

    @staticmethod
    def get_intimidator_chance(ov10: bytes, config: Pmd2Data) -> u16:
        block = config.bin_sections.overlay10.data.INTIMIDATOR_ACTIVATION_CHANCE
        return read_u16(ov10, block.address)

    @staticmethod
    def set_intimidator_chance(value: u16, ov10: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.overlay10.data.INTIMIDATOR_ACTIVATION_CHANCE
        write_u16(ov10, value, block.address)

    @staticmethod
    def get_gummi_iq_gains(
        arm9: bytes, config: Pmd2Data, add_types_patch_applied: bool
    ) -> List[List[int]]:
        dim, byte_size = IQ_GAINS_TABLES[add_types_patch_applied]
        block = config.bin_sections.arm9.data.IQ_GUMMI_GAIN_TABLE
        lst = []
        for y in range(0, dim):
            row: List[int] = []
            lst.append(row)
            for x in range(0, dim):
                row.append(
                    read_dynamic(
                        arm9,
                        block.address + ((y * dim) + x) * byte_size,
                        length=byte_size,
                        big_endian=False,
                        signed=False,
                    )
                )
        return lst

    @staticmethod
    def set_gummi_iq_gains(
        value: List[List[int]],
        arm9: bytearray,
        config: Pmd2Data,
        add_types_patch_applied: bool,
    ) -> None:
        dim, byte_size = IQ_GAINS_TABLES[add_types_patch_applied]
        block = config.bin_sections.arm9.data.IQ_GUMMI_GAIN_TABLE
        lst_flattened = list(chain.from_iterable(value))
        if len(lst_flattened) != dim * dim:
            raise ValueError("IQ gain table does not match ROM size")
        if byte_size == 1:
            for i, b in enumerate(lst_flattened):
                write_u8(arm9, u8_checked(b), block.address + i * byte_size)
        else:
            for i, b in enumerate(lst_flattened):
                write_u16(arm9, u16_checked(b), block.address + i * byte_size)

    @staticmethod
    def get_gummi_belly_heal(
        arm9: bytes, config: Pmd2Data, add_types_patch_applied: bool
    ) -> List[List[int]]:
        dim, byte_size = IQ_GAINS_TABLES[add_types_patch_applied]
        block = config.bin_sections.arm9.data.GUMMI_BELLY_RESTORE_TABLE
        lst = []
        for y in range(0, dim):
            row: List[int] = []
            lst.append(row)
            for x in range(0, dim):
                row.append(
                    read_dynamic(
                        arm9,
                        block.address + ((y * dim) + x) * byte_size,
                        length=byte_size,
                        big_endian=False,
                        signed=False,
                    )
                )
        return lst

    @staticmethod
    def set_gummi_belly_heal(
        value: List[List[int]],
        arm9: bytearray,
        config: Pmd2Data,
        add_types_patch_applied: bool,
    ) -> None:
        dim, byte_size = IQ_GAINS_TABLES[add_types_patch_applied]
        block = config.bin_sections.arm9.data.GUMMI_BELLY_RESTORE_TABLE
        lst_flattened = list(chain.from_iterable(value))
        if len(lst_flattened) != dim * dim:
            raise ValueError("IQ gain table does not match ROM size")
        if byte_size == 1:
            for i, b in enumerate(lst_flattened):
                write_u8(arm9, u8_checked(b), block.address + i * byte_size)
        else:
            for i, b in enumerate(lst_flattened):
                write_u16(arm9, u16_checked(b), block.address + i * byte_size)

    @staticmethod
    def get_wonder_gummi_gain(arm9: bytes, config: Pmd2Data) -> u8:
        block = config.bin_sections.arm9.data.WONDER_GUMMI_IQ_GAIN
        return read_u8(arm9, block.address)

    @staticmethod
    def set_wonder_gummi_gain(value: u8, arm9: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.arm9.data.WONDER_GUMMI_IQ_GAIN
        write_u8(arm9, value, block.address)

    @staticmethod
    def get_juice_bar_nectar_gain(arm9: bytes, config: Pmd2Data) -> u8:
        block = config.bin_sections.arm9.data.JUICE_BAR_NECTAR_IQ_GAIN
        return read_u8(arm9, block.address)

    @staticmethod
    def set_juice_bar_nectar_gain(value: u8, arm9: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.arm9.data.JUICE_BAR_NECTAR_IQ_GAIN
        write_u8(arm9, value, block.address)

    @staticmethod
    def get_nectar_gain(ov29: bytes, config: Pmd2Data) -> u8:
        block = config.bin_sections.overlay29.data.NECTAR_IQ_BOOST
        return read_u8(ov29, block.address)

    @staticmethod
    def set_nectar_gain(value: u8, ov29: bytearray, config: Pmd2Data) -> None:
        block = config.bin_sections.overlay29.data.NECTAR_IQ_BOOST
        write_u8(ov29, value, block.address)

    @staticmethod
    def get_iq_skills(arm9bin: bytes, config: Pmd2Data) -> List[IqSkill]:
        block = config.bin_sections.arm9.data.IQ_SKILLS
        block_restr = config.bin_sections.arm9.data.IQ_SKILL_RESTRICTIONS
        assert block.length is not None
        assert block_restr.length is not None
        assert (
            block.length // IQ_SKILL_ENTRY_LEN
            == block_restr.length // IQ_SKILL_RESTR_ENTRY_LEN
        )
        lst = []
        for i in range(0, block.length // IQ_SKILL_ENTRY_LEN):
            lst.append(
                IqSkill(
                    read_i32(arm9bin, block.address + (i * IQ_SKILL_ENTRY_LEN)),
                    read_i16(
                        arm9bin, block_restr.address + (i * IQ_SKILL_RESTR_ENTRY_LEN)
                    ),
                )
            )
        return lst

    @staticmethod
    def set_iq_skills(
        value: List[IqSkill], arm9bin: bytearray, config: Pmd2Data
    ) -> None:
        block = config.bin_sections.arm9.data.IQ_SKILLS
        block_restr = config.bin_sections.arm9.data.IQ_SKILL_RESTRICTIONS
        assert block.length is not None
        assert block_restr.length is not None
        assert (
            block.length // IQ_SKILL_ENTRY_LEN
            == block_restr.length // IQ_SKILL_RESTR_ENTRY_LEN
        )
        expected_length = int(block.length / IQ_SKILL_ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )
        for i, entry in enumerate(value):
            arm9bin[
                block.address
                + i * IQ_SKILL_ENTRY_LEN : block.address
                + (i + 1) * IQ_SKILL_ENTRY_LEN
            ] = entry.iq_required.to_bytes(
                IQ_SKILL_ENTRY_LEN, byteorder="little", signed=True
            )
            arm9bin[
                block_restr.address
                + i * IQ_SKILL_RESTR_ENTRY_LEN : block_restr.address
                + (i + 1) * IQ_SKILL_RESTR_ENTRY_LEN
            ] = entry.restriction_group.to_bytes(
                IQ_SKILL_RESTR_ENTRY_LEN, byteorder="little", signed=True
            )


class IqGroupsSkills:
    @staticmethod
    def read_uncompressed(arm9: bytes, config: Pmd2Data) -> List[List[u8]]:
        block = config.bin_sections.arm9.data.IQ_GROUP_SKILLS
        ret = []
        for i in range(block.address, block.address + block.length, IQ_GROUP_LIST_LEN):
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
        block = config.extra_bin_sections.arm9.data.COMPRESSED_IQ_GROUP_SKILLS
        ret = []
        for i in range(
            block.address, block.address + block.length, IQ_GROUP_COMPRESSED_LIST_LEN
        ):
            skill_list = []
            for j in range(0, IQ_GROUP_COMPRESSED_LIST_LEN):
                current_byte = arm9[i + j]
                for k in range(0, 8):
                    if current_byte & 1 << k != 0:
                        skill_list.append(u8(j * 8 + k))
            ret.append(skill_list)
        return ret

    @staticmethod
    def write_compressed(
        arm9: bytearray, data: List[List[u8]], config: Pmd2Data
    ) -> None:
        block = config.extra_bin_sections.arm9.data.COMPRESSED_IQ_GROUP_SKILLS
        assert block.length is not None
        expected_length = int(block.length / IQ_GROUP_COMPRESSED_LIST_LEN)
        if len(data) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )

        for i, group in enumerate(data):
            group_offset = block.address + i * IQ_GROUP_COMPRESSED_LIST_LEN
            # Clear current group before writing anything
            arm9[group_offset : group_offset + IQ_GROUP_COMPRESSED_LIST_LEN] = [
                0
            ] * IQ_GROUP_COMPRESSED_LIST_LEN

            for skill in group:
                byte = skill >> 3
                bit = skill & 7
                skill_offset = group_offset + byte
                arm9[skill_offset] = arm9[skill_offset] | 1 << bit
