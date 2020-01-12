from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bg_list_dat.model import BgList
from skytemple_files.graphics.bg_list_dat.writer import BgListWriter


class BgListDatHandler(DataHandler[BgList]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> BgList:
        return BgList(data)

    @classmethod
    def serialize(cls, data: BgList) -> bytes:
        return BgListWriter(data).write()
