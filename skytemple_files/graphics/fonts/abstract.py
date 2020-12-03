#  Copyright 2020 Parakoopa
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

from typing import Dict

from abc import ABC, abstractmethod
from xml.etree.ElementTree import Element

from skytemple_files.common.util import *

class AbstractFont(ABC, AutoString):
    
    @abstractmethod
    def to_pil(self) -> Dict[int, 'Image']:pass

    @abstractmethod
    def export_to_xml(self) -> Tuple[Element, Dict[int, 'Image']]:pass
    
    @abstractmethod
    def import_from_xml(self, xml: Element, tables: Dict[int, 'Image']):pass
