from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bma.model import Bma


class BmaHandler(DataHandler[Bma]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Bma:
        return Bma(data)

    @classmethod
    def serialize(cls, data: Bma) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        pass  # todo
