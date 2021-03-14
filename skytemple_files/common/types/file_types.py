#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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
from skytemple_files.compression_container.pkdpx.handler import PkdpxHandler
from skytemple_files.container.bin_pack.handler import BinPackHandler
from skytemple_files.container.dungeon_bin.handler import DungeonBinHandler
from skytemple_files.container.dungeon_bin.sub.at4px_dpc import DbinAt4pxDpcHandler
from skytemple_files.container.dungeon_bin.sub.at4px_dpci import DbinAt4pxDpciHandler
from skytemple_files.container.dungeon_bin.sub.sir0_at4px import DbinSir0At4pxHandler
from skytemple_files.container.dungeon_bin.sub.sir0_at4px_dma import DbinSir0At4pxDmaHandler
from skytemple_files.container.dungeon_bin.sub.sir0_pkdpx import DbinSir0PkdpxHandler
from skytemple_files.container.dungeon_bin.sub.sir0_image_1033 import DbinSir0Image1033Handler
from skytemple_files.container.dungeon_bin.sub.sir0_pkdpx_dbg import DbinSir0PkdpxDbgHandler
from skytemple_files.container.dungeon_bin.sub.sir0_weird_data_file import DbinSir0WeirdDataFileHandler
from skytemple_files.container.dungeon_bin.sub.sir0_dpla import DbinSir0DplaHandler
from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.data.item_s_p.handler import ItemSPHandler
from skytemple_files.data.level_bin_entry.handler import LevelBinEntryHandler
from skytemple_files.data.md.handler import MdHandler
from skytemple_files.data.str.handler import StrHandler
from skytemple_files.data.waza_p.handler import WazaPHandler
from skytemple_files.data.item_p.handler import ItemPHandler
from skytemple_files.data.tbl_talk.handler import TblTalkHandler
from skytemple_files.dungeon_data.fixed_bin.handler import FixedBinHandler
from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler
from skytemple_files.dungeon_data.mappa_g_bin.handler import MappaGBinHandler
from skytemple_files.graphics.bgp.handler import BgpHandler
from skytemple_files.graphics.bma.handler import BmaHandler
from skytemple_files.graphics.bpa.handler import BpaHandler
from skytemple_files.graphics.bpc.handler import BpcHandler
from skytemple_files.graphics.bpl.handler import BplHandler
from skytemple_files.graphics.dbg.handler import DbgHandler
from skytemple_files.graphics.dma.handler import DmaHandler
from skytemple_files.graphics.dpc.handler import DpcHandler
from skytemple_files.graphics.dpci.handler import DpciHandler
from skytemple_files.graphics.dpl.handler import DplHandler
from skytemple_files.graphics.dpla.handler import DplaHandler
from skytemple_files.graphics.img_itm.handler import ImgItmHandler
from skytemple_files.graphics.img_trp.handler import ImgTrpHandler
from skytemple_files.graphics.kao.handler import KaoHandler
from skytemple_files.compression_container.common_at.handler import CommonAtHandler
from skytemple_files.compression_container.at3px.handler import At3pxHandler
from skytemple_files.compression_container.at4px.handler import At4pxHandler
from skytemple_files.compression_container.atupx.handler import AtupxHandler
from skytemple_files.compression_container.at4pn.handler import At4pnHandler
from skytemple_files.compression.px.handler import PxHandler
from skytemple_files.compression.custom_999.handler import Custom999Handler
from skytemple_files.compression.rle_nibble.handler import RleNibbleHandler
from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler
from skytemple_files.graphics.w16.handler import W16Handler
from skytemple_files.graphics.wan_wat.handler import WanHandler
from skytemple_files.graphics.wte.handler import WteHandler
from skytemple_files.graphics.wtu.handler import WtuHandler
from skytemple_files.graphics.chr.handler import ChrHandler
from skytemple_files.graphics.colvec.handler import ColvecHandler
from skytemple_files.graphics.zmappat.handler import ZMappaTHandler
from skytemple_files.graphics.fonts.font_dat.handler import FontDatHandler
from skytemple_files.graphics.fonts.font_sir0.handler import FontSir0Handler
from skytemple_files.graphics.fonts.banner_font.handler import BannerFontHandler
from skytemple_files.graphics.fonts.graphic_font.handler import GraphicFontHandler
from skytemple_files.graphics.pal.handler import PalHandler
from skytemple_files.list.actor.handler import ActorListBinHandler
from skytemple_files.script.lsd.handler import LsdHandler
from skytemple_files.script.ssa_sse_sss.handler import SsaHandler
from skytemple_files.script.ssb.handler import SsbHandler


class FileType:
    """A list of supported file types. Values are their data handlers."""
    UNKNOWN = None

    KAO = KaoHandler

    COMMON_AT = CommonAtHandler
    AT3PX = At3pxHandler
    AT4PX = At4pxHandler
    ATUPX = AtupxHandler
    PKDPX = PkdpxHandler
    AT4PN = At4pnHandler

    PX = PxHandler
    CUSTOM_999 = Custom999Handler
    GENERIC_NRL = GenericNrlHandler
    
    RLE_NIBBLE = RleNibbleHandler

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

    DUNGEON_BIN = DungeonBinHandler
    DPL = DplHandler
    DPLA = DplaHandler
    DPC = DpcHandler
    DPCI = DpciHandler
    DMA = DmaHandler
    DBG = DbgHandler

    FONT_DAT = FontDatHandler
    FONT_SIR0 = FontSir0Handler
    BANNER_FONT = BannerFontHandler
    GRAPHIC_FONT = GraphicFontHandler
    
    CHR = ChrHandler
    
    WTE = WteHandler
    WTU = WtuHandler

    WAN = WanHandler
    WAT = WanHandler

    W16 = W16Handler
    STR = StrHandler
    LSD = LsdHandler

    SSA = SsaHandler
    SSE = SsaHandler
    SSS = SsaHandler
    SSB = SsbHandler
    
    PAL = PalHandler

    SIR0 = Sir0Handler
    BIN_PACK = BinPackHandler

    MD = MdHandler
    LEVEL_BIN_ENTRY = LevelBinEntryHandler
    WAZA_P = WazaPHandler
    ITEM_P = ItemPHandler
    ITEM_SP = ItemSPHandler
    TBL_TALK = TblTalkHandler

    # These handlers assume the content to be Sir0 wrapped by default:
    MAPPA_BIN = MappaBinHandler
    MAPPA_G_BIN = MappaGBinHandler
    FIXED_BIN = FixedBinHandler
    
    # dungeon.bin sub file handlers
    DBIN_SIR0_DPLA = DbinSir0DplaHandler
    DBIN_SIR0_AT4PX_DMA = DbinSir0At4pxDmaHandler
    DBIN_AT4PX_DPC = DbinAt4pxDpcHandler
    DBIN_AT4PX_DPCI = DbinAt4pxDpciHandler
    DBIN_SIR0_AT4PX = DbinSir0At4pxHandler
    DBIN_SIR0_PKDPX = DbinSir0PkdpxHandler
    DBIN_SIR0_PKDPX_DBG = DbinSir0PkdpxDbgHandler
    DBIN_SIR0_WEIRD_DATA_FILE = DbinSir0WeirdDataFileHandler
    DBIN_SIR0_IMAGE_1033 = DbinSir0Image1033Handler
    DBIN_SIR0_COLVEC = ColvecHandler
    DBIN_SIR0_IMG_ITM = ImgItmHandler
    DBIN_SIR0_IMG_TRP = ImgTrpHandler
    DBIN_SIR0_ZMAPPAT = ZMappaTHandler

    # Please don't use these directly, use them via the ppmdu_config instead!
    # (skytemple_files.common.util.get_ppmdu_config_for_rom).
    ACTOR_LIST_BIN = ActorListBinHandler
