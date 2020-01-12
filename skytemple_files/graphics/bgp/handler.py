from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bgp.model import Bgp


class BgpHandler(DataHandler[Bgp]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Bgp:
        from skytemple_files.common.types.file_types import FileType
        return Bgp(FileType.AT4PX.deserialize(data).decompress())

    @classmethod
    def serialize(cls, data: Bgp) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        pass  # todo
