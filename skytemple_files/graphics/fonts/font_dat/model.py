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

from typing import Dict, List, Tuple, no_type_check
from xml.etree.ElementTree import Element

from PIL import Image
from range_typed_integers import u8

from skytemple_files.common.i18n_util import _
from skytemple_files.common.util import (
    read_u8,
    read_u32,
)
from skytemple_files.common.xml_util import validate_xml_attribs, validate_xml_tag
from skytemple_files.graphics.fonts import (
    FONT_VALID_TABLES,
    XML_CHAR,
    XML_CHAR__ID,
    XML_TABLE__ID,
    XML_FONT,
    FONT_DEFAULT_BPROW,
    XML_TABLE,
    XML_CHAR__BPROW,
    XML_CHAR__WIDTH,
)
from skytemple_files.graphics.fonts.abstract import AbstractFont, AbstractFontEntry
from skytemple_files.graphics.fonts.font_dat import FONT_DAT_SIZE, FONT_DAT_ENTRY_LEN


class FontDatEntry(AbstractFontEntry):
    def __init__(self, char: u8, table: u8, width: u8, bprow: u8, data: bytes):
        self.char = char
        self.table = table
        self.width = width
        self.bprow = bprow  # bytes per row; never checked by the game
        self.data = data

    @classmethod
    def get_class_properties(cls) -> List[str]:
        return ["char", "width", "bprow"]

    def get_properties(self) -> Dict[str, int]:
        """Returns a dictionnary of the properties of the entry"""
        return {"char": self.char, "width": self.width, "bprow": self.bprow}

    def set_properties(self, properties: Dict[str, int]):
        """Sets a list of the properties of the entry"""
        if "char" in properties:
            self.char = u8(properties["char"])
        if "width" in properties:
            self.width = u8(properties["width"])
        if "bprow" in properties:
            self.bprow = u8(properties["bprow"])

    def to_pil(self) -> Image.Image:
        data = []
        bprow = FONT_DEFAULT_BPROW  # Unused, so always use default
        for i in range(len(self.data) // bprow):
            pos = 0
            for j in range(bprow):
                v = self.data[i * bprow + j]
                for x in range(8):
                    if pos < FONT_DAT_SIZE:
                        if v & (2**x):
                            data.append(0xF)
                        else:
                            data.append(0x0)
                    pos += 1
        image = Image.frombytes(
            mode="P", size=(FONT_DAT_SIZE, FONT_DAT_SIZE), data=bytes(data)
        )
        return image

    def to_xml(self) -> Element:
        attrs = {XML_CHAR__ID: str(self.char), XML_CHAR__WIDTH: str(self.width)}
        if self.bprow != FONT_DEFAULT_BPROW:
            attrs[XML_CHAR__BPROW] = str(self.bprow)
        xml_entry = Element(XML_CHAR, attrs)
        return xml_entry

    @classmethod
    def from_pil(
        cls, img: Image.Image, char: u8, table: u8, width: u8, bprow_field: u8
    ) -> "FontDatEntry":
        if img.mode != "P":
            raise AttributeError(_("This must be a color indexed image!"))
        bprow = FONT_DEFAULT_BPROW  # Unused, so always use default
        data = []
        raw_data = img.tobytes("raw", "P")
        for i in range(FONT_DAT_SIZE):
            data += [0] * bprow
            for j in range(FONT_DAT_SIZE):
                v = raw_data[i * FONT_DAT_SIZE + j]
                pos = -bprow + j // 8  # pylint: disable=invalid-unary-operand-type
                if v:
                    data[pos] = data[pos] | (2 ** (j % 8))
        return FontDatEntry(char, table, width, bprow_field, bytes(data))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FontDatEntry):
            return False
        return (
            self.char == other.char
            and self.table == other.table
            and self.width == other.width
            and self.bprow == other.bprow
            and self.data == other.data
        )


class FontDat(AbstractFont):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        number_entries = read_u32(data, 0)

        self.entries = []
        for i in range(4, 4 + number_entries * FONT_DAT_ENTRY_LEN, FONT_DAT_ENTRY_LEN):
            self.entries.append(
                FontDatEntry(
                    read_u8(data, i + 0x00),
                    read_u8(data, i + 0x01),
                    read_u8(data, i + 0x02),
                    read_u8(data, i + 0x03),
                    data[i + 0x4 : i + FONT_DAT_ENTRY_LEN],
                )
            )

    def get_entry_image_size(self) -> int:
        return FONT_DAT_SIZE

    def get_entry_properties(self) -> List[str]:
        return FontDatEntry.get_class_properties()

    def delete_entry(self, entry: AbstractFontEntry):
        self.entries.remove(entry)  # type: ignore

    def create_entry_for_table(self, table: u8) -> AbstractFontEntry:
        entry = FontDatEntry(
            u8(0), table, u8(0), FONT_DEFAULT_BPROW, bytes(FONT_DAT_ENTRY_LEN - 0x4)
        )
        self.entries.append(entry)
        return entry

    def get_entries_from_table(self, table: u8) -> List[AbstractFontEntry]:
        entries = []
        for item in self.entries:
            if item.table == table:
                entries.append(item)
        return entries  # type: ignore

    def to_pil(self) -> Dict[int, Image.Image]:
        tables = dict()
        for t in FONT_VALID_TABLES:
            tables[t] = Image.new(
                mode="P", size=(FONT_DAT_SIZE * 16, FONT_DAT_SIZE * 16), color=0
            )
            tables[t].putpalette([min(255, 256 - (i // 3) * 16) for i in range(16 * 3)])
        for item in self.entries:
            if item.table in FONT_VALID_TABLES:
                tables[item.table].paste(
                    item.to_pil(),
                    box=(
                        (item.char % 16) * FONT_DAT_SIZE,
                        (item.char // 16) * FONT_DAT_SIZE,
                    ),
                )
        return tables

    def export_to_xml(self) -> Tuple[Element, Dict[int, Image.Image]]:
        font_xml = Element(XML_FONT)

        tables = dict()
        for t in FONT_VALID_TABLES:
            tables[t] = Element(XML_TABLE, {XML_TABLE__ID: str(t)})
            font_xml.append(tables[t])
        for item in self.entries:
            if item.table in FONT_VALID_TABLES:
                xml_char = item.to_xml()
                validate_xml_tag(xml_char, XML_CHAR)
                tables[item.table].append(xml_char)
        return font_xml, self.to_pil()

    @no_type_check
    def import_from_xml(self, xml: Element, tables: Dict[int, Image.Image]):
        self.entries = []
        validate_xml_tag(xml, XML_FONT)
        for child in xml:
            validate_xml_tag(child, XML_TABLE)
            validate_xml_attribs(child, [XML_TABLE__ID])
            t = int(child.get(XML_TABLE__ID))
            if t in FONT_VALID_TABLES and t in tables:
                for char in child:
                    validate_xml_tag(char, XML_CHAR)
                    validate_xml_attribs(char, [XML_CHAR__ID, XML_CHAR__WIDTH])
                    charid = int(char.get(XML_CHAR__ID))
                    width = int(char.get(XML_CHAR__WIDTH))
                    bprow = int(char.get(XML_CHAR__BPROW, default=FONT_DEFAULT_BPROW))
                    x = (charid % 16) * FONT_DAT_SIZE
                    y = (charid // 16) * FONT_DAT_SIZE
                    self.entries.append(
                        FontDatEntry.from_pil(
                            tables[t].crop(
                                box=[x, y, x + FONT_DAT_SIZE, y + FONT_DAT_SIZE]
                            ),
                            charid,
                            t,
                            width,
                            bprow,
                        )
                    )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FontDat):
            return False
        return self.entries == other.entries
