#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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

from typing import Dict, Optional

from skytemple_files.common.util import *
from skytemple_files.graphics.fonts import *
from skytemple_files.graphics.fonts.font_sir0 import *
from skytemple_files.graphics.fonts.abstract import AbstractFont, AbstractFontEntry
from xml.etree.ElementTree import Element
from skytemple_files.common.xml_util import validate_xml_tag, XmlValidateError, validate_xml_attribs
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.common.i18n_util import f, _
try:
    from PIL import Image
except ImportError:
    from pil import Image



class FontSir0Entry(AbstractFontEntry):
    def __init__(self, char: int, table: int, width: int, cat: int, padding: int, data: bytes):
        self.char = char
        self.table = table
        self.width = width
        self.cat = cat
        self.padding = padding
        self.data = data

    def to_pil(self) -> Image.Image:
        data = b''.join([bytes([v%16, v//16]) for v in self.data])
        image = Image.frombytes(mode='P', size=(FONT_SIR0_SIZE,FONT_SIR0_SIZE), data=data)
        return image

    def to_xml(self) -> Element:
        attrs = {XML_CHAR__ID: str(self.char),
                XML_CHAR__WIDTH: str(self.width)}
        if self.cat!=FONT_DEFAULT_CAT:
            attrs[XML_CHAR__CAT] = str(self.cat)
        if self.padding!=FONT_DEFAULT_PADDING:
            attrs[XML_CHAR__PADDING] = str(self.padding)
        xml_entry = Element(XML_CHAR, attrs)
        return xml_entry
    
    @classmethod
    def get_class_properties(cls) -> List[str]:
        return ["char", "width", "cat", "padding"]

    def get_properties(self) -> Dict[str, int]:
        """Returns a dictionnary of the properties of the entry"""
        return {"char":self.char, "width":self.width, "cat":self.cat, "padding":self.padding}

    def set_properties(self, properties: Dict[str, int]):
        """Sets a list of the properties of the entry"""
        if "char" in properties:
            self.char = properties["char"]
        if "width" in properties:
            self.width = properties["width"]
        if "cat" in properties:
            self.cat = properties["cat"]
        if "padding" in properties:
            self.padding = properties["padding"]
    
    @classmethod
    def from_pil(cls, img: Image.Image, char: int, table: int, width: int, cat: int, padding: int) -> 'FontSir0Entry':
        if img.mode!='P':
            raise AttributeError(_("This must be a color indexed image!"))
        data = []
        raw_data = img.tobytes("raw", "P")
        for i in range(FONT_SIR0_DATA_LEN):
            v = 0
            for j in range(2):
                v += raw_data[i*2+j]*(16**j)
            data.append(v)
        return FontSir0Entry(char, table, width, cat, padding, bytes(data))
    
    def __eq__(self, other):
        if not isinstance(other, FontSir0Entry):
            return False
        return self.char == other.char and \
               self.table == other.table and \
               self.width == other.width and \
               self.cat == other.cat and \
               self.padding == other.padding and \
               self.data == other.data


class FontSir0(Sir0Serializable, AbstractFont):
    def __init__(self, data: Optional[bytes], header_pnt: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        number_entries = read_uintle(data, header_pnt, 4)
        pt_entries = read_uintle(data, header_pnt+0x4, 4)
        
        self.entries = []
        for i in range(pt_entries, pt_entries + number_entries * FONT_SIR0_ENTRY_LEN, FONT_SIR0_ENTRY_LEN):
            pt_data = read_uintle(data, i + 0x00, 4)
            
            self.entries.append(FontSir0Entry(
                read_uintle(data, i + 0x04),
                read_uintle(data, i + 0x05),
                read_uintle(data, i + 0x06, 4),
                read_uintle(data, i + 0x0A),
                read_uintle(data, i + 0x0B),
                data[pt_data:pt_data + FONT_SIR0_DATA_LEN]
            ))
    
    @classmethod
    def sir0_unwrap(cls, content_data: bytes, data_pointer: int,
                    static_data: Optional[Pmd2Data] = None) -> 'Sir0Serializable':
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> Tuple[bytes, List[int], Optional[int]]:
        from skytemple_files.graphics.fonts.font_sir0.writer import FontSir0Writer
        return FontSir0Writer(self).write()
    
    def get_entry_image_size(self) -> int:
        return FONT_SIR0_SIZE
        
    def get_entry_properties(self) -> List[str]:
        return FontSir0Entry.get_class_properties()

    def delete_entry(self, entry: AbstractFontEntry):
        self.entries.remove(entry)
    
    def create_entry_for_table(self, table) -> AbstractFontEntry:
        entry = FontSir0Entry(0, table, 0, FONT_DEFAULT_CAT, FONT_DEFAULT_PADDING, bytes(FONT_SIR0_DATA_LEN))
        self.entries.append(entry)
        return entry
        
    def get_entries_from_table(self, table) -> List[AbstractFontEntry]:
        entries = []
        for item in self.entries:
            if item.table == table:
                entries.append(item)
        return entries
    
    def to_pil(self) -> Dict[int, Image.Image]:
        tables = dict()
        for t in FONT_VALID_TABLES:
            tables[t] = Image.new(mode='P', size=(FONT_SIR0_SIZE*16, FONT_SIR0_SIZE*16), color=0)
            tables[t].putpalette([min(255, 256-(i//3)*16) for i in range(16*3)])
        for item in self.entries:
            if item.table in FONT_VALID_TABLES:
                tables[item.table].paste(item.to_pil(), box=((item.char%16)*FONT_SIR0_SIZE, (item.char//16)*FONT_SIR0_SIZE))
        return tables

    def export_to_xml(self) -> Tuple[Element, Dict[int, Image.Image]]:
        font_xml = Element(XML_FONT)
        
        tables = dict()
        for t in FONT_VALID_TABLES:
            tables[t] = Element(XML_TABLE, {
                XML_TABLE__ID: str(t)
            })
            font_xml.append(tables[t])
        for item in self.entries:
            if item.table in FONT_VALID_TABLES:
                xml_char = item.to_xml()
                validate_xml_tag(xml_char, XML_CHAR)
                tables[item.table].append(xml_char)
        return font_xml, self.to_pil()
    
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
                    cat = int(char.get(XML_CHAR__CAT, default=FONT_DEFAULT_CAT))
                    padding = int(char.get(XML_CHAR__PADDING, default=FONT_DEFAULT_PADDING))
                    x = (charid%16)*FONT_SIR0_SIZE
                    y = (charid//16)*FONT_SIR0_SIZE
                    self.entries.append(FontSir0Entry.from_pil(tables[t].crop(box=[x, y, x+FONT_SIR0_SIZE, y+FONT_SIR0_SIZE]), charid, t, width, cat, padding))
        pass
    def __eq__(self, other):
        if not isinstance(other, FontSir0):
            return False
        return self.entries == other.entries
