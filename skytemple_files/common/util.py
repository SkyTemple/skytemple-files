from bitstring import BitStream


def read_bytes(data: BitStream, start: int, length=1, byte_size=8) -> BitStream:
    """Read a number of bytes (default 1) from a BitStream"""
    return data[start*byte_size:(start+length)*byte_size]
