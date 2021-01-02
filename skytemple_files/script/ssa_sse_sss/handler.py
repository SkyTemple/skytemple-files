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
from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.script.ssa_sse_sss.model import Ssa
from skytemple_files.script.ssa_sse_sss.writer import SsaWriter


class SsaHandler(DataHandler[Ssa]):
    @classmethod
    def deserialize(cls, data: bytes, scriptdata=None, **kwargs) -> Ssa:
        if scriptdata is None:
            scriptdata = Pmd2XmlReader.load_default().script_data
        return Ssa(scriptdata, data)

    @classmethod
    def serialize(cls, data: Ssa, **kwargs) -> bytes:
        return SsaWriter(data).write()
