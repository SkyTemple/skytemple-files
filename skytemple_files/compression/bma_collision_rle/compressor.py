from skytemple_files.common.util import read_uintle

RLE_MAX_LOOKAHEAD_SIZE = 127


# noinspection PyAttributeOutsideInit
class BmaCollisionRleCompressor:
    def __init__(self, uncompressed_data: bytes):
        if not isinstance(uncompressed_data, memoryview):
            uncompressed_data = memoryview(uncompressed_data)
        self.uncompressed_data = uncompressed_data
        self.length_input = len(uncompressed_data)
        self.reset()

    def reset(self):
        # At worst we have input data of 0101 repeating.
        self.compressed_data = bytearray(self.length_input)
        self.cursor = 0
        self.bytes_written = 0

    def compress(self) -> bytes:
        self.reset()

        while self.cursor < self.length_input:
            self._process()

        return self.compressed_data[:self.bytes_written]

    def _process(self):
        next = self._read()
        repeats = self._look_ahead_repeats(next)
        self.cursor += repeats
        if next > 0:
            # Write 1
            w = 0x80 + repeats
        else:
            # Write 0
            w = repeats
        self._write(w)

    def _read(self):
        """Read a single byte and increase cursor"""
        if self.cursor >= self.length_input:
            raise ValueError("BMA Collision RLE Compressor: Reached EOF while reading data.")
        oc = self.cursor
        self.cursor += 1
        return 1 if read_uintle(self.uncompressed_data, oc) > 0 else 0

    def _write(self, data):
        """Writes to the output as byte"""
        self.compressed_data[self.bytes_written] = data
        self.bytes_written += 1

    def _look_ahead_repeats(self, data):
        """Look how often the byte in the input data repeats, up to RLE_MAX_LOOKAHEAD_SIZE"""
        nc = self.cursor
        repeats = 0
        while read_uintle(self.uncompressed_data, nc) == data and \
                repeats < RLE_MAX_LOOKAHEAD_SIZE and \
                nc < self.length_input:
            repeats += 1
            nc += 1
        return repeats
