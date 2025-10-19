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
from abc import ABC, abstractmethod

from range_typed_integers import (
    i32,
    i32_checked,
    i16,
    i16_checked,
    i8,
    i8_checked,
    u32,
    u32_checked,
    u16,
    u16_checked,
    u8,
    u8_checked,
    i64_checked,
)

from skytemple_files.common.i18n_util import _

from skytemple_files.common.util import (
    write_i32,
    read_i32,
    read_i16,
    write_i16,
    read_i8,
    write_i8,
    read_u32,
    write_u32,
    read_u16,
    write_u16,
    read_u8,
    write_u8,
    read_bytes,
    write_bytes,
)
from skytemple_files.hardcoded.symbols.unsupported_type_error import UnsupportedTypeError

CHAR_ARRAY_REGEX = re.compile(r"char\[(\d+)]$")
DATA_PROCESSING_INSTRUCTION_TYPE = "struct data_processing_instruction"


class RWValue(ABC):
    """
    The RWValue class, short for "Readable/Writable Value", allows reading or writing a single value to a given offset
    in one of the binaries.

    This abstract class allows reading an writing values as strings. Each subclass allows reading and writing them as
    concrete data types.
    """

    # The offset within the binary to read/write to.
    offset: int

    @classmethod
    def from_c_type(cls, type_str: str, offset: int) -> "RWValue":
        """
        Used to create an instance of one of the subclasses of this class depending on the specified C type.
        Pmdsky-debug custom types are also supported.
        :param type_str: String that represents the C type to use as a reference to create the instance. Must be one
        of the types supported by the subclasses of this class.
        :param offset: Offset within the binary to read/write to.
        :return: The new instance of one of the subclasses of this class
        :raises UnsupportedTypeError: If the specified C type is not supported
        """
        if type_str == "int" or type_str == "int32" or type_str == "int32_t":
            return RWInt32Value(offset)
        elif type_str == "uint" or type_str == "uint32" or type_str == "uint32_t":
            return RWUInt32Value(offset)
        elif type_str == "int16" or type_str == "int16_t":
            return RWInt16Value(offset)
        elif type_str == "uint16" or type_str == "uint16_t":
            return RWUInt16Value(offset)
        elif type_str == "int8" or type_str == "int8_t":
            return RWInt8Value(offset)
        elif type_str == "uint8" or type_str == "uint8_t" or type_str == "bool":
            return RWUInt8Value(offset)
        elif type_str == "struct fx64_16":
            return RWFx6416Value(offset)
        elif type_str == "fx32_16":
            return RWFx3216Value(offset)
        elif type_str == "fx32_8":  # Other fx types are currently unsupported since no relevant symbols use them
            return RWFx328Value(offset)
        elif type_str == DATA_PROCESSING_INSTRUCTION_TYPE:
            # The only part of a data processing instruction that might be interesting to edit is its shifted immediate
            # value (first 3 nibbles), so we only process that part.
            return RWShiftedImmediateValue(offset)
        else:
            # Check for char arrays
            match = re.match(CHAR_ARRAY_REGEX, type_str)
            if match:
                size = int(match.group(1))
                return RWCharArrayValue(offset, size)
            else:
                raise UnsupportedTypeError('Unsupported C type "' + type_str + '".')

    @abstractmethod
    def read_str(self, binary: bytes, index: int = 0) -> str:
        """
        Reads the value from the binary and offset specified when instantiating the class and converts it to a string.
        :param binary: Binary the data should be read from
        :param index: If > 0, the operation will be treated as an array element access, and the array element on the
        given index will be returned.
        :return: The value represented by this instance, as a string.
        """
        ...

    @abstractmethod
    def write_str(self, binary: bytearray, value: str, index: int = 0):
        """
        Writes the given value to the binary and offset specified when instantiating the class. This method will
        attempt to convert the given string to the type represented by this instance.
        :param binary: Binary the data should be written to
        :param value: Value to write
        :param index: If > 0, the operation will be treated as an array element access, and the array element on the
        given index will be overwritten.
        :raises ValueError: If the given string cannot be converted to the underlying data type.
        """
        ...

    @property
    @abstractmethod
    def _type_size(self) -> int:
        """
        Returns the size of the type represented by this instance
        """
        ...


class RWInt32Value(RWValue):
    def __init__(self, offset: int):
        self.offset = offset

    def read(self, binary: bytes, index: int = 0) -> i32:
        return read_i32(binary, self.offset + index * self._type_size)

    def write(self, binary: bytearray, value: i32, index: int = 0):
        write_i32(binary, value, self.offset + index * self._type_size)

    def read_str(self, binary: bytes, index: int = 0) -> str:
        return str(self.read(binary, index))

    def write_str(self, binary: bytearray, value: str, index: int = 0):
        try:
            converted_value = i32_checked(int(value))
        except OverflowError as e:
            raise ValueError(e)
        self.write(binary, converted_value, index)

    @property
    def _type_size(self) -> int:
        return 4


class RWInt16Value(RWValue):
    def __init__(self, offset: int):
        self.offset = offset

    def read(self, binary: bytes, index: int = 0) -> i16:
        return read_i16(binary, self.offset + index * self._type_size)

    def write(self, binary: bytearray, value: i16, index: int = 0):
        write_i16(binary, value, self.offset + index * self._type_size)

    def read_str(self, binary: bytes, index: int = 0) -> str:
        return str(self.read(binary, index))

    def write_str(self, binary: bytearray, value: str, index: int = 0):
        try:
            converted_value = i16_checked(int(value))
        except OverflowError as e:
            raise ValueError(e)
        self.write(binary, converted_value, index)

    @property
    def _type_size(self) -> int:
        return 2


class RWInt8Value(RWValue):
    def __init__(self, offset: int):
        self.offset = offset

    def read(self, binary: bytes, index: int = 0) -> i8:
        return read_i8(binary, self.offset + index * self._type_size)

    def write(self, binary: bytearray, value: i8, index: int = 0):
        write_i8(binary, value, self.offset + index * self._type_size)

    def read_str(self, binary: bytes, index: int = 0) -> str:
        return str(self.read(binary, index))

    def write_str(self, binary: bytearray, value: str, index: int = 0):
        try:
            converted_value = i8_checked(int(value))
        except OverflowError as e:
            raise ValueError(e)
        self.write(binary, converted_value, index)

    @property
    def _type_size(self) -> int:
        return 1


class RWUInt32Value(RWValue):
    def __init__(self, offset: int):
        self.offset = offset

    def read(self, binary: bytes, index: int = 0) -> u32:
        return read_u32(binary, self.offset + index * self._type_size)

    def write(self, binary: bytearray, value: u32, index: int = 0):
        write_u32(binary, value, self.offset + index * self._type_size)

    def read_str(self, binary: bytes, index: int = 0) -> str:
        return str(self.read(binary, index))

    def write_str(self, binary: bytearray, value: str, index: int = 0):
        try:
            converted_value = u32_checked(int(value))
        except OverflowError as e:
            raise ValueError(e)
        self.write(binary, converted_value, index)

    @property
    def _type_size(self) -> int:
        return 4


class RWUInt16Value(RWValue):
    def __init__(self, offset: int):
        self.offset = offset

    def read(self, binary: bytes, index: int = 0) -> u16:
        return read_u16(binary, self.offset + index * self._type_size)

    def write(self, binary: bytearray, value: u16, index: int = 0):
        write_u16(binary, value, self.offset + index * self._type_size)

    def read_str(self, binary: bytes, index: int = 0) -> str:
        return str(self.read(binary, index))

    def write_str(self, binary: bytearray, value: str, index: int = 0):
        try:
            converted_value = u16_checked(int(value))
        except OverflowError as e:
            raise ValueError(e)
        self.write(binary, converted_value, index)

    @property
    def _type_size(self) -> int:
        return 2


class RWUInt8Value(RWValue):
    def __init__(self, offset: int):
        self.offset = offset

    def read(self, binary: bytes, index: int = 0) -> u8:
        return read_u8(binary, self.offset + index * self._type_size)

    def write(self, binary: bytearray, value: u8, index: int = 0):
        write_u8(binary, value, self.offset + index * self._type_size)

    def read_str(self, binary: bytes, index: int = 0) -> str:
        return str(self.read(binary, index))

    def write_str(self, binary: bytearray, value: str, index: int = 0):
        try:
            converted_value = u8_checked(int(value))
        except OverflowError as e:
            raise ValueError(e)
        self.write(binary, converted_value, index)

    @property
    def _type_size(self) -> int:
        return 1


class RWFx6416Value(RWValue):
    """
    RWValue subclass for values of type Fx64_16, which defines 64-bit signed fixed-point numbers with 16 fraction bits.
    It represents the number (upper << 16) + (lower >> 16) + (lower & 0xFFFF) * 2^-16.
    """

    def __init__(self, offset: int):
        self.offset = offset

    def read(self, binary: bytes, index: int = 0) -> float:
        upper_bytes = read_bytes(binary, self.offset + index * self._type_size, 4)
        lower_bytes = read_bytes(binary, self.offset + 4 + index * self._type_size, 4)
        value_big_endian = upper_bytes[::-1] + lower_bytes[::-1]

        int_val = int.from_bytes(value_big_endian, "big", signed=True)
        return i64_checked(int_val) * 2**-16

    def write(self, binary: bytearray, value: float, index: int = 0):
        value_as_bytes = i64_checked(round(value * 2**16)).to_bytes(8, "big")
        upper_bytes_le = value_as_bytes[3::-1]
        lower_bytes_le = value_as_bytes[7:3:-1]
        write_bytes(binary, upper_bytes_le, self.offset + index * self._type_size, 4)
        write_bytes(binary, lower_bytes_le, self.offset + 4 + index * self._type_size, 4)

    def read_str(self, binary: bytes, index: int = 0) -> str:
        return str(self.read(binary, index))

    def write_str(self, binary: bytearray, value: str, index: int = 0):
        converted_value = float(value)
        self.write(binary, converted_value, index)

    @property
    def _type_size(self) -> int:
        return 8


class RWFx3216Value(RWValue):
    """
    RWValue subclass for values of type Fx32_16, which defines 32-bit signed fixed-point numbers with 16 fraction bits.
    It represents the number (value >> 16) + (value & 0xFFFF) * 2^-16.
    """

    def __init__(self, offset: int):
        self.offset = offset

    def read(self, binary: bytes, index: int = 0) -> float:
        return read_i32(binary, self.offset + index * self._type_size) / 2**16

    def write(self, binary: bytearray, value: float, index: int = 0):
        write_i32(binary, i32_checked(round(value * 2**16)), self.offset + index * self._type_size)

    def read_str(self, binary: bytes, index: int = 0) -> str:
        return str(self.read(binary, index))

    def write_str(self, binary: bytearray, value: str, index: int = 0):
        converted_value = float(value)
        self.write(binary, converted_value, index)

    @property
    def _type_size(self) -> int:
        return 4


class RWFx328Value(RWValue):
    """
    RWValue subclass for values of type Fx32_8, which defines 32-bit signed fixed-point numbers with 8 fraction bits.
    It represents the number (value >> 24) + (value & 0xFF) * 2^-8.
    """

    def __init__(self, offset: int):
        self.offset = offset

    def read(self, binary: bytes, index: int = 0) -> float:
        return read_i32(binary, self.offset + index * self._type_size) / 2**8

    def write(self, binary: bytearray, value: float, index: int = 0):
        write_i32(binary, i32_checked(round(value * 2**8)), self.offset + index * self._type_size)

    def read_str(self, binary: bytes, index: int = 0) -> str:
        return str(self.read(binary, index))

    def write_str(self, binary: bytearray, value: str, index: int = 0):
        converted_value = float(value)
        self.write(binary, converted_value, index)

    @property
    def _type_size(self) -> int:
        return 4


class RWShiftedImmediateValue(RWValue):
    """
    RWValue subclass for shifted immediate values that are embedded into ARM instructions. The values are represented
    by a base B (0-255) and a rotation parameter R (0-15). Values are encoded as B >>> (R * 2), where ">>>" is the
    rotate right operator.
    This class does not support array indexing.
    """

    def __init__(self, offset: int):
        self.offset = offset

    def read(self, binary: bytes) -> int:
        base = read_u8(binary, self.offset)
        rot_amount = (read_u8(binary, self.offset + 1) & 0xF) * 2
        return (base >> rot_amount) | (base << (32 - rot_amount) & 0xFFFFFFFF)

    def write(self, binary: bytearray, value: int):
        base, rot_param = self._get_shifted_immediate(value)
        write_u8(binary, u8(base), self.offset)
        # Make sure we don't overwrite the instruction's nibble 3
        nibble_3 = read_u8(binary, self.offset + 1) & 0xF0
        write_u8(binary, u8(nibble_3 + rot_param), self.offset + 1)

    def read_str(self, binary: bytes, index: int = 0) -> str:
        if index != 0:
            raise ValueError("Shifted immediates do not support array indexing")
        return str(self.read(binary))

    def write_str(self, binary: bytearray, value: str, index: int = 0):
        if index != 0:
            raise ValueError("Shifted immediates do not support array indexing")

        converted_value = int(value)
        self.write(binary, converted_value)

    @property
    def _type_size(self) -> int:
        return 2

    def _get_shifted_immediate(self, value: int) -> tuple[int, int]:
        """
        Given an integer, attempts to encode it as a shifted immediate
        :param value: Original value to encode
        :return: Tuple containing the base B and rotation parameter R
        :raises ValueError: If the specified value cannot be expressed as a shifted immediate
        """
        valid = 0 <= value < 2**32
        if valid:
            for i in range(0, 32, 2):
                andval = (0xFFFFFF00 >> i) | (0xFFFFFF00 << (32 - i) & 0xFFFFFFFF)
                if value & andval == 0:
                    return (value << i & 0xFFFFFFFF) | (value >> (32 - i)), i // 2
        raise ValueError(_(f"'{str(value)}' cannot be encoded as a shifted immediate."))


class RWCharArrayValue(RWValue):
    """
    RWValue subclass for char arrays. Does not support array indexing.
    """

    # Size in bytes
    size: int

    def __init__(self, offset: int, size: int):
        self.offset = offset
        self.size = size

    def read(self, binary: bytes) -> str:
        _bytes = read_bytes(binary, self.offset, self.size)
        end = _bytes.find(b"\0")
        if end == -1:
            return _bytes.decode("ascii")
        else:
            return _bytes[:end].decode("ascii")

    def write(self, binary: bytearray, value: str):
        # Check there's enough space to write the string and the null terminator
        if len(value) + 1 <= self.size:
            _bytes = value.encode("ascii")
            _bytes = _bytes + b"\0"
            write_bytes(binary, _bytes, self.offset)
        else:
            raise ValueError("String too large to fit on char array.")

    def read_str(self, binary: bytes, index: int = 0) -> str:
        if index != 0:
            raise ValueError("Char arrays do not support array indexing")
        return self.read(binary)

    def write_str(self, binary: bytearray, value: str, index: int = 0):
        if index != 0:
            raise ValueError("Char arrays do not support array indexing")
        self.write(binary, value)

    @property
    def _type_size(self) -> int:
        return self.size
