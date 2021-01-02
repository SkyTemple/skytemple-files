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

import os
from pathlib import PurePosixPath
from typing import List, Union, Optional

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import *
from skytemple_files.graphics.bma.model import Bma
from skytemple_files.graphics.bpc.model import Bpc
from skytemple_files.graphics.bpl.model import Bpl

DIR = 'MAP_BG'
BPC_EXT = '.bpc'
BPL_EXT = '.bpl'
BMA_EXT = '.bma'
BPA_EXT = '.bpa'


class BgListEntry:
    def __init__(self, bpl_name: str, bpc_name: str, bma_name: str, bpa_names: List[Optional[str]]):
        # ALL names can only be 1-8 character ASCII strings with only uppercase
        # letters. This is checked during serialization in the writer.
        self.bpl_name = bpl_name
        self.bpc_name = bpc_name
        self.bma_name = bma_name
        self.bpa_names = bpa_names
        # There can only be 8 BPAs. There isn't more space!
        assert len(bpa_names) == 8

    def __str__(self):
        return f"BPL: {self.bpl_name}, BPC: {self.bpc_name}, BMA: {self.bma_name}, BPAs: {self.bpa_names}"

    def get_bpl(self, rom_or_directory_root: Union[str, NintendoDSRom]) -> Bpl:
        """
        Returns the BPL model that is referenced in this entry.
        Can be serialized with the BPL DataHandler. Original filename in self.bpl_name.
        """
        from skytemple_files.common.types.file_types import FileType
        return FileType.BPL.deserialize(self._get_file(
            str(PurePosixPath(DIR).joinpath(self.bpl_name.lower() + BPL_EXT)),
            rom_or_directory_root
        ))

    def get_bpc(self, rom_or_directory_root: Union[str, NintendoDSRom], bpc_tiling_width=3, bpc_tiling_height=3) -> Bpc:
        """
        Returns the BPC model that is referenced in this entry.
        Can be serialized with the BPC DataHandler. Original filename in self.bpc_name.
        """
        from skytemple_files.common.types.file_types import FileType
        return FileType.BPC.deserialize(self._get_file(
            str(PurePosixPath(DIR).joinpath(self.bpc_name.lower() + BPC_EXT)),
            rom_or_directory_root
        ), tiling_width=bpc_tiling_width, tiling_height=bpc_tiling_height)

    def get_bma(self, rom_or_directory_root: Union[str, NintendoDSRom]) -> Bma:
        """
        Returns the BMA model that is referenced in this entry.
        Can be serialized with the BMA DataHandler. Original filename in self.bma_name.
        """
        from skytemple_files.common.types.file_types import FileType
        return FileType.BMA.deserialize(self._get_file(
            str(PurePosixPath(DIR).joinpath(self.bma_name.lower() + BMA_EXT)),
            rom_or_directory_root
        ))

    def get_bpas(self, rom_or_directory_root: Union[str, NintendoDSRom]):
        """
        Returns a list of BPA models that are referenced in this entry.
        Can be serialized with the BPA DataHandler. Original filenames in self.bpa_names.
        All BPA slots are returned, in order, even empty ones (None).
        """
        from skytemple_files.common.types.file_types import FileType
        bpas = []
        for bpa_name in self.bpa_names:
            if bpa_name is not None:
                bpas.append(FileType.BPA.deserialize(self._get_file(
                    str(PurePosixPath(DIR).joinpath(bpa_name.lower() + BPA_EXT)),
                    rom_or_directory_root
                )))
            else:
                bpas.append(None)
        return bpas

    def _get_file(self, filename, rom_or_directory_root) -> bytes:
        if isinstance(rom_or_directory_root, NintendoDSRom):
            return rom_or_directory_root.getFileByName(filename)
        elif isinstance(rom_or_directory_root, str):
            with open(os.path.join(rom_or_directory_root, filename), 'rb') as f:
                data = f.read()
            return data
        raise ValueError("Provided rom_or_directory is neither a string nor a NintendoDSRom.")


class BgList:
    """BgList model. To edit entries, manipulate the levels list."""
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        self.level: List[BgListEntry] = []
        for entry in iter_bytes(data, 11*8):
            bpas = []
            for potential_bpa in iter_bytes(entry, 8, 24, 88):
                if bytes(potential_bpa)[0] != 0:
                    bpas.append(bytes(potential_bpa).rstrip(b'\0').decode('ascii'))
                else:
                    bpas.append(None)

            self.level.append(BgListEntry(
                read_bytes(bytes(entry), 0, 8).rstrip(b'\0').decode('ascii'),
                read_bytes(bytes(entry), 8, 8).rstrip(b'\0').decode('ascii'),
                read_bytes(bytes(entry), 16, 8).rstrip(b'\0').decode('ascii'),
                bpas
            ))

    def find_bma(self, name) -> int:
        """Count all occurrences of this BMA in the list."""
        count = 0
        for l in self.level:
            if l.bma_name == name:
                count += 1
        return count

    def find_bpl(self, name) -> int:
        """Count all occurrences of this BPL in the list."""
        count = 0
        for l in self.level:
            if l.bpl_name == name:
                count += 1
        return count

    def find_bpc(self, name) -> int:
        """Count all occurrences of this BPL in the list."""
        count = 0
        for l in self.level:
            if l.bpc_name == name:
                count += 1
        return count

    def find_bpa(self, name) -> int:
        """Count all occurrences of this BPA in the list."""
        count = 0
        for l in self.level:
            for bpa in l.bpa_names:
                if bpa == name:
                    count += 1
        return count
