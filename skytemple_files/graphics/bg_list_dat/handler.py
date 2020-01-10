from bitstring import BitStream

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bg_list_dat.model import BgList


class BgListDatHandler(DataHandler[BgList]):
    @classmethod
    def deserialize(cls, data: BitStream, **kwargs) -> BgList:
        return BgList(data)

    @classmethod
    def serialize(cls, data: BgList) -> BitStream:
        pass  # todo
