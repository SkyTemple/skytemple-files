#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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

# Contains information about the size and fields of some struct types
from typing import List

from skytemple_files.hardcoded.symbols.unsupported_type_error import UnsupportedTypeError


class StructField:
    """
    Represents a struct field
    """

    # Name of the field.
    name: str
    # Offset of this field within its containing struct
    offset: int
    # Field type, as a string
    type: str

    def __init__(self, name: str, offset: int, _type: str):
        self.name = name
        self.offset = offset
        self.type = _type


# List containing information about all structs that have been manually implemented.
# Each entry maps the name of the struct (without the "struct" prefix) to a tuple of two elements. The first one
# contains the full size of the struct, while the second is a list containing all its fields.
# fmt: off
KNOWN_STRUCT_DATA = {
    "rgba": (4, [
        StructField("r", 0, "uint8"),
        StructField("g", 1, "uint8"),
        StructField("b", 2, "uint8"),
        StructField("a", 3, "uint8"),
    ]),
    "exclusive_item_effect_entry": (2, [
        StructField("effect_id", 0, "struct exclusive_item_effect_id_8"),
        StructField("stat_boost_index", 1, "uint8"),
    ]),
    "exclusive_item_stat_boost_entry": (4, [
        StructField("atk", 0, "int8"),
        StructField("def", 1, "int8"),
        StructField("sp_atk", 2, "int8"),
        StructField("sp_def", 3, "int8"),
    ]),
    "partner_talk_kind_table_entry": (8, [
        StructField("talk_kind", 0, "enum talk_kind"),
        StructField("id", 4, "enum monster_id"),
    ]),
    "portrait_layout": (6, [
        StructField("offset_x", 0, "int16"),
        StructField("offset_y", 2, "int16"),
        StructField("try_flip", 4, "bool"),
        # Padding byte omitted
    ]),
    "status_description": (4, [
        StructField("name_str_id", 0, "int16"),
        StructField("desc_str_id", 2, "int16"),
    ]),
    "forbidden_forgot_move_entry": (6, [
        StructField("monster_id", 0, "struct monster_id_16"),
        StructField("origin_id", 2, "struct dungeon_id_16"),
        StructField("move_id", 4, "struct move_id_16"),
    ]),
    "dungeon_unlock_entry": (2, [
        StructField("dungeon_id", 0, "struct dungeon_id_8"),
        StructField("scenario_balance_min", 1, "uint8"),
    ]),
    "simple_menu_id_item": (8, [
        StructField("string_id", 0, "uint16"),
        StructField("result_value", 4, "int"),
    ]),
    "simple_menu_item": (260, [
        StructField("string", 0, "char[256]"),
        StructField("result_value", 256, "int"),
    ]),
    "castform_weather_attributes": (6, [
        StructField("castform_type", 0, "struct type_id_8"),
        StructField("castform_male_id", 2, "struct monster_id_16"),
        StructField("castform_female_id", 4, "struct monster_id_16"),
    ]),
    "type_matchup_combinator_table": (64, [
        StructField("combination", 0, "enum type_matchup[4][4]"),
    ]),
    "natural_gift_item_info": (6, [
        StructField("item_id", 0, "struct item_id_16"),
        StructField("type_id", 2, "struct type_id_8"),
        StructField("base_power_boost", 4, "int16"),
    ]),
    "type_matchup_table": (648, [
        StructField("matchups", 0, "struct type_matchup_16[18][18]"),
    ]),
    "tileset_property": (12, [
        StructField("field_0x0", 0, "int32"),
        StructField("field_0x4", 4, "uint8"),
        StructField("field_0x5", 5, "uint8"),
        StructField("field_0x6", 6, "uint8"),
        StructField("nature_power_variant", 8, "struct nature_power_variant_16"),
        StructField("field_0xa", 10, "uint8"),
        StructField("is_water_tileset", 11, "bool"),
    ]),
    "damage_negating_exclusive_eff_entry": (8, [
        StructField("type", 0, "enum type_id"),
        StructField("effect", 4, "enum exclusive_item_effect_id"),
    ]),
    "two_turn_move_and_status": (4, [
        StructField("move", 0, "struct move_id_16"),
        StructField("status", 2, "struct status_two_turn_id_16"),
    ]),
    "monster_sprite_data_entry": (2, [
        StructField("sprite_size", 0, "uint8_t"),
        StructField("sprite_file_size", 1, "uint8_t"),
    ])
}
# fmt: on


def get_struct_size(type_str: str) -> int:
    """
    Given a string representing a struct type, returns its total size in bytes
    :param type_str: Struct type
    :return: Size of the given struct type, in bytes
    :raises ValueError: If the given type is not a struct type
    :raises UnsupportedTypeError: If the given type is not supported
    """
    if type_str.startswith("struct "):
        type_str_short = type_str.removeprefix("struct ")

        try:
            return KNOWN_STRUCT_DATA[type_str_short][0]
        except KeyError:
            raise UnsupportedTypeError('Unsupported C type "' + type_str + '".')
    else:
        raise ValueError("The specified type is not a struct type.")


def get_struct_fields(type_str: str) -> List[StructField]:
    """
    Given a string representing a struct type, returns the fields it contains
    :param type_str: Struct type
    :return: List of fields for the given struct type
    :raises ValueError: If the given type is not a struct type
    :raises UnsupportedTypeError: If the given type is not supported
    """
    if type_str.startswith("struct "):
        type_str_short = type_str.removeprefix("struct ")

        try:
            return KNOWN_STRUCT_DATA[type_str_short][1]
        except KeyError:
            raise UnsupportedTypeError('Unsupported C type "' + type_str + '".')
    else:
        raise ValueError("The specified type is not a struct type.")
