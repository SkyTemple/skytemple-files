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
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>

from skytemple_files.common.util import *

class Custom999Decompressor:
    def __init__(self, compressed_data: bytes, decompressed_size: int):
        self.compressed_data = compressed_data
        self.decompressed_size = decompressed_size

    def decompress(self) -> bytes:
        offset = 0
        code = self.compressed_data[offset]
        decompressed = [code]
        prev = code

        # In the original 999 algorithm: 
        # offset += 2
        
        offset += 1

        nbits = 0
        flags = 0
        
        while len(decompressed) < self.decompressed_size*2:
            while nbits < 17:
                if offset < len(self.compressed_data):
                    flags |= self.compressed_data[offset] << nbits
                    offset += 1
                nbits += 8
            nbit = 0
            while nbit<=8:
                if (flags & (1 << nbit)) != 0:
                    break
                nbit += 1
            
            n = (1 << nbit) - 1
            n += (flags >> (nbit + 1)) & n

            current_flag = offset - nbits//8
            if nbits%8!=0:
                current_flag -= 1
            if n == 1:
                decompressed.append(prev)

                t = prev
                prev = code
                code = t
            else:
                if n != 0:
                    prev = code
                code = (code + (n >> 1) * (1 - 2 * (n & 1))) & 0xF # & 0xFF in the original algorithm
                decompressed.append(code)
            
            flags >>= 2 * nbit + 1
            nbits  -= 2 * nbit + 1

        # In the original algorithm: 
        # return bytes(decompressed)
        
        new_data = []
        for l, h in chunks(decompressed, 2):
            new_data.append(l+h*16)
        return bytes(new_data)
