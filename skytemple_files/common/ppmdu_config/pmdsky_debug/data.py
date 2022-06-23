#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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

import warnings
from enum import Enum, auto
from typing import Dict, List, Optional

from skytemple_files.common.ppmdu_config.pmdsky_debug.util import MultiCasingDict
from skytemple_files.common.util import AutoString

_DEPRECATION_WARNING = (
    "Binary symbols are no longer distinguished by type, "
    "please use symbols attribute instead."
    "Functions and data blocks can still be told apart, by checking the new"
    "'type' attribute of the symbols."
)


class Pmd2BinarySymbolType(Enum):
    DATA = auto()
    FUNCTION = auto()


class SymbolHasNoEndError(RuntimeError):
    pass


class Pmd2BinarySymbol(AutoString):
    def __init__(
        self,
        name: str,
        begin: int,
        end: Optional[int],
        description: str,
        typ: Optional[Pmd2BinarySymbolType] = None,
    ):
        self.name: str = name
        self.begin: int = begin
        self._end: Optional[int] = end
        self.parent: Optional["Pmd2Binary"] = None
        self.description = description
        self.type: Pmd2BinarySymbolType = (
            typ if typ is not None else Pmd2BinarySymbolType.DATA
        )

    def add_parent(self, parent: "Pmd2Binary") -> None:
        self.parent = parent

    @property
    def end(self) -> int:
        if self._end is None:
            raise SymbolHasNoEndError("This symbol does not have an end defined.")
        return self._end

    @property
    def begin_absolute(self) -> int:
        if self.parent is None:
            raise RuntimeError(
                "Absolute begin of this symbol is unknown (no parent assigned)."
            )
        return self.parent.loadaddress + self.begin

    @property
    def end_absolute(self) -> int:
        if self.parent is None:
            raise RuntimeError(
                "Absolute begin of this symbol is unknown (no parent assigned)."
            )
        return self.parent.loadaddress + self.end


# Re-exports for backwards compatibility
Pmd2BinaryBlock = Pmd2BinarySymbol
Pmd2BinaryFunction = Pmd2BinarySymbol
Pmd2BinaryPointer = Pmd2BinarySymbol


class Pmd2Binary(AutoString):
    def __init__(
        self,
        filepath: str,
        loadaddress: int,
        length: int,
        description: str,
        symbols: List[Pmd2BinarySymbol],
    ):
        self.filepath = filepath
        self.loadaddress = loadaddress
        self.length = length
        self.description = description
        self.symbols: MultiCasingDict[Pmd2BinarySymbol] = MultiCasingDict(
            (x.name, x) for x in symbols
        )

    @property
    def blocks(self) -> Dict[str, Pmd2BinarySymbol]:
        """For backwards compatibility."""
        warnings.warn(_DEPRECATION_WARNING, DeprecationWarning)
        return self.symbols

    @property
    def functions(self) -> Dict[str, Pmd2BinarySymbol]:
        """For backwards compatibility."""
        warnings.warn(_DEPRECATION_WARNING, DeprecationWarning)
        return {
            k: v
            for k, v in self.symbols.items()
            if v.type == Pmd2BinarySymbolType.FUNCTION
        }

    @property
    def pointers(self) -> Dict[str, Pmd2BinarySymbol]:
        """For backwards compatibility."""
        warnings.warn(_DEPRECATION_WARNING, DeprecationWarning)
        return self.symbols
