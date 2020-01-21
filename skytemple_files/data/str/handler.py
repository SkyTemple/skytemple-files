from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.data.str.model import Str


class StrHandler(DataHandler[Str]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Str:
        return Str(data)

    @classmethod
    def serialize(cls, data: Str) -> bytes:
        return data.to_bytes()
