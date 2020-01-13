import warnings
from typing import List

from ndspy.fnt import Folder
from ndspy.rom import NintendoDSRom


DEBUG = False


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
        end = len(data) - start
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


def _check_memoryview(data):
    """Check if data is actually a memory view object and if not warn. Only used for testing, otherwise does nothing."""
    if DEBUG and not isinstance(data, memoryview):
        warnings.warn('Byte operation without memoryview.')


def lcm(x, y):
    from math import gcd
    return x * y // gcd(x, y)
