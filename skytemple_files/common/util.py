from typing import List

from bitstring import BitStream
from ndspy.fnt import Folder
from ndspy.rom import NintendoDSRom


def read_bytes(data: BitStream, start: int, length=1, byte_size=8) -> BitStream:
    """Read a number of bytes (default 1) from a BitStream"""
    return data[start*byte_size:(start+length)*byte_size]


def get_files_from_rom_with_extension(rom: NintendoDSRom, ext: str) -> List[str]:
    """Returns paths to files in the ROM ending with the specified extension."""
    return _get_files_from_rom_with_extension__recursion('', rom.filenames, ext)


def _get_files_from_rom_with_extension__recursion(path: str, folder: Folder, ext: str) -> List[str]:
    files = [path + x for x in folder.files if x.endswith('.' + ext)]
    for subfolder in folder.folders:
        files += _get_files_from_rom_with_extension__recursion(
            path + subfolder[0] + '/', subfolder[1], ext
        )
    return files


def lcm(x, y):
    from math import gcd
    return x * y // gcd(x, y)