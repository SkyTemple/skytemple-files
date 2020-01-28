"""The custom text codec used by the game, based on ASCII. NOTE: Not for Japenese version!"""
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

import codecs
import string

from typing import Tuple

# prepare encoding map - First fill with ascii printable
_encode_table = {
    letter: bytes(letter, 'ascii') for letter in string.printable
}
# Add special PMD characters:
_special_characters = {
    # 129 is a two byte special character, see below
    'Œ': bytes([140]),
    'œ': bytes([156]),
    '¡': bytes([161]),
    'ª': bytes([170]),
    '≪': bytes([171]),
    '°': bytes([176]),
    'º': bytes([186]),
    '♂': bytes([189]),
    '♀': bytes([190]),
    '¿': bytes([191]),
    'À': bytes([192]),
    'Á': bytes([193]),
    'Â': bytes([194]),
    'Ä': bytes([196]),
    'Ç': bytes([199]),
    'È': bytes([200]),
    'É': bytes([201]),
    'Ì': bytes([204]),
    'Í': bytes([205]),
    'Ñ': bytes([209]),
    'Ò': bytes([210]),
    'Ó': bytes([211]),
    'Ö': bytes([214]),
    'Ù': bytes([217]),
    'Ú': bytes([218]),
    'Ü': bytes([220]),
    'ß': bytes([223]),
    'à': bytes([224]),
    'á': bytes([225]),
    'â': bytes([226]),
    'ä': bytes([228]),
    'ç': bytes([231]),
    'è': bytes([232]),
    'é': bytes([233]),
    'ê': bytes([234]),
    'ë': bytes([235]),
    'ì': bytes([236]),
    'í': bytes([237]),
    'î': bytes([238]),
    'ï': bytes([239]),
    'ñ': bytes([241]),
    'ò': bytes([242]),
    'ó': bytes([243]),
    'ô': bytes([244]),
    'ö': bytes([246]),
    'ù': bytes([249]),
    'ú': bytes([250]),
    'û': bytes([251]),
    'ü': bytes([252])
}
_encode_table.update(_special_characters)

# prepare inverse map
_decode_table = {ord(v): k for k, v in _encode_table.items()}

# Special cases for two byte special characters (129+X):
_two_byte_special_characters = {
    # TODO: There are probably more supported,
    #       but these are the only ones used in str files.
    '↑': bytes([170]),
    '↓': bytes([171]),
    '♪': bytes([244])
}
_decode_two_byte_special_characters = {ord(v): k for k, v in _two_byte_special_characters.items()}

PMD2_STR_ENCODER = 'pmd2str'


def pmd2_encode(text: str) -> Tuple[bytes, int]:
    bytearr = bytearray(len(text) * 2)
    cursor = 0
    for c in text:
        if c in _encode_table:
            bytearr[cursor:cursor] = _encode_table[c]
            cursor += 1
        elif c in _two_byte_special_characters:
            bytearr[cursor] = 129
            bytearr[cursor+1:cursor+1] = _two_byte_special_characters[c]
            cursor += 2
        else:
            raise ValueError(
                f"String contains characters, that are not printable as PMD2 text. "
                f"First unprintable char: {c}"
            )
    return bytes(bytearr[:cursor]), cursor


def pmd2_decode(binary: bytes) -> Tuple[str, int]:
    len_str = len(binary)
    str = ""
    current_is_special_character = False
    for x in binary:
        if current_is_special_character:
            # Previous character was 129, and this is now a special character:
            if x in _decode_two_byte_special_characters:
                str += _decode_two_byte_special_characters[x]
            else:
                raise ValueError(
                    f"Input byte stream contains unknown two byte character. Can not convert. "
                    f"First unknown char: 129,{x}"
                )
            current_is_special_character = False
        else:
            # Normal character
            if x == 129:
                # Next is a special character! Woo!
                current_is_special_character = True
                len_str -= 1
            elif x in _decode_table:
                str += _decode_table[x]
            else:
                raise ValueError(
                    f"Input byte stream contains unknown characters. Can not convert. "
                    f"First unknown char: {x}"
                )
    return str, len_str


def pmd2_codec_search_function(encoding_name):
    if encoding_name == PMD2_STR_ENCODER:
        return codecs.CodecInfo(pmd2_encode, pmd2_decode, name=PMD2_STR_ENCODER)


def init():
    codecs.register(pmd2_codec_search_function)
