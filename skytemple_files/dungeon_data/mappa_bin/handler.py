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

from skytemple_files.common.impl_cfg import get_implementation_type, ImplementationType
from skytemple_files.common.types.hybrid_data_handler import (
    WriterProtocol,
    HybridSir0DataHandler,
)
from skytemple_files.common.util import OptionalKwargs
from skytemple_files.dungeon_data.mappa_bin.protocol import (
    MappaBinProtocol,
    MappaFloorProtocol,
    MappaFloorLayoutProtocol,
    MappaMonsterProtocol,
    MappaItemListProtocol,
    MappaTrapListProtocol,
    MappaFloorTerrainSettingsProtocol,
)


class MappaBinHandler(HybridSir0DataHandler[MappaBinProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[MappaBinProtocol]:
        from skytemple_files.dungeon_data.mappa_bin._python_impl.model import MappaBin

        return MappaBin

    @classmethod
    def load_native_model(cls) -> Type[MappaBinProtocol]:
        from skytemple_rust.st_mappa_bin import (
            MappaBin,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return MappaBin

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol["PyMappaBin"]]:  # type: ignore
        from skytemple_files.dungeon_data.mappa_bin._python_impl.writer import (
            MappaBinWriter,
        )

        return MappaBinWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol["NativeMappaBin"]]:  # type: ignore
        from skytemple_rust.st_mappa_bin import (
            MappaBinWriter,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return MappaBinWriter

    @classmethod
    def get_floor_model(cls) -> Type[MappaFloorProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_mappa_bin import (
                MappaFloor as MappaFloorNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return MappaFloorNative
        from skytemple_files.dungeon_data.mappa_bin._python_impl.floor import MappaFloor

        return MappaFloor

    @classmethod
    def get_floor_layout_model(cls) -> Type[MappaFloorLayoutProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_mappa_bin import (
                MappaFloorLayout as MappaFloorLayoutNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return MappaFloorLayoutNative
        from skytemple_files.dungeon_data.mappa_bin._python_impl.floor_layout import (
            MappaFloorLayout,
        )

        return MappaFloorLayout

    @classmethod
    def get_monster_model(cls) -> Type[MappaMonsterProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_mappa_bin import (
                MappaMonster as MappaMonsterNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return MappaMonsterNative
        from skytemple_files.dungeon_data.mappa_bin._python_impl.monster import (
            MappaMonster,
        )

        return MappaMonster

    @classmethod
    def get_item_list_model(cls) -> Type[MappaItemListProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_mappa_bin import (
                MappaItemList as MappaItemListNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return MappaItemListNative
        from skytemple_files.dungeon_data.mappa_bin._python_impl.item_list import (
            MappaItemList,
        )

        return MappaItemList

    @classmethod
    def get_trap_list_model(cls) -> Type[MappaTrapListProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_mappa_bin import (
                MappaTrapList as MappaTrapListNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return MappaTrapListNative
        from skytemple_files.dungeon_data.mappa_bin._python_impl.trap_list import (
            MappaTrapList,
        )

        return MappaTrapList

    @classmethod
    def get_terrain_settings_model(cls) -> Type[MappaFloorTerrainSettingsProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_mappa_bin import (
                MappaFloorTerrainSettings as MappaFloorTerrainSettingsNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return MappaFloorTerrainSettingsNative
        from skytemple_files.dungeon_data.mappa_bin._python_impl.floor_layout import (
            MappaFloorTerrainSettings,
        )

        return MappaFloorTerrainSettings

    @classmethod
    def deserialize_raw(cls, data: bytes, **kwargs: OptionalKwargs) -> MappaBinProtocol:
        raise NotImplementedError("Not implemented for Mappa.")

    @classmethod
    def serialize_raw(cls, data: MappaBinProtocol, **kwargs: OptionalKwargs) -> bytes:
        return data.sir0_serialize_parts()[0]
