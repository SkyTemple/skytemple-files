from skytemple_files.compression.generic_nrl.compressor import GenericNrlCompressor

DEBUG = False


# noinspection PyAttributeOutsideInit
class BpcTilemapCompressor(GenericNrlCompressor):
    """
    The compression ist just simple NRL in two runs, first
    skipping all low bytes and then all high bytes.
    """

    def compress(self) -> bytes:
        self.reset()
        if DEBUG:
            print("BPC Tilemap NRL compressor start...")

        # First we process all the high bytes (LE)
        self.cursor = 1
        while self.cursor < self.length_input:
            self._process(2)

        if DEBUG:
            print(f"End Phase 1. Begin Phase 2.")
            print(f"Cursor begin phase 2: {self.bytes_written}")

        # And then all the low bytes (LE)
        self.cursor = 0
        while self.cursor < self.length_input:
            self._process(2)

        return self.compressed_data[:self.bytes_written]
