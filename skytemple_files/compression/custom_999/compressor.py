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

class Custom999Compressor:
    def __init__(self, uncompressed_data: bytes):
        if not isinstance(uncompressed_data, memoryview):
            uncompressed_data = memoryview(uncompressed_data)
        self.uncompressed_data = uncompressed_data

    def compress(self) -> bytes:

        new_data = []
        for b in self.uncompressed_data:
            new_data.append(b%16)
            new_data.append(b//16)
        data = bytes(new_data)

        # For the original algorithm:
        # data = self.uncompressed_data
        
        compressed = []
        compressed.append(data[0])
        # Add another 0 byte for the original algorithm
        # compressed.append(0)
        prev = data[0]
        current = data[0]
        bit_list = []
        for b in data[1:]:
            if b==current:
                bit_list.append(1)
            elif b==prev:
                bit_list.append(0)
                bit_list.append(1)
                bit_list.append(0)
                t = prev
                prev = current
                current = t
            else:
                prev = current
                diff = b-current
                if diff<0:
                    diff = abs(diff)
                    sign = -1
                else:
                    sign = 1
                
                if diff>=0x8: # For the original algorithm: diff>=0x80
                    diff = 0x10-diff # For the original algorithm: diff = 0x100-diff
                    sign = -sign
                if sign>0:
                    code = 0
                else:
                    code = 1
                code += diff<<1

                len_code = len(bin(code+1))-2 - 1
                code = (code+1)%(2**len_code)
                
                tmp = []
                for i in range(len_code):
                    bit_list.append(0)
                    tmp.append(code % 2)
                    code //= 2
                bit_list.append(1)
                bit_list += tmp
                current = b
        while len(bit_list)>0:
                current = bit_list[:8]
                bit_list = bit_list[8:]
                compressed.append(0)
                for i, b in enumerate(current):
                    compressed[-1] += b * (2**i)
        return bytes(compressed)
    
