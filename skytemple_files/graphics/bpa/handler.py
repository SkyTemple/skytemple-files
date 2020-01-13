from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bpa.model import Bpa
from skytemple_files.graphics.bpa.writer import BpaWriter


class BpaHandler(DataHandler[Bpa]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Bpa:
        return Bpa(data)

    @classmethod
    def serialize(cls, data: Bpa) -> bytes:
        return BpaWriter(data).write()
