from skytemple_files.graphics.kao.handler import KaoHandler
from skytemple_files.compression_container.at4px.handler import At4pxHandler
from skytemple_files.compression.px.handler import PxHandler


class FileType:
    """A list of supported file types. Values are their data handlers."""
    UNKNOWN = None
    KAO = KaoHandler
    AT4PX = At4pxHandler
    PX = PxHandler
