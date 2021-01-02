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

from ndspy.rom import NintendoDSRom

from skytemple_files.common import string_codec
from skytemple_files.common.ppmdu_config.data import Pmd2Binary, Pmd2LooseBinFile
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import create_file_in_rom, get_binary_from_rom_ppmdu, read_var_length_string, \
    read_uintle, write_uintle


class ListExtractor:
    """Extracts binary data from the ROM's arm9 binary or overlays into a new file inside the ROM"""
    def __init__(self, rom: NintendoDSRom, binary: Pmd2Binary, spec: Pmd2LooseBinFile):
        self._rom = rom
        self._out_path = spec.filepath
        self._key = spec.srcdata
        self._binary = binary
        if self._key not in self._binary.blocks:
            raise ValueError("The source data block for the patch was not found in the configuration.")
        self._block = binary.blocks[self._key]

    def extract(self, entry_len: int, string_offs_per_entry: List[int], write_subheader=True):
        """Performs the extraction. Raises a RuntimeError on error."""
        try:
            binary = get_binary_from_rom_ppmdu(self._rom, self._binary)
            data = self._wrap_sir0(binary, binary[self._block.begin:self._block.end],
                                   entry_len, string_offs_per_entry, write_subheader)
            if self._out_path not in self._rom.filenames:
                create_file_in_rom(self._rom, self._out_path, data)
            else:
                self._rom.setFileByName(self._out_path, data)
        except BaseException as ex:
            raise RuntimeError("Error during extraction for patch.") from ex

    def _wrap_sir0(self, full_binary: bytes, table_data: bytes,
                   entry_len: int, string_offs_per_entry: List[int], write_subheader) -> bytes:
        table_data = bytearray(table_data)
        out_data = bytearray()
        pointer_offsets = []

        # 1. Write strings
        number_entries = 0
        for i in range(0, len(table_data), entry_len):
            for string_off in string_offs_per_entry:
                new_pointer = self._push_string(
                    full_binary,
                    out_data,
                    read_uintle(table_data, i + string_off, 4) - self._binary.loadaddress
                )
                pointer_offsets.append(i + string_off)
                write_uintle(table_data, new_pointer, i + string_off, 4)
            number_entries += 1
        # Padding
        self._pad(out_data)

        # 2. Correct string pointer offsets
        pointer_offsets = [off + len(out_data) for off in pointer_offsets]

        # 3. Append table
        pointer_data_block = len(out_data)
        out_data += table_data
        # Padding
        self._pad(out_data)

        # 4. Write sub-header
        if write_subheader:
            data_pointer = len(out_data)
            pointer_offsets.append(len(out_data))
            out_data += pointer_data_block.to_bytes(4, byteorder='little', signed=False)
            out_data += number_entries.to_bytes(4, byteorder='little', signed=False)
        else:
            data_pointer = pointer_data_block

        # 5. Convert into SIR0
        return FileType.SIR0.serialize(FileType.SIR0.wrap(out_data, pointer_offsets, data_pointer))

    def _push_string(self, full_binary: bytes, out_data: bytearray, pointer: int) -> int:
        """Add the string that's being pointed to to in full_binary to out_data and return a new relative pointer"""
        str_len, string = read_var_length_string(full_binary, pointer)
        new_pointer = len(out_data)
        out_data += bytes(string, string_codec.PMD2_STR_ENCODER)
        number_of_nulls = self._read_nulls(full_binary, pointer + str_len) + 1
        out_data += (b'\0' * number_of_nulls)
        return new_pointer

    def _pad(self, out_data):
        if len(out_data) % 16 != 0:
            out_data += bytes(0xAA for _ in range(0, 16 - (len(out_data) % 16)))

    def _read_nulls(self, out_data, pnt):
        nulls = 0
        while out_data[pnt] == 0:
            pnt += 1
            nulls += 1
        return nulls
