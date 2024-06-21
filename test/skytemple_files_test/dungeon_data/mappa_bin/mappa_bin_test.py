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
from typing import no_type_check, Callable, Optional, TypeVar, List, Tuple

from range_typed_integers import i8, u8, u16, i16

from skytemple_files.common.impl_cfg import env_use_native
from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler
from skytemple_files.dungeon_data.mappa_bin.protocol import (
    MappaBinProtocol,
    MappaFloorLayoutProtocol,
    MappaMonsterProtocol,
    MappaTrapListProtocol,
    MappaItemListProtocol,
)
from skytemple_files_test.case import SkyTempleFilesTestCase, fixpath, romtest
from skytemple_files_test.dungeon_data.mappa_bin.fixture import (
    eq_mappa_floor_layout_protocol,
    eq_mappa_floor_terrain_settings_protocol,
    eq_mappa_item_list_protocol,
    eq_mappa_trap_list_protocol,
    eq_mappa_monster_protocol,
    eq_mappa_floor_protocol,
    MappaFloorLayoutStub,
    MappaMonsterStub,
    MappaTrapListStub,
    MappaItemListStub,
)
from skytemple_files_test.dungeon_data.mappa_bin.fixture_autogen import (
    FIX_FLOOR_LAYOUTS,
    FIX_TERRAIN_SETTINGS_LISTS,
    FIX_MONSTER_LISTS,
    FIX_TRAP_LISTS,
    FIX_ITEM_LISTS,
    FIX_FLOOR_LISTS,
    FIX_FLOORS,
)

EP = TypeVar("EP")


class MdTestCase(SkyTempleFilesTestCase[MappaBinHandler, MappaBinProtocol]):
    handler = MappaBinHandler

    def test_mappa_floor_terrain_settings__init__(self):
        for expected in FIX_TERRAIN_SETTINGS_LISTS:
            subject = self.handler.get_terrain_settings_model()(
                expected.has_secondary_terrain,
                expected.unk1,
                expected.generate_imperfect_rooms,
                expected.unk3,
                expected.unk4,
                expected.unk5,
                expected.unk6,
                expected.unk7,
            )

            self.assertTrue(eq_mappa_floor_terrain_settings_protocol(expected, subject))

    def test_mappa_floor_terrain_settings__eq__(self):
        subject_not_same = self.handler.get_terrain_settings_model()(
            FIX_TERRAIN_SETTINGS_LISTS[0].has_secondary_terrain,
            FIX_TERRAIN_SETTINGS_LISTS[0].unk1,
            FIX_TERRAIN_SETTINGS_LISTS[0].generate_imperfect_rooms,
            FIX_TERRAIN_SETTINGS_LISTS[0].unk3,
            FIX_TERRAIN_SETTINGS_LISTS[0].unk4,
            FIX_TERRAIN_SETTINGS_LISTS[0].unk5,
            FIX_TERRAIN_SETTINGS_LISTS[0].unk6,
            FIX_TERRAIN_SETTINGS_LISTS[0].unk7,
        )

        for expected in FIX_TERRAIN_SETTINGS_LISTS[1:]:
            subject1 = self.handler.get_terrain_settings_model()(
                expected.has_secondary_terrain,
                expected.unk1,
                expected.generate_imperfect_rooms,
                expected.unk3,
                expected.unk4,
                expected.unk5,
                expected.unk6,
                expected.unk7,
            )
            subject2 = self.handler.get_terrain_settings_model()(
                expected.has_secondary_terrain,
                expected.unk1,
                expected.generate_imperfect_rooms,
                expected.unk3,
                expected.unk4,
                expected.unk5,
                expected.unk6,
                expected.unk7,
            )

            self.assertEqual(subject1, subject2)
            self.assertEqual(subject2, subject1)
            self.assertNotEqual(subject1, subject_not_same)
            self.assertNotEqual(subject_not_same, subject1)

    def test_mappa_floor_terrain_settings_attrs(self):
        e = self.handler.get_terrain_settings_model()(False, False, False, False, False, False, False, False)

        e.unk1 = True
        e.unk3 = True
        e.unk4 = True
        e.unk5 = True
        e.unk6 = True
        e.unk7 = True
        e.generate_imperfect_rooms = True
        e.has_secondary_terrain = True

        self.assertEqual(e.unk1, True)
        self.assertEqual(e.unk3, True)
        self.assertEqual(e.unk4, True)
        self.assertEqual(e.unk5, True)
        self.assertEqual(e.unk6, True)
        self.assertEqual(e.unk7, True)
        self.assertEqual(e.generate_imperfect_rooms, True)
        self.assertEqual(e.has_secondary_terrain, True)

    def test_mappa_floor_layout__init__(self):
        for expected in FIX_FLOOR_LAYOUTS:
            subject = self.handler.get_floor_layout_model()(
                expected.structure,
                expected.room_density,
                expected.tileset_id,
                expected.music_id,
                expected.weather,
                expected.floor_connectivity,
                expected.initial_enemy_density,
                expected.kecleon_shop_chance,
                expected.monster_house_chance,
                expected.unused_chance,
                expected.sticky_item_chance,
                expected.dead_ends,
                expected.secondary_terrain,
                self.handler.get_terrain_settings_model()(
                    expected.terrain_settings.has_secondary_terrain,
                    expected.terrain_settings.unk1,
                    expected.terrain_settings.generate_imperfect_rooms,
                    expected.terrain_settings.unk3,
                    expected.terrain_settings.unk4,
                    expected.terrain_settings.unk5,
                    expected.terrain_settings.unk6,
                    expected.terrain_settings.unk7,
                ),
                expected.unk_e,
                expected.item_density,
                expected.trap_density,
                expected.floor_number,
                expected.fixed_floor_id,
                expected.extra_hallway_density,
                expected.buried_item_density,
                expected.water_density,
                expected.darkness_level,
                expected.max_coin_amount,
                expected.kecleon_shop_item_positions,
                expected.empty_monster_house_chance,
                expected.unk_hidden_stairs,
                expected.hidden_stairs_spawn_chance,
                expected.enemy_iq,
                expected.iq_booster_boost,
            )

            self.assertTrue(eq_mappa_floor_layout_protocol(expected, subject))

    def test_mappa_floor_layout__eq__(self):
        subject_not_same = self.handler.get_floor_layout_model()(
            FIX_FLOOR_LAYOUTS[0].structure,
            FIX_FLOOR_LAYOUTS[0].room_density,
            FIX_FLOOR_LAYOUTS[0].tileset_id,
            FIX_FLOOR_LAYOUTS[0].music_id,
            FIX_FLOOR_LAYOUTS[0].weather,
            FIX_FLOOR_LAYOUTS[0].floor_connectivity,
            FIX_FLOOR_LAYOUTS[0].initial_enemy_density,
            FIX_FLOOR_LAYOUTS[0].kecleon_shop_chance,
            FIX_FLOOR_LAYOUTS[0].monster_house_chance,
            FIX_FLOOR_LAYOUTS[0].unused_chance,
            FIX_FLOOR_LAYOUTS[0].sticky_item_chance,
            FIX_FLOOR_LAYOUTS[0].dead_ends,
            FIX_FLOOR_LAYOUTS[0].secondary_terrain,
            self.handler.get_terrain_settings_model()(
                FIX_FLOOR_LAYOUTS[0].terrain_settings.has_secondary_terrain,
                FIX_FLOOR_LAYOUTS[0].terrain_settings.unk1,
                FIX_FLOOR_LAYOUTS[0].terrain_settings.generate_imperfect_rooms,
                FIX_FLOOR_LAYOUTS[0].terrain_settings.unk3,
                FIX_FLOOR_LAYOUTS[0].terrain_settings.unk4,
                FIX_FLOOR_LAYOUTS[0].terrain_settings.unk5,
                FIX_FLOOR_LAYOUTS[0].terrain_settings.unk6,
                FIX_FLOOR_LAYOUTS[0].terrain_settings.unk7,
            ),
            FIX_FLOOR_LAYOUTS[0].unk_e,
            FIX_FLOOR_LAYOUTS[0].item_density,
            FIX_FLOOR_LAYOUTS[0].trap_density,
            FIX_FLOOR_LAYOUTS[0].floor_number,
            FIX_FLOOR_LAYOUTS[0].fixed_floor_id,
            FIX_FLOOR_LAYOUTS[0].extra_hallway_density,
            FIX_FLOOR_LAYOUTS[0].buried_item_density,
            FIX_FLOOR_LAYOUTS[0].water_density,
            FIX_FLOOR_LAYOUTS[0].darkness_level,
            FIX_FLOOR_LAYOUTS[0].max_coin_amount,
            FIX_FLOOR_LAYOUTS[0].kecleon_shop_item_positions,
            FIX_FLOOR_LAYOUTS[0].empty_monster_house_chance,
            FIX_FLOOR_LAYOUTS[0].unk_hidden_stairs,
            FIX_FLOOR_LAYOUTS[0].hidden_stairs_spawn_chance,
            FIX_FLOOR_LAYOUTS[0].enemy_iq,
            FIX_FLOOR_LAYOUTS[0].iq_booster_boost,
        )
        for expected in FIX_FLOOR_LAYOUTS[1:]:
            subject1 = self.handler.get_floor_layout_model()(
                expected.structure,
                expected.room_density,
                expected.tileset_id,
                expected.music_id,
                expected.weather,
                expected.floor_connectivity,
                expected.initial_enemy_density,
                expected.kecleon_shop_chance,
                expected.monster_house_chance,
                expected.unused_chance,
                expected.sticky_item_chance,
                expected.dead_ends,
                expected.secondary_terrain,
                self.handler.get_terrain_settings_model()(
                    expected.terrain_settings.has_secondary_terrain,
                    expected.terrain_settings.unk1,
                    expected.terrain_settings.generate_imperfect_rooms,
                    expected.terrain_settings.unk3,
                    expected.terrain_settings.unk4,
                    expected.terrain_settings.unk5,
                    expected.terrain_settings.unk6,
                    expected.terrain_settings.unk7,
                ),
                expected.unk_e,
                expected.item_density,
                expected.trap_density,
                expected.floor_number,
                expected.fixed_floor_id,
                expected.extra_hallway_density,
                expected.buried_item_density,
                expected.water_density,
                expected.darkness_level,
                expected.max_coin_amount,
                expected.kecleon_shop_item_positions,
                expected.empty_monster_house_chance,
                expected.unk_hidden_stairs,
                expected.hidden_stairs_spawn_chance,
                expected.enemy_iq,
                expected.iq_booster_boost,
            )
            subject2 = self.handler.get_floor_layout_model()(
                expected.structure,
                expected.room_density,
                expected.tileset_id,
                expected.music_id,
                expected.weather,
                expected.floor_connectivity,
                expected.initial_enemy_density,
                expected.kecleon_shop_chance,
                expected.monster_house_chance,
                expected.unused_chance,
                expected.sticky_item_chance,
                expected.dead_ends,
                expected.secondary_terrain,
                self.handler.get_terrain_settings_model()(
                    expected.terrain_settings.has_secondary_terrain,
                    expected.terrain_settings.unk1,
                    expected.terrain_settings.generate_imperfect_rooms,
                    expected.terrain_settings.unk3,
                    expected.terrain_settings.unk4,
                    expected.terrain_settings.unk5,
                    expected.terrain_settings.unk6,
                    expected.terrain_settings.unk7,
                ),
                expected.unk_e,
                expected.item_density,
                expected.trap_density,
                expected.floor_number,
                expected.fixed_floor_id,
                expected.extra_hallway_density,
                expected.buried_item_density,
                expected.water_density,
                expected.darkness_level,
                expected.max_coin_amount,
                expected.kecleon_shop_item_positions,
                expected.empty_monster_house_chance,
                expected.unk_hidden_stairs,
                expected.hidden_stairs_spawn_chance,
                expected.enemy_iq,
                expected.iq_booster_boost,
            )

            self.assertEqual(subject1, subject2)
            self.assertEqual(subject2, subject1)
            self.assertNotEqual(subject1, subject_not_same)
            self.assertNotEqual(subject_not_same, subject1)

    def test_mappa_floor_layout_attrs(self):
        e = self.handler.get_floor_layout_model()(
            u8(0),
            i8(0),
            u8(0),
            u8(0),
            u8(0),
            u8(0),
            i8(0),
            u8(0),
            u8(0),
            u8(0),
            u8(0),
            False,
            u8(0),
            self.handler.get_terrain_settings_model()(False, False, False, False, False, False, False, False),
            False,
            u8(0),
            u8(0),
            u8(0),
            u8(0),
            u8(0),
            u8(0),
            u8(0),
            u8(0),
            0,
            u8(0),
            u8(0),
            u8(0),
            u8(0),
            u16(0),
            i16(0),
        )

        e.structure = u8(4)
        e.room_density = i8(-123)
        e.tileset_id = u8(123)
        e.music_id = u8(123)
        e.weather = u8(5)
        e.floor_connectivity = u8(123)
        e.initial_enemy_density = i8(-123)
        e.kecleon_shop_chance = u8(123)
        e.monster_house_chance = u8(123)
        e.unused_chance = u8(123)
        e.sticky_item_chance = u8(123)
        e.dead_ends = True
        e.secondary_terrain = u8(123)
        e.terrain_settings.has_secondary_terrain = True
        e.terrain_settings.unk1 = True
        e.terrain_settings.generate_imperfect_rooms = True
        e.terrain_settings.unk3 = True
        e.terrain_settings.unk4 = True
        e.terrain_settings.unk5 = True
        e.terrain_settings.unk6 = True
        e.terrain_settings.unk7 = True
        e.unk_e = True
        e.item_density = u8(123)
        e.trap_density = u8(123)
        e.floor_number = u8(123)
        e.fixed_floor_id = u8(123)
        e.extra_hallway_density = u8(123)
        e.buried_item_density = u8(123)
        e.water_density = u8(123)
        e.darkness_level = u8(3)
        e.max_coin_amount = 120
        e.kecleon_shop_item_positions = u8(123)
        e.empty_monster_house_chance = u8(123)
        e.unk_hidden_stairs = u8(123)
        e.hidden_stairs_spawn_chance = u8(123)
        e.enemy_iq = u16(0xFFF)
        e.iq_booster_boost = i16(-0xFFF)

        self.assertEqual(e.structure, u8(4))
        self.assertEqual(e.room_density, i8(-123))
        self.assertEqual(e.tileset_id, u8(123))
        self.assertEqual(e.music_id, u8(123))
        self.assertEqual(e.weather, u8(5))
        self.assertEqual(e.floor_connectivity, u8(123))
        self.assertEqual(e.initial_enemy_density, i8(-123))
        self.assertEqual(e.kecleon_shop_chance, u8(123))
        self.assertEqual(e.monster_house_chance, u8(123))
        self.assertEqual(e.unused_chance, u8(123))
        self.assertEqual(e.sticky_item_chance, u8(123))
        self.assertEqual(e.dead_ends, True)
        self.assertEqual(e.secondary_terrain, u8(123))
        self.assertEqual(e.terrain_settings.has_secondary_terrain, True)
        self.assertEqual(e.terrain_settings.unk1, True)
        self.assertEqual(e.terrain_settings.generate_imperfect_rooms, True)
        self.assertEqual(e.terrain_settings.unk3, True)
        self.assertEqual(e.terrain_settings.unk4, True)
        self.assertEqual(e.terrain_settings.unk5, True)
        self.assertEqual(e.terrain_settings.unk6, True)
        self.assertEqual(e.terrain_settings.unk7, True)
        self.assertEqual(e.unk_e, True)
        self.assertEqual(e.item_density, u8(123))
        self.assertEqual(e.trap_density, u8(123))
        self.assertEqual(e.floor_number, u8(123))
        self.assertEqual(e.fixed_floor_id, u8(123))
        self.assertEqual(e.extra_hallway_density, u8(123))
        self.assertEqual(e.buried_item_density, u8(123))
        self.assertEqual(e.water_density, u8(123))
        self.assertEqual(e.darkness_level, u8(3))
        self.assertEqual(e.max_coin_amount, 120)
        self.assertEqual(e.kecleon_shop_item_positions, u8(123))
        self.assertEqual(e.empty_monster_house_chance, u8(123))
        self.assertEqual(e.unk_hidden_stairs, u8(123))
        self.assertEqual(e.hidden_stairs_spawn_chance, u8(123))
        self.assertEqual(e.enemy_iq, u16(0xFFF))
        self.assertEqual(e.iq_booster_boost, i16(-0xFFF))

    def test_mappa_item_list__init__(self):
        for expected in FIX_ITEM_LISTS:
            subject = self.handler.get_item_list_model()(expected.categories, expected.items)

            self.assertTrue(eq_mappa_item_list_protocol(expected, subject))

    def test_mappa_item_list_from_bytes(self):
        for i, expected in enumerate(FIX_ITEM_LISTS[:10]):
            with open(self._item_list_fix_path(i), "rb") as f:
                fix = f.read()
            subject = self.handler.get_item_list_model().from_bytes(fix, 0)

            self.assertTrue(eq_mappa_item_list_protocol(expected, subject))

    def test_mappa_item_list_to_bytes(self):
        for i in range(0, 10):
            with open(self._item_list_fix_path(i), "rb") as f:
                expected = f.read()
            subject = self.handler.get_item_list_model().from_bytes(expected, 0)
            result = subject.to_bytes()

            self.assertEqual(expected, result)

    def test_mappa_item_list__eq__(self):
        subject_not_same = self.handler.get_item_list_model()(
            FIX_ITEM_LISTS[0].categories,
            FIX_ITEM_LISTS[0].items,
        )

        for expected in FIX_ITEM_LISTS[1:]:
            subject1 = self.handler.get_item_list_model()(expected.categories, expected.items)
            subject2 = self.handler.get_item_list_model()(expected.categories, expected.items)

            self.assertEqual(subject1, subject2)
            self.assertEqual(subject2, subject1)
            self.assertNotEqual(subject1, subject_not_same)
            self.assertNotEqual(subject_not_same, subject1)

    def test_mappa_item_list_attrs(self):
        e = self.handler.get_item_list_model()({}, {})

        e.categories = {1: 2, 10: 20, 3: 30}
        e.items = {4: 5, 6: 7}

        self.assertEqual(e.categories, {1: 2, 10: 20, 3: 30})
        self.assertEqual(e.items, {4: 5, 6: 7})

    def test_mappa_monster__init__(self):
        for expected_list in FIX_MONSTER_LISTS:
            for expected in expected_list:
                subject = self.handler.get_monster_model()(
                    expected.level,
                    expected.main_spawn_weight,
                    expected.monster_house_spawn_weight,
                    expected.md_index,
                )

                self.assertTrue(eq_mappa_monster_protocol(expected, subject))

    def test_mappa_monster__eq__(self):
        subject_not_same = self.handler.get_monster_model()(
            FIX_MONSTER_LISTS[0][0].level,
            FIX_MONSTER_LISTS[0][0].main_spawn_weight,
            FIX_MONSTER_LISTS[0][0].monster_house_spawn_weight,
            FIX_MONSTER_LISTS[0][0].md_index,
        )

        for expected_list in FIX_MONSTER_LISTS[1:]:
            for expected in expected_list:
                subject1 = self.handler.get_monster_model()(
                    expected.level,
                    expected.main_spawn_weight,
                    expected.monster_house_spawn_weight,
                    expected.md_index,
                )
                subject2 = self.handler.get_monster_model()(
                    expected.level,
                    expected.main_spawn_weight,
                    expected.monster_house_spawn_weight,
                    expected.md_index,
                )

                self.assertEqual(subject1, subject2)
                self.assertEqual(subject2, subject1)
                self.assertNotEqual(subject1, subject_not_same)
                self.assertNotEqual(subject_not_same, subject1)

    def test_mappa_monster_attrs(self):
        e = self.handler.get_monster_model()(u8(0), u16(0), u16(0), u16(0))

        e.level = u8(123)
        e.main_spawn_weight = u16(0xFFF)
        e.monster_house_spawn_weight = u16(0x1FFF)
        e.md_index = u16(1234)

        self.assertEqual(e.level, u8(123))
        self.assertEqual(e.main_spawn_weight, u16(0xFFF))
        self.assertEqual(e.monster_house_spawn_weight, u16(0x1FFF))
        self.assertEqual(e.md_index, u16(1234))

    def test_mappa_trap_list__init__(self):
        for expected in FIX_TRAP_LISTS:
            subject = self.handler.get_trap_list_model()(expected.weights)

            self.assertTrue(eq_mappa_trap_list_protocol(expected, subject))

    def test_mappa_trap_list__eq__(self):
        subject_not_same = self.handler.get_trap_list_model()(FIX_TRAP_LISTS[0].weights)

        for expected in FIX_TRAP_LISTS[1:]:
            subject1 = self.handler.get_trap_list_model()(expected.weights)
            subject2 = self.handler.get_trap_list_model()(expected.weights)

            self.assertEqual(subject1, subject2)
            self.assertEqual(subject2, subject1)
            self.assertNotEqual(subject1, subject_not_same)
            self.assertNotEqual(subject_not_same, subject1)

    def test_mappa_trap_list_attrs(self):
        e = self.handler.get_trap_list_model()([u16(0)] * 25)

        self.assertEqual(
            e.weights,
            {
                u8(0): u16(0),
                u8(1): u16(0),
                u8(2): u16(0),
                u8(3): u16(0),
                u8(4): u16(0),
                u8(5): u16(0),
                u8(6): u16(0),
                u8(7): u16(0),
                u8(8): u16(0),
                u8(9): u16(0),
                u8(10): u16(0),
                u8(11): u16(0),
                u8(12): u16(0),
                u8(13): u16(0),
                u8(14): u16(0),
                u8(15): u16(0),
                u8(16): u16(0),
                u8(17): u16(0),
                u8(18): u16(0),
                u8(19): u16(0),
                u8(20): u16(0),
                u8(21): u16(0),
                u8(22): u16(0),
                u8(23): u16(0),
                u8(24): u16(0),
            },
        )

        e.weights = {
            u8(0): u16(1),
            u8(1): u16(10),
            u8(2): u16(30),
            u8(3): u16(23),
            u8(4): u16(21),
            u8(5): u16(11),
            u8(6): u16(123),
            u8(7): u16(1234),
            u8(8): u16(0),
            u8(9): u16(10),
            u8(10): u16(12),
            u8(11): u16(12),
            u8(12): u16(13),
            u8(13): u16(0),
            u8(14): u16(15),
            u8(15): u16(4),
            u8(16): u16(8),
            u8(17): u16(9),
            u8(18): u16(10),
            u8(19): u16(11),
            u8(20): u16(12),
            u8(21): u16(13),
            u8(22): u16(14),
            u8(23): u16(15),
            u8(24): u16(9),
        }

        self.assertEqual(
            e.weights,
            {
                u8(0): u16(1),
                u8(1): u16(10),
                u8(2): u16(30),
                u8(3): u16(23),
                u8(4): u16(21),
                u8(5): u16(11),
                u8(6): u16(123),
                u8(7): u16(1234),
                u8(8): u16(0),
                u8(9): u16(10),
                u8(10): u16(12),
                u8(11): u16(12),
                u8(12): u16(13),
                u8(13): u16(0),
                u8(14): u16(15),
                u8(15): u16(4),
                u8(16): u16(8),
                u8(17): u16(9),
                u8(18): u16(10),
                u8(19): u16(11),
                u8(20): u16(12),
                u8(21): u16(13),
                u8(22): u16(14),
                u8(23): u16(15),
                u8(24): u16(9),
            },
        )

    def test_mappa_floor__init__(self):
        for expected in FIX_FLOORS:
            subject = self.handler.get_floor_model()(
                *self._make_floor_model_params(
                    expected.layout,
                    expected.monsters,
                    expected.traps,
                    expected.floor_items,
                    expected.shop_items,
                    expected.monster_house_items,
                    expected.buried_items,
                    expected.unk_items1,
                    expected.unk_items2,
                )
            )

            self.assertTrue(eq_mappa_floor_protocol(expected, subject))

    def test_mappa_floor__eq__(self):
        subject_not_same = self.handler.get_floor_model()(
            *self._make_floor_model_params(
                FIX_FLOORS[0].layout,
                FIX_FLOORS[0].monsters,
                FIX_FLOORS[0].traps,
                FIX_FLOORS[0].floor_items,
                FIX_FLOORS[0].shop_items,
                FIX_FLOORS[0].monster_house_items,
                FIX_FLOORS[0].buried_items,
                FIX_FLOORS[0].unk_items1,
                FIX_FLOORS[0].unk_items2,
            )
        )

        for expected in FIX_FLOORS[1:]:
            subject1 = self.handler.get_floor_model()(
                *self._make_floor_model_params(
                    expected.layout,
                    expected.monsters,
                    expected.traps,
                    expected.floor_items,
                    expected.shop_items,
                    expected.monster_house_items,
                    expected.buried_items,
                    expected.unk_items1,
                    expected.unk_items2,
                )
            )
            subject2 = self.handler.get_floor_model()(
                *self._make_floor_model_params(
                    expected.layout,
                    expected.monsters,
                    expected.traps,
                    expected.floor_items,
                    expected.shop_items,
                    expected.monster_house_items,
                    expected.buried_items,
                    expected.unk_items1,
                    expected.unk_items2,
                )
            )

            self.assertEqual(subject1, subject2)
            self.assertEqual(subject2, subject1)
            self.assertNotEqual(subject1, subject_not_same)
            self.assertNotEqual(subject_not_same, subject1)

    def test_mappa_floor_attrs(self):
        e = self.handler.get_floor_model()(
            *self._make_floor_model_params(
                FIX_FLOORS[0].layout,
                FIX_FLOORS[0].monsters,
                FIX_FLOORS[0].traps,
                FIX_FLOORS[0].floor_items,
                FIX_FLOORS[0].shop_items,
                FIX_FLOORS[0].monster_house_items,
                FIX_FLOORS[0].buried_items,
                FIX_FLOORS[0].unk_items1,
                FIX_FLOORS[0].unk_items2,
            )
        )

        self.assertTrue(eq_mappa_floor_layout_protocol(FIX_FLOORS[0].layout, e.layout))
        self.assertEqual(len(FIX_FLOORS[0].monsters), len(e.monsters))
        for exp, act in zip(FIX_FLOORS[0].monsters, e.monsters):
            self.assertTrue(eq_mappa_monster_protocol(exp, act))
        self.assertTrue(eq_mappa_trap_list_protocol(FIX_FLOORS[0].traps, e.traps))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[0].floor_items, e.floor_items))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[0].shop_items, e.shop_items))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[0].monster_house_items, e.monster_house_items))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[0].buried_items, e.buried_items))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[0].unk_items1, e.unk_items1))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[0].unk_items2, e.unk_items2))

        (
            e.layout,
            e.monsters,
            e.traps,
            e.floor_items,
            e.shop_items,
            e.monster_house_items,
            e.buried_items,
            e.unk_items1,
            e.unk_items2,
        ) = self._make_floor_model_params(
            FIX_FLOORS[1].layout,
            FIX_FLOORS[1].monsters,
            FIX_FLOORS[1].traps,
            FIX_FLOORS[1].floor_items,
            FIX_FLOORS[1].shop_items,
            FIX_FLOORS[1].monster_house_items,
            FIX_FLOORS[1].buried_items,
            FIX_FLOORS[1].unk_items1,
            FIX_FLOORS[1].unk_items2,
        )

        self.assertTrue(eq_mappa_floor_layout_protocol(FIX_FLOORS[1].layout, e.layout))
        self.assertEqual(len(FIX_FLOORS[1].monsters), len(e.monsters))
        for exp, act in zip(FIX_FLOORS[1].monsters, e.monsters):
            self.assertTrue(eq_mappa_monster_protocol(exp, act))
        self.assertTrue(eq_mappa_trap_list_protocol(FIX_FLOORS[1].traps, e.traps))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[1].floor_items, e.floor_items))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[1].shop_items, e.shop_items))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[1].monster_house_items, e.monster_house_items))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[1].buried_items, e.buried_items))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[1].unk_items1, e.unk_items1))
        self.assertTrue(eq_mappa_item_list_protocol(FIX_FLOORS[1].unk_items2, e.unk_items2))

    def test_mappa__init__(self):
        floor_lists = []
        for in_list in FIX_FLOOR_LISTS:
            out_list = []
            floor_lists.append(out_list)
            for in_floor in in_list:
                out_list.append(
                    self.handler.get_floor_model()(
                        *self._make_floor_model_params(
                            in_floor.layout,
                            in_floor.monsters,
                            in_floor.traps,
                            in_floor.floor_items,
                            in_floor.shop_items,
                            in_floor.monster_house_items,
                            in_floor.buried_items,
                            in_floor.unk_items1,
                            in_floor.unk_items2,
                        )
                    )
                )

        actual = self.handler.get_model_cls()(floor_lists)

        self.assertEqual(len(FIX_FLOOR_LISTS), len(actual.floor_lists))
        for fl_expected, fl_actual in zip(FIX_FLOOR_LISTS, actual.floor_lists):
            self.assertEqual(len(fl_expected), len(fl_actual))
            for f_expected, f_actual in zip(fl_expected, fl_actual):
                self.assertTrue(eq_mappa_floor_protocol(f_expected, f_actual))

    def test_mappa_sir0_serialize_parts(self):
        first = self._load_main_fixture(self._mappa_fix_path())

        # Serialize the parts, make sure the offsets make sense and try to re-construct.
        data, offsets, header_pointer = first.sir0_serialize_parts()
        # TODO: How to check the offsets?

        second = self.handler.get_model_cls().sir0_unwrap(data, header_pointer)

        self.assertEqual(first, second)
        # Sanity check - this double checks __eq__ isn't just returning True; but see the other tests too.
        second.remove_floor_list(0)
        self.assertNotEqual(first, second)

    def test_mappa_load_via_handler(self):
        actual = self._load_main_fixture(self._mappa_fix_path())

        self.assertEqual(len(FIX_FLOOR_LISTS), len(actual.floor_lists))
        for fl_expected, fl_actual in zip(FIX_FLOOR_LISTS, actual.floor_lists):
            self.assertEqual(len(fl_expected), len(fl_actual))
            for f_expected, f_actual in zip(fl_expected, fl_actual):
                self.assertTrue(eq_mappa_floor_protocol(f_expected, f_actual))

    def test_mappa_save_via_handler(self):
        loaded = self._load_main_fixture(self._mappa_fix_path())
        actual = self._save_and_reload_main_fixture(loaded)

        self.assertEqual(len(FIX_FLOOR_LISTS), len(actual.floor_lists))
        for fl_expected, fl_actual in zip(FIX_FLOOR_LISTS, actual.floor_lists):
            self.assertEqual(len(fl_expected), len(fl_actual))
            for f_expected, f_actual in zip(fl_expected, fl_actual):
                self.assertTrue(eq_mappa_floor_protocol(f_expected, f_actual))

    def test_mappa_sir0_unwrap(self):
        # Note, this test requires the Python Sir0 model to function correctly!
        with open(self._mappa_fix_path(), "rb") as f:
            sir0 = Sir0Handler.load_python_model().from_bin(f.read())
        actual = self.handler.get_model_cls().sir0_unwrap(sir0.content, sir0.data_pointer)

        self.assertEqual(len(FIX_FLOOR_LISTS), len(actual.floor_lists))
        for fl_expected, fl_actual in zip(FIX_FLOOR_LISTS, actual.floor_lists):
            self.assertEqual(len(fl_expected), len(fl_actual))
            for f_expected, f_actual in zip(fl_expected, fl_actual):
                self.assertTrue(eq_mappa_floor_protocol(f_expected, f_actual))

    def test_mappa_add_floor_list(self):
        subject = self._make_simple_mappa()
        new_list = [
            self.handler.get_floor_model()(
                *self._make_floor_model_params(
                    FIX_FLOORS[3].layout,
                    FIX_FLOORS[3].monsters,
                    FIX_FLOORS[3].traps,
                    FIX_FLOORS[3].floor_items,
                    FIX_FLOORS[3].shop_items,
                    FIX_FLOORS[3].monster_house_items,
                    FIX_FLOORS[3].buried_items,
                    FIX_FLOORS[3].unk_items1,
                    FIX_FLOORS[3].unk_items2,
                )
            )
        ]

        subject.add_floor_list(new_list)

        self.assertEqual(3, len(subject.floor_lists))
        self.assertEqual(2, len(subject.floor_lists[0]))
        self.assertEqual(1, len(subject.floor_lists[1]))
        self.assertEqual(1, len(subject.floor_lists[1]))
        eq_mappa_floor_protocol(FIX_FLOORS[0], subject.floor_lists[0][0])
        eq_mappa_floor_protocol(FIX_FLOORS[1], subject.floor_lists[0][1])
        eq_mappa_floor_protocol(FIX_FLOORS[2], subject.floor_lists[1][0])
        eq_mappa_floor_protocol(FIX_FLOORS[3], subject.floor_lists[2][0])

    def test_mappa_remove_floor_list(self):
        subject = self._make_simple_mappa()

        subject.remove_floor_list(1)
        self.assertEqual(1, len(subject.floor_lists))
        self.assertEqual(2, len(subject.floor_lists[0]))
        eq_mappa_floor_protocol(FIX_FLOORS[0], subject.floor_lists[0][0])
        eq_mappa_floor_protocol(FIX_FLOORS[1], subject.floor_lists[0][1])

        subject.remove_floor_list(0)
        self.assertEqual(0, len(subject.floor_lists))

    def test_mappa_add_floor_to_floor_list(self):
        subject = self._make_simple_mappa()

        subject.add_floor_to_floor_list(
            0,
            self.handler.get_floor_model()(
                *self._make_floor_model_params(
                    FIX_FLOORS[3].layout,
                    FIX_FLOORS[3].monsters,
                    FIX_FLOORS[3].traps,
                    FIX_FLOORS[3].floor_items,
                    FIX_FLOORS[3].shop_items,
                    FIX_FLOORS[3].monster_house_items,
                    FIX_FLOORS[3].buried_items,
                    FIX_FLOORS[3].unk_items1,
                    FIX_FLOORS[3].unk_items2,
                )
            ),
        )

        subject.add_floor_to_floor_list(
            1,
            self.handler.get_floor_model()(
                *self._make_floor_model_params(
                    FIX_FLOORS[4].layout,
                    FIX_FLOORS[4].monsters,
                    FIX_FLOORS[4].traps,
                    FIX_FLOORS[4].floor_items,
                    FIX_FLOORS[4].shop_items,
                    FIX_FLOORS[4].monster_house_items,
                    FIX_FLOORS[4].buried_items,
                    FIX_FLOORS[4].unk_items1,
                    FIX_FLOORS[4].unk_items2,
                )
            ),
        )

        self.assertEqual(2, len(subject.floor_lists))
        self.assertEqual(3, len(subject.floor_lists[0]))
        self.assertEqual(2, len(subject.floor_lists[1]))
        eq_mappa_floor_protocol(FIX_FLOORS[0], subject.floor_lists[0][0])
        eq_mappa_floor_protocol(FIX_FLOORS[1], subject.floor_lists[0][1])
        eq_mappa_floor_protocol(FIX_FLOORS[2], subject.floor_lists[1][0])
        eq_mappa_floor_protocol(FIX_FLOORS[3], subject.floor_lists[0][2])
        eq_mappa_floor_protocol(FIX_FLOORS[4], subject.floor_lists[1][1])

    def test_insert_floor_in_floor_list(self):
        subject = self._make_simple_mappa()

        subject.insert_floor_in_floor_list(
            0,
            1,
            self.handler.get_floor_model()(
                *self._make_floor_model_params(
                    FIX_FLOORS[3].layout,
                    FIX_FLOORS[3].monsters,
                    FIX_FLOORS[3].traps,
                    FIX_FLOORS[3].floor_items,
                    FIX_FLOORS[3].shop_items,
                    FIX_FLOORS[3].monster_house_items,
                    FIX_FLOORS[3].buried_items,
                    FIX_FLOORS[3].unk_items1,
                    FIX_FLOORS[3].unk_items2,
                )
            ),
        )

        subject.insert_floor_in_floor_list(
            1,
            0,
            self.handler.get_floor_model()(
                *self._make_floor_model_params(
                    FIX_FLOORS[4].layout,
                    FIX_FLOORS[4].monsters,
                    FIX_FLOORS[4].traps,
                    FIX_FLOORS[4].floor_items,
                    FIX_FLOORS[4].shop_items,
                    FIX_FLOORS[4].monster_house_items,
                    FIX_FLOORS[4].buried_items,
                    FIX_FLOORS[4].unk_items1,
                    FIX_FLOORS[4].unk_items2,
                )
            ),
        )

        self.assertEqual(2, len(subject.floor_lists))
        self.assertEqual(3, len(subject.floor_lists[0]))
        self.assertEqual(2, len(subject.floor_lists[1]))
        eq_mappa_floor_protocol(FIX_FLOORS[0], subject.floor_lists[0][0])
        eq_mappa_floor_protocol(FIX_FLOORS[3], subject.floor_lists[0][1])
        eq_mappa_floor_protocol(FIX_FLOORS[4], subject.floor_lists[1][0])
        eq_mappa_floor_protocol(FIX_FLOORS[1], subject.floor_lists[0][2])
        eq_mappa_floor_protocol(FIX_FLOORS[2], subject.floor_lists[1][1])

    def test_mappa_remove_floor_from_floor_list(self):
        subject = self._make_simple_mappa()

        subject.remove_floor_from_floor_list(0, 1)

        self.assertEqual(2, len(subject.floor_lists))
        self.assertEqual(1, len(subject.floor_lists[0]))
        self.assertEqual(1, len(subject.floor_lists[1]))
        eq_mappa_floor_protocol(FIX_FLOORS[0], subject.floor_lists[0][0])
        eq_mappa_floor_protocol(FIX_FLOORS[2], subject.floor_lists[1][0])

        subject.remove_floor_from_floor_list(1, 0)

        self.assertEqual(2, len(subject.floor_lists))
        self.assertEqual(1, len(subject.floor_lists[0]))
        self.assertEqual(0, len(subject.floor_lists[1]))
        eq_mappa_floor_protocol(FIX_FLOORS[0], subject.floor_lists[0][0])

    def test_mappa__eq__(self):
        def make():
            floor_lists = []
            for in_list in FIX_FLOOR_LISTS:
                out_list = []
                floor_lists.append(out_list)
                for in_floor in in_list:
                    out_list.append(
                        self.handler.get_floor_model()(
                            *self._make_floor_model_params(
                                in_floor.layout,
                                in_floor.monsters,
                                in_floor.traps,
                                in_floor.floor_items,
                                in_floor.shop_items,
                                in_floor.monster_house_items,
                                in_floor.buried_items,
                                in_floor.unk_items1,
                                in_floor.unk_items2,
                            )
                        )
                    )
            return self.handler.get_model_cls()(floor_lists)

        subject1 = make()
        subject2 = make()
        subject_not_same = self.handler.get_model_cls()(
            [
                [
                    self.handler.get_floor_model()(
                        *self._make_floor_model_params(
                            FIX_FLOORS[0].layout,
                            FIX_FLOORS[0].monsters,
                            FIX_FLOORS[0].traps,
                            FIX_FLOORS[0].floor_items,
                            FIX_FLOORS[0].shop_items,
                            FIX_FLOORS[0].monster_house_items,
                            FIX_FLOORS[0].buried_items,
                            FIX_FLOORS[0].unk_items1,
                            FIX_FLOORS[0].unk_items2,
                        )
                    )
                ]
            ]
        )

        self.assertEqual(subject1, subject2)
        self.assertEqual(subject2, subject1)
        self.assertNotEqual(subject1, subject_not_same)
        self.assertNotEqual(subject_not_same, subject1)

    def test_mappa_attrs(self):
        floor_lists = []
        for in_list in FIX_FLOOR_LISTS:
            out_list = []
            floor_lists.append(out_list)
            for in_floor in in_list:
                out_list.append(
                    self.handler.get_floor_model()(
                        *self._make_floor_model_params(
                            in_floor.layout,
                            in_floor.monsters,
                            in_floor.traps,
                            in_floor.floor_items,
                            in_floor.shop_items,
                            in_floor.monster_house_items,
                            in_floor.buried_items,
                            in_floor.unk_items1,
                            in_floor.unk_items2,
                        )
                    )
                )

        actual = self.handler.get_model_cls()([])

        self.assertEqual([], actual.floor_lists)

        actual.floor_lists = floor_lists

        self.assertEqual(len(FIX_FLOOR_LISTS), len(actual.floor_lists))
        for fl_expected, fl_actual in zip(FIX_FLOOR_LISTS, actual.floor_lists):
            self.assertEqual(len(fl_expected), len(fl_actual))
            for f_expected, f_actual in zip(fl_expected, fl_actual):
                self.assertTrue(eq_mappa_floor_protocol(f_expected, f_actual))

    @romtest(file_names=["mappa_s.bin"], path="BALANCE/")
    def test_using_rom(self, _, file):
        before = self.handler.deserialize(file)
        data, _, header_pointer = before.sir0_serialize_parts()
        after = self.handler.get_model_cls().sir0_unwrap(data, header_pointer)

        self.assertEqual(before, after)

    def test_cross_native_implementation(self):
        """Tests the native implementation against the Python implementation."""
        if not env_use_native():
            self.skipTest("This test is only enabled when the native implementations are tested.")
            return
        with open(self._mappa_fix_path(), "rb") as f:
            sir0 = Sir0Handler.deserialize(f.read())
        loaded_py = self.handler.load_python_model().sir0_unwrap(sir0.content, sir0.data_pointer)
        loaded_rs = self.handler.load_native_model().sir0_unwrap(sir0.content, sir0.data_pointer)

        loaded_py_sir0 = Sir0Handler.wrap_obj(loaded_py)
        loaded_rs_sir0 = Sir0Handler.wrap_obj(loaded_rs)
        loaded_py_reloaded_with_rs = self.handler.load_native_model().sir0_unwrap(
            loaded_py_sir0.content, loaded_py_sir0.data_pointer
        )
        loaded_rs_reloaded_with_py = self.handler.load_python_model().sir0_unwrap(
            loaded_rs_sir0.content, loaded_rs_sir0.data_pointer
        )

        self.assertEqual(len(FIX_FLOOR_LISTS), len(loaded_rs_reloaded_with_py.floor_lists))
        for fl_expected, fl_actual in zip(FIX_FLOOR_LISTS, loaded_rs_reloaded_with_py.floor_lists):
            self.assertEqual(len(fl_expected), len(fl_actual))
            for f_expected, f_actual in zip(fl_expected, fl_actual):
                self.assertTrue(eq_mappa_floor_protocol(f_expected, f_actual))

        self.assertEqual(len(FIX_FLOOR_LISTS), len(loaded_py_reloaded_with_rs.floor_lists))
        for fl_expected, fl_actual in zip(FIX_FLOOR_LISTS, loaded_py_reloaded_with_rs.floor_lists):
            self.assertEqual(len(fl_expected), len(fl_actual))
            for f_expected, f_actual in zip(fl_expected, fl_actual):
                self.assertTrue(eq_mappa_floor_protocol(f_expected, f_actual))

    def assertProtocolsEqual(
        self,
        expected: EP,
        actual: EP,
        compare_fn: Callable[[EP, EP], bool],
        msg: Optional[str] = None,
    ):
        if msg is None:
            msg = ""
        else:
            msg += "\n"
        self.assertTrue(
            compare_fn(expected, actual),
            f"{msg}Entities must be equal.\n1st: \n{expected}\n2nd:{actual}",
        )

    @no_type_check
    @classmethod
    @fixpath
    def _mappa_fix_path(cls):
        return "fixtures", "fixture.bin"

    @no_type_check
    @classmethod
    @fixpath
    def _item_list_fix_path(cls, i: int):
        return "fixtures", f"item_list{i}.bin"

    def _make_simple_mappa(self):
        return self.handler.get_model_cls()(
            [
                [
                    self.handler.get_floor_model()(
                        *self._make_floor_model_params(
                            FIX_FLOORS[0].layout,
                            FIX_FLOORS[0].monsters,
                            FIX_FLOORS[0].traps,
                            FIX_FLOORS[0].floor_items,
                            FIX_FLOORS[0].shop_items,
                            FIX_FLOORS[0].monster_house_items,
                            FIX_FLOORS[0].buried_items,
                            FIX_FLOORS[0].unk_items1,
                            FIX_FLOORS[0].unk_items2,
                        )
                    ),
                    self.handler.get_floor_model()(
                        *self._make_floor_model_params(
                            FIX_FLOORS[1].layout,
                            FIX_FLOORS[1].monsters,
                            FIX_FLOORS[1].traps,
                            FIX_FLOORS[1].floor_items,
                            FIX_FLOORS[1].shop_items,
                            FIX_FLOORS[1].monster_house_items,
                            FIX_FLOORS[1].buried_items,
                            FIX_FLOORS[1].unk_items1,
                            FIX_FLOORS[1].unk_items2,
                        )
                    ),
                ],
                [
                    self.handler.get_floor_model()(
                        *self._make_floor_model_params(
                            FIX_FLOORS[2].layout,
                            FIX_FLOORS[2].monsters,
                            FIX_FLOORS[2].traps,
                            FIX_FLOORS[2].floor_items,
                            FIX_FLOORS[2].shop_items,
                            FIX_FLOORS[2].monster_house_items,
                            FIX_FLOORS[2].buried_items,
                            FIX_FLOORS[2].unk_items1,
                            FIX_FLOORS[2].unk_items2,
                        )
                    )
                ],
            ]
        )

    def _make_floor_model_params(
        self,
        layout: MappaFloorLayoutStub,
        monsters: List[MappaMonsterStub],
        traps: MappaTrapListStub,
        floor_items: MappaItemListStub,
        shop_items: MappaItemListStub,
        monster_house_items: MappaItemListStub,
        buried_items: MappaItemListStub,
        unk_items1: MappaItemListStub,
        unk_items2: MappaItemListStub,
    ) -> Tuple[
        MappaFloorLayoutProtocol,
        List[MappaMonsterProtocol],
        MappaTrapListProtocol,
        MappaItemListProtocol,
        MappaItemListProtocol,
        MappaItemListProtocol,
        MappaItemListProtocol,
        MappaItemListProtocol,
        MappaItemListProtocol,
    ]:
        return (
            self.handler.get_floor_layout_model()(
                layout.structure,
                layout.room_density,
                layout.tileset_id,
                layout.music_id,
                layout.weather,
                layout.floor_connectivity,
                layout.initial_enemy_density,
                layout.kecleon_shop_chance,
                layout.monster_house_chance,
                layout.unused_chance,
                layout.sticky_item_chance,
                layout.dead_ends,
                layout.secondary_terrain,
                self.handler.get_terrain_settings_model()(
                    layout.terrain_settings.has_secondary_terrain,
                    layout.terrain_settings.unk1,
                    layout.terrain_settings.generate_imperfect_rooms,
                    layout.terrain_settings.unk3,
                    layout.terrain_settings.unk4,
                    layout.terrain_settings.unk5,
                    layout.terrain_settings.unk6,
                    layout.terrain_settings.unk7,
                ),
                layout.unk_e,
                layout.item_density,
                layout.trap_density,
                layout.floor_number,
                layout.fixed_floor_id,
                layout.extra_hallway_density,
                layout.buried_item_density,
                layout.water_density,
                layout.darkness_level,
                layout.max_coin_amount,
                layout.kecleon_shop_item_positions,
                layout.empty_monster_house_chance,
                layout.unk_hidden_stairs,
                layout.hidden_stairs_spawn_chance,
                layout.enemy_iq,
                layout.iq_booster_boost,
            ),
            [
                self.handler.get_monster_model()(
                    monster.level,
                    monster.main_spawn_weight,
                    monster.monster_house_spawn_weight,
                    monster.md_index,
                )
                for monster in monsters
            ],
            self.handler.get_trap_list_model()(traps.weights),
            self.handler.get_item_list_model()(floor_items.categories, floor_items.items),
            self.handler.get_item_list_model()(shop_items.categories, shop_items.items),
            self.handler.get_item_list_model()(monster_house_items.categories, monster_house_items.items),
            self.handler.get_item_list_model()(buried_items.categories, buried_items.items),
            self.handler.get_item_list_model()(unk_items1.categories, unk_items1.items),
            self.handler.get_item_list_model()(unk_items2.categories, unk_items2.items),
        )
