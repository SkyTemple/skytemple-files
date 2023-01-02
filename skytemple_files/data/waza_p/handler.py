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
from skytemple_files.data.waza_p.protocol import (
    WazaPProtocol,
    LevelUpMoveProtocol,
    WazaMoveProtocol,
    WazaMoveRangeSettingsProtocol,
    MoveLearnsetProtocol,
)


class WazaPHandler(HybridSir0DataHandler[WazaPProtocol]):
    @classmethod
    def load_python_model(cls) -> Type[WazaPProtocol]:
        from skytemple_files.data.waza_p._model import WazaP

        return WazaP

    @classmethod
    def load_native_model(cls) -> Type[WazaPProtocol]:
        from skytemple_rust.st_waza_p import (
            WazaP,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return WazaP

    @classmethod
    def load_python_writer(cls) -> Type[WriterProtocol["PyWazaP"]]:  # type: ignore
        from skytemple_files.data.waza_p._writer import WazaPWriter

        return WazaPWriter

    @classmethod
    def load_native_writer(cls) -> Type[WriterProtocol["NativeWazaP"]]:  # type: ignore
        from skytemple_rust.st_waza_p import (
            WazaPWriter,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return WazaPWriter

    @classmethod
    def get_level_up_model(cls) -> Type[LevelUpMoveProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_waza_p import (
                LevelUpMove as LevelUpMoveNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return LevelUpMoveNative
        from skytemple_files.data.waza_p._model import (
            LevelUpMove,
        )

        return LevelUpMove

    @classmethod
    def get_move_model(cls) -> Type[WazaMoveProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_waza_p import (
                WazaMove as WazaMoveNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return WazaMoveNative
        from skytemple_files.data.waza_p._model import (
            WazaMove,
        )

        return WazaMove

    @classmethod
    def get_range_settings_model(cls) -> Type[WazaMoveRangeSettingsProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_waza_p import (
                WazaMoveRangeSettings as WazaMoveRangeSettingsNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return WazaMoveRangeSettingsNative
        from skytemple_files.data.waza_p._model import (
            WazaMoveRangeSettings,
        )

        return WazaMoveRangeSettings

    @classmethod
    def get_learnset_model(cls) -> Type[MoveLearnsetProtocol]:
        if get_implementation_type() == ImplementationType.NATIVE:
            from skytemple_rust.st_waza_p import (
                MoveLearnset as MoveLearnsetNative,
            )  # pylint: disable=no-name-in-module,no-member,import-error

            return MoveLearnsetNative
        from skytemple_files.data.waza_p._model import (
            MoveLearnset,
        )

        return MoveLearnset

    @classmethod
    def deserialize_raw(cls, data: bytes, **kwargs: OptionalKwargs) -> WazaPProtocol:
        return cls.get_model_cls()(data, 0)

    @classmethod
    def serialize_raw(cls, data: WazaPProtocol, **kwargs: OptionalKwargs) -> bytes:
        return data.sir0_serialize_parts()[0]
