import abc
from bitstring import BitStream
from typing import TypeVar, Generic, List

T = TypeVar('T')


class DataHandler(Generic[T], abc.ABC):
    """
    Handler base class for a file or data type.
    Can convert it's type into high-level representations and back.
    """

    @classmethod
    @abc.abstractmethod
    def unserialize(cls, data: BitStream) -> T:
        """Loads the internal high-level representation for this data type"""
        pass

    @classmethod
    @abc.abstractmethod
    def serialize(cls, data: T) -> BitStream:
        """Converts the internal high-level representation back into a bit stream."""
        pass

    @classmethod
    @abc.abstractmethod
    def coverage(cls, data: BitStream) -> List[BitStream]:
        """
        Report data coverage of this data handler.
        Fill all bytes in the data stream like so:

        0x00: I don't know what this data is for, and I don't use it
        0x01: I know this data, but don't use it (it's not relevant)
        0xff: I know this data and use it
        0x??: This data is compressed and (may) match multiple other conditions, return list at
              index 0x?? contains a BitStream representation of the coverage of the
              uncompressed data. [?? = 0x02 - 0xfe]

        The BitStream passed consists only of 0 by default.

        This method is used by the data_coverage tests to check how much
        of the ROM skytemple_files already covers.

        """
        pass
