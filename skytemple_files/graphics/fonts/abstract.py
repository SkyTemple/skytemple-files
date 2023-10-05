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

from abc import ABC, abstractmethod
from xml.etree.ElementTree import Element

from PIL import Image
from range_typed_integers import u8

from skytemple_files.common.util import AutoString


class AbstractFontEntry(ABC, AutoString):
    @classmethod
    @abstractmethod
    def get_class_properties(cls) -> list[str]:
        """Returns a list of the properties of this class"""

    @abstractmethod
    def get_properties(self) -> dict[str, int]:
        """Returns a dictionnary of the properties of the entry"""

    @abstractmethod
    def set_properties(self, properties: dict[str, int]) -> None:
        """Sets a list of the properties of the entry"""


class AbstractFont(ABC, AutoString):
    @abstractmethod
    def get_entry_image_size(self) -> int:
        """Gets the size of image entries of this table"""

    @abstractmethod
    def get_entry_properties(self) -> list[str]:
        """Gets the properties of entries of this table"""

    @abstractmethod
    def get_entries_from_table(self, table: u8) -> list[AbstractFontEntry]:
        """Gets all entries of a specific table"""

    @abstractmethod
    def delete_entry(self, entry: AbstractFontEntry) -> None:
        """Deletes the specified entry"""

    @abstractmethod
    def create_entry_for_table(self, table: u8) -> AbstractFontEntry:
        """Create an entry for a table"""

    @abstractmethod
    def to_pil(self) -> dict[int, Image.Image]:
        """Returns all tables as a dictionnary of images"""

    @abstractmethod
    def export_to_xml(self) -> tuple[Element, dict[int, Image.Image]]:
        """Exports all entries as xml with tables as a dictionnary of images"""

    @abstractmethod
    def import_from_xml(self, xml: Element, tables: dict[int, Image.Image]) -> None:
        """Imports all entries font xml with tables as a dictionnary of images"""
