#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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
from __future__ import annotations

import atexit
import bisect
import contextlib
import logging
import os
import re
import stat
import unicodedata
import warnings
from abc import abstractmethod
from enum import Enum
from itertools import groupby
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    overload,
    Literal,
)

from pmdsky_debug_py.protocol import SectionProtocol

import sys
from ndspy.fnt import Folder
from ndspy.rom import NintendoDSRom
from PIL import Image
from range_typed_integers import (
    i8,
    i16,
    i32,
    u8,
    u16,
    u32,
)

from skytemple_files.common import string_codec
from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.ppmdu_config.rom_data.loader import RomDataLoader
from skytemple_files.common.warnings import DeprecatedToBeRemovedWarning
from skytemple_files.user_error import UserValueError

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

if TYPE_CHECKING:
    from skytemple_files.common.ppmdu_config.data import Pmd2Data

# Useful type consts
OptionalKwargs = Optional[Any]
ByteReadable = Union[bytes, Sequence[int]]

# Useful files:
MONSTER_MD = "BALANCE/monster.md"
MONSTER_BIN = "MONSTER/monster.bin"
DUNGEON_BIN = "DUNGEON/dungeon.bin"

OVERLAY_RE = re.compile(r"overlay(\d+)", re.IGNORECASE)

DEBUG = False
logger = logging.getLogger(__name__)


# Explicit re-exports for backwards-compatibility
# noinspection PyUnresolvedReferences
from skytemple_files.common.compat_13x import (  # nopycln: import
    read_sintbe,
    read_sintle,
    read_uintbe,
    read_uintle,
    write_sintbe,
    write_sintle,
    write_uintbe,
    write_uintle,
    get_binary_from_rom_ppmdu,
    set_binary_in_rom_ppmdu,
)


class CapturableProtocol(Protocol):
    @abstractmethod
    def _capture_(self) -> str:
        pass


# A type that can be captured and serialized in structured events, such as for error reports
# Mypy can't handle cyclic dependencies yet :(
Capturable = Union[int, str, bool, Iterable["Capturable"], Dict[str, "Capturable"], None, CapturableProtocol]  # type: ignore
Captured = Union[int, str, bool, List["Captured"], Dict[str, "Captured"], None]  # type: ignore


# noinspection PyProtectedMember
def capture_capturable(c: Capturable) -> Captured:
    from collections.abc import Iterable

    if c is None:
        return None
    if isinstance(c, str) or isinstance(c, int) or isinstance(c, bool):
        return c
    if isinstance(c, dict):
        return {k: capture_capturable(v) for k, v in c.items()}
    if isinstance(c, Iterable):
        return [capture_capturable(v) for v in c]
    return c._capture_()  # type: ignore


# noinspection PyProtectedMember
def capture_any(c: Any) -> Captured:
    from collections.abc import Iterable

    if c is None:
        return None
    if isinstance(c, str) or isinstance(c, int) or isinstance(c, bool):
        return c
    if isinstance(c, dict):
        return {k: capture_any(v) for k, v in c.items()}
    if isinstance(c, Iterable):
        return [capture_any(v) for v in c]
    if hasattr(c, "_capture_"):
        return c._capture_()
    return _capture_generic_object(c)


def _capture_generic_object(obj: Any, recursion_check=None):
    if recursion_check is None:
        recursion_check = []
    if obj in recursion_check:
        return "?? Cyclic structure."
    if isinstance(obj, Enum):
        return str(obj)
    if hasattr(obj, "__slots__"):
        return _capture_generic_object(
            dict((name, getattr(obj, name)) for name in getattr(obj, "__slots__")),
            recursion_check + [obj],
        )
    if hasattr(obj, "__dict__"):
        return _capture_generic_object(vars(obj), recursion_check + [obj])
    return f"?? Unserializable: {repr(obj)}"


def normalize_string(x: str) -> bytes:
    """Returns a normalized ASCII string for sorting purposes."""
    # TODO, does not handle everything
    x = x.lower()
    return unicodedata.normalize("NFKD", x).encode("ascii", "ignore")


def open_utf8(file: str, mode="r", *args, **kwargs):  # type: ignore
    """Like open, but always uses the utf-8 encoding, on all platforms."""
    return open(file, mode, *args, encoding="utf-8", **kwargs)  # type: ignore


def add_extension_if_missing(fn: str, ext: str) -> str:
    """Adds a default file extension if it is missing."""
    if "." not in os.path.basename(fn):
        return fn + "." + ext
    return fn


def read_bytes(data: bytes, start: int = 0, length: int = 1) -> bytes:
    """
    Read a number of bytes (default 1) from a bytes-like object
    Recommended usage with memoryview for performance!
    """
    return data[start : (start + length)]


def read_dynamic(
    data: ByteReadable, start: int = 0, *, length: int, signed: bool, big_endian: bool
) -> int:
    """
    Return an integer from the bytes-like object at the given position.
    """
    return int.from_bytes(
        data[start : (start + length)],
        byteorder="big" if big_endian else "little",
        signed=signed,
    )


def read_u8(data: ByteReadable, start: int = 0) -> u8:
    """Returns an unsigned 8-bit integer from the bytes-like object at the given position."""
    return u8(data[start])


def read_i8(data: ByteReadable, start: int = 0) -> i8:
    """Returns a signed 8-bit integer from the bytes-like object at the given position."""
    return i8(data[start] - 256 if data[start] >= 128 else data[start])


def read_u16(data: ByteReadable, start: int = 0, *, big_endian: bool = False) -> u16:
    """Returns an unsigned 16-bit integer from the bytes-like object at the given position."""
    return u16(
        int.from_bytes(
            data[start : (start + 2)],
            byteorder="big" if big_endian else "little",
            signed=False,
        )
    )


def read_i16(data: ByteReadable, start: int = 0, *, big_endian: bool = False) -> i16:
    """Returns a signed 16-bit integer from the bytes-like object at the given position."""
    return i16(
        int.from_bytes(
            data[start : (start + 2)],
            byteorder="big" if big_endian else "little",
            signed=True,
        )
    )


def read_u32(data: ByteReadable, start: int = 0, *, big_endian: bool = False) -> u32:
    """Returns an unsigned 32-bit integer from the bytes-like object at the given position."""
    return u32(
        int.from_bytes(
            data[start : (start + 4)],
            byteorder="big" if big_endian else "little",
            signed=False,
        )
    )


def read_i32(data: ByteReadable, start: int = 0, *, big_endian: bool = False) -> i32:
    """Returns a signed 32-bit integer from the bytes-like object at the given position."""
    return i32(
        int.from_bytes(
            data[start : (start + 4)],
            byteorder="big" if big_endian else "little",
            signed=True,
        )
    )


def read_var_length_string(
    data: bytes, start: int = 0, codec: str = string_codec.PMD2_STR_ENCODER
) -> Tuple[int, str]:
    """Reads a zero terminated string of characters."""
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


def write_u8(data: bytearray, to_write: u8, start: int = 0):
    """Writes an unsigned 8-bit integer into the bytearray at the given position."""
    data[start : start + 1] = to_write.to_bytes(1, byteorder="little", signed=False)


def write_i8(data: bytearray, to_write: i8, start: int = 0):
    """Writes a signed 8-bit integer into the bytearray at the given position."""
    data[start : start + 1] = to_write.to_bytes(1, byteorder="little", signed=True)


def write_u16(
    data: bytearray, to_write: u16, start: int = 0, *, big_endian: bool = False
):
    """Writes an unsigned 16-bit integer into the bytearray at the given position."""
    data[start : start + 2] = to_write.to_bytes(
        2, byteorder="big" if big_endian else "little", signed=False
    )


def write_i16(
    data: bytearray, to_write: i16, start: int = 0, *, big_endian: bool = False
):
    """Writes a signed 16-bit integer into the bytearray at the given position."""
    data[start : start + 2] = to_write.to_bytes(
        2, byteorder="big" if big_endian else "little", signed=True
    )


def write_u32(
    data: bytearray, to_write: u32, start: int = 0, *, big_endian: bool = False
):
    """Writes an unsigned 32-bit integer into the bytearray at the given position."""
    data[start : start + 4] = to_write.to_bytes(
        4, byteorder="big" if big_endian else "little", signed=False
    )


def write_i32(
    data: bytearray, to_write: i32, start: int = 0, *, big_endian: bool = False
):
    """Writes a signed 32-bit integer into the bytearray at the given position."""
    data[start : start + 4] = to_write.to_bytes(
        4, byteorder="big" if big_endian else "little", signed=True
    )


def iter_bits(number: int) -> Iterable[int]:
    """Iterate over the bits of a byte, starting with the high bit"""
    bit = 0x80
    while bit > 0:
        if number & bit:
            yield 1
        else:
            yield 0
        bit >>= 1


def iter_bytes(
    data: bytes, slice_size: int, start: int = 0, end: Optional[int] = None
) -> Iterable[bytes]:
    if end is None:
        end = len(data)
    _check_memoryview(data)
    for i in range(start, end, slice_size):
        yield data[i : i + slice_size]


def iter_bytes_4bit_le(
    data: bytes, start: int = 0, end: Optional[int] = None
) -> Iterable[int]:
    """
    Generator that generates two 4 bit integers for each byte in the bytes-like object data.
    The 4 bit integers are expected to be stored little endian in the bytes.
    """
    for byte in iter_bytes(data, 1, start, end):
        upper = byte[0] >> 4
        lower = byte[0] & 0x0F
        yield lower
        yield upper


def generate_bitfield(vs: Iterable[bool]) -> int:
    """Generates a bitfield from the values in `vs`. Highest bit to lowest!"""
    val = 0
    for v in vs:
        if v:
            val += 1
        val <<= 1
    return val >> 1


def get_files_from_rom_with_extension(rom: NintendoDSRom, ext: str) -> List[str]:
    """Returns paths to files in the ROM ending with the specified extension."""
    return _get_files_from_rom_with_extension__recursion("", rom.filenames, ext)


def get_files_from_folder_with_extension(folder: Folder, ext: str) -> List[str]:
    """Returns paths to files in the ROM ending with the specified extension."""
    return _get_files_from_rom_with_extension__recursion("", folder, ext)


def _get_files_from_rom_with_extension__recursion(
    path: str, folder: Folder, ext: str
) -> List[str]:
    if ext == "":
        # Use all files
        files = [path + x for x in folder.files]
    else:
        files = [path + x for x in folder.files if x.endswith("." + ext)]
    for subfolder in folder.folders:
        files += _get_files_from_rom_with_extension__recursion(
            path + subfolder[0] + "/", subfolder[1], ext
        )
    return files


def get_rom_folder(rom: NintendoDSRom, path: str) -> Optional[Folder]:
    """Returns the folder in the ROM."""
    return rom.filenames.subfolder(path)


def _check_memoryview(data: bytes) -> None:
    """Check if data is actually a memory view object and if not warn. Only used for testing, otherwise does nothing."""
    if DEBUG and not isinstance(data, memoryview):
        warnings.warn("Byte operation without memoryview.")


def lcm(x: int, y: int) -> int:
    from math import gcd

    return x * y // gcd(x, y)


def make_palette_colors_unique(inp: List[List[int]]) -> List[List[int]]:
    """
    Works with a list of lists of rgb color palettes and returns a modified copy.

    Returns a list that does not contain duplicate colors. This is done by slightly changing
    the color values of duplicate colors.
    """
    # List of single RGB colors
    already_collected_colors: List[List[int]] = []
    out = []
    for palette in inp:
        out_p: List[int] = []
        out.append(out_p)
        for color_idx in range(0, len(palette), 3):
            color = palette[color_idx : color_idx + 3]
            new_color = _mpcu__check(color, already_collected_colors)
            already_collected_colors.append(new_color)
            out_p += new_color

    return out


def _mpcu__check(
    color: List[int],
    already_collected_colors: List[List[int]],
    change_next: int = 0,
    change_amount: int = 1,
) -> List[int]:
    if color not in already_collected_colors:
        return color
    else:
        # Try to find a unique color
        # Yes I didn't really think all that much when writing this and it doesn't even cover all possibilities.
        if change_next == 0:
            # r + 1
            new_color = [color[0] + change_amount, color[1], color[2]]
        elif change_next == 1:
            # g + 1
            new_color = [color[0] - change_amount, color[1] + change_amount, color[2]]
        elif change_next == 2:
            # b + 1
            new_color = [color[0], color[1] - change_amount, color[2] + change_amount]
        elif change_next == 3:
            # gb + 1
            new_color = [color[0], color[1] + change_amount, color[2]]
        elif change_next == 4:
            # rgb + 1
            new_color = [color[0] + change_amount, color[1], color[2]]
        elif change_next == 5:
            # rg + 1
            new_color = [color[0], color[1], color[2] - change_amount]
        elif change_next == 6:
            # b - 1
            new_color = [
                color[0] - change_amount,
                color[1] - change_amount,
                color[2] - change_amount,
            ]
        elif change_next == 7:
            # g - 1
            new_color = [color[0], color[1] - change_amount, color[2] + change_amount]
        else:
            # r - 1
            new_color = [color[0] - change_amount, color[1] + change_amount, color[2]]
        for i in [0, 1, 2]:
            if new_color[i] < 0:
                new_color[i] = 0
            elif new_color[i] > 255:
                new_color[i] = 255
        new_change_next = (change_next + 1) % 8
        if new_change_next == 0:
            change_amount += 1
        return _mpcu__check(
            new_color, already_collected_colors, new_change_next, change_amount
        )


@overload
def get_resources_dir(*, as_string: Literal[True] = True) -> str:
    ...


@overload
def get_resources_dir(*, as_string: Literal[False]) -> Path:
    ...


def get_resources_dir(*, as_string: bool = True) -> Union[str, Path]:
    # This is a bit tricky now that pkg_resources is gone, because importlib does
    # things different to support virtual files.
    # See: https://importlib-resources.readthedocs.io/en/latest/migration.html#pkg-resources-resource-filename
    file_manager = contextlib.ExitStack()
    atexit.register(file_manager.close)
    ref = importlib_resources.files("skytemple_files") / "_resources"
    path = file_manager.enter_context(importlib_resources.as_file(ref)).absolute()
    if as_string:
        return str(path)
    return path


def get_ppmdu_config_for_rom(rom: NintendoDSRom) -> "Pmd2Data":
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
    try:
        game_code = rom.idCode.decode("ascii")
        arm9off14 = read_u16(rom.arm9[0xE:0x10], 0)
    except (ValueError, IndexError):
        raise UserValueError(
            _("The file you tried to open does not seem to be a valid NDS ROM file.")
        )

    matched_edition = None
    for edition_name, edition in data_general.game_editions.items():
        if (
            edition.issupported
            and edition.gamecode == game_code
            and edition.arm9off14 == arm9off14
        ):
            matched_edition = edition_name
            break

    if not matched_edition:
        raise UserValueError(_("This ROM is not supported by SkyTemple."))

    # TODO: This is a bit silly. There should be a better check than to parse the XML twice.
    config = Pmd2XmlReader.load_default(matched_edition)

    # Patch the config with real data from the ROM
    RomDataLoader(rom).load_into(config)
    return config


class Binary(Enum):
    arm9 = "arm9"
    arm7 = "arm7"
    overlay0 = "overlay0"
    overlay1 = "overlay1"
    overlay2 = "overlay2"
    overlay3 = "overlay3"
    overlay4 = "overlay4"
    overlay5 = "overlay5"
    overlay6 = "overlay6"
    overlay7 = "overlay7"
    overlay8 = "overlay8"
    overlay9 = "overlay9"
    overlay10 = "overlay10"
    overlay11 = "overlay11"
    overlay12 = "overlay12"
    overlay13 = "overlay13"
    overlay14 = "overlay14"
    overlay15 = "overlay15"
    overlay16 = "overlay16"
    overlay17 = "overlay17"
    overlay18 = "overlay18"
    overlay19 = "overlay19"
    overlay20 = "overlay20"
    overlay21 = "overlay21"
    overlay22 = "overlay22"
    overlay23 = "overlay23"
    overlay24 = "overlay24"
    overlay25 = "overlay25"
    overlay26 = "overlay26"
    overlay27 = "overlay27"
    overlay28 = "overlay28"
    overlay29 = "overlay29"
    overlay30 = "overlay30"
    overlay31 = "overlay31"
    overlay32 = "overlay32"
    overlay33 = "overlay33"
    overlay34 = "overlay34"
    overlay35 = "overlay35"
    overlay36 = "overlay36"

    def get_overlay_id(self):
        if self == Binary.arm9 or self == Binary.arm7:
            raise ValueError("Can only be called for overlays")
        return int(self.value[7:])


def get_binary_from_rom(rom: NintendoDSRom, binary: SectionProtocol) -> bytearray:
    """Returns the correct binary from the rom, using the binary block specifications."""
    if binary.name == "arm9":
        return bytearray(rom.arm9 + rom.arm9PostData)
    if binary.name == "arm7":
        return bytearray(rom.arm7)
    if binary.name.startswith("overlay"):
        match = OVERLAY_RE.match(binary.name)
        if match is not None:
            ov_id = int(match.group(1))
            overlays = rom.loadArm9Overlays([ov_id])
            if len(overlays) > 0:
                return bytearray(overlays[ov_id].data)
    raise ValueError(f(_("Binary {binary.name} not found.")))


def set_binary_in_rom(rom: NintendoDSRom, binary: SectionProtocol, data: bytes) -> None:
    """Sets the correct binary in the rom, using the binary block specifications."""
    if binary.name == "arm9":
        rom.arm9 = bytes(data)
        return
    if binary.name == "arm7":
        rom.arm7 = bytes(data)
        return
    if binary.name.startswith("overlay"):
        match = OVERLAY_RE.match(binary.name)
        if match is not None:
            ov_id = int(match.group(1))
            overlays = rom.loadArm9Overlays([ov_id])
            if len(overlays) > 0:
                rom.files[overlays[ov_id].fileID] = data
                return
    raise ValueError(f(_("Binary {binary.name} not found.")))


def is_binary_in_rom(rom: NintendoDSRom, binary: Optional[SectionProtocol]) -> bool:
    """Returns true if the specified binary is present in the rom"""
    if binary is None:
        return False
    try:
        get_binary_from_rom(rom, binary)
        return True
    except ValueError:
        return False


def create_file_in_rom(rom: NintendoDSRom, path: str, data: bytes) -> None:
    """Create a file in the ROM using the requested filename"""
    path_list = path.split("/")
    dir_name = "/".join(path_list[:-1])
    file_name = path_list[-1]
    folder: Optional[Folder] = rom.filenames.subfolder(dir_name)
    if folder is None:
        raise FileNotFoundError(f(_("Folder {dir_name} does not exist.")))
    folder_first_file_id = folder.firstID
    if file_name in folder.files:
        raise FileExistsError(f(_("File {file_name} already exists in this folder.")))
    index_of_new_file = bisect.bisect(folder.files, file_name)
    folder.files.insert(index_of_new_file, file_name)

    def recursive_increment_folder_start_idx(rfolder: Folder, new_idx: int) -> None:
        if rfolder != folder and rfolder.firstID >= new_idx:
            rfolder.firstID += 1
        for _, sfolder in rfolder.folders:
            recursive_increment_folder_start_idx(sfolder, new_idx)

    recursive_increment_folder_start_idx(rom.filenames, folder_first_file_id)
    rom.files.insert(folder_first_file_id + index_of_new_file, data)


def folder_in_rom_exists(rom: NintendoDSRom, path: str) -> bool:
    """Checks if a folder exists in the ROM."""
    return rom.filenames.subfolder(path) is not None


def create_folder_in_rom(rom: NintendoDSRom, path: str) -> None:
    """Creates a folder in the ROM."""
    folder = rom.filenames.subfolder(path)
    if folder is not None:
        raise FileNotFoundError(f(_("Folder {path} already exists.")))
    path_list = path.split("/")
    par_dir_name = "/".join(path_list[:-1])
    parent_dir: Optional[Folder] = rom.filenames.subfolder(par_dir_name)
    if parent_dir is None:
        raise FileNotFoundError(f(_("Folder {dir_name} does not exist.")))

    found = False
    first_id = -1
    last_child_count = -1
    for s_name, s_folder in sorted(parent_dir.folders, key=lambda f: f[0]):
        first_id = s_folder.firstID
        last_child_count = len(s_folder.files)
        if s_name > path_list[-1]:
            found = True
            break
    if not found:
        first_id = first_id + last_child_count

    new_folder = Folder(firstID=first_id)
    parent_dir.folders.append((path_list[-1], new_folder))


T = TypeVar("T")


def chunks(lst: Sequence[T], n: int) -> Iterable[Sequence[T]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def shrink_list(lst: List[T]) -> List[Tuple[T, int]]:
    return [(element, len(list(i))) for element, i in groupby(lst)]


def list_insert_enlarge(
    lst: List[T], index: int, value: T, filler_fn: Callable[[], T]
) -> None:
    """Inserts an element value at index index in lst. If the list is not big enough,
    it is enlarged and empty slots are filled with the return value of filler_fn."""
    if len(lst) <= index:
        lst += [filler_fn() for _ in range(index - len(lst))]
    lst.append(value)


def simple_quant(img: Image.Image, can_have_transparency: bool = True) -> Image.Image:
    """
    Simple single-palette image quantization. Reduces to 15 colors and adds one transparent color at index 0.
    The transparent (alpha=0) pixels in the input image are converted to that color (if can_have_transparency=True).
    If you need to do tiled multi-palette quantization, use Tilequant instead!
    """
    if can_have_transparency:
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        transparency_map = [px[3] == 0 for px in img.getdata()]
    else:
        if img.mode != "RGB":
            img = img.convert("RGB")
        transparency_map = [False for px in img.getdata()]
    qimg = img.quantize(15, dither=0)
    # Get the original palette and add the transparent color
    qimg.putpalette([0, 0, 0] + qimg.getpalette()[:762])  # type: ignore
    # Shift up all pixel values by 1 and add the transparent pixels
    pixels = qimg.load()  # type: ignore
    k = 0
    for j in range(img.size[1]):
        for i in range(img.size[0]):
            if transparency_map[k]:
                pixels[i, j] = 0
            else:
                pixels[i, j] += 1
            k += 1
    return qimg


@contextlib.contextmanager
def mutate_sequence(obj: object, attr: str) -> Generator[List[Any], None, None]:
    """
    This context manager provides the attribute sequence value behind the attribute as a list (copy),
    and then assigns the attribute to that list. So while you can "mutate" the "original" sequence this way,
    it's slow. If performance matters at all consider doing it differently.
    TODO: Better typing (probably impossible?)
    """
    seq: Sequence[Any] = getattr(obj, attr)
    l = list(seq)
    yield l
    setattr(obj, attr, l)


class AutoString:
    """Utility base class, that implements convenient __str__ and __repr__ based on object attributes."""

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}<{str({k: v for k, v in self.__dict__.items() if v is not None and not k[0] == '_'})}>"


class EnumCompatibleInt(int):
    """For backwards compatibility"""

    _DEPR_WARN = "This (formerly '{}') is now an int and should no longer be used like an enum instance."
    _DEPR_VER = (1, 5, 0)

    # noinspection PyAttributeOutsideInit
    def former(self, f: str) -> None:
        # I don't quite know how to pass arguments to __new__ or __init__ of builtin type subclasses.
        self._former = f

    @property
    def value(self) -> int:
        warnings.warn(
            DeprecatedToBeRemovedWarning(
                self._DEPR_WARN.format(self._former), self._DEPR_VER
            ),
            stacklevel=2,
        )
        logger.warning(self._DEPR_WARN.format(self._former))
        return self

    @property
    def name(self) -> str:
        warnings.warn(
            DeprecatedToBeRemovedWarning(
                self._DEPR_WARN.format(self._former), self._DEPR_VER
            ),
            stacklevel=2,
        )
        logger.warning(self._DEPR_WARN.format(self._former))
        return str(self)


def set_rw_permission_folder(folder_path: str) -> None:
    """
    Set the folder with the given to having the r+w permission.
    Does nothing on Windows.
    """
    try:
        os.chmod(folder_path, stat.S_IREAD + stat.S_IWRITE + stat.S_IEXEC)
        for root, dirs, files in os.walk(folder_path, topdown=True):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                os.chmod(file_path, stat.S_IREAD + stat.S_IWRITE)
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.chmod(dir_path, stat.S_IREAD + stat.S_IWRITE + stat.S_IEXEC)
    except NotImplementedError:  # This isn't needed on Windows
        pass
