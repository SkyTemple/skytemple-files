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

from typing import Type

from skytemple_files.common.util import OptionalKwargs
from skytemple_files.compression_container.base_handler import (
    CompressionContainerHandler,
)
from skytemple_files.compression_container.protocol import CompressionContainerProtocol


class At4pnHandler(CompressionContainerHandler):
    @classmethod
    def magic_word(cls) -> bytes:
        return b"AT4PN"

    @classmethod
    def load_python_model(cls) -> Type[CompressionContainerProtocol]:
        from skytemple_files.compression_container.at4pn.model import At4pn

        return At4pn

    @classmethod
    def load_native_model(cls) -> Type[CompressionContainerProtocol]:
        from skytemple_rust.st_at4pn import (
            At4pn,
        )

        return At4pn

    @classmethod
    def deserialize(
        cls, data: bytes, **kwargs: OptionalKwargs
    ) -> CompressionContainerProtocol:
        """Load a container into a high-level representation"""
        if not cls.matches(data):
            raise ValueError(
                f"The provided data is not a {str(cls.magic_word(), 'ascii')} container."
            )
        return cls.get_model_cls()(data, False)

    @classmethod
    def new(cls, data: bytes) -> CompressionContainerProtocol:
        """Turn uncompressed data into a new AT4PN container"""
        return cls.get_model_cls()(data, True)
