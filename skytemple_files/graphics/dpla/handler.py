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

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.dpla.model import Dpla


class DplaHandler(DataHandler[Dpla]):
    """
    Dpla handler. Note that this isn't actually used, since dpla is notmally Sir0 wrapped,
    see skytemple_files.container.dungeon_bin.sub.sir0_dpla.DbinSir0DbplaHandler.
    If used directly, we assume the file starts with the pointers to the palette.
    """
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Dpla:
        return Dpla(data, 0)

    @classmethod
    def serialize(cls, data: Dpla, **kwargs) -> bytes:
        return data.sir0_serialize_parts()[0]
