import os
from pathlib import PurePosixPath
from typing import List, Union

from bitstring import BitStream
from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import read_bytes
from skytemple_files.graphics.bma.model import Bma
from skytemple_files.graphics.bpc.model import Bpc
from skytemple_files.graphics.bpl.model import Bpl

DIR = 'MAP_BG'
BPC_EXT = '.bpc'
BPL_EXT = '.bpl'
BMA_EXT = '.bma'
BPA_EXT = '.bpa'


class BgListEntry:
    def __init__(self, bpl_name: str, bpc_name: str, bma_name: str, bpa_names: List[str]):
        self.bpl_name = bpl_name
        self.bpc_name = bpc_name
        self.bma_name = bma_name
        self.bpa_names = bpa_names
        # There can only be 8 BPAs. There isn't more space!
        assert len(bpa_names) <= 8

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
        """
        from skytemple_files.common.types.file_types import FileType
        bpas = []
        for bpa_name in self.bpa_names:
            bpas.append(FileType.BPA.deserialize(self._get_file(
                str(PurePosixPath(DIR).joinpath(bpa_name.lower() + BPA_EXT)),
                rom_or_directory_root
            )))
        return bpas

    def _get_file(self, filename, rom_or_directory_root) -> BitStream:
        if isinstance(rom_or_directory_root, NintendoDSRom):
            return BitStream(rom_or_directory_root.getFileByName(filename))
        elif isinstance(rom_or_directory_root, str):
            with open(os.path.join(rom_or_directory_root, filename), 'rb') as f:
                data = f.read()
            return BitStream(data)
        raise ValueError("Provided rom_or_directory is neither a string nor a NintendoDSRom.")


class BgList:
    def __init__(self, data: BitStream):
        self.level: List[BgListEntry] = []
        for entry in data.cut(11*8*8):
            bpas = []
            for potential_bpa in entry.cut(8*8, 24*8, 88*8):
                if potential_bpa.uint != 0:
                    bpas.append(potential_bpa.bytes.rstrip(b'\0').decode('ascii'))

            self.level.append(BgListEntry(
                read_bytes(entry, 0, 8).bytes.rstrip(b'\0').decode('ascii'),
                read_bytes(entry, 8, 8).bytes.rstrip(b'\0').decode('ascii'),
                read_bytes(entry, 16, 8).bytes.rstrip(b'\0').decode('ascii'),
                bpas
            ))
