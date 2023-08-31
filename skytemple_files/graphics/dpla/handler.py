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

from skytemple_files.common.types.hybrid_data_handler import HybridSir0DataHandler
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.graphics.dpla.protocol import DplaProtocol


class DplaHandler(HybridSir0DataHandler[DplaProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[DplaProtocol]:
        from skytemple_files.graphics.dpla._model import Dpla

        return Dpla

    @classmethod
    def load_native_model(cls) -> Type[DplaProtocol]:
        from skytemple_rust.st_dpla import (
            Dpla,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return Dpla

    @classmethod
    def deserialize_raw(cls, data: bytes, **kwargs: OptionalKwargs) -> DplaProtocol:
        return cls.get_model_cls()(data, 0)

    @classmethod
    def serialize_raw(cls, data: DplaProtocol, **kwargs: OptionalKwargs) -> bytes:
        return data.sir0_serialize_parts()[0]
