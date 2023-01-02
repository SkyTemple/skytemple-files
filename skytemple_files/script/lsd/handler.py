#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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

from __future__ import annotations

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.script.lsd.model import Lsd


class LsdHandler(DataHandler[Lsd]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> Lsd:
        return Lsd(data)

    @classmethod
    def serialize(cls, data: Lsd, **kwargs: OptionalKwargs) -> bytes:
        return data.to_bytes()

    @classmethod
    def new(cls) -> Lsd:
        return Lsd(None)
