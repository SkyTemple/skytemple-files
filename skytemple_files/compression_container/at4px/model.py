import bitstring
from bitstring import BitStream

from skytemple_files.common.util import read_bytes


class At4px:
    def __init__(self, data: BitStream=None):
        """
        Create a AT4PX container from already compressed data.
        Setting data None is private, use compress instead for compressing data.
        """
        if data:
            self.length_compressed = self.cont_size(data)
            self.compression_flags = read_bytes(data, 7, 9)
            self.length_decompressed = read_bytes(data, 0x10, 2).uintle
            self.compressed_data = data[0x12*8:]

    def decompress(self) -> BitStream:
        """Returns the uncompressed data stored in the container"""
        from skytemple_files.common.types.file_types import FileType

        data = FileType.PX.decompress(self.compressed_data, self.compression_flags)
        # Sanity assertion, if everything is implemented correctly this doesn't fail.
        assert len(data) / 8 == self.length_decompressed
        return data

    def to_bit_stream(self) -> BitStream:
        """Converts the container back into a bit (compressed) representation"""
        return BitStream(bytes('AT4PX', 'ascii')) \
               + bitstring.pack('intle:16', self.length_compressed) \
               + self.compression_flags \
               + bitstring.pack('intle:16', self.length_decompressed) \
               + self.compressed_data

    @classmethod
    def cont_size(cls, data: BitStream, byte_offset=0):
        return read_bytes(data, byte_offset + 5, 2).uintle

    @classmethod
    def compress(cls, data: BitStream) -> 'At4px':
        """Create a new AT4PX container from originally uncompressed data."""
        from skytemple_files.common.types.file_types import FileType

        new_container = cls()
        flags, px_data = FileType.PX.compress(data)

        new_container.compression_flags = flags
        new_container.length_decompressed = int(len(data) / 8)
        new_container.compressed_data = px_data
        new_container.length_compressed = int(len(px_data) / 8) + 0x12
        return new_container
