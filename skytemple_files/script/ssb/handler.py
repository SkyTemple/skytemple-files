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
from skytemple_files.common.ppmdu_config.data import GAME_REGION_EU, GAME_REGION_US, Pmd2Data, GAME_REGION_JP
from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.script.ssb.header import SsbHeaderEu, SsbHeaderUs, SsbHeaderJp
from skytemple_files.script.ssb.model import Ssb
from skytemple_files.script.ssb.writer import SsbWriter


class SsbHandler(DataHandler[Ssb]):
    @classmethod
    def deserialize(cls, data: bytes, static_data: Pmd2Data = None, **kwargs) -> Ssb:
        if static_data is None:
            static_data = Pmd2XmlReader.load_default()
        if static_data.game_region == GAME_REGION_EU:
            ssb_header = SsbHeaderEu(data)
        elif static_data.game_region == GAME_REGION_US:
            ssb_header = SsbHeaderUs(data)
        elif static_data.game_region == GAME_REGION_JP:
            ssb_header = SsbHeaderJp(data)
        else:
            raise ValueError(f"Unsupported game edition: {static_data.game_edition}")

        return Ssb(data, ssb_header, ssb_header.data_offset, static_data.script_data, string_codec=static_data.string_encoding)

    @classmethod
    def serialize(cls, data: Ssb, static_data: Pmd2Data = None, **kwargs) -> bytes:
        if static_data is None:
            static_data = Pmd2XmlReader.load_default()

        return SsbWriter(data, static_data).write()

    @classmethod
    def create(cls, static_data: Pmd2Data = None) -> Ssb:
        """Create a new empty script"""
        if static_data is None:
            static_data = Pmd2XmlReader.load_default()

        if static_data.game_region == GAME_REGION_US:
            header_cls = SsbHeaderUs
        elif static_data.game_region == GAME_REGION_EU:
            header_cls = SsbHeaderEu
        else:
            raise ValueError(f"Unsupported game edition: {static_data.game_edition}")

        return Ssb.create_empty(static_data.script_data, header_cls.supported_langs())
