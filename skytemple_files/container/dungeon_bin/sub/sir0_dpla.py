#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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
from skytemple_files.graphics.dpla.model import Dpla


class DbinSir0DplaHandler(DataHandler[Dpla]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> Dpla:
        from skytemple_files.common.types.file_types import FileType

        sir0 = FileType.SIR0.deserialize(data)
        return FileType.SIR0.unwrap_obj(sir0, Dpla)  # type: ignore

    @classmethod
    def serialize(cls, data: Dpla, **kwargs: OptionalKwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType

        sir0 = FileType.SIR0.wrap_obj(data)  # type: ignore
        return FileType.SIR0.serialize(sir0)
