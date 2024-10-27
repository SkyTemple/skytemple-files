#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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
from skytemple_files.graphics.sma.model import SmaFile
from skytemple_files.graphics.sma.sheets import ExportSheets

class SmaHandler(DataHandler[SmaFile]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> SmaFile:
        from skytemple_files.common.types.file_types import FileType

        return FileType.SIR0.unwrap_obj(FileType.SIR0.deserialize(data), SmaFile)  # type: ignore

    @classmethod
    def serialize(cls, data: SmaFile, **kwargs: OptionalKwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType

        return FileType.SIR0.serialize(FileType.SIR0.wrap_obj(data))  # type: ignore

    @classmethod
    def export_sheets(cls, out_dir: str, sma: SmaFile, palette_idx: int) -> None:
        return ExportSheets(out_dir, sma, palette_idx)  # type: ignore

