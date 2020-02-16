#  Copyright 2020 Parakoopa
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.

from skytemple_files.compression.bma_collision_rle.handler import BmaCollisionRleHandler
from skytemple_files.compression.bma_layer_nrl.handler import BmaLayerNrlHandler
from skytemple_files.compression.bpc_image.handler import BpcImageHandler
from skytemple_files.compression.bpc_tilemap.handler import BpcTilemapHandler
from skytemple_files.compression.generic_nrl.handler import GenericNrlHandler
from skytemple_files.data.str.handler import StrHandler
from skytemple_files.graphics.bgp.handler import BgpHandler
from skytemple_files.graphics.bma.handler import BmaHandler
from skytemple_files.graphics.bpa.handler import BpaHandler
from skytemple_files.graphics.bpc.handler import BpcHandler
from skytemple_files.graphics.bpl.handler import BplHandler
from skytemple_files.graphics.kao.handler import KaoHandler
from skytemple_files.compression_container.at4px.handler import At4pxHandler
from skytemple_files.compression.px.handler import PxHandler
from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler
from skytemple_files.script.lsd.handler import LsdHandler
from skytemple_files.script.ssa_sse_sss.handler import SsaHandler
from skytemple_files.script.ssb.handler import SsbHandler


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
    STR = StrHandler
    LSD = LsdHandler
    SSA = SsaHandler
    SSE = SsaHandler
    SSS = SsaHandler
    SSB = SsbHandler
