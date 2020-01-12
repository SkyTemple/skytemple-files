import abc
from typing import TypeVar, Generic

T = TypeVar('T')


class DataHandler(Generic[T], abc.ABC):
    """
    Handler base class for a file or data type.
    Can convert it's type into high-level representations and back.
    """

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, data: bytes, **kwargs) -> T:
        """Loads the internal high-level representation for this data type"""
        pass

    @classmethod
    @abc.abstractmethod
    def serialize(cls, data: T) -> bytes:
        """Converts the internal high-level representation back into a bit stream."""
        pass
