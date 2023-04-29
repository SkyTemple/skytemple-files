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

from typing import Dict, Optional, List, Tuple, no_type_check
from xml.etree.ElementTree import Element

from PIL import Image
from range_typed_integers import i16, u32

from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.util import (
    read_u8,
    read_i16,
    read_u32,
)
from skytemple_files.common.xml_util import (
    XmlValidateError,
    validate_xml_attribs,
    validate_xml_tag,
)
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.graphics.fonts import (
    FONT_VALID_TABLES,
    u8,
    XML_CHAR,
    XML_HEADER,
    XML_CHAR__ID,
    XML_TABLE__ID,
    XML_FONT,
    XML_TABLE,
    XML_CHAR__WIDTH,
    XML_HEADER__UNKNOWN,
)
from skytemple_files.graphics.fonts.abstract import AbstractFont, AbstractFontEntry
from skytemple_files.graphics.fonts.banner_font import (
    BANNER_FONT_DATA_LEN,
    BANNER_FONT_ENTRY_LEN,
    BANNER_FONT_SIZE,
)
from skytemple_files.graphics.pal.model import Pal


class BannerFontEntry(AbstractFontEntry):
    char: u8
    table: u8
    width: i16

    def __init__(self, char: u8, table: u8, width: i16, data: bytes):
        self.char = char
        self.table = table
        self.width = width
        self.data = data

    def to_pil(self) -> Image.Image:
        image = Image.frombytes(
            mode="P", size=(BANNER_FONT_SIZE, BANNER_FONT_SIZE), data=self.data
        )
        return image

    def to_xml(self) -> Element:
        attrs = {XML_CHAR__ID: str(self.char), XML_CHAR__WIDTH: str(self.width)}
        xml_entry = Element(XML_CHAR, attrs)
        return xml_entry

    @classmethod
    def get_class_properties(cls) -> List[str]:
        return ["char", "width"]

    def get_properties(self) -> Dict[str, int]:
        """Returns a dictionnary of the properties of the entry"""
        return {"char": self.char, "width": self.width}

    def set_properties(self, properties: Dict[str, int]):
        """Sets a list of the properties of the entry"""
        if "char" in properties:
            self.char = u8(properties["char"])
        if "width" in properties:
            self.width = i16(properties["width"])

    @classmethod
    def from_pil(
        cls, img: Image.Image, char: u8, table: u8, width: i16
    ) -> "BannerFontEntry":
        if img.mode != "P":
            raise AttributeError(_("This must be a color indexed image!"))
        return BannerFontEntry(char, table, width, img.tobytes("raw", "P"))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BannerFontEntry):
            return False
        return (
            self.char == other.char
            and self.table == other.table
            and self.width == other.width
            and self.data == other.data
        )


class BannerFont(Sir0Serializable, AbstractFont):
    unknown: u32

    def __init__(self, data: bytes, header_pnt: int):
        from skytemple_files.common.types.file_types import FileType

        if not isinstance(data, memoryview):
            data = memoryview(data)
        pt_entries = read_u32(data, header_pnt)
        number_entries = read_u32(data, header_pnt + 0x4)
        self.unknown = read_u32(data, header_pnt + 0x8)
        self.palette = None

        self.entries = []
        for i in range(
            pt_entries,
            pt_entries + number_entries * BANNER_FONT_ENTRY_LEN,
            BANNER_FONT_ENTRY_LEN,
        ):
            pt_data = read_u32(data, i + 0x00)

            self.entries.append(
                BannerFontEntry(
                    read_u8(data, i + 0x04),
                    read_u8(data, i + 0x05),
                    read_i16(data, i + 0x06),
                    FileType.RLE_NIBBLE.decompress(
                        data[pt_data:], BANNER_FONT_DATA_LEN
                    ),
                )
            )

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: u32,
    ) -> "Sir0Serializable":
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[u32], Optional[u32]]:
        from skytemple_files.graphics.fonts.banner_font.writer import BannerFontWriter

        return BannerFontWriter(self).write()  # type: ignore

    def set_palette(self, palette: Pal):
        self.palette = palette  # type: ignore

    def get_palette_raw(self) -> List[int]:
        if self.palette:
            return self.palette.get_palette_4bpc()
        else:
            return [(i // 3) * 16 for i in range(16 * 3)]

    def set_palette_raw(self, data: List[int]):
        if self.palette:
            self.palette.set_palette_4bpc(data)

    def get_entry_image_size(self) -> int:
        return BANNER_FONT_SIZE

    def get_entry_properties(self) -> List[str]:
        return BannerFontEntry.get_class_properties()

    def delete_entry(self, entry: AbstractFontEntry):
        self.entries.remove(entry)  # type: ignore

    def create_entry_for_table(self, table: u8) -> AbstractFontEntry:
        entry = BannerFontEntry(u8(0), u8(table), i16(0), bytes(BANNER_FONT_DATA_LEN))
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
                mode="P", size=(BANNER_FONT_SIZE * 16, BANNER_FONT_SIZE * 16), color=0
            )
            tables[t].putpalette(self.get_palette_raw())
        for item in self.entries:
            if item.table in FONT_VALID_TABLES:
                tables[item.table].paste(
                    item.to_pil(),
                    box=(
                        (item.char % 16) * BANNER_FONT_SIZE,
                        (item.char // 16) * BANNER_FONT_SIZE,
                    ),
                )
            else:
                print(f"Invalid {item}")
        return tables

    def export_to_xml(self) -> Tuple[Element, Dict[int, Image.Image]]:
        font_xml = Element(XML_FONT)

        font_xml.append(Element(XML_HEADER, {XML_HEADER__UNKNOWN: str(self.unknown)}))
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
        self.unknown = 0
        pal_table = 256
        validate_xml_tag(xml, XML_FONT)
        for child in xml:
            if child.tag == XML_TABLE:
                validate_xml_attribs(child, [XML_TABLE__ID])
                t = int(child.get(XML_TABLE__ID))
                if t in FONT_VALID_TABLES and t in tables:
                    if pal_table > t:
                        pal_table = t
                        self.set_palette_raw(memoryview(tables[t].palette.palette))
                    for char in child:
                        validate_xml_tag(char, XML_CHAR)
                        validate_xml_attribs(char, [XML_CHAR__ID, XML_CHAR__WIDTH])
                        charid = int(char.get(XML_CHAR__ID))
                        width = int(char.get(XML_CHAR__WIDTH))
                        x = (charid % 16) * BANNER_FONT_SIZE
                        y = (charid // 16) * BANNER_FONT_SIZE
                        self.entries.append(
                            BannerFontEntry.from_pil(
                                tables[t].crop(
                                    box=[
                                        x,
                                        y,
                                        x + BANNER_FONT_SIZE,
                                        y + BANNER_FONT_SIZE,
                                    ]
                                ),
                                charid,
                                t,
                                width,
                            )
                        )
            elif child.tag == XML_HEADER:
                validate_xml_attribs(child, [XML_HEADER__UNKNOWN])
                self.unknown = int(child.get(XML_HEADER__UNKNOWN))
            else:
                raise XmlValidateError(f(_("Font parsing: Unexpected {child.tag}")))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BannerFont):
            return False
        return self.entries == other.entries
