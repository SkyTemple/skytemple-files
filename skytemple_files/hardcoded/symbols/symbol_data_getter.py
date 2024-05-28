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
from typing import List, Dict

from pmdsky_debug_py.protocol import SectionProtocol, Symbol

from skytemple_files.common.ppmdu_config.data import Pmd2Data


class SymbolDataGetter:
    """
    Class used to retrieve information about Symbols and binary sections defined for the current ROM.
    """

    pmd2_data: Pmd2Data
    sections_dict: Dict[str, SectionProtocol]

    def __init__(self, pmd2_data: Pmd2Data):
        self.pmd2_data = pmd2_data
        self.sections_dict = dict(vars(pmd2_data.bin_sections))

    def get_binary_names(self, starting_with: List[str] = None) -> List[str]:
        """
        Returns the names of all binaries that start with one of the specified strings, or all binaries if
        starting_with is not specified.
        :param starting_with: If present, only binaries that start with one of the strings listed here will be returned.
        :return: List containing the names of all the binaries that matched the criteria
        """
        result = []
        for section in list(self.sections_dict.keys()):
            if starting_with is None or self._starts_with_any(section, starting_with):
                result.append(section)
        return result

    def has_data_symbols(self, binary: str) -> bool:
        """
        Checks if a given binary has at least one data symbol
        :param binary: Name of the binary to check
        :return: True if the binary has at least one data symbol, false otherwise
        :raises ValueError: If a binary with the given name does not exist
        """
        try:
            section = self.sections_dict[binary]
        except KeyError:
            raise ValueError("The given binary does not exist.")

        for symbol_name in dict(vars(section.data)).keys():
            if not symbol_name.startswith("_"):
                return True
        return False

    def get_data_symbols(self, binary: str) -> List[Symbol]:
        """
        Given the name of a binary, returns the list of data symbols it contains.
        :param binary: Name of the binary to retrieve symbols from
        :return: List of data symbols for the given binary
        :raises ValueError: If a binary with the given name does not exist
        """
        try:
            section = self.sections_dict[binary]
        except KeyError:
            raise ValueError("The given binary does not exist.")

        result = []
        for symbol_name in dict(vars(section.data)).keys():
            if not symbol_name.startswith("_"):
                symbol: Symbol = getattr(section.data, symbol_name)
                if symbol is not None:
                    result.append(symbol)

        return result

    def _starts_with_any(self, string: str, prefixes: List[str]) -> bool:
        for prefix in prefixes:
            if string.startswith(prefix):
                return True
        return False
