#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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

from pathlib import Path
from typing import TYPE_CHECKING, Sequence
import json

from range_typed_integers import u32

from skytemple_files.common.impl_cfg import get_implementation_type, ImplementationType
from skytemple_files.common.ppmdu_config.data import Pmd2StringBlock
from skytemple_files.common.types.file_storage import AssetSpec, Asset
from skytemple_files.common.types.hybrid_data_handler import (
    WriterProtocol,
    HybridSir0DataHandler,
)
from skytemple_files.common.util import OptionalKwargs, serialize_enum_or_default, deserialize_enum_or_default
from skytemple_files.data.md.protocol import PokeType
from skytemple_files.data.str.handler import StrHandler
from skytemple_files.data.str.model import Str
from skytemple_files.data.waza_p.protocol import (
    WazaPProtocol,
    LevelUpMoveProtocol,
    WazaMoveProtocol,
    WazaMoveRangeSettingsProtocol,
    MoveLearnsetProtocol,
    WazaMoveCategory,
)


if TYPE_CHECKING:
    from skytemple_files.data.waza_p._model import WazaP as PyWazaP
    from skytemple_rust.st_waza_p import WazaP as NativeWazaP


MOVES = "moves"
LEARNSETS = "learnsets"


class WazaPHandler(HybridSir0DataHandler[WazaPProtocol]):
    @classmethod
    def load_python_model(cls) -> type[WazaPProtocol]:
        from skytemple_files.data.waza_p._model import WazaP

        return WazaP

    @classmethod
    def load_native_model(cls) -> type[WazaPProtocol]:
        from skytemple_rust.st_waza_p import (
            WazaP,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return WazaP

    @classmethod
    def load_python_writer(cls) -> type[WriterProtocol[PyWazaP]]:  # type: ignore
        from skytemple_files.data.waza_p._writer import WazaPWriter

        return WazaPWriter

    @classmethod
    def load_native_writer(cls) -> type[WriterProtocol[NativeWazaP]]:  # type: ignore
        from skytemple_rust.st_waza_p import (
            WazaPWriter,
        )  # pylint: disable=no-name-in-module,no-member,import-error

        return WazaPWriter

    @classmethod
    def get_level_up_model(cls) -> type[LevelUpMoveProtocol]:
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
    def get_move_model(cls) -> type[WazaMoveProtocol]:
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
    def get_range_settings_model(cls) -> type[WazaMoveRangeSettingsProtocol]:
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
    def get_learnset_model(cls) -> type[MoveLearnsetProtocol]:
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

    @classmethod
    def asset_specs(cls, path_to_rom_obj: Path) -> Sequence[AssetSpec]:
        if path_to_rom_obj == Path("BALANCE", "waza_p.bin"):
            return [
                AssetSpec(Path("pokemon", "moves.json"), path_to_rom_obj, MOVES),
                AssetSpec(Path("pokemon", "learnsets.json"), path_to_rom_obj, LEARNSETS),
            ]
        return []

    @classmethod
    def serialize_asset(
        cls, spec: AssetSpec, path_to_rom_obj: Path, data: WazaPProtocol, **kwargs: OptionalKwargs
    ) -> Asset:
        if spec.category == MOVES:
            moves_list = []
            move: WazaMoveProtocol

            strings, string_blocks = cls._get_strings_from_rom(["Move Names"], **kwargs)

            for move in data.moves:
                serialized_move = {
                    "base_power": move.base_power,
                    "type": serialize_enum_or_default(PokeType, move.type),
                    "category": serialize_enum_or_default(WazaMoveCategory, move.category),
                    "settings_range": cls._serialize_move_range_settings(move.settings_range),
                    "settings_range_ai": cls._serialize_move_range_settings(move.settings_range_ai),
                    "base_pp": move.base_pp,
                    "ai_weight": move.ai_weight,
                    "miss_accuracy": move.miss_accuracy,
                    "accuracy": move.accuracy,
                    "ai_condition1_chance": move.ai_condition1_chance,
                    "number_chained_hits": move.number_chained_hits,
                    "max_upgrade_level": move.max_upgrade_level,
                    "crit_chance": move.crit_chance,
                    "affected_by_magic_coat": move.affected_by_magic_coat,
                    "is_snatchable": move.is_snatchable,
                    "uses_mouth": move.uses_mouth,
                    "ai_frozen_check": move.ai_frozen_check,
                    "ignores_taunted": move.ignores_taunted,
                    "range_check_text": move.range_check_text,
                    "move_id": move.move_id,
                    "message_id": move.message_id,
                }
                if strings is not None:
                    move_name_index = string_blocks["Move Names"].begin + move.move_id
                    if move_name_index <= string_blocks["Move Names"].end:
                        serialized_move["name"] = strings.strings[move_name_index]
                moves_list.append(serialized_move)

            return Asset(spec, None, None, None, None, bytes(json.dumps(moves_list, indent=4), "utf-8"))
        elif spec.category == LEARNSETS:
            learnsets = []
            learnset: MoveLearnsetProtocol

            strings, string_blocks = cls._get_strings_from_rom(["Move Names", "Pokemon Names"], **kwargs)

            def get_move_value(move_id: u32) -> str | u32:
                if strings is None:
                    return move_id
                else:
                    move_name_idx = string_blocks["Move Names"].begin + move_id
                    if move_name_idx <= string_blocks["Move Names"].end:
                        return strings.strings[move_name_idx]

            for i, learnset in enumerate(data.learnsets):
                serialized_learnset = {
                    "level_up_moves": [
                        {
                            "move_id": get_move_value(level_up_move.move_id),
                            "level_id": level_up_move.level_id,
                        }
                        for level_up_move in learnset.level_up_moves
                    ],
                    "tm_hm_moves": [get_move_value(move_id) for move_id in learnset.tm_hm_moves],
                    "egg_moves": [get_move_value(move_id) for move_id in learnset.egg_moves],
                }

                if strings is not None:
                    serialized_learnset["pokemon_name"] = strings.strings[string_blocks["Pokemon Names"].begin + i]

                learnsets.append(serialized_learnset)

            return Asset(spec, None, None, None, None, bytes(json.dumps(learnsets, indent=4), "utf-8"))
        else:
            raise ValueError(f"Attempted to serialize unknown category {spec.category} from waza_p.")

    @classmethod
    def deserialize_from_assets(
        cls,
        assets: Sequence[Asset],
        **kwargs: OptionalKwargs,
    ) -> WazaPProtocol:
        protocol: WazaPProtocol = cls.get_model_cls()(bytes(), 0)

        assets_by_category = {asset.spec.category: asset for asset in assets}

        # Keep track of move names/IDs to deserialize learnsets later.
        move_names_to_ids: dict[str, u32] = {}
        if MOVES in assets_by_category:
            move_asset = assets_by_category[MOVES]
            moves = json.loads(move_asset.data)
            protocol.moves = []
            for move_json in moves:
                move = cls.get_move_model()(bytes())
                protocol.moves.append(move)

                move.base_power = move_json["base_power"]
                move.type = deserialize_enum_or_default(PokeType, move_json["type"])
                move.category = deserialize_enum_or_default(WazaMoveCategory, move_json["category"])
                move.settings_range = cls.get_range_settings_model()(bytes())
                move.settings_range = cls._deserialize_move_range_settings(move_json["settings_range"])
                move.settings_range_ai = cls._deserialize_move_range_settings(move_json["settings_range_ai"])
                move.base_pp = move_json["base_pp"]
                move.ai_weight = move_json["ai_weight"]
                move.miss_accuracy = move_json["miss_accuracy"]
                move.accuracy = move_json["accuracy"]
                move.ai_condition1_chance = move_json["ai_condition1_chance"]
                move.number_chained_hits = move_json["number_chained_hits"]
                move.max_upgrade_level = move_json["max_upgrade_level"]
                move.crit_chance = move_json["crit_chance"]
                move.affected_by_magic_coat = move_json["affected_by_magic_coat"]
                move.is_snatchable = move_json["is_snatchable"]
                move.uses_mouth = move_json["uses_mouth"]
                move.ai_frozen_check = move_json["ai_frozen_check"]
                move.ignores_taunted = move_json["ignores_taunted"]
                move.range_check_text = move_json["range_check_text"]
                move.move_id = move_json["move_id"]
                move.message_id = move_json["message_id"]

                if "name" in move_json:
                    move_names_to_ids[move_json["name"]] = move_json["move_id"]

        if LEARNSETS in assets_by_category:
            learnset_asset = assets_by_category[LEARNSETS]
            learnsets = json.loads(learnset_asset.data)
            protocol.learnsets = []

            def get_move_id(move_value: str | u32) -> u32:
                if isinstance(move_value, str):
                    if move_value in move_names_to_ids:
                        return move_names_to_ids[move_value]
                    else:
                        raise KeyError(f"Invalid move name {move_value} in learnset.")

                return move_value

            for learnset_json in learnsets:
                learnset = cls.get_learnset_model()(
                    [
                        cls.get_level_up_model()(get_move_id(level_up["move_id"]), level_up["level_id"])
                        for level_up in learnset_json["level_up_moves"]
                    ],
                    [get_move_id(move_value) for move_value in learnset_json["tm_hm_moves"]],
                    [get_move_id(move_value) for move_value in learnset_json["egg_moves"]],
                )
                protocol.learnsets.append(learnset)

        return protocol

    @staticmethod
    def _serialize_move_range_settings(settings: WazaMoveRangeSettingsProtocol) -> dict:
        return {
            "target": settings.target,
            "range": settings.range,
            "condition": settings.condition,
            "unused": settings.unused,
        }

    @classmethod
    def _deserialize_move_range_settings(cls, settings_json: dict) -> WazaMoveRangeSettingsProtocol:
        settings = cls.get_range_settings_model()(bytes())
        settings.target = settings_json["target"]
        settings.range = settings_json["range"]
        settings.condition = settings_json["condition"]
        settings.unused = settings_json["unused"]
        return settings

    @staticmethod
    def _get_strings_from_rom(
        block_names: list[str], **kwargs: OptionalKwargs
    ) -> tuple[Str | None, dict[str, Pmd2StringBlock] | None]:
        """
        Fetches blocks of strings from the ROM if it is specified in kwargs.
        """
        if "rom_project" in kwargs:
            rom_project = kwargs["rom_project"]
            # Default to English strings (NA/EU). Use Japanese strings if this is the JP ROM.
            try:
                strings_file = rom_project.rom.getFileByName("MESSAGE/text_e.str")
            except ValueError:
                strings_file = rom_project.rom.getFileByName("MESSAGE/text_j.str")
            strings = StrHandler.deserialize(strings_file)
            string_blocks = {
                block_name: rom_project.static_data.string_index_data.string_blocks[block_name]
                for block_name in block_names
            }
            return strings, string_blocks
        return None, None
