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

MAX_COPY = 0x7
MAX_SINGLE = 0x7

class RleNibbleCompressor:
    def __init__(self, uncompressed_data: bytes):
        if not isinstance(uncompressed_data, memoryview):
            uncompressed_data = memoryview(uncompressed_data)
        self.uncompressed_data = uncompressed_data

    def compress(self) -> bytes:
        """Compresses the input data"""
        self.compressed_data = []
        buffer_single = []
        i = 0
        while i<len(self.uncompressed_data):
            nb = self._search_max_seq(i)
            while nb>3:
                self._write_singles(buffer_single)
                buffer_single = []
                copy = min(MAX_COPY, nb)
                self._write_copy(self.uncompressed_data[i], copy)
                i+=copy
                nb -= copy
            if nb!=0:
                buffer_single.append(self.uncompressed_data[i])
                i+=1
        self._write_singles(buffer_single)
        compact_data = []
        for x in range(len(self.compressed_data)//2):
            v = 0
            for i in range(2):
                v += self.compressed_data[x*2+i]*(16**(1-i))
            compact_data.append(v)
        if len(self.compressed_data)%2!=0:
            compact_data.append(self.compressed_data[-1]*16)
        return bytes(compact_data)
    
    def _search_max_seq(self, i):
        nibble = self.uncompressed_data[i]
        nb = 1
        while i+nb<len(self.uncompressed_data) and self.uncompressed_data[i+nb]==nibble:
            nb+=1
        return nb
    
    def _write_copy(self, nibble, nb_copy):
        self.compressed_data.append(nb_copy+0x8)
        self.compressed_data.append(nibble)
        
    def _write_singles(self, buffer_single):
        while len(buffer_single)>0:
            tmp = buffer_single[:MAX_SINGLE]
            self.compressed_data.append(len(tmp))
            self.compressed_data.extend(tmp)
            buffer_single = buffer_single[MAX_SINGLE:]
