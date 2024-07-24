"""
Handling SSB encoded numbers. From pmdsky-debug's documentation for `ScriptParamToInt`:

>   Converts the given opcode parameter to a signed integer.
>
>   The parameter will be returned unchanged unless one of its two most significant bits (0x8000 and 0x4000) are set,
>   in which case both bits will be cleared and the original value will be modified according to the following two
>   rules:
>   - If the 0x4000 bit is set (sign bit), the value will be set to -16384 + value.
>   - If the 0x8000 bit is set (fixed-point flag), the value will be set to value / 256, rounded down.
>   Both rules can be applied, in the same order as listed, if both conditions are met.
>
>   r0: Parameter to convert
>   return: The input parameter, as a signed integer
"""

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

from explorerscript.error import SsbCompilerError
from explorerscript.ssb_converting.ssb_data_types import SsbOpParamFixedPoint

from skytemple_files.common.i18n_util import _

ONE_256TH = 1 / 256


def parse_ssb_encoding(v: int) -> int | SsbOpParamFixedPoint:
    """Convert a ssb encoded number into either a raw 15-bit signed integer or a fixed point parameter"""
    raw_v = v
    # sign flag
    if raw_v & 0x4000:
        v = -0x4000 + (raw_v & 0x3FFF)
    # fixed point flag
    if raw_v & 0x8000:
        whole: int | type[SsbOpParamFixedPoint.NegativeZero] = (abs(v) & 0x7FFF) >> 8
        if v < 0:  # correct sign
            if whole == 0:
                whole = SsbOpParamFixedPoint.NegativeZero
            else:
                whole *= -1  # type: ignore
        fract_256 = abs(v) & 0xFF
        if fract_256 == 0:
            fract_str = "0"
        else:
            fract_float = ONE_256TH * fract_256
            fract_str = str(round(fract_float, 4)).split(".")[1]
        return SsbOpParamFixedPoint(whole, fract_str)
    else:
        return v


def fixed_point_to_ssb_encoding(v: SsbOpParamFixedPoint) -> int:
    """Encodes a fixed point value in Ssb format"""
    as_str = str(v)
    is_negative = as_str.startswith("-")
    parts = as_str.split(".")
    whole = 0
    if len(parts) == 1:
        fract_raw = parts[0]
    elif len(parts) == 2:
        whole = int(parts[0])
        fract_raw = parts[1]
    else:
        raise AssertionError("invalid fixed point value")
    whole = abs(whole)
    fract_float = float(f"0.{fract_raw}")
    fract_256 = fract_float / ONE_256TH
    fract = round(fract_256)

    value = ((whole & 0xFF) << 8) + (fract & 0xFF)

    if is_negative and value != 0x4000:
        value = 0x4000 + ((value - 1) ^ 0x3FFF)

    if (not is_negative and value > 0x3FFF) or value > 0x7FFF or value < 0:
        raise SsbCompilerError(
            _(
                "The value '{}' can not be saved. Please use a value between -64.0 and 63.996 for fixed point numbers."
            ).format(as_str)
        )

    return 0x8000 + value
