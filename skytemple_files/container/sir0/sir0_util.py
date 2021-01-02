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

from typing import List


# Based on C++ algorithm by psy_commando from
# https://projectpokemon.org/docs/mystery-dungeon-nds/sir0siro-format-r46/
def decode_sir0_pointer_offsets(data: bytes, pointer_offset_list_pointer: int, relative=True) -> List[int]:
    decoded = []
    # This is used to sum up all offsets and obtain the offset relative to the file, and not the last offset
    offsetsum = 0
    # temp buffer to assemble longer offsets
    buffer = 0
    # This contains whether the byte read on the previous turn of the loop had the bit flag
    # indicating to append the next byte!
    last_had_bit_flag = False
    for curbyte in data[pointer_offset_list_pointer:len(data)]:
        if not last_had_bit_flag and curbyte == 0:
            break
        # Ignore the first bit, using the 0x7F bitmask, as its reserved.
        # And append or assign the next byte's value to the buffer.
        buffer |= curbyte & 0x7F

        if (0x80 & curbyte) != 0:
            last_had_bit_flag = True
            # If first bit is 1, bitshift left the current buffer, to append the next byte.
            buffer <<= 7
        else:
            last_had_bit_flag = False
            # If we don't need to append, add the value of the current buffer to the offset sum this far,
            # and add that value to the output vector. Then clear the buffer.
            if relative:
                offsetsum += buffer
                decoded.append(offsetsum)
            else:
                decoded.append(buffer)
            buffer = 0

    return decoded


# Based on C++ algorithm by psy_commando from
# https://projectpokemon.org/docs/mystery-dungeon-nds/sir0siro-format-r46/
def encode_sir0_pointer_offsets(buffer: bytearray, pointer_offsets: List[int], relative=True):
    cursor = 0
    # used to add up the sum of all the offsets up to the current one
    offset_so_far = 0
    for offset in pointer_offsets:
        if relative:
            offset_to_encode = offset - offset_so_far
        else:
            # If we are not working relative, we can just use the offset directly.
            offset_to_encode = offset
        # This tells the loop whether it needs to encode null bytes, if at least one higher byte was non-zero
        has_higher_non_zero = False
        # Set the value to the latest offset, so we can properly subtract it from the next offset.
        offset_so_far = offset

        # Encode every bytes of the 4 bytes integer we have to
        for i in range(4, 0, -1):
            currentbyte = (offset_to_encode >> (7 * (i - 1))) & 0x7F
            # the lowest byte to encode is special
            if i == 1:
                # If its the last byte to append, leave the highest bit to 0 !
                buffer[cursor] = currentbyte
                cursor += 1
            elif currentbyte != 0 or has_higher_non_zero:
                # if any bytes but the lowest one! If not null OR if we have encoded a higher non-null byte before!
                buffer[cursor] = currentbyte | 0x80
                cursor += 1
                has_higher_non_zero = True

    return cursor + 1
