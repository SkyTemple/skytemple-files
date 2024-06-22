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
import re

# List of struct types in pmdsky-debug that end with "_8" or "_16". Normally, a struct ending in that string
# represents an enum type stored in a smaller value (1 or 2 bytes, respectively), but there's some structs that
# actually have one of those strings at the end of its name. We list them here so we know they need to be
# interpreted as structs, not simplified types.
KNOWN_STRUCTS_WITH_8_OR_16_SUFFIX = ["struct uvec2_16", "struct vec2_16", "struct fx64_16"]
STRUCT_8_REGEX = re.compile(r"struct [\d\w_]+_8$")
STRUCT_16_REGEX = re.compile(r"struct [\d\w_]+_16$")
STRUCT_8_OR_16_REGEX = re.compile(r"struct ([\d\w_]+)_(8|16)$")


def get_size_equivalent_type(type_str: str) -> str:
    """
    In terms of size, some custom pmdsky-debug types are equivalent to simpler types. For example,
    "struct monster_id_16" is equivalent to "uint16", and "enum monster_id" is equivalent to "uint32". This methods
    attempts to get the size equivalent of a known complex type. If successful, returns the size equivalent type.
    Otherwise, returns the original type.
    :param type_str: Original type
    :return If the original type has a simpler size equivalent type, returns that new type. Otherwise, returns the
    original type.
    """
    if type_str.startswith("enum "):
        return "uint32"
    else:
        if type_str in KNOWN_STRUCTS_WITH_8_OR_16_SUFFIX:
            # Actually a struct, return as-is
            return type_str
        else:
            # Check if this is a struct that actually represents an enum value
            if re.match(STRUCT_8_REGEX, type_str):
                return "uint8"
            elif re.match(STRUCT_16_REGEX, type_str):
                return "uint16"
            else:
                return type_str


def get_enum_equivalent_type(type_str: str) -> str:
    """
    Given a string that represents a C type, tries to convert it to its equivalent enum type representation.
    For example, "struct monster_id_16" is equivalent to "enum monster_id".
    If successful, returns the equivalent enum type. If not, returns the original type.
    :param type_str: Original type
    :return If the original type has a simpler enum equivalent type, returns that new type. Otherwise, returns the
    original type.
    """
    if type_str.startswith("struct "):
        if type_str in KNOWN_STRUCTS_WITH_8_OR_16_SUFFIX:
            # Actually a struct, return as-is
            return type_str
        else:
            match = re.match(STRUCT_8_OR_16_REGEX, type_str)
            if match:
                type_name = match.group(1)
                return "enum " + type_name
            else:
                return type_str
    else:
        return type_str
