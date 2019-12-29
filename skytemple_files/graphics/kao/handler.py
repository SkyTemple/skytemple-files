from typing import List

from bitstring import BitStream

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import read_bytes
from skytemple_files.graphics.kao.model import Kao, SUBENTRIES, SUBENTRY_LEN
from skytemple_files.graphics.kao.writer import KaoWriter


class KaoHandler(DataHandler[Kao]):
    @classmethod
    def unserialize(cls, data: BitStream) -> Kao:
        # First 160 bytes are padding
        first_toc = next(x for x, val in enumerate(data.cut(8)) if val.int != 0)
        assert first_toc % SUBENTRIES*SUBENTRY_LEN == 0  # Padding should be a whole TOC entry
        # first pointer = end of TOC
        first_pointer = read_bytes(data, first_toc, SUBENTRY_LEN).intle
        toc_len = int((first_pointer - first_toc) / (SUBENTRIES*SUBENTRY_LEN))
        return Kao(data, first_toc, toc_len)

    @classmethod
    def serialize(cls, data: Kao) -> BitStream:
        return KaoWriter(data).write()

    @classmethod
    def coverage(cls, data: BitStream) -> List[BitStream]:
        # todo
        pass
