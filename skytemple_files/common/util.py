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
import bisect
import re
import warnings
from itertools import groupby
from typing import List, Tuple, TYPE_CHECKING, Iterable

import pkg_resources
from PIL import Image
from PIL.Image import NONE
from ndspy.fnt import Folder
from ndspy.rom import NintendoDSRom

from skytemple_files.common import string_codec
from skytemple_files.common.ppmdu_config.rom_data.loader import RomDataLoader
from skytemple_files.common.i18n_util import f, _

if TYPE_CHECKING:
    from skytemple_files.common.ppmdu_config.data import Pmd2Data, Pmd2Binary

# Useful files:
MONSTER_MD = 'BALANCE/monster.md'
MONSTER_BIN = 'MONSTER/monster.bin'

DEBUG = False


def open_utf8(file, mode='r', *args, **kwargs):
    """Like open, but always uses the utf-8 encoding, on all platforms."""
    return open(file, mode, *args, encoding='utf-8', **kwargs)


def read_bytes(data: bytes, start=0, length=1) -> bytes:
    """
    Read a number of bytes (default 1) from a bytes-like object
    Recommended usage with memoryview for performance!
    """
    _check_memoryview(data)
    return data[start:(start+length)]


def read_uintle(data: bytes, start=0, length=1) -> int:
    """
    Return an unsiged integer in little endian from the bytes-like object at the given position.
    Recommended usage with memoryview for performance!
    """
    _check_memoryview(data)
    return int.from_bytes(data[start:(start+length)], byteorder='little', signed=False)


def read_sintle(data: bytes, start=0, length=1) -> int:
    """
    Return an signed integer in little endian from the bytes-like object at the given position.
    Recommended usage with memoryview for performance!
    """
    _check_memoryview(data)
    return int.from_bytes(data[start:(start+length)], byteorder='little', signed=True)


def read_uintbe(data: bytes, start=0, length=1) -> int:
    """
    Return an unsiged integer in big endian from the bytes-like object at the given position.
    Recommended usage with memoryview for performance!
    """
    _check_memoryview(data)
    return int.from_bytes(data[start:(start+length)], byteorder='big', signed=False)


def read_sintbe(data: bytes, start=0, length=1) -> int:
    """
    Return an signed integer in big endian from the bytes-like object at the given position.
    Recommended usage with memoryview for performance!
    """
    _check_memoryview(data)
    return int.from_bytes(data[start:(start+length)], byteorder='big', signed=True)


def read_var_length_string(data: bytes, start=0, codec=string_codec.PMD2_STR_ENCODER) -> Tuple[int, str]:
    """Reads a zero terminated string of characters. """
    if codec == string_codec.PMD2_STR_ENCODER:
        string_codec.init()
    bytes_of_string = bytearray()
    current_byte = -1
    cursor = start
    while current_byte != 0:
        current_byte = data[cursor]
        cursor += 1
        if current_byte != 0:
            bytes_of_string.append(current_byte)

    return cursor - start, str(bytes_of_string, codec)


def write_uintle(data: bytes, to_write: int, start=0, length=1):
    """
    Write an unsiged integer in little endian to the bytes-like mutable object at the given position.
    """
    data[start:start+length] = to_write.to_bytes(length, byteorder='little', signed=False)


def write_sintle(data: bytes, to_write: int, start=0, length=1):
    """
    Write an signed integer in little endian to the bytes-like mutable object at the given position.
    """
    data[start:start+length] = to_write.to_bytes(length, byteorder='little', signed=True)


def write_uintbe(data: bytes, to_write: int, start=0, length=1):
    """
    Write an unsiged integer in big endian to the bytes-like mutable object at the given position.
    """
    data[start:start+length] = to_write.to_bytes(length, byteorder='big', signed=False)


def write_sintbe(data: bytes, to_write: int, start=0, length=1):
    """
    Write an signed integer in big endian to the bytes-like mutable object at the given position.
    """
    data[start:start+length] = to_write.to_bytes(length, byteorder='big', signed=True)


def iter_bits(number: int):
    """Iterate over the bits of a byte, starting with the high bit"""
    bit = 0x80
    while bit > 0:
        if number & bit:
            yield 1
        else:
            yield 0
        bit >>= 1


def iter_bytes(data: bytes, slice_size, start=0, end=None):
    if end is None:
        end = len(data)
    _check_memoryview(data)
    for i in range(start, end, slice_size):
        yield data[i: i + slice_size]


def iter_bytes_4bit_le(data: bytes, start=0, end=None):
    """
    Generator that generates two 4 bit integers for each byte in the bytes-like object data.
    The 4 bit integers are expected to be stored little endian in the bytes.
    """
    for byte in iter_bytes(data, 1, start, end):
        upper = byte[0] >> 4
        lower = byte[0] & 0x0f
        yield lower
        yield upper


def generate_bitfield(vs: Iterable[bool]):
    """Generates a bitfield from the values in `vs`. Highest bit to lowest!"""
    val = 0
    for v in vs:
        if v:
            val += 1
        val <<= 1
    return val >> 1


def get_files_from_rom_with_extension(rom: NintendoDSRom, ext: str) -> List[str]:
    """Returns paths to files in the ROM ending with the specified extension."""
    return _get_files_from_rom_with_extension__recursion('', rom.filenames, ext)


def get_files_from_folder_with_extension(folder: Folder, ext: str) -> List[str]:
    """Returns paths to files in the ROM ending with the specified extension."""
    return _get_files_from_rom_with_extension__recursion('', folder, ext)


def _get_files_from_rom_with_extension__recursion(path: str, folder: Folder, ext: str) -> List[str]:
    if ext == '':
        # Use all files
        files = [path + x for x in folder.files]
    else:
        files = [path + x for x in folder.files if x.endswith('.' + ext)]
    for subfolder in folder.folders:
        files += _get_files_from_rom_with_extension__recursion(
            path + subfolder[0] + '/', subfolder[1], ext
        )
    return files


def get_rom_folder(rom: NintendoDSRom, path: str) -> Folder:
    """Returns the folder in the ROM."""
    return rom.filenames.subfolder(path)


def _check_memoryview(data):
    """Check if data is actually a memory view object and if not warn. Only used for testing, otherwise does nothing."""
    if DEBUG and not isinstance(data, memoryview):
        warnings.warn('Byte operation without memoryview.')


def lcm(x, y):
    from math import gcd
    return x * y // gcd(x, y)


def make_palette_colors_unique(inp: List[List[int]]) -> List[List[int]]:
    """
    Works with a list of lists of rgb color palettes and returns a modified copy.

    Returns a list that does not contain duplicate colors. This is done by slightly changing
    the color values of duplicate colors.
    """
    # List of single RGB colors
    already_collected_colors = []
    out = []
    for palette in inp:
        out_p = []
        out.append(out_p)
        for color_idx in range(0, len(palette), 3):
            color = palette[color_idx:color_idx+3]
            new_color = _mpcu__check(color, already_collected_colors)
            already_collected_colors.append(new_color)
            out_p += new_color

    return out


def _mpcu__check(color: List[int], already_collected_colors: List[List[int]], change_next=0, change_amount=1) -> List[int]:
    if color not in already_collected_colors:
        return color
    else:
        # Try to find a unique color
        # Yes I didn't really think all that much when writing this and it doesn't even cover all possibilities.
        if change_next == 0:
            # r + 1
            new_color = [color[0] + change_amount, color[1]                , color[2]                ]
        elif change_next == 1:
            # g + 1
            new_color = [color[0] - change_amount, color[1] + change_amount, color[2]                ]
        elif change_next == 2:
            # b + 1
            new_color = [color[0]                , color[1] - change_amount, color[2] + change_amount]
        elif change_next == 3:
            # gb + 1
            new_color = [color[0]                , color[1] + change_amount, color[2]]
        elif change_next == 4:
            # rgb + 1
            new_color = [color[0] + change_amount, color[1]                , color[2]]
        elif change_next == 5:
            # rg + 1
            new_color = [color[0]                , color[1]                , color[2] - change_amount]
        elif change_next == 6:
            # b - 1
            new_color = [color[0] - change_amount, color[1] - change_amount, color[2] - change_amount]
        elif change_next == 7:
            # g - 1
            new_color = [color[0]                , color[1] - change_amount, color[2] + change_amount]
        else:
            # r - 1
            new_color = [color[0] - change_amount, color[1] + change_amount, color[2]                ]
        for i in [0, 1, 2]:
            if new_color[i] < 0:
                new_color[i] = 0
            elif new_color[i] > 255:
                new_color[i] = 255
        new_change_next = (change_next + 1) % 8
        if new_change_next == 0:
            change_amount += 1
        return _mpcu__check(new_color, already_collected_colors, new_change_next, change_amount)


def get_resources_dir():
    return pkg_resources.resource_filename('skytemple_files', '_resources')


def get_ppmdu_config_for_rom(rom: NintendoDSRom) -> 'Pmd2Data':
    """
    Returns the Pmd2Data for the given ROM.
    If the ROM is not a valid and supported PMD EoS ROM, raises ValueError.

    The configuration is loaded from the pmd2data.xml using the XML logic described in the README.rst
    of the ``skytemple_files.common.ppmdu_config`` package.

    Additionally supported data from the ROM is loaded and replaces the data loaded from the XML, if possible.
    See the README.rst for the package ``skytemple_files.common.ppmdu_config.rom_data`` for more information.
    """
    from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
    data_general = Pmd2XmlReader.load_default()
    game_code = rom.idCode.decode('ascii')
    arm9off14 = read_uintle(rom.arm9[0xE:0x10], 0, 2)

    matched_edition = None
    for edition_name, edition in data_general.game_editions.items():
        if edition.issupported and edition.gamecode == game_code and edition.arm9off14 == arm9off14:
            matched_edition = edition_name
            break

    if not matched_edition:
        raise ValueError(_("This ROM is not supported by SkyTemple."))

    # TODO: This is a bit silly. There should be a better check than to parse the XML twice.
    config = Pmd2XmlReader.load_default(matched_edition)

    # Patch the config with real data from the ROM
    RomDataLoader(rom).load_into(config)
    return config


def get_binary_from_rom_ppmdu(rom: NintendoDSRom, binary: 'Pmd2Binary'):
    """Returns the correct binary from the rom, using the binary block specifications."""
    parts = binary.filepath.split('/')
    if parts[0] == 'arm9.bin':
        return rom.arm9 + rom.arm9PostData
    if parts[0] == 'arm7.bin':
        return rom.arm7
    if parts[0] == 'overlay':
        if len(parts) > 1:
            r = re.compile(r'overlay_(\d+).bin', re.IGNORECASE)
            match = r.match(parts[1])
            if match is not None:
                ov_id = int(match.group(1))
                overlays = rom.loadArm9Overlays([ov_id])
                if len(overlays) > 0:
                    return overlays[ov_id].data
    raise ValueError(f(_("Binary {binary.filepath} not found.")))


def set_binary_in_rom_ppmdu(rom: NintendoDSRom, binary: 'Pmd2Binary', data: bytes):
    """Sets the correct binary in the rom, using the binary block specifications."""
    parts = binary.filepath.split('/')
    if parts[0] == 'arm9.bin':
        rom.arm9 = bytes(data)
        return
    if parts[0] == 'arm7.bin':
        rom.arm7 = bytes(data)
        return
    if parts[0] == 'overlay':
        if len(parts) > 1:
            r = re.compile(r'overlay_(\d+).bin', re.IGNORECASE)
            match = r.match(parts[1])
            if match is not None:
                ov_id = int(match.group(1))
                overlays = rom.loadArm9Overlays([ov_id])
                if len(overlays) > 0:
                    rom.files[overlays[ov_id].fileID] = data
                    return
    raise ValueError(f(_("Binary {binary.filepath} not found.")))


def create_file_in_rom(rom: NintendoDSRom, path: str, data: bytes):
    """Create a file in the ROM using the requested filename"""
    path_list = path.split('/')
    dir_name = '/'.join(path_list[:-1])
    file_name = path_list[-1]
    folder: Folder = rom.filenames.subfolder(dir_name)
    if folder is None:
        raise FileNotFoundError(f(_("Folder {dir_name} does not exist.")))
    folder_first_file_id = folder.firstID
    if file_name in folder.files:
        raise FileExistsError(f(_("File {file_name} already exists in this folder.")))
    index_of_new_file = bisect.bisect(folder.files, file_name)
    folder.files.insert(index_of_new_file, file_name)

    def recursive_increment_folder_start_idx(rfolder: Folder, if_bigger_than):
        if rfolder.firstID > if_bigger_than:
            rfolder.firstID += 1
        for _, sfolder in rfolder.folders:
            recursive_increment_folder_start_idx(sfolder, if_bigger_than)

    recursive_increment_folder_start_idx(rom.filenames, folder_first_file_id)
    rom.files.insert(folder_first_file_id + index_of_new_file, data)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def shrink_list(lst):
    return [(element, len(list(i))) for element, i in groupby(lst)]


def list_insert_enlarge(lst, index, value, filler_fn):
    """Inserts an element value at index index in lst. If the list is not big enough,
    it is enlarged and empty slots are filled with the return value of filler_fn."""
    if len(lst) <= index:
        lst += [filler_fn() for _ in range(index - len(lst))]
    lst.append(value)


def simple_quant(img: Image.Image) -> Image.Image:
    """
    Simple single-palette image quantization. Reduces to 15 colors and adds one transparent color at index 0.
    The transparent (alpha=0) pixels in the input image are converted to that color.
    If you need to do tiled multi-palette quantization, use Tilequant instead!
    """
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    transparency_map = [px[3] == 0 for px in img.getdata()]
    qimg = img.quantize(15, dither=NONE)
    # Get the original palette and add the transparent color
    qimg.putpalette([0, 0, 0] + qimg.getpalette()[:762])
    # Shift up all pixel values by 1 and add the transparent pixels
    pixels = qimg.load()
    k = 0
    for j in range(img.size[1]):
        for i in range(img.size[0]):
            if transparency_map[k]:
                pixels[i, j] = 0
            else:
                pixels[i, j] += 1
            k += 1
    return qimg


class AutoString:
    """Utility base class, that implements convenient __str__ and __repr__ based on object attributes."""

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.__class__.__name__}<{str({k:v for k,v in self.__dict__.items() if v  is not None and not k[0] == '_'})}>"
