from bitstring import BitStream

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bpl.model import Bpl


class BplHandler(DataHandler[Bpl]):
    @classmethod
    def deserialize(cls, data: BitStream, **kwargs) -> Bpl:
        return Bpl(data)

    @classmethod
    def serialize(cls, data: Bpl) -> BitStream:
        pass  # todo
