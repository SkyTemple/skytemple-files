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

class RleNibbleDecompressor:
    def __init__(self, compressed_data: bytes, decompressed_size: int):
        self.compressed_data = compressed_data
        self.decompressed_size = decompressed_size

    def decompress(self) -> bytes:
        out = []
        copy_next = -1
        nb_keep = 0
        for b in self.compressed_data:
            if len(out)>=self.decompressed_size:break
            for i in range(2):
                v = (b//(16**(1-i)))%16
                if copy_next<0 and not nb_keep:
                    if v>=8:
                        copy_next = v-8
                    else:
                        nb_keep = v
                elif copy_next>=0:
                    out += [v]*copy_next
                    copy_next = -1
                elif nb_keep>0:
                    out.append(v)
                    nb_keep -= 1
        return bytes(out)
