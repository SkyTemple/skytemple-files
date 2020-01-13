from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.bpc.model import Bpc
from skytemple_files.graphics.bpc.writer import BpcWriter


class BpcHandler(DataHandler[Bpc]):
    @classmethod
    def deserialize(cls, data: bytes, tiling_width=3, tiling_height=3, **kwargs) -> Bpc:
        """
        Creates a BPC. A BPC contains two layers of image data. The image data is
        grouped in 8x8 tiles, and these tiles are grouped in {tiling_width}x{tiling_height}
        chunks using a tile mapping.
        These chunks are referenced in the BMA tile to build the actual image.
        The tiling sizes are also stored in the BMA file.
        Each tile mapping is aso asigned a palette number. The palettes are stored in the BPL
        file for the map background and always contain 16 colors.

        The default for tiling_width and height are 3x3, because the game seems to be hardcoded this way.
        """
        return Bpc(data, tiling_width, tiling_height)

    @classmethod
    def serialize(cls, data: Bpc) -> bytes:
        return BpcWriter(data).write()
