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

from skytemple_files.common.string_codec import PMD2_STR_ENCODER
from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.data.str.model import Str


class StrHandler(DataHandler[Str]):
    @classmethod
    def deserialize(cls, data: bytes, *, string_encoding: str = PMD2_STR_ENCODER, **kwargs: OptionalKwargs) -> Str:  # type: ignore
        return Str(data, string_encoding)

    @classmethod
    def serialize(cls, data: Str, **kwargs: OptionalKwargs) -> bytes:
        return data.to_bytes()
