#  Copyright 2020-2025 SkyTemple Contributors
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

NEXT_ARRAY_SECTION_REGEX = re.compile(r"((\[\d+])+)(.*)")
ARRAY_SECTION_INDEX_REGEX = re.compile(r"\[(\d+)]")
NEXT_STRUCT_FIELD_REGEX = re.compile(r"(\.([a-z_0-9]+))(.*)")


class SymbolPath(str):
    """
    String that represents a path though the values of multiple compound symbols.
    It uses C-like notation to represent array values and struct fields.
    Example: Following path "[12].some_field[3]" would access element #12 of this symbol, which should be a struct.
    Then it would access struct field "some_field", which should be an array, and would finally access element #3 on
    that array.
    """

    path_str: str

    def __init__(self, path_str: str):
        self.path_str = path_str

    def get_next_array(self) -> tuple[list[int], "SymbolPath"]:
        """
        Returns the next section of the path, assuming it's an array section. Also returns the rest of the path
        after removing the first section.
        :return: Tuple of two elements. The first element will contain the next section of the path, as a list of
        integers, each representing an array index. The second will contain the rest of the path after removing the
        first element.
        :raises ValueError: If the next section of the path is not an array section.
        """
        # Search for values in the form "[XXX][XXX]..." at the start of the string
        next_section_match = re.match(NEXT_ARRAY_SECTION_REGEX, self.path_str)
        if next_section_match:
            next_section_str = next_section_match.group(1)
            rest_of_path = next_section_match.group(3)
            # Now get the index for each dimension
            indexes = []
            for index in re.findall(ARRAY_SECTION_INDEX_REGEX, next_section_str):
                indexes.append(int(index))
            return indexes, SymbolPath(rest_of_path)
        else:
            raise ValueError('Next section of path "' + self.path_str + '" is not an array section.')

    def get_next_array_flat(self) -> tuple[int, "SymbolPath"]:
        """
        Same as get_next_array, but all dimensions of the array section will be merged together. Their total size
        will be returned as a single integer.
        """
        next_array, rest_of_path = self.get_next_array()
        merged_size = 1
        for element in next_array:
            merged_size *= element
        return merged_size, rest_of_path

    def get_next_field(self) -> tuple[str, "SymbolPath"]:
        """
        Returns the next section of the path, assuming it's a struct field. Also returns the rest of the path
        after removing the first section.
        :return: Tuple of two elements. The first element will contain the next section of the path, as a string
        representing the name of the struct field. The second will contain the rest of the path after removing the
        first element.
        :raises ValueError: If the next section of the path is not a struct field.
        """
        next_symbol_match = re.match(NEXT_STRUCT_FIELD_REGEX, self.path_str)
        if next_symbol_match:
            next_symbol_name = next_symbol_match.group(2)
            rest_of_path = next_symbol_match.group(3)
            return next_symbol_name, SymbolPath(rest_of_path)
        else:
            raise ValueError('Next section of path "' + self.path_str + '" is not a struct field.')
