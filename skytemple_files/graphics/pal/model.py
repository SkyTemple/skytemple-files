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
from skytemple_files.common.util import *


class Pal(AutoString):
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.palette = list(data)

    def get_palette_2bpc(self) -> List[int]:
        """Returns the palette converting the data from 2 bpc to 3 bpc"""
        data = []
        for x in range(len(self.palette)//2):
            v = 0
            for i in range(2):
                v += self.palette[x*2+i]*(256**i)
            data.append((v%32)*8)
            data.append(((v>>5)%32)*8)
            data.append(((v>>10)%32)*8)
        return data
        
    def get_palette(self) -> List[int]:
        """Returns the palette data"""
        return self.palette
        
    def get_palette_4bpc(self) -> List[int]:
        """Returns the palette converting the data from 4 bpc to 3 bpc"""
        data = []
        for i, x in enumerate(self.palette):
            if i%4!=3:
                data.append(x)
        return data
    
    def set_palette_2bpc(self, data: List[int]):
        """Sets the palette converting the data given from 3 bpc to 2 bpc"""
        self.palette = []
        for x in range(len(data)//3):
            color = []
            for i in range(3):
                color.append(data[x*3+i])
            v = (color[0]//8) + ((color[1]//8)<<5) + ((color[2]//8)<<10)
            self.palette.append(v%256)
            self.palette.append(v//256)
    
    def set_palette(self, data: List[int]):
        """Sets the palette data"""
        self.palette = data
        
    def set_palette_4bpc(self, data: List[int], padding=0xff):
        """Sets the palette converting the data given from 3 bpc to 4 bpc"""
        self.palette = []
        for i, x in enumerate(data):
            self.palette.append(x)
            if i%3==2:
                self.palette.append(padding)

    def __eq__(self, other):
        if not isinstance(other, Pal):
            return False
        return self.palette == other.palette
