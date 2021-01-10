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
from skytemple_files.graphics.dbg.model import Dbg


class DbinSir0PkdpxDbgHandler(DataHandler[Dbg]):
    """A proxy data handler for Dbg compressed as At container wrapped in Sir0."""

    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Dbg:
        from skytemple_files.common.types.file_types import FileType
        pkdpx = FileType.DBIN_SIR0_PKDPX.deserialize(data)
        return FileType.DBG.deserialize(pkdpx.decompress())

    @classmethod
    def serialize(cls, data: Dbg, **kwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        serialized = FileType.DBG.serialize(data)
        return FileType.DBIN_SIR0_PKDPX.serialize(FileType.DBIN_SIR0_PKDPX.compress(serialized))
