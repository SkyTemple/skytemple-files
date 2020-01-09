# noinspection PyAttributeOutsideInit
from bitstring import BitStream


class BmaCollisionRleCompressor:
    def __init__(self, uncompressed_data: BitStream):
        self.uncompressed_data = uncompressed_data
        self.reset()

    def reset(self):
        pass

    def compress(self) -> BitStream:
        self.reset()
        raise NotImplementedError()
