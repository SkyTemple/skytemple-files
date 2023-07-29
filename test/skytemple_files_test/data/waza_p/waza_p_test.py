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

import typing
from typing import Optional

from range_typed_integers import u8, u16, u32

from skytemple_files.common.impl_cfg import env_use_native
from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.data.waza_p.handler import WazaPHandler
from skytemple_files.data.waza_p.protocol import (
    WazaPProtocol,
    MoveLearnsetProtocol,
    LevelUpMoveProtocol,
    WazaMoveProtocol,
    WazaMoveRangeSettingsProtocol
)
from skytemple_files_test.case import SkyTempleFilesTestCase, romtest, fixpath
from skytemple_files_test.data.waza_p.fixture import eq_move, eq_move_list, eq_learnset, eq_learnset_list, \
    FIX_MOVE_RANGE_SETTINGS, WazaLearnsetStub, LevelUpMoveStub, eq_level_up_move_list
from skytemple_files_test.data.waza_p.fixture_autogen import FIX_MOVES, FIX_MOVES_BYTES, FIX_LEARNSETS


class WazaPTestCase(
    SkyTempleFilesTestCase[WazaPHandler, WazaPProtocol[
        WazaMoveProtocol[WazaMoveRangeSettingsProtocol],
        MoveLearnsetProtocol[LevelUpMoveProtocol]
    ]]
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

            self.assertEqual(expected_settings['range'], subject.range)
            self.assertEqual(expected_settings['target'], subject.target)
            self.assertEqual(expected_settings['unused'], subject.unused)
            self.assertEqual(expected_settings['condition'], subject.condition)
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
        actual: WazaPProtocol = self.handler.get_model_cls()(
            sir0.content, sir0.data_pointer
        )

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

        second = self.handler.get_model_cls().sir0_unwrap(
            data, header_pointer
        )

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
            self.skipTest(
                "This test is only enabled when the native implementations are tested."
            )
            return
        with open(self._fix_path(), 'rb') as f:
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
