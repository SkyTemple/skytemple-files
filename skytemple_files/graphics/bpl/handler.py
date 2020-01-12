from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bpl.model import Bpl


class BplHandler(DataHandler[Bpl]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Bpl:
        return Bpl(data)

    @classmethod
    def serialize(cls, data: Bpl) -> bytes:
        pass  # todo
