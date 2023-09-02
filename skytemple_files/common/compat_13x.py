"""Compatibility with skytemple-files 1.3.x."""
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

import re
import warnings
from typing import TYPE_CHECKING

from ndspy.rom import NintendoDSRom
from pmdsky_debug_py.protocol import SectionProtocol

from skytemple_files.common.warnings import DeprecatedToBeRemovedWarning

if TYPE_CHECKING:
    from skytemple_files.common.util import ByteReadable
    from skytemple_files.common.ppmdu_config.data import Pmd2Data

_RW_DEPR_WARNING = (
    "The functions read_{s|u}int{be|le} and write_{s|u}int{be|le} are deprecated. "
    "Use the specific read/write functions instead."
    "See https://github.com/SkyTemple/skytemple-files/blob/master/docs/140_migration.rst "
    "for info on how to update."
)
_RW_DEPR_WARNING_VER = (1, 7, 0)
_BIN_DEPR_VER = (1, 7, 0)


def read_uintle(data: ByteReadable, start: int = 0, length: int = 1) -> int:
    """
    Return an unsigned integer in little endian from the bytes-like object at the given position.
    Recommended usage with memoryview for performance!

    .. deprecated:: 1.4.0
           Use the more specific read_* (read_i8, read_u16, etc.) functions instead.
           Use read_dynamic if you need a varying length.
    """
    warnings.warn(
        DeprecatedToBeRemovedWarning(_RW_DEPR_WARNING, _RW_DEPR_WARNING_VER),
        stacklevel=2,
    )
    return int.from_bytes(
        data[start : (start + length)], byteorder="little", signed=False
    )


def read_sintle(data: ByteReadable, start: int = 0, length: int = 1) -> int:
    """
    Return a signed integer in little endian from the bytes-like object at the given position.
    Recommended usage with memoryview for performance!

    .. deprecated:: 1.4.0
           Use the more specific read_* (read_i8, read_u16, etc.) functions instead.
           Use read_dynamic if you need a varying length.
    """
    warnings.warn(
        DeprecatedToBeRemovedWarning(_RW_DEPR_WARNING, _RW_DEPR_WARNING_VER),
        stacklevel=2,
    )
    return int.from_bytes(
        data[start : (start + length)], byteorder="little", signed=True
    )


def read_uintbe(data: ByteReadable, start: int = 0, length: int = 1) -> int:
    """
    Return an unsigned integer in big endian from the bytes-like object at the given position.
    Recommended usage with memoryview for performance!

    .. deprecated:: 1.4.0
           Use the more specific read_* (read_i8, read_u16, etc.) functions instead.
           Use read_dynamic if you need a varying length.
    """
    warnings.warn(
        DeprecatedToBeRemovedWarning(_RW_DEPR_WARNING, _RW_DEPR_WARNING_VER),
        stacklevel=2,
    )
    return int.from_bytes(data[start : (start + length)], byteorder="big", signed=False)


def read_sintbe(data: ByteReadable, start: int = 0, length: int = 1) -> int:
    """
    Return a signed integer in big endian from the bytes-like object at the given position.
    Recommended usage with memoryview for performance!

    .. deprecated:: 1.4.0
           Use the more specific read_* (read_i8, read_u16, etc.) functions instead.
           Use read_dynamic if you need a varying length.
    """
    warnings.warn(
        DeprecatedToBeRemovedWarning(_RW_DEPR_WARNING, _RW_DEPR_WARNING_VER),
        stacklevel=2,
    )
    return int.from_bytes(data[start : (start + length)], byteorder="big", signed=True)


def write_uintle(
    data: bytearray, to_write: int, start: int = 0, length: int = 1
) -> None:
    """
    Write an unsigned integer in little endian to the bytes-like mutable object at the given position.

    .. deprecated:: 1.4.0
           Use the more specific write_* (write_i8, write_u16, etc.) functions instead.
    """
    warnings.warn(
        DeprecatedToBeRemovedWarning(_RW_DEPR_WARNING, _RW_DEPR_WARNING_VER),
        stacklevel=2,
    )
    data[start : start + length] = to_write.to_bytes(
        length, byteorder="little", signed=False
    )


def write_sintle(
    data: bytearray, to_write: int, start: int = 0, length: int = 1
) -> None:
    """
    Write a signed integer in little endian to the bytes-like mutable object at the given position.

    .. deprecated:: 1.4.0
           Use the more specific write_* (write_i8, write_u16, etc.) functions instead.
    """
    warnings.warn(
        DeprecatedToBeRemovedWarning(_RW_DEPR_WARNING, _RW_DEPR_WARNING_VER),
        stacklevel=2,
    )
    data[start : start + length] = to_write.to_bytes(
        length, byteorder="little", signed=True
    )


def write_uintbe(
    data: bytearray, to_write: int, start: int = 0, length: int = 1
) -> None:
    """
    Write an unsigned integer in big endian to the bytes-like mutable object at the given position.

    .. deprecated:: 1.4.0
           Use the more specific write_* (write_i8, write_u16, etc.) functions instead.
    """
    warnings.warn(
        DeprecatedToBeRemovedWarning(_RW_DEPR_WARNING, _RW_DEPR_WARNING_VER),
        stacklevel=2,
    )
    data[start : start + length] = to_write.to_bytes(
        length, byteorder="big", signed=False
    )


def write_sintbe(
    data: bytearray, to_write: int, start: int = 0, length: int = 1
) -> None:
    """
    Write a signed integer in big endian to the bytes-like mutable object at the given position.

    .. deprecated:: 1.4.0
           Use the more specific write_* (write_i8, write_u16, etc.) functions instead.
    """
    warnings.warn(
        DeprecatedToBeRemovedWarning(_RW_DEPR_WARNING, _RW_DEPR_WARNING_VER),
        stacklevel=2,
    )
    data[start : start + length] = to_write.to_bytes(
        length, byteorder="big", signed=True
    )


def get_binary_from_rom_ppmdu(
    rom: NintendoDSRom, binary: _DeprecatedBinaryProxy
) -> bytearray:
    """
    .. deprecated:: 1.4.0
        This was used in SkyTemple 1.3.x and prior to get a binary from the ROM using values
        from `Pmd2Data.binaries`. This is deprecated and has been replaced by
        `skytemple_files.common.util.get_binary_from_rom`, which uses the pmdsky-debug
        binary definitions instead (`Pmd2Data.bin_sections`). Please switch to that function.

        https://github.com/SkyTemple/skytemple-files/blob/master/docs/140_migration.rst
        for info on how to update.
    """
    warnings.warn(
        DeprecatedToBeRemovedWarning(
            "This has been replaced by `get_binary_from_rom`. "
            "See https://github.com/SkyTemple/skytemple-files/blob/master/docs/140_migration.rst "
            "for info on how to update.",
            _BIN_DEPR_VER,
        ),
        stacklevel=2,
    )
    from skytemple_files.common.util import get_binary_from_rom

    return get_binary_from_rom(rom, binary.bin_section)


def set_binary_in_rom_ppmdu(
    rom: NintendoDSRom, binary: _DeprecatedBinaryProxy, data: bytes
):
    """
    .. deprecated:: 1.4.0
        This was used in SkyTemple 1.3.x and prior to set a binary from the ROM, looked up via
        values from `Pmd2Data.binaries`. This is deprecated and has been replaced by
        `skytemple_files.common.util.set_binary_in_rom`, which uses the pmdsky-debug
        binary definitions instead (`Pmd2Data.bin_sections`). Please switch to that function.

        https://github.com/SkyTemple/skytemple-files/blob/master/docs/140_migration.rst
        for info on how to update.
    """
    warnings.warn(
        DeprecatedToBeRemovedWarning(
            "This has been replaced by `set_binary_in_rom`. "
            "See https://github.com/SkyTemple/skytemple-files/blob/master/docs/140_migration.rst "
            "for info on how to update.",
            _BIN_DEPR_VER,
        ),
        stacklevel=2,
    )
    from skytemple_files.common.util import set_binary_in_rom

    set_binary_in_rom(rom, binary.bin_section, data)


class _DeprecatedBinaryProxy:
    def __init__(self, bin_section: SectionProtocol):
        self.bin_section = bin_section


class _DeprecatedBinaries:
    """
    Simulates the pre-1.4.0 binaries dictionary,
    by returning proxy objects mapping to `Pmd2Data.bin_sections` or
    `Pmd2Data.extra_bin_sections`.
    """

    def __init__(self, parent: Pmd2Data):
        self._parent = parent

    def __getitem__(self, item) -> _DeprecatedBinaryProxy:
        warnings.warn(
            DeprecatedToBeRemovedWarning(
                "The `binaries` attribute of `Pmd2Data` is deprecated. "
                "Use the `bin_sections` and/or `extra_bin_sections` attributes instead."
                "See https://github.com/SkyTemple/skytemple-files/blob/master/docs/140_migration.rst "
                "for info on how to update.",
                _BIN_DEPR_VER,
            ),
            stacklevel=2,
        )

        parts = item.split("/")
        if parts[0] == "arm9.bin":
            return _DeprecatedBinaryProxy(self._parent.bin_sections.arm9)
        if parts[0] == "overlay":
            if len(parts) > 1:
                r = re.compile(r"overlay_(\d+).bin", re.IGNORECASE)
                match = r.match(parts[1])
                if match is not None:
                    ov_id = int(match.group(1))
                    if ov_id == 36:
                        return _DeprecatedBinaryProxy(
                            self._parent.extra_bin_sections.overlay36  # type: ignore
                        )
                    elif hasattr(self._parent.bin_sections, f"overlay{ov_id}"):
                        return _DeprecatedBinaryProxy(
                            getattr(self._parent.bin_sections, f"overlay{ov_id}")
                        )
        raise KeyError(item)
