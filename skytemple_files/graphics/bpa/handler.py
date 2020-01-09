from bitstring import BitStream

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bpa.model import Bpa


class BpaHandler(DataHandler[Bpa]):
    @classmethod
    def deserialize(cls, data: BitStream, **kwargs) -> Bpa:
        return Bpa(data)

    @classmethod
    def serialize(cls, data: Bpa) -> BitStream:
        from skytemple_files.common.types.file_types import FileType
        pass  # todo
