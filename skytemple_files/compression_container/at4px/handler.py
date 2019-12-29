from typing import List

from bitstring import BitStream

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import read_bytes
from skytemple_files.compression_container.at4px.model import At4px


class At4pxHandler(DataHandler[At4px]):
    @classmethod
    def unserialize(cls, data: BitStream) -> At4px:
        """Load a AT4PX container into a high-level representation"""
        if not cls.matches(data):
            raise ValueError("The provided data is not an AT4PX container.")
        return At4px(data)

    @classmethod
    def serialize(cls, data: At4px) -> BitStream:
        """Convert the high-level AT4PX representation back into a BitStream."""
        return data.to_bit_stream()

    @classmethod
    def compress(cls, data: BitStream) -> At4px:
        """Turn uncompressed data into a new AT4PX container"""
        return At4px.compress(data)

    @classmethod
    def cont_size(cls, data: BitStream, byte_offset=0):
        """Get the size of an AT4PX container starting at the given offset in data."""
        if not cls.matches(data, byte_offset):
            raise ValueError("The provided data is not an AT4PX container.")
        return At4px.cont_size(data, byte_offset)

    @classmethod
    def matches(cls, data: BitStream, byte_offset=0):
        """Check if the given data stream is a At4px container"""
        try:
            return str(read_bytes(data, byte_offset, 5).bytes, 'ascii') == 'AT4PX'
        except UnicodeDecodeError:
            return False

    @classmethod
    def coverage(cls, data: BitStream) -> List[BitStream]:
        # todo
        pass
