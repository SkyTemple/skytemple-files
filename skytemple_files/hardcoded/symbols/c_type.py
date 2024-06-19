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
from typing import List

from skytemple_files.common.rw_value import DATA_PROCESSING_INSTRUCTION_TYPE
from skytemple_files.hardcoded.symbols.manual.equivalent_types import get_size_equivalent_type
from skytemple_files.hardcoded.symbols.manual.structs import get_struct_size
from skytemple_files.hardcoded.symbols.unsupported_type_error import UnsupportedTypeError

TYPE_REGEX = re.compile(r"(((enum )|(struct ))?[a-z0-9_*]+)((\[\d+])*)$")
ARRAY_NOTATION_REGEX = re.compile(r"\[(\d+)]")


class CType:
    """
    Represents a C type, and its array dimensions if it's an array type.
    """

    # String that contains the base type. Cannot be an array type.
    base_type: str
    # Size of each array dimension. Empty if the type is not an array type.
    dim_sizes: List[int]

    def __init__(self, base_type: str, dim_sizes: List[int] = None):
        if dim_sizes is None:
            dim_sizes = []
        self.base_type = base_type
        self.dim_sizes = dim_sizes

    @classmethod
    def from_str(cls, type_str: str) -> "CType":
        """
        Creates a new instance of the class from a type string
        :param type_str: String that represents a C type
        :return: New instance of the class
        """
        match = re.match(TYPE_REGEX, type_str)
        if match:
            base_type = match.group(1)
            size = []

            array_notation = match.group(5)
            if array_notation != "":
                for dimension in re.findall(ARRAY_NOTATION_REGEX, array_notation):
                    size.append(int(dimension))

            return CType(base_type, size)
        else:
            raise ValueError("Invalid C type string")

    @classmethod
    def dim_down_array_type(cls, array_type: "CType"):
        """
        Creates a new instance of the class by taking an existing type that represents an array type and removing the
        first of its dimensions.
        :param array_type: Existing array type
        :return: New instance of the class
        :raises ValueError: If ther provided type is not an array type
        """
        if not array_type.is_array_type():
            raise ValueError("Cannot create a lower dimension type from a non-array type")

        return CType(array_type.base_type, array_type.dim_sizes[1:])

    def __str__(self) -> str:
        if self.is_array_type():
            return self.base_type + "".join(["[" + str(size) + "]" for size in self.dim_sizes])
        else:
            return self.base_type

    def is_array_type(self) -> bool:
        """
        :return: True if the current type represents an array type, false otherwise.
        """
        return len(self.dim_sizes) > 0

    def is_struct_type(self) -> bool:
        """
        :return: True if the current type represents a struct type, false otherwise.
        """
        return "struct" in self.base_type

    def get_total_num_elements(self) -> int:
        """
        Returns the total number of elements this type contains across all its dimensions.
        If it's not an array, returns 1.
        :return: Total number of elements on this type
        """
        total = 1
        for dim_size in self.dim_sizes:
            total *= dim_size
        return total

    def get_base_type_size(self) -> int:
        """
        Gets the size of the base type in bytes. Not all types support this operation.
        :return: Size of the base type represented by this instance, in bytes
        :raises UnsupportedTypeError: If this type does not support this operation.
        """
        # Attempt to convert it to a simple type, if possible
        simplified_base_type = get_size_equivalent_type(self.base_type)

        if simplified_base_type == "int" or simplified_base_type == "int32" or simplified_base_type == "int32_t":
            return 4
        elif simplified_base_type == "uint" or simplified_base_type == "uint32" or simplified_base_type == "uint32_t":
            return 4
        elif simplified_base_type == "int16" or simplified_base_type == "int16_t":
            return 2
        elif simplified_base_type == "uint16" or simplified_base_type == "uint16_t":
            return 2
        elif simplified_base_type == "int8" or simplified_base_type == "int8_t":
            return 1
        elif simplified_base_type == "uint8" or simplified_base_type == "uint8_t" or simplified_base_type == "bool":
            return 1
        elif simplified_base_type == "struct fx64_16":
            return 8
        elif simplified_base_type == "fx32_16":
            return 4
        elif simplified_base_type == "fx32_8":
            return 4
        elif simplified_base_type == DATA_PROCESSING_INSTRUCTION_TYPE:
            return 4
        elif simplified_base_type.startswith("struct "):
            return get_struct_size(simplified_base_type)
        else:
            raise UnsupportedTypeError("Unsupported C type \"" + simplified_base_type + "\".")

    def get_size(self) -> int:
        """
        Gets the total size of this type in bytes. Not all types support this operation.
        :return: Total size of this type, in bytes
        :raises UnsupportedTypeError: If this type does not support this operation.
        """
        return self.get_base_type_size() * self.get_total_num_elements()

    def get_multi_dimension_index(self, linear_index: int) -> List[int]:
        """
        Given a linear index between 0 and the product of all elements in self.array_size (upper bound exclusive),
        returns the equivalent index for each dimension.
        For example, if array_size is [10][3], and linear_index is 5, the result would be [1, 2].
        :param linear_index: Linear index to convert
        :return: Indexes on each of the dimensions of this type that correspond to the provided linear index
        :raises ValueError If this type is not an array type
        """
        if not self.is_array_type():
            raise ValueError("Cannot convert a linear index using a non-array type")

        current_linear_index = linear_index
        result = []
        for i in range(len(self.dim_sizes)):
            division_factor = 1
            for j in range(i + 1, len(self.dim_sizes)):
                division_factor *= self.dim_sizes[j]
            current_dim_index = current_linear_index // division_factor
            current_linear_index = current_linear_index % division_factor
            result.append(current_dim_index)
        return result
