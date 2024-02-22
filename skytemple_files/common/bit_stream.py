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
from __future__ import annotations

from math import ceil
from typing import Iterable, Sequence, Iterator, overload, Literal, Optional

from skytemple_files.common.util import chunks


class BitStream(Sequence[bool]):
    """
    Arbitrary list of bits. Can grow but not shrink.
    Useful for use cases that don't work with byte aligned bit operations.

    Currently, not the most efficient implementation, but good enough for small use cases.

    # Length
    `__len__` returns the length in bits. `len_in_bytes` returns the length in bytes.

    # Getting and Setting items
    Getting slices out of the stream will open a mutable view into the stream, which also has type
    BitStream. Setting slices will copy the values (same rules as __init__). Deleting items is not possible.
    New values can be appended with `append`, `extend` or by in-place adding values (same rules as __init__).
    Trying to add new values when the BitStream is a sub-view of another BitStream raises a `ValueError`.

    # Conversion to bytes and numbers
    Converting `to_bytes` returns a `bytes` object. If the bit stream does not align to the size of a byte (8 bits),
    the bytes are padded at the END (meaning the last byte's numeric value may be higher than expected).
    Converting to a number (`to_number`) converts the bit stream into a single number. In this case the numeric value
    is padded at the BEGINNING to match byte boundaries. Endianess can be set, as well as signedness.
    """

    # The underlying data structure
    _impl: list[bool]
    # The start index in the underlying data structure
    _start: int
    # The max length of this view.
    _len: int

    def __init__(self, source: Iterable[int] | bytes | Iterable[bool] | BitStream):
        """
        Create the BitStream either from
        - an iterable of ints (can be `bytes` or subtype), each integer must be in the range 0-255 and will
          be interpreted as 8 bits.
        - an iterable of bools, each entry will be interpreted as 1 bit.
        - another bit stream (copies all data)
        """
        if isinstance(source, BitStream):
            self._impl = source._impl[source._start : source._start + source._len]
        else:
            impl = []
            source_is_bytes_like = None
            for v in source:
                if source_is_bytes_like is None:
                    assert isinstance(v, int)
                    source_is_bytes_like = not isinstance(v, bool)
                if source_is_bytes_like:
                    for bit in reversed(range(0, 8)):
                        impl.append((v & (1 << bit)) > 0)
                else:
                    impl.append(bool(v))
            self._impl = impl

        self._start = 0
        self._len = len(self._impl)

    def __iter__(self) -> Iterator[bool]:
        if self._start == 0 and self._len == len(self._impl):
            return iter(self._impl)
        return iter(self._impl[self._start : self._start + self._len])

    @overload
    def __getitem__(self, index: int) -> bool: ...
    @overload
    def __getitem__(self, index: slice) -> BitStream: ...
    def __getitem__(self, index):
        if isinstance(index, slice):
            n = BitStream([])
            n._impl = self._impl
            n._start = index.start + self._start
            # Try getting a slice to confirm the bounds are valid and to get the correct length
            the_list_slice = n._impl[
                n._start : min(index.stop, self._len) + self._start
            ]
            n._len = len(the_list_slice)
            return n
        else:
            if index > self._len:
                raise IndexError(index)
            return self._impl[self._start + index]

    @overload
    def __setitem__(self, index: int, value: bool) -> None: ...
    @overload
    def __setitem__(
        self, index: slice, value: int | Iterable[int] | Iterable[bool] | BitStream
    ) -> None: ...
    def __setitem__(self, index, value):
        if isinstance(index, slice):
            if index.step is not None:
                raise ValueError(
                    "BitStream: slices with custom step size are not supported."
                )
            slice_len = index.stop - index.start
            if isinstance(value, int):
                value = [True if x == "1" else False for x in bin(value)[2:]]
                if len(value) < slice_len:
                    value = ([False] * (slice_len - len(value))) + value  # type: ignore
            self._do_setitem(value, slice_len, index.start)
        else:
            self._impl[index + self._start] = value

    def _do_setitem(
        self,
        value: Iterable[int] | Iterable[bool] | BitStream,
        asserted_length_of_value: int,
        offset: int,
    ):
        set_value = BitStream(value)._impl
        if len(set_value) != asserted_length_of_value:
            raise ValueError("BitStream: set value does not match slice length.")
        if asserted_length_of_value > self._len:
            raise IndexError("BitStream: Value passed in out of range for stream.")
        start = offset + self._start
        end = start + asserted_length_of_value
        self._impl[start:end] = set_value

    def append(self, value: bool) -> None:
        self._assert_full_view()
        self._impl.append(value)
        self._len += 1

    def extend(self, values: Iterable[int] | Iterable[bool] | BitStream) -> None:
        self._assert_full_view()
        self._impl += BitStream(values)._impl
        self._len = len(self._impl)

    def __iadd__(self, values: Iterable[int] | Iterable[bool] | BitStream) -> BitStream:
        self.extend(values)
        return self

    def __add__(self, other: Iterable[int] | Iterable[bool] | BitStream) -> BitStream:
        self_copy = BitStream(self)
        self_copy.extend(other)
        return self_copy

    def __len__(self):
        return self._len

    def len_in_bytes(self):
        return ceil(len(self) / 8)

    def to_bytes(self) -> bytes:
        return self._do_to_bytes(True)

    def to_number(
        self, byteorder: Literal["little", "big"] = "big", signed=False
    ) -> int:
        raw = self._do_to_bytes(False)
        return int.from_bytes(raw, byteorder, signed=signed)

    @classmethod
    def from_number(cls, number: int, bits: Optional[int] = None) -> BitStream:
        """
        Converts the number to a BitStream. If no desired amount of bits is set,
        the least amount possible is returned (all `False` are stripped until the first `True`).
        """
        as_bytes = number.to_bytes(ceil(number / 255), "big")
        slf = BitStream(as_bytes)
        output = slf._impl
        try:
            first_true = output.index(True)
        except ValueError:
            return BitStream([])

        slf = BitStream(output[first_true:])
        if bits is not None:
            if bits < len(slf):
                raise OverflowError("Too many bits in provided number")
            if bits > len(slf):
                slf = BitStream([False] * (bits - len(slf))) + slf

        return slf

    def _do_to_bytes(self, pad_at_end) -> bytes:
        output = bytearray([0] * self.len_in_bytes())
        idx = 0
        for bits in chunks(self, 8):
            byte = 0
            bit_idx = 0
            if len(bits) < 8 and pad_at_end:
                bits = list(bits) + ([False] * (8 - len(bits)))
            for bit in reversed(bits):
                if bit:
                    byte += 1 << bit_idx
                bit_idx += 1
            output[idx] = byte
            idx += 1
        return output

    def _assert_full_view(self):
        if self._start > 0:
            raise ValueError("Can not add new values to a sub-view BitStream.")

    def __eq__(self, other):
        if isinstance(other, BitStream):
            if self._start == 0 and other._start == 0 and self._len == other._len:
                return self._impl == other._impl
            return (
                self._impl[self._start : self._start + self._len]
                == other._impl[other._start : other._start + other._len]
            )
        return False

    def __hash__(self):
        return hash((self._impl, self._start, self._len))

    def __str__(self):
        return "".join(
            [str(int(x)) for x in self._impl[self._start : self._start + self._len]]
        )

    def __repr__(self):
        return f"BitStream({repr(self._impl[self._start : self._start + self._len])})"
