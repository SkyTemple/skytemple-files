"""Converts BgList models back into the binary format used by the game"""
import string

from skytemple_files.graphics.bg_list_dat.model import BgList

ALLOWED_CHARS = set(string.digits + string.ascii_uppercase)
MAX_LEN = 8


class BgListWriter:
    def __init__(self, model: BgList):
        self.model = model
        self.data = None
        self.bytes_written = 0

    def write(self) -> bytes:
        # At max we will need 11 8 character cstrings for each entry:
        self.data = bytearray(len(self.model.level) * 11 * 9)
        self.bytes_written = 0
        for l in self.model.level:
            # BPL
            self._write_string(l.bpl_name)
            self._write_string(l.bpc_name)
            self._write_string(l.bma_name)
            for i in range(0, 8):
                if l.bpa_names[i] is not None:
                    self._write_string(l.bpa_names[i])
                else:
                    self._write_string("")

        return self.data[:self.bytes_written]

    def _write_string(self, string: str):
        byts = self._read_string(string)
        self.data[self.bytes_written:self.bytes_written + MAX_LEN] = byts
        self.bytes_written += MAX_LEN

    def _read_string(self, string: str):
        if set(string) > ALLOWED_CHARS:
            raise ValueError(f"The string '{string}' can not be used for bg_list.dat. Only "
                             f"digits and uppercase characters are allowed.")
        length = len(string)
        if length > MAX_LEN:
            raise ValueError(f"The string '{string}' is too long for bg_list.dat. Max size "
                             f"is {MAX_LEN}")
        out = bytearray(MAX_LEN)
        out[0:length] = bytearray(string, 'ascii')
        return out
