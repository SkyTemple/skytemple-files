from skytemple_files.common.util import *


class At4px:
    def __init__(self, data: bytes=None):
        """
        Create a AT4PX container from already compressed data.
        Setting data None is private, use compress instead for compressing data.
        """
        if data:
            self.length_compressed = self.cont_size(data)
            self.compression_flags = read_bytes(data, 7, 9)
            self.length_decompressed = read_uintle(data, 0x10, 2)
            self.compressed_data = data[0x12:]

    def decompress(self) -> bytes:
        """Returns the uncompressed data stored in the container"""
        from skytemple_files.common.types.file_types import FileType

        data = FileType.PX.decompress(self.compressed_data, self.compression_flags)
        # Sanity assertion, if everything is implemented correctly this doesn't fail.
        assert len(data) == self.length_decompressed
        return data

    def to_bytes(self) -> bytes:
        """Converts the container back into a bit (compressed) representation"""
        return b'AT4PX'\
               + self.length_compressed.to_bytes(2, 'little') \
               + self.compression_flags \
               + self.length_decompressed.to_bytes(2, 'little') \
               + self.compressed_data

    @classmethod
    def cont_size(cls, data: bytes, byte_offset=0):
        return read_uintle(data, byte_offset + 5, 2)

    @classmethod
    def compress(cls, data: bytes) -> 'At4px':
        """Create a new AT4PX container from originally uncompressed data."""
        from skytemple_files.common.types.file_types import FileType

        new_container = cls()
        flags, px_data = FileType.PX.compress(data)

        new_container.compression_flags = flags
        new_container.length_decompressed = len(data)
        new_container.compressed_data = px_data
        new_container.length_compressed = len(px_data) + 0x12
        return new_container
