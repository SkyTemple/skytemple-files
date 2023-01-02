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

from skytemple_files.common.types.hybrid_data_handler import HybridDataHandler
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.dungeon_data.mappa_bin.protocol import MappaItemListProtocol


class ItemListHandler(HybridDataHandler[MappaItemListProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[MappaItemListProtocol]:
        from skytemple_files.dungeon_data.mappa_bin._python_impl.item_list import (
            MappaItemList,
        )

        return MappaItemList

    @classmethod
    def load_native_model(cls) -> Type[MappaItemListProtocol]:
        from skytemple_rust.st_mappa_bin import (
            MappaItemList,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return MappaItemList

    @classmethod
    def load_python_writer(cls):  # type: ignore
        raise NotImplementedError("Not applicable.")

    @classmethod
    def load_native_writer(cls):  # type: ignore
        raise NotImplementedError("Not applicable.")

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> MappaItemListProtocol:  # type: ignore
        return cls.get_model_cls().from_bytes(data, 0)

    @classmethod
    def serialize(cls, data: MappaItemListProtocol, **kwargs: OptionalKwargs) -> bytes:
        return data.to_bytes()
