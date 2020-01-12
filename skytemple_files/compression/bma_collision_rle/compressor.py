# noinspection PyAttributeOutsideInit


class BmaCollisionRleCompressor:
    def __init__(self, uncompressed_data: bytes):
        self.uncompressed_data = uncompressed_data
        self.reset()

    def reset(self):
        pass

    def compress(self) -> bytes:
        self.reset()
        raise NotImplementedError()
