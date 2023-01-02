"""
Implementation configuration.
Using this module, you can switch between implementations (Python or native using Rust) for
all modules that support native code.

You should only modify this before any other skytemple_files component is loaded,
otherwise the behaviour could be unexpected.

This defaults to use the Python implementations if SKYTEMPLE_USE_NATIVE is not set.
If it is set, it defaults to the native implementations.
"""
from __future__ import annotations

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
import os
from enum import Enum

ENV_SKYTEMPLE_USE_NATIVE = "SKYTEMPLE_USE_NATIVE"


class ImplementationType(Enum):
    PYTHON = "PYTHON"
    NATIVE = "RUST"


def env_use_native() -> bool:
    return bool(int(os.getenv(ENV_SKYTEMPLE_USE_NATIVE, False)))


_impltype = ImplementationType.NATIVE if env_use_native() else ImplementationType.PYTHON


def change_implementation_type(typ: ImplementationType) -> None:
    global _impltype
    _impltype = typ


def get_implementation_type() -> ImplementationType:
    return _impltype
