from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bpl.model import Bpl
from skytemple_files.graphics.bpl.writer import BplWriter


class BplHandler(DataHandler[Bpl]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Bpl:
        return Bpl(data)

    @classmethod
    def serialize(cls, data: Bpl) -> bytes:
        return BplWriter(data).write()
