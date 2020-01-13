from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bma.model import Bma
from skytemple_files.graphics.bma.writer import BmaWriter


class BmaHandler(DataHandler[Bma]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Bma:
        return Bma(data)

    @classmethod
    def serialize(cls, data: Bma) -> bytes:
        return BmaWriter(data).write()
