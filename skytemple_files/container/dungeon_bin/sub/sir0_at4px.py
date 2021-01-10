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
from skytemple_files.compression_container.common_at.model import CommonAt
from skytemple_files.compression_container.common_at.handler import COMMON_AT_BEST_3

class DbinSir0At4pxHandler(DataHandler[CommonAt]):
    """A proxy data handler for At wrapped in Sir0."""

    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> CommonAt:
        from skytemple_files.common.types.file_types import FileType
        sir0 = FileType.SIR0.deserialize(data)
        # We don't support more than the two default pointers, since we will also on serialize with those!
        assert len(sir0.content_pointer_offsets) == 0, "The Sir0 contains an unexpected amount of pointers."
        # We don't support a data pointer, because we will also serialize without.
        assert sir0.data_pointer == 0,  "The Sir0 contains a data pointer. That is not supported."
        # XXX: The developers messed up and somehow managed to include parts of
        # the sir0 "footer" in the compressed size.
        return FileType.COMMON_AT.deserialize(sir0.content)

    @classmethod
    def serialize(cls, data: CommonAt, **kwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        sir0 = FileType.SIR0.wrap(FileType.COMMON_AT.serialize(data), [], None)
        return FileType.SIR0.serialize(sir0)

    @classmethod
    def compress(cls, data: bytes) -> CommonAt:
        from skytemple_files.common.types.file_types import FileType
        return FileType.COMMON_AT.compress(data, COMMON_AT_BEST_3)

    @classmethod
    def cont_size(cls, data: bytes, byte_offset=0):
        """Get the size of an AT4PX container starting at the given offset in data."""
        from skytemple_files.common.types.file_types import FileType
        sir0 = FileType.SIR0.deserialize(data)
        return FileType.COMMON_AT.cont_size(sir0.content, byte_offset)

    @classmethod
    def matches(cls, data: bytes, byte_offset=0):
        """Check if the given data stream is an At container"""
        from skytemple_files.common.types.file_types import FileType
        sir0 = FileType.SIR0.deserialize(data)
        return FileType.COMMON_AT.matches(sir0.content, byte_offset)
