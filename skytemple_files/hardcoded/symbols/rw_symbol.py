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

from abc import ABC, abstractmethod

from pmdsky_debug_py.protocol import Symbol

from skytemple_files.common.rw_value import RWValue
from skytemple_files.hardcoded.symbols.c_type import CType, get_size_equivalent_type
from skytemple_files.hardcoded.symbols.unsupported_type_error import UnsupportedTypeError
from skytemple_files.hardcoded.symbols.manual.structs import StructField, get_struct_fields
from skytemple_files.hardcoded.symbols.symbol_path import SymbolPath


class RWSymbol(ABC):
    """
    The RWSymbol class, short for "Readable/Writable Symbol", can be used to read/write the value of a pmdsky-debug
    symbol to a given binary.
    """

    # Symbol name
    name: str

    @classmethod
    def from_basic_data(cls, name: str, offset: int, type_str: str) -> "RWSymbol":
        """
        Attempts to create a new instance of this class given basic symbol information. The exact subclass of the
        instance will depend on the specified type string.
        :param name: Name of the symbol
        :param offset: Offset within the binary where data will be read and written to
        :param type_str: Type of the symbol
        :return: New RWSymbol instance
        :raises UnsupportedTypeError: If the type of the input symbol is not supported by the RWSymbol subclasses.
        """
        if "*" in type_str:
            raise UnsupportedTypeError("Pointer types are unsupported by RWSymbol.")
        else:
            c_type = CType.from_str(type_str)
            if c_type.is_array_type() and not c_type.base_type == "char":
                # Array type
                if 0 in c_type.dim_sizes:
                    # Unknown or variable size, unsupported
                    raise UnsupportedTypeError(
                        'Unsupported symbol type "' + type_str + '" due to unknown or variable ' "array size."
                    )
                else:
                    return RWArraySymbol(name, offset, type_str)
            else:
                if c_type.is_array_type() and c_type.base_type == "char" and 0 in c_type.dim_sizes:
                    # Unknown or variable-length string, unsupported
                    raise UnsupportedTypeError(
                        'Unsupported symbol type "' + type_str + '" due to unknown or variable ' "array string length."
                    )

                # Simplify the type if possible
                type_str = get_size_equivalent_type(type_str)

                # Try to create a simple symbol first (some structs are handled as simple symbols, such as
                # struct fx_64_16)
                try:
                    return RWSimpleSymbol(name, offset, type_str)
                except UnsupportedTypeError:
                    pass

                # Check if it's a struct type and try to handle it as such if so
                if "struct" in type_str:
                    # Check if it's one of the struct types that have been manually implemented.
                    # If the type is not supported, this call raises UnsupportedTypeError.
                    struct_fields = get_struct_fields(type_str)
                    return RWStructSymbol(name, offset, struct_fields)
                else:
                    # This type is not an array type, is not supported by RWSimpleSymbol and it's not a supported
                    # struct type either, raise an error.
                    raise UnsupportedTypeError('Unsupported C type "' + type_str + '".')

    @classmethod
    def from_symbol(cls, symbol: Symbol) -> "RWSymbol":
        """
        Attempts to create a new RWSymbol with the information from the given symbol.
        :param symbol: Symbol to use to create the RWSymbol. Must have exactly one address and a type.
        :return: New RWSymbol instance
        :raises UnsupportedTypeError: If the type of the input symbol is not supported by the RWSymbol subclasses.
        :raises ValueError: If the provided symbol does not have exactly one address or it does not have a type.
        """
        if symbol.addresses is None:
            raise ValueError("Cannot instantiate RWSymbol with a Symbol that has no addresses.")
        if len(symbol.addresses) != 1:
            # TODO: Maybe support symbols with multiple addresses? Although it's uncommon for data symbols.
            raise ValueError(
                "Cannot instantiate RWSymbol with a Symbol that has " + str(len(symbol.addresses)) + " addresses."
            )
        if symbol.c_type is None:
            raise ValueError("Cannot instantiate RWSymbol with a Symbol that does not have a type.")

        return cls.from_basic_data(symbol.name, symbol.addresses[0], symbol.c_type)

    @abstractmethod
    def read_str_with_path(self, binary: bytes, path: SymbolPath) -> str:
        """
        Allows reading the value of this symbol. If it's a compound symbol (like an array or a struct), this method
        allows reading the value of any sub-symbols contained in this symbol.
        :param binary: Binary to read the data from
        :param path: Path to the symbol to read
        :return: The value of the specified symbol or sub-symbol, as a string
        :raises ValueError: If the specified path is invalid
        """
        ...

    @abstractmethod
    def write_str_with_path(self, binary: bytearray, path: SymbolPath, value: str):
        """
        Allows writing a value to this symbol. If it's a compound symbol (like an array or a struct), this method
        allows writing a value to any sub-symbols contained in this symbol.
        :param binary: Binary to write the data to
        :param path: Path to the symbol to read
        :param value: Value to write, as a string. It will be converted to the appropriate type beforehand.
        :raises ValueError: If the specified path is invalid
        """
        ...


class RWSimpleSymbol(RWSymbol):
    """
    Represents a simple (that is, non-array and non-struct) symbol. Its associated value can be read and modified.
    """

    _rw_value: RWValue

    def __init__(self, name: str, offset: int, type_str: str):
        self.name = name
        self._rw_value = RWValue.from_c_type(type_str, offset)

    def get_rw_value(self) -> RWValue:
        """
        :return: RWValue instance associated to this symbol. It can be used to read/write its value to its associated
        binary.
        """
        return self._rw_value

    def read_str_with_path(self, binary: bytes, path: SymbolPath) -> str:
        if path != "":
            raise ValueError('Cannot follow non empty path "' + path + '" on simple symbol "' + self.name + '".')
        return self._rw_value.read_str(binary)

    def write_str_with_path(self, binary: bytearray, path: SymbolPath, value: str):
        if path != "":
            raise ValueError('Cannot follow non empty path "' + path + '" on simple symbol "' + self.name + '".')
        self._rw_value.write_str(binary, value)


class RWArraySymbol(RWSymbol):
    """
    Represents an array symbol. It contains a list of RWSymbol instances.
    """

    elements: list[RWSymbol]

    def __init__(self, name: str, offset: int, type_str: str):
        c_type = CType.from_str(type_str)
        base_type_size = c_type.get_base_type_size()

        self.name = name
        self.elements = []

        # Create sub-symbols
        for i in range(c_type.get_total_num_elements()):
            self.elements.append(
                RWSymbol.from_basic_data(self.name + "[" + str(i) + "]", offset + i * base_type_size, c_type.base_type)
            )

    def read_str_with_path(self, binary: bytes, path: SymbolPath) -> str:
        index, rest_of_path = path.get_next_array_flat()
        return self.elements[index].read_str_with_path(binary, rest_of_path)

    def write_str_with_path(self, binary: bytearray, path: SymbolPath, value: str):
        index, rest_of_path = path.get_next_array_flat()
        self.elements[index].write_str_with_path(binary, rest_of_path, value)


class RWStructSymbol(RWSymbol):
    """
    Represents a struct symbol. It contains a dict of RWSymbol instances.
    """

    fields: dict[str, RWSymbol]

    def __init__(self, name: str, offset: int, fields: list[StructField]):
        """
        Creates a new instance of this class
        :param fields: List containing information about the fields of this struct
        """
        self.name = name
        self.fields = {}

        for field in fields:
            self.fields[field.name] = RWSymbol.from_basic_data(
                name + "." + field.name, offset + field.offset, field.type
            )

    def read_str_with_path(self, binary: bytes, path: SymbolPath) -> str:
        field_name, rest_of_path = path.get_next_field()
        try:
            return self.fields[field_name].read_str_with_path(binary, rest_of_path)
        except KeyError:
            raise ValueError("Struct symbol " + self.name + ' has no field named "' + field_name + '".')

    def write_str_with_path(self, binary: bytearray, path: SymbolPath, value: str):
        field_name, rest_of_path = path.get_next_field()
        try:
            return self.fields[field_name].write_str_with_path(binary, rest_of_path, value)
        except KeyError:
            raise ValueError("Struct symbol " + self.name + ' has no field named "' + field_name + '".')
