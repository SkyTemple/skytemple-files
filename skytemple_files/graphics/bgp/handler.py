from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bgp.model import Bgp
from skytemple_files.graphics.bgp.writer import BgpWriter


class BgpHandler(DataHandler[Bgp]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Bgp:
        from skytemple_files.common.types.file_types import FileType
        return Bgp(FileType.AT4PX.deserialize(data).decompress())

    @classmethod
    def serialize(cls, data: Bgp) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        return FileType.AT4PX.serialize(
            FileType.AT4PX.compress(
                BgpWriter(data).write()
            )
        )
