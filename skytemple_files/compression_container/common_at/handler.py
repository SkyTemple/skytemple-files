#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
from __future__ import annotations

import os
from enum import Enum, auto
from typing import List, Optional

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import OptionalKwargs, read_bytes
from skytemple_files.compression_container.at3px.handler import At3pxHandler
from skytemple_files.compression_container.at4pn.handler import At4pnHandler
from skytemple_files.compression_container.at4px.handler import At4pxHandler
from skytemple_files.compression_container.atupx.handler import AtupxHandler
from skytemple_files.compression_container.base_handler import (
    CompressionContainerHandler,
)
from skytemple_files.compression_container.pkdpx.handler import PkdpxHandler
from skytemple_files.compression_container.protocol import CompressionContainerProtocol


class CommonAtType(Enum):
    AT4PN = auto(), At4pnHandler, True
    AT3PX = auto(), At3pxHandler, True
    AT4PX = auto(), At4pxHandler, True
    ATUPX = auto(), AtupxHandler, False
    PKDPX = auto(), PkdpxHandler, True

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
        self, _: int, handler: CompressionContainerHandler, auto_allowed: bool
    ):
        self.handler = handler
        self.auto_allowed = auto_allowed


# Pre-built lists for compression
COMMON_AT_BEST_3 = [
    CommonAtType.AT4PN,
    CommonAtType.ATUPX,
    CommonAtType.AT3PX,
    CommonAtType.PKDPX,
]
COMMON_AT_BEST_4 = [
    CommonAtType.AT4PN,
    CommonAtType.ATUPX,
    CommonAtType.AT4PX,
    CommonAtType.PKDPX,
]
COMMON_AT_MUST_COMPRESS_3 = [CommonAtType.ATUPX, CommonAtType.AT3PX, CommonAtType.PKDPX]
COMMON_AT_MUST_COMPRESS_4 = [CommonAtType.ATUPX, CommonAtType.AT4PX, CommonAtType.PKDPX]
COMMON_AT_PKD = [CommonAtType.PKDPX]

DEBUG = False


class CommonAtHandler(DataHandler[CompressionContainerProtocol]):
    allowed_types = set()
    for t in CommonAtType:
        if t.auto_allowed:
            if t == CommonAtType.ATUPX:
                # For native handler:
                os.environ["SKYTEMPLE_ALLOW_ATUPX"] = "1"
            allowed_types.add(t)

    @classmethod
    def allow(cls, compression_type: CommonAtType):
        if compression_type == CommonAtType.ATUPX:
            # For native handler:
            os.environ["SKYTEMPLE_ALLOW_ATUPX"] = "1"
        cls.allowed_types.add(compression_type)
        if DEBUG:
            print("*** COMMON AT DEBUG: Allowed types =", cls.allowed_types)

    @classmethod
    def disallow(cls, compression_type: CommonAtType):
        try:
            # For native handler:
            cls.allowed_types.remove(compression_type)
            del os.environ["SKYTEMPLE_ALLOW_ATUPX"]
        except KeyError as ke:
            pass  # TODO, add warning
        if DEBUG:
            print("*** COMMON AT DEBUG: Allowed types =", cls.allowed_types)

    @classmethod
    def deserialize(
        cls, data: bytes, **kwargs: OptionalKwargs
    ) -> CompressionContainerProtocol:
        """Load a Common At container into a high-level representation"""
        for t in CommonAtType:
            if t.handler is not None:
                if t.handler.matches(data):
                    if DEBUG:
                        print("*** COMMON AT DEBUG: Opened =", t)
                    return t.handler.deserialize(data, **kwargs)
        raise ValueError(f"The provided data is not an AT container ({read_bytes(data, 0, 5)}).")  # type: ignore

    @classmethod
    def serialize(
        cls, data: CompressionContainerProtocol, **kwargs: OptionalKwargs
    ) -> bytes:
        """Convert the high-level AT representation back into a BitStream."""
        return data.to_bytes()

    @classmethod
    def compress(
        cls, data: bytes, compression_type: Optional[List[CommonAtType]] = None
    ) -> CompressionContainerProtocol:
        """Turn uncompressed data into a new AT container"""
        if compression_type is None:
            compression_type = COMMON_AT_BEST_4
        new_data: Optional[CompressionContainerProtocol] = None
        new_size = -1
        if DEBUG:
            print("*** COMMON AT DEBUG: Compress Start")
        for t in compression_type:
            if t in CommonAtHandler.allowed_types:
                try:
                    cont = t.handler.compress(data)  # pylint: disable=no-member
                    size = len(cont.to_bytes())
                    if DEBUG:
                        print("*** COMMON AT DEBUG: Compress", t, "size", size)
                    if new_data is None or size < new_size:
                        new_data = cont
                        new_size = size
                except:
                    pass
        if DEBUG:
            print("*** COMMON AT DEBUG: Compress End")
        if new_data is None:
            raise ValueError("No useable compression algorithm.")
        return new_data

    @classmethod
    def cont_size(cls, data: bytes, byte_offset=0):
        for t in CommonAtType:
            if t.handler.matches(data, byte_offset):
                return t.handler.cont_size(data, byte_offset)
        raise ValueError("The provided data is not an AT container.")

    @classmethod
    def matches(cls, data: bytes, byte_offset=0):
        """Check if the given data stream is an AT container"""
        for t in CommonAtType:
            if t.handler.matches(data, byte_offset):
                return True
        return False
