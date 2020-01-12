from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bpa.model import Bpa


class BpaHandler(DataHandler[Bpa]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Bpa:
        return Bpa(data)

    @classmethod
    def serialize(cls, data: Bpa) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        pass  # todo
