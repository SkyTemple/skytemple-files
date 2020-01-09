from skytemple_files.compression.bma_collision_rle.handler import BmaCollisionRleHandler
from skytemple_files.compression.bma_layer_nrl.handler import BmaLayerNrlHandler
from skytemple_files.compression.bpc_image.handler import BpcImageHandler
from skytemple_files.compression.bpc_tilemap.handler import BpcTilemapHandler
from skytemple_files.compression.generic_nrl.handler import GenericNrlHandler
from skytemple_files.graphics.bgp.handler import BgpHandler
from skytemple_files.graphics.bma.handler import BmaHandler
from skytemple_files.graphics.bpa.handler import BpaHandler
from skytemple_files.graphics.bpc.handler import BpcHandler
from skytemple_files.graphics.bpl.handler import BplHandler
from skytemple_files.graphics.kao.handler import KaoHandler
from skytemple_files.compression_container.at4px.handler import At4pxHandler
from skytemple_files.compression.px.handler import PxHandler
from skytemple_files.unique.bg_list_dat.handler import BgListDatHandler


class FileType:
    """A list of supported file types. Values are their data handlers."""
    UNKNOWN = None
    KAO = KaoHandler
    AT4PX = At4pxHandler
    PX = PxHandler
    BGP = BgpHandler
    BG_LIST_DAT = BgListDatHandler
    BPL = BplHandler
    BPC = BpcHandler
    BPC_IMAGE = BpcImageHandler
    BPC_TILEMAP = BpcTilemapHandler
    BMA = BmaHandler
    BMA_LAYER_NRL = BmaLayerNrlHandler
    BMA_COLLISION_RLE = BmaCollisionRleHandler
    BPA = BpaHandler
    GENERIC_NRL = GenericNrlHandler
