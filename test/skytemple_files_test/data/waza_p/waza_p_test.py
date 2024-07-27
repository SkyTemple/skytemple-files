#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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

import json
import typing
from pathlib import Path

from range_typed_integers import u8, u16, u32

from common.types.file_storage import AssetSpec, Asset
from data.md.protocol import PokeType
from data.waza_p._model import WazaP
from skytemple_files.common.impl_cfg import env_use_native
from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.data.waza_p.handler import WazaPHandler, MOVES, LEARNSETS
from skytemple_files.data.waza_p.protocol import (
    WazaPProtocol,
    MoveLearnsetProtocol,
    LevelUpMoveProtocol,
    WazaMoveProtocol,
    WazaMoveRangeSettingsProtocol, WazaMoveCategory,
)
from skytemple_files_test.case import SkyTempleFilesTestCase, romtest, fixpath
from skytemple_files_test.data.waza_p.fixture import (
    eq_move,
    eq_move_list,
    eq_learnset_list,
    FIX_MOVE_RANGE_SETTINGS,
    LevelUpMoveStub,
    eq_level_up_move_list,
)
from skytemple_files_test.data.waza_p.fixture_autogen import (
    FIX_MOVES,
    FIX_MOVES_BYTES,
    FIX_LEARNSETS,
)


class WazaPTestCase(
    SkyTempleFilesTestCase[
        WazaPHandler,
        WazaPProtocol[
            WazaMoveProtocol[WazaMoveRangeSettingsProtocol],
            MoveLearnsetProtocol[LevelUpMoveProtocol],
        ],
    ]
):
    handler = WazaPHandler

    def test_move__init__(self):
        for expected, expected_inp in zip(FIX_MOVES, FIX_MOVES_BYTES):
            subject = self.handler.get_move_model()(expected_inp)

            self.assertTrue(eq_move(expected, subject))

    def test_move_to_bytes(self):
        for expected_inp in FIX_MOVES_BYTES:
            subject = self.handler.get_move_model()(expected_inp)

            self.assertEqual(expected_inp, subject.to_bytes())

    def test_move__eq__(self):
        subject_not_same = self.handler.get_move_model()(FIX_MOVES_BYTES[0])

        for expected in FIX_MOVES_BYTES[1:]:
            subject1 = self.handler.get_move_model()(expected)
            subject2 = self.handler.get_move_model()(expected)

            self.assertEqual(subject1, subject2)
            self.assertEqual(subject2, subject1)
            self.assertNotEqual(subject1, subject_not_same)
            self.assertNotEqual(subject_not_same, subject1)

    def test_move_attrs(self):
        e = self.handler.get_move_model()(FIX_MOVES_BYTES[0])

        e.base_power = u16(1233)
        e.type = u8(2)
        e.category = u8(1)
        e.settings_range.target = 4
        e.settings_range.range = 3
        e.settings_range.condition = 2
        e.settings_range.unused = 1
        e.settings_range_ai.target = 10
        e.settings_range_ai.range = 15
        e.settings_range_ai.condition = 1
        e.settings_range_ai.unused = 11
        e.base_pp = u8(22)
        e.ai_weight = u8(31)
        e.miss_accuracy = u8(44)
        e.accuracy = u8(56)
        e.ai_condition1_chance = u8(123)
        e.number_chained_hits = u8(124)
        e.max_upgrade_level = u8(125)
        e.crit_chance = u8(126)
        e.affected_by_magic_coat = True
        e.is_snatchable = True
        e.uses_mouth = False
        e.ai_frozen_check = True
        e.ignores_taunted = True
        e.range_check_text = u8(3)
        e.move_id = u16(4)
        e.message_id = u8(5)

        self.assertEqual(u16(1233), e.base_power)
        self.assertEqual(u8(2), e.type)
        self.assertEqual(u8(1), e.category)
        self.assertEqual(4, e.settings_range.target)
        self.assertEqual(3, e.settings_range.range)
        self.assertEqual(2, e.settings_range.condition)
        self.assertEqual(1, e.settings_range.unused)
        self.assertEqual(0x1234, int(e.settings_range))
        self.assertEqual(10, e.settings_range_ai.target)
        self.assertEqual(15, e.settings_range_ai.range)
        self.assertEqual(1, e.settings_range_ai.condition)
        self.assertEqual(11, e.settings_range_ai.unused)
        self.assertEqual(0xB1FA, int(e.settings_range_ai))
        self.assertEqual(u8(22), e.base_pp)
        self.assertEqual(u8(31), e.ai_weight)
        self.assertEqual(u8(44), e.miss_accuracy)
        self.assertEqual(u8(56), e.accuracy)
        self.assertEqual(u8(123), e.ai_condition1_chance)
        self.assertEqual(u8(124), e.number_chained_hits)
        self.assertEqual(u8(125), e.max_upgrade_level)
        self.assertEqual(u8(126), e.crit_chance)
        self.assertEqual(True, e.affected_by_magic_coat)
        self.assertEqual(True, e.is_snatchable)
        self.assertEqual(False, e.uses_mouth)
        self.assertEqual(True, e.ai_frozen_check)
        self.assertEqual(True, e.ignores_taunted)
        self.assertEqual(u8(3), e.range_check_text)
        self.assertEqual(u16(4), e.move_id)
        self.assertEqual(u8(5), e.message_id)

    def test_move_range_settings__init__and__int__(self):
        for inp, expected_settings, expected_int in FIX_MOVE_RANGE_SETTINGS:
            subject = self.handler.get_range_settings_model()(inp)

            self.assertEqual(expected_settings["range"], subject.range)
            self.assertEqual(expected_settings["target"], subject.target)
            self.assertEqual(expected_settings["unused"], subject.unused)
            self.assertEqual(expected_settings["condition"], subject.condition)
            self.assertEqual(expected_int, int(subject))

    def test_move_range_settings__eq__(self):
        subject_not_same = self.handler.get_range_settings_model()(FIX_MOVE_RANGE_SETTINGS[0][0])
        for inp, _, _ in FIX_MOVE_RANGE_SETTINGS[1:]:
            subject1 = self.handler.get_range_settings_model()(inp)
            subject2 = self.handler.get_range_settings_model()(inp)

            self.assertEqual(subject1, subject2)
            self.assertEqual(subject2, subject1)
            self.assertNotEqual(subject1, subject_not_same)
            self.assertNotEqual(subject_not_same, subject1)

    def test_move_range_settings_attrs(self):
        subject = self.handler.get_range_settings_model()(bytes([0x00, 0x00]))

        subject.range = 3
        subject.condition = 2
        subject.unused = 1
        subject.target = 4

        self.assertEqual(3, subject.range)
        self.assertEqual(2, subject.condition)
        self.assertEqual(1, subject.unused)
        self.assertEqual(4, subject.target)
        self.assertEqual(0x1234, int(subject))

    def test_move_learnset__eq__(self):
        waza = self._load_main_fixture(self._fix_path())
        waza2 = self._load_main_fixture(self._fix_path())
        subject_not_same = waza.learnsets[0]
        for subject1, subject2 in zip(waza.learnsets[1:], waza2.learnsets[1:]):
            self.assertEqual(list(subject1.level_up_moves), list(subject2.level_up_moves))
            self.assertEqual(subject1.level_up_moves, subject2.level_up_moves)
            self.assertEqual(list(subject1.tm_hm_moves), list(subject2.tm_hm_moves))
            self.assertEqual(subject1.tm_hm_moves, subject2.tm_hm_moves)
            self.assertEqual(list(subject1.egg_moves), list(subject2.egg_moves))
            self.assertEqual(subject1.egg_moves, subject2.egg_moves)
            self.assertEqual(subject1, subject2)
            self.assertEqual(subject2, subject1)
            self.assertNotEqual(subject1, subject_not_same)
            self.assertNotEqual(subject_not_same, subject1)

    def test_move_learnset_attrs(self):
        subject = self._load_main_fixture(self._fix_path()).learnsets[0]

        self.assertTrue(eq_level_up_move_list(FIX_LEARNSETS[0].level_up_moves, subject.level_up_moves))
        self.assertEqual(FIX_LEARNSETS[0].tm_hm_moves, list(subject.tm_hm_moves))
        self.assertEqual(FIX_LEARNSETS[0].egg_moves, list(subject.egg_moves))

        subject.level_up_moves.pop()
        self.assertTrue(eq_level_up_move_list(FIX_LEARNSETS[0].level_up_moves[:-1], subject.level_up_moves))
        cloned = [LevelUpMoveStub.stub_new(x.level_id, x.move_id) for x in FIX_LEARNSETS[0].level_up_moves[:-1]]
        subject.level_up_moves[0].level_id = 1234
        subject.level_up_moves[0].move_id = 5678
        cloned[0].level_id = 1234
        cloned[0].move_id = 5678
        self.assertTrue(eq_level_up_move_list(cloned, subject.level_up_moves))

        subject.tm_hm_moves.pop()
        self.assertEqual(FIX_LEARNSETS[0].tm_hm_moves[:-1], list(subject.tm_hm_moves))
        cloned = list(FIX_LEARNSETS[0].tm_hm_moves[:-1])
        subject.tm_hm_moves[0] = u32(1234)
        cloned[0] = u32(1234)
        self.assertEqual(cloned, list(subject.tm_hm_moves))

        subject.egg_moves.pop()
        self.assertEqual(FIX_LEARNSETS[0].egg_moves[:-1], list(subject.egg_moves))
        cloned = list(FIX_LEARNSETS[0].egg_moves[:-1])
        subject.egg_moves[0] = u32(1234)
        cloned[0] = u32(1234)
        self.assertEqual(cloned, list(subject.egg_moves))

    def test_level_up_move__eq__(self):
        waza = self._load_main_fixture(self._fix_path())
        waza2 = self._load_main_fixture(self._fix_path())
        subject_not_same = waza.learnsets[0].level_up_moves[0]
        for subject1, subject2 in zip(waza.learnsets[0].level_up_moves[1:], waza2.learnsets[0].level_up_moves[1:]):
            self.assertEqual(subject1, subject2)
            self.assertEqual(subject2, subject1)
            self.assertNotEqual(subject1, subject_not_same)
            self.assertNotEqual(subject_not_same, subject1)

    def test_level_up_move_attrs(self):
        subject = self._load_main_fixture(self._fix_path()).learnsets[0].level_up_moves

        self.assertTrue(eq_level_up_move_list(FIX_LEARNSETS[0].level_up_moves, subject))

        subject.pop()
        self.assertTrue(eq_level_up_move_list(FIX_LEARNSETS[0].level_up_moves[:-1], subject))
        cloned = [LevelUpMoveStub.stub_new(x.level_id, x.move_id) for x in FIX_LEARNSETS[0].level_up_moves[:-1]]
        subject[0].level_id = 1234
        subject[0].move_id = 5678
        cloned[0].level_id = 1234
        cloned[0].move_id = 5678
        self.assertTrue(eq_level_up_move_list(cloned, subject))

    def test_wazap__init__(self):
        with open(self._fix_path(), "rb") as f:
            sir0 = Sir0Handler.load_python_model().from_bin(f.read())
        actual: WazaPProtocol = self.handler.get_model_cls()(sir0.content, sir0.data_pointer)

        self.assertTrue(eq_move_list(FIX_MOVES, actual.moves))
        self.assertTrue(eq_learnset_list(FIX_LEARNSETS, actual.learnsets))

    def test_wazap__eq__(self):
        subject_not_same = self._load_main_fixture(self._fix_path())
        subject_not_same.moves = []
        subject1 = self._load_main_fixture(self._fix_path())
        subject2 = self._load_main_fixture(self._fix_path())

        self.assertEqual(subject1, subject2)
        self.assertEqual(subject2, subject1)
        self.assertNotEqual(subject1, subject_not_same)
        self.assertNotEqual(subject_not_same, subject1)

    def test_wazap_sir0_serialize_parts(self):
        first = self._load_main_fixture(self._fix_path())

        # Serialize the parts, make sure the offsets make sense and try to re-construct.
        data, offsets, header_pointer = first.sir0_serialize_parts()
        # TODO: How to check the offsets?

        second = self.handler.get_model_cls().sir0_unwrap(data, header_pointer)

        self.assertEqual(first, second)

    def test_wazap_sir0_unwrap(self):
        with open(self._fix_path(), "rb") as f:
            sir0 = Sir0Handler.load_python_model().from_bin(f.read())
        actual: WazaPProtocol = self.handler.get_model_cls().sir0_unwrap(  # type: ignore
            sir0.content, sir0.data_pointer
        )

        self.assertTrue(eq_move_list(FIX_MOVES, actual.moves))
        self.assertTrue(eq_learnset_list(FIX_LEARNSETS, actual.learnsets))

    def test_wazap_load_via_handler(self):
        actual = self._load_main_fixture(self._fix_path())

        self.assertTrue(eq_move_list(FIX_MOVES, actual.moves))
        self.assertTrue(eq_learnset_list(FIX_LEARNSETS, actual.learnsets))

    def test_wazap_save_via_handler(self):
        loaded = self._load_main_fixture(self._fix_path())
        actual = self._save_and_reload_main_fixture(loaded)

        self.assertTrue(eq_move_list(FIX_MOVES, actual.moves))
        self.assertTrue(eq_learnset_list(FIX_LEARNSETS, actual.learnsets))

    def test_wazap_attrs(self):
        actual = self._load_main_fixture(self._fix_path())

        self.assertTrue(eq_move_list(FIX_MOVES, actual.moves))
        self.assertTrue(eq_learnset_list(FIX_LEARNSETS, actual.learnsets))

        copy_moves = list(actual.moves)
        copy_moves.pop()
        actual.moves = list(copy_moves)
        copy_learnsets = list(actual.learnsets)
        copy_learnsets.pop()
        actual.learnsets = list(copy_learnsets)

        self.assertTrue(eq_move_list(copy_moves, actual.moves))
        self.assertTrue(eq_learnset_list(copy_learnsets, actual.learnsets))
        self.assertFalse(eq_move_list(FIX_MOVES, actual.moves))
        self.assertFalse(eq_learnset_list(FIX_LEARNSETS, actual.learnsets))

        actual.moves.pop()
        actual.learnsets.pop()

        self.assertTrue(eq_move_list(copy_moves[:-1], actual.moves))
        self.assertTrue(eq_learnset_list(copy_learnsets[:-1], actual.learnsets))
        self.assertFalse(eq_move_list(copy_moves, actual.moves))
        self.assertFalse(eq_learnset_list(copy_learnsets, actual.learnsets))

    def test_cross_native_implementation(self):
        """Tests the native implementation against the Python implementation."""
        if not env_use_native():
            self.skipTest("This test is only enabled when the native implementations are tested.")
            return
        with open(self._fix_path(), "rb") as f:
            sir0 = Sir0Handler.deserialize(f.read())
        loaded_py = self.handler.load_python_model().sir0_unwrap(sir0.content, sir0.data_pointer)
        loaded_rs = self.handler.load_native_model().sir0_unwrap(sir0.content, sir0.data_pointer)

        loaded_py_sir0 = Sir0Handler.wrap_obj(loaded_py)
        loaded_rs_sir0 = Sir0Handler.wrap_obj(loaded_rs)
        loaded_py_reloaded_with_rs: WazaPProtocol = self.handler.load_native_model().sir0_unwrap(  # type: ignore
            loaded_py_sir0.content, loaded_py_sir0.data_pointer
        )
        loaded_rs_reloaded_with_py: WazaPProtocol = self.handler.load_python_model().sir0_unwrap(  # type: ignore
            loaded_rs_sir0.content, loaded_rs_sir0.data_pointer
        )

        self.assertTrue(eq_move_list(FIX_MOVES, loaded_py_reloaded_with_rs.moves))
        self.assertTrue(eq_learnset_list(FIX_LEARNSETS, loaded_py_reloaded_with_rs.learnsets))

        self.assertTrue(eq_move_list(FIX_MOVES, loaded_rs_reloaded_with_py.moves))
        self.assertTrue(eq_learnset_list(FIX_LEARNSETS, loaded_rs_reloaded_with_py.learnsets))

    def test_asset_specs_relevant_file(self):
        file_path = Path("BALANCE", "waza_p.bin")
        specs = self.handler.asset_specs(file_path)
        self.assertEqual(2, len(specs))
        self.assertEqual(Path("pokemon", "moves.json"), specs[0].path)
        self.assertEqual(file_path, specs[0].rom_path)
        self.assertEqual(MOVES, specs[0].category)
        self.assertEqual(Path("pokemon", "learnsets.json"), specs[1].path)
        self.assertEqual(file_path, specs[1].rom_path)
        self.assertEqual(LEARNSETS, specs[1].category)

    def test_serialize_assets_moves(self):
        waza = self._load_main_fixture(self._fix_path())
        asset = self.handler.serialize_asset(AssetSpec(Path(), Path(), MOVES), Path(), waza)

        asset_data = json.loads(asset.data)
        self.assertEqual(559, len(asset_data))

        move_data = asset_data[0]
        self.assertEqual(25484, move_data["base_power"])
        self.assertEqual("STEEL", move_data["type"])
        self.assertEqual("PHYSICAL", move_data["category"])
        self.assertEqual(14, move_data["settings_range"]["target"])
        self.assertEqual(6, move_data["settings_range"]["range"])
        self.assertEqual(5, move_data["settings_range"]["condition"])
        self.assertEqual(0, move_data["settings_range"]["unused"])
        self.assertEqual(8, move_data["settings_range_ai"]["target"])
        self.assertEqual(14, move_data["settings_range_ai"]["range"])
        self.assertEqual(3, move_data["settings_range_ai"]["condition"])
        self.assertEqual(13, move_data["settings_range_ai"]["unused"])
        self.assertEqual(233, move_data["base_pp"])
        self.assertEqual(129, move_data["ai_weight"])
        self.assertEqual(44, move_data["miss_accuracy"])
        self.assertEqual(253, move_data["accuracy"])
        self.assertEqual(109, move_data["ai_condition1_chance"])
        self.assertEqual(141, move_data["number_chained_hits"])
        self.assertEqual(140, move_data["max_upgrade_level"])
        self.assertEqual(85, move_data["crit_chance"])
        self.assertFalse(move_data["affected_by_magic_coat"])
        self.assertFalse(move_data["is_snatchable"])
        self.assertTrue(move_data["uses_mouth"])
        self.assertTrue(move_data["ai_frozen_check"])
        self.assertTrue(move_data["ignores_taunted"])
        self.assertEqual(129, move_data["range_check_text"])
        self.assertEqual(8899, move_data["move_id"])
        self.assertEqual(179, move_data["message_id"])

    def test_deserialize_assets_moves(self):
        move_json = {
            "base_power": 25484,
            "type": "STEEL",
            "category": "PHYSICAL",
            "settings_range": {
                "target": 14,
                "range": 6,
                "condition": 5,
                "unused": 0
            },
            "settings_range_ai": {
                "target": 8,
                "range": 14,
                "condition": 3,
                "unused": 13
            },
            "base_pp": 233,
            "ai_weight": 129,
            "miss_accuracy": 44,
            "accuracy": 253,
            "ai_condition1_chance": 109,
            "number_chained_hits": 141,
            "max_upgrade_level": 140,
            "crit_chance": 85,
            "affected_by_magic_coat": False,
            "is_snatchable": False,
            "uses_mouth": True,
            "ai_frozen_check": True,
            "ignores_taunted": True,
            "range_check_text": 129,
            "move_id": 8899,
            "message_id": 179
        }

        asset = Asset(AssetSpec(Path(), Path(), MOVES), None, None, None, None, bytes(json.dumps([move_json]), "utf-8"))
        waza = self.handler.deserialize_from_assets([asset])
        self.assertEqual(1, len(waza.moves))

        move = waza.moves[0]
        self.assertEqual(25484, move.base_power)
        self.assertEqual(PokeType.STEEL, move.type)
        self.assertEqual(WazaMoveCategory.PHYSICAL, move.category)
        self.assertEqual(14, move.settings_range.target)
        self.assertEqual(6, move.settings_range.range)
        self.assertEqual(5, move.settings_range.condition)
        self.assertEqual(0, move.settings_range.unused)
        self.assertEqual(8, move.settings_range_ai.target)
        self.assertEqual(14, move.settings_range_ai.range)
        self.assertEqual(3, move.settings_range_ai.condition)
        self.assertEqual(13, move.settings_range_ai.unused)
        self.assertEqual(233, move.base_pp)
        self.assertEqual(129, move.ai_weight)
        self.assertEqual(44, move.miss_accuracy)
        self.assertEqual(253, move.accuracy)
        self.assertEqual(109, move.ai_condition1_chance)
        self.assertEqual(141, move.number_chained_hits)
        self.assertEqual(140, move.max_upgrade_level)
        self.assertEqual(85, move.crit_chance)
        self.assertFalse(move.affected_by_magic_coat)
        self.assertFalse(move.is_snatchable)
        self.assertTrue(move.uses_mouth)
        self.assertTrue(move.ai_frozen_check)
        self.assertTrue(move.ignores_taunted)
        self.assertEqual(129, move.range_check_text)
        self.assertEqual(8899, move.move_id)
        self.assertEqual(179, move.message_id)


    @romtest(file_names=["waza_p.bin", "waza_p2.bin"], path="BALANCE/")
    def test_using_rom(self, _, file):
        before = self.handler.deserialize(file)
        after = self._save_and_reload_main_fixture(before)

        self.assertTrue(eq_move_list(before.moves, after.moves))
        self.assertTrue(eq_learnset_list(before.learnsets, after.learnsets))

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path(cls):
        return "fixtures", "fixture.bin"
