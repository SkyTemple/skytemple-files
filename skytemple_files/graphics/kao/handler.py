from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import *
from skytemple_files.graphics.kao.model import Kao, SUBENTRIES, SUBENTRY_LEN
from skytemple_files.graphics.kao.writer import KaoWriter


class KaoHandler(DataHandler[Kao]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Kao:
        if not isinstance(data, memoryview):
            data = memoryview(data)
        # First 160 bytes are padding
        first_toc = next(x for x, val in enumerate(data) if val != 0)
        assert first_toc % SUBENTRIES*SUBENTRY_LEN == 0  # Padding should be a whole TOC entry
        # first pointer = end of TOC
        first_pointer = read_uintle(data, first_toc, SUBENTRY_LEN)
        toc_len = int((first_pointer - first_toc) / (SUBENTRIES*SUBENTRY_LEN))
        return Kao(data, first_toc, toc_len)

    @classmethod
    def serialize(cls, data: Kao) -> bytes:
        return KaoWriter(data).write()
