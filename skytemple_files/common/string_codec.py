"""The custom text codec used by the game, based on ANSI+Shift-JIS. NOTE: Not for Japenese version!"""
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

import codecs
import string

from typing import Tuple

# prepare encoding map - First fill with ascii printable
_encode_table = {
    letter: bytes(letter, 'ascii') for letter in string.printable
}
# Add special PMD characters:
_ansi_characters = {
    # 0x81 begins Shift-JIS mode, see below
    '‚': bytes([0x82]),
    'ƒ': bytes([0x83]),
    '„': bytes([0x84]),
    '…': bytes([0x85]),
    '†': bytes([0x86]),
    '‡': bytes([0x87]),
    'ˆ': bytes([0x88]),
    '‰': bytes([0x89]),
    'Š': bytes([0x8A]),
    '‹': bytes([0x8B]),
    'Œ': bytes([0x8C]),
    # undefined
    'Ž': bytes([0x8E]),
    # undefined
    # undefined
    '‘': bytes([0x91]),
    '’': bytes([0x92]),
    '“': bytes([0x93]),
    '”': bytes([0x94]),
    '•': bytes([0x95]),
    '–': bytes([0x96]),
    '—': bytes([0x97]),
    '˜': bytes([0x98]),
    '™': bytes([0x99]),
    'š': bytes([0x9A]),
    '›': bytes([0x9B]),
    'œ': bytes([0x9C]),
    # undefined
    'ž': bytes([0x9E]),
    'Ÿ': bytes([0x9F]),
    # not printable
    '¡': bytes([0xA1]),
    '¢': bytes([0xA2]),
    '£': bytes([0xA3]),
    '¤': bytes([0xA4]),
    '¥': bytes([0xA5]),
    '¦': bytes([0xA6]),
    '§': bytes([0xA7]),
    '¨': bytes([0xA8]),
    '©': bytes([0xA9]),
    'ª': bytes([0xAA]),
    '«': bytes([0xAB]),
    '¬': bytes([0xAC]),
    # not printable
    '®': bytes([0xAE]),
    '¯': bytes([0xAF]),
    '°': bytes([0xB0]),
    '±': bytes([0xB1]),
    '²': bytes([0xB2]),
    '³': bytes([0xB3]),
    '´': bytes([0xB4]),
    'µ': bytes([0xB5]),
    '¶': bytes([0xB6]),
    '·': bytes([0xB7]),
    '¸': bytes([0xB8]),
    '¹': bytes([0xB9]),
    'º': bytes([0xBA]),
    '»': bytes([0xBB]),
    '¼': bytes([0xBC]),
    '♂': bytes([0xBD]),  # NOT STANDARD
    '♀': bytes([0xBE]),  # NOT STANDARD
    '¿': bytes([0xBF]),
    'À': bytes([0xC0]),
    'Á': bytes([0xC1]),
    'Â': bytes([0xC2]),
    'Ã': bytes([0xC3]),
    'Ä': bytes([0xC4]),
    'Å': bytes([0xC5]),
    'Æ': bytes([0xC6]),
    'Ç': bytes([0xC7]),
    'È': bytes([0xC8]),
    'É': bytes([0xC9]),
    'Ê': bytes([0xCA]),
    'Ë': bytes([0xCB]),
    'Ì': bytes([0xCC]),
    'Í': bytes([0xCD]),
    'Î': bytes([0xCE]),
    'Ï': bytes([0xCF]),
    'Ð': bytes([0xD0]),
    'Ñ': bytes([0xD1]),
    'Ò': bytes([0xD2]),
    'Ó': bytes([0xD3]),
    'Ô': bytes([0xD4]),
    'Õ': bytes([0xD5]),
    'Ö': bytes([0xD6]),
    '×': bytes([0xD7]),
    'Ø': bytes([0xD8]),
    'Ù': bytes([0xD9]),
    'Ú': bytes([0xDA]),
    'Û': bytes([0xDB]),
    'Ü': bytes([0xDC]),
    'Ý': bytes([0xDD]),
    'Þ': bytes([0xDE]),
    'ß': bytes([0xDF]),
    'à': bytes([0xE0]),
    'á': bytes([0xE1]),
    'â': bytes([0xE2]),
    'ã': bytes([0xE3]),
    'ä': bytes([0xE4]),
    'å': bytes([0xE5]),
    'æ': bytes([0xE6]),
    'ç': bytes([0xE7]),
    'è': bytes([0xE8]),
    'é': bytes([0xE9]),
    'ê': bytes([0xEA]),
    'ë': bytes([0xEB]),
    'ì': bytes([0xEC]),
    'í': bytes([0xED]),
    'î': bytes([0xEE]),
    'ï': bytes([0xEF]),
    'ð': bytes([0xF0]),
    'ñ': bytes([0xF1]),
    'ò': bytes([0xF2]),
    'ó': bytes([0xF3]),
    'ô': bytes([0xF4]),
    'õ': bytes([0xF5]),
    'ö': bytes([0xF6]),
    '÷': bytes([0xF7]),
    'ø': bytes([0xF8]),
    'ù': bytes([0xF9]),
    'ú': bytes([0xFA]),
    'û': bytes([0xFB]),
    'ü': bytes([0xFC]),
    'ý': bytes([0xFD]),
    'þ': bytes([0xFE]),
    'ÿ': bytes([0xFF])
}
_encode_table.update(_ansi_characters)

# prepare inverse map
_decode_table = {ord(v): k for k, v in _encode_table.items()}

# Special cases for two byte special characters (Shift-JIS, 0x81+X):
_shift_jis_characters = {
    # Doesn't support any characters that are also in the ASCII or ANSI set
    '　': bytes([0x40]),
    '、': bytes([0x41]),
    '。': bytes([0x42]),
    '，': bytes([0x43]),
    '．': bytes([0x44]),
    '・': bytes([0x45]),
    '：': bytes([0x46]),
    '；': bytes([0x47]),
    '？': bytes([0x48]),
    '！': bytes([0x49]),
    '゛': bytes([0x4A]),
    '゜': bytes([0x4B]),
    '｀': bytes([0x4D]),
    '＾': bytes([0x4F]),
    '￣': bytes([0x50]),
    '＿': bytes([0x51]),
    'ヽ': bytes([0x52]),
    'ヾ': bytes([0x53]),
    'ゝ': bytes([0x54]),
    'ゞ': bytes([0x55]),
    '〃': bytes([0x56]),
    '仝': bytes([0x57]),
    '々': bytes([0x58]),
    '〆': bytes([0x59]),
    '〇': bytes([0x5A]),
    'ー': bytes([0x5B]),
    '―': bytes([0x5C]),
    '‐': bytes([0x5D]),
    '／': bytes([0x5E]),
    '〜': bytes([0x60]),
    '‖': bytes([0x61]),
    '｜': bytes([0x62]),
    '‥': bytes([0x64]),
    '（': bytes([0x69]),
    '）': bytes([0x6A]),
    '〔': bytes([0x6B]),
    '〕': bytes([0x6C]),
    '［': bytes([0x6D]),
    '］': bytes([0x6E]),
    '｛': bytes([0x6F]),
    '｝': bytes([0x70]),
    '〈': bytes([0x71]),
    '〉': bytes([0x72]),
    '《': bytes([0x73]),
    '》': bytes([0x74]),
    '「': bytes([0x75]),
    '」': bytes([0x76]),
    '『': bytes([0x77]),
    '』': bytes([0x78]),
    '【': bytes([0x79]),
    '】': bytes([0x7A]),
    '＋': bytes([0x7B]),
    '−': bytes([0x7C]),
    '＝': bytes([0x81]),
    '≠': bytes([0x82]),
    '＜': bytes([0x83]),
    '＞': bytes([0x84]),
    '≦': bytes([0x85]),
    '≧': bytes([0x86]),
    '∞': bytes([0x87]),
    '∴': bytes([0x88]),
    '′': bytes([0x8C]),
    '″': bytes([0x8D]),
    '℃': bytes([0x8E]),
    '￥': bytes([0x8F]),
    '＄': bytes([0x90]),
    '％': bytes([0x93]),
    '＃': bytes([0x94]),
    '＆': bytes([0x95]),
    '＊': bytes([0x96]),
    '＠': bytes([0x97]),
    '☆': bytes([0x99]),
    '★': bytes([0x9A]),
    '○': bytes([0x9B]),
    '●': bytes([0x9C]),
    '◎': bytes([0x9D]),
    '◇': bytes([0x9E]),
    '◆': bytes([0x9F]),
    '□': bytes([0xA0]),
    '■': bytes([0xA1]),
    '△': bytes([0xA2]),
    '▲': bytes([0xA3]),
    '▽': bytes([0xA4]),
    '▼': bytes([0xA5]),
    '※': bytes([0xA6]),
    '〒': bytes([0xA7]),
    '→': bytes([0xA8]),
    '←': bytes([0xA9]),
    '↑': bytes([0xAA]),
    '↓': bytes([0xAB]),
    '〓': bytes([0xAC]),
    '∈': bytes([0xB8]),
    '∋': bytes([0xB9]),
    '⊆': bytes([0xBA]),
    '⊇': bytes([0xBB]),
    '⊂': bytes([0xBC]),
    '⊃': bytes([0xBD]),
    '∪': bytes([0xBE]),
    '∩': bytes([0xBF]),
    '∧': bytes([0xC8]),
    '∨': bytes([0xC9]),
    '⇒': bytes([0xCB]),
    '⇔': bytes([0xCC]),
    '∀': bytes([0xCD]),
    '∃': bytes([0xCE]),
    '∠': bytes([0xDA]),
    '⊥': bytes([0xDB]),
    '⌒': bytes([0xDC]),
    '∂': bytes([0xDD]),
    '∇': bytes([0xDE]),
    '≡': bytes([0xDF]),
    '≒': bytes([0xE0]),
    '≪': bytes([0xE1]),
    '≫': bytes([0xE2]),
    '√': bytes([0xE3]),
    '∽': bytes([0xE4]),
    '∝': bytes([0xE5]),
    '∵': bytes([0xE6]),
    '∫': bytes([0xE7]),
    '∬': bytes([0xE8]),
    'Å': bytes([0xF0]),
    '♯': bytes([0xF2]),
    '♭': bytes([0xF3]),
    '♪': bytes([0xF4]),
    '◯': bytes([0xFC])
}
_decode_shift_jis_characters = {ord(v): k for k, v in _shift_jis_characters.items()}

PMD2_STR_ENCODER = 'pmd2str'
was_init = False


def pmd2_encode(text: str, *args) -> Tuple[bytes, int]:
    bytearr = bytearray(len(text) * 2)
    cursor = 0
    for c in text:
        if c in _encode_table:
            bytearr[cursor:cursor] = _encode_table[c]
            cursor += 1
        elif c in _shift_jis_characters:
            bytearr[cursor] = 129
            bytearr[cursor+1:cursor+1] = _shift_jis_characters[c]
            cursor += 2
        else:
            raise ValueError(
                f"String contains characters, that are not printable as PMD2 text. "
                f"First unprintable char: {c}"
            )
    return bytes(bytearr[:cursor]), cursor


def pmd2_decode(binary: bytes, *args) -> Tuple[str, int]:
    len_str = len(binary)
    str = ""
    current_is_special_character = False
    for x in binary:
        if current_is_special_character:
            # Previous character was 129, and this is now a special character:
            if x in _decode_shift_jis_characters:
                str += _decode_shift_jis_characters[x]
            else:
                raise ValueError(
                    f"Input byte stream contains unknown Shift-JIS character. Can not convert. "
                    f"First unknown char: 0x81 {x}"
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
    global was_init
    if not was_init:
        codecs.register(pmd2_codec_search_function)
        was_init = True
