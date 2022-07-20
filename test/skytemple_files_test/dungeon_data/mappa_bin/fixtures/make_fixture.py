from __future__ import annotations

import random
from typing import List

from range_typed_integers import u16, u8, i8, i16
from skytemple_files.container.sir0.handler import Sir0Handler

from skytemple_files.dungeon_data.mappa_bin._python_impl.floor import MappaFloor
from skytemple_files.dungeon_data.mappa_bin._python_impl.floor_layout import (
    MappaFloorLayout,
    MappaFloorTerrainSettings,
)
from skytemple_files.dungeon_data.mappa_bin._python_impl.item_list import MappaItemList
from skytemple_files.dungeon_data.mappa_bin._python_impl.monster import MappaMonster
from skytemple_files.dungeon_data.mappa_bin._python_impl.trap_list import MappaTrapList
from skytemple_files.dungeon_data.mappa_bin.handler import MappaBinHandler
from skytemple_files.dungeon_data.mappa_bin.protocol import (
    MappaFloorStructureType,
    MappaFloorWeather,
    MappaFloorDarknessLevel,
    GUARANTEED, MAX_ITEM_ID,
)


def randomize_monster_list_protocol() -> List[MappaMonster]:
    lst = []
    for _ in range(4, random.randint(4, 30)):
        lst.append(randomize_monster_protocol())
    return lst


def randomize_monster_protocol() -> MappaMonster:
    return MappaMonster(
        u8(random.randint(0, 100)),
        u16(random.randint(0, 65_535)),
        u16(random.randint(0, 65_535)),
        u16(random.randint(0, 65_535)),
    )


def randomize_trap_list_protocol() -> MappaTrapList:
    traps = []
    for _ in range(0, 25):
        traps.append(u16(random.randint(0, 10000)))
    return MappaTrapList(traps)


def randomize_item_list_protocol() -> MappaItemList:
    categories = {}
    items = {}
    for i in range(0, 0xF):
        if random.randint(0, 2):
            if random.randint(0, 20) == 0:
                categories[i] = GUARANTEED
            else:
                categories[i] = random.randint(0, 10000)
    for i in range(0, MAX_ITEM_ID):
        if random.randint(0, 4) == 0:
            if random.randint(0, 20) == 0:
                items[i] = GUARANTEED
            else:
                items[i] = random.randint(0, 10000)
    return MappaItemList(categories, items)


def randomize_terrain_settings_protocol() -> MappaFloorTerrainSettings:
    return MappaFloorTerrainSettings(
        bool(random.randint(0, 1)),
        bool(random.randint(0, 1)),
        bool(random.randint(0, 1)),
        bool(random.randint(0, 1)),
        bool(random.randint(0, 1)),
        bool(random.randint(0, 1)),
        bool(random.randint(0, 1)),
        bool(random.randint(0, 1)),
    )


def randomize_floor_layout_protocol() -> MappaFloorLayout:
    return MappaFloorLayout(
        structure=u8(random.choice(list(MappaFloorStructureType)).value),
        room_density=i8(random.randint(-128, 127)),
        tileset_id=u8(random.randint(0, 255)),
        music_id=u8(random.randint(0, 255)),
        weather=u8(random.choice(list(MappaFloorWeather)).value),
        floor_connectivity=u8(random.randint(0, 255)),
        initial_enemy_density=i8(random.randint(-128, 127)),
        kecleon_shop_chance=u8(random.randint(0, 255)),
        monster_house_chance=u8(random.randint(0, 255)),
        unused_chance=u8(random.randint(0, 255)),
        sticky_item_chance=u8(random.randint(0, 255)),
        dead_ends=bool(random.randint(0, 1)),
        secondary_terrain=u8(random.randint(0, 255)),
        terrain_settings=randomize_terrain_settings_protocol(),
        unk_e=bool(random.randint(0, 1)),
        item_density=u8(random.randint(0, 255)),
        trap_density=u8(random.randint(0, 255)),
        floor_number=u8(random.randint(0, 255)),
        fixed_floor_id=u8(random.randint(0, 255)),
        extra_hallway_density=u8(random.randint(0, 255)),
        buried_item_density=u8(random.randint(0, 255)),
        water_density=u8(random.randint(0, 255)),
        darkness_level=u8(random.choice(list(MappaFloorDarknessLevel)).value),
        max_coin_amount=random.randint(0, 32) * 5,
        kecleon_shop_item_positions=u8(random.randint(0, 255)),
        empty_monster_house_chance=u8(random.randint(0, 255)),
        unk_hidden_stairs=u8(random.randint(0, 255)),
        hidden_stairs_spawn_chance=u8(random.randint(0, 255)),
        enemy_iq=u16(random.randint(0, 65_535)),
        iq_booster_boost=i16(random.randint(-32_768, 32_767)),
    )


def p_floor_layout(layout: MappaFloorLayout) -> str:
    return f"""{layout.structure},
{layout.room_density},
{layout.tileset_id},
{layout.music_id},
{layout.weather},
{layout.floor_connectivity},
{layout.initial_enemy_density},
{layout.kecleon_shop_chance},
{layout.monster_house_chance},
{layout.unused_chance},
{layout.sticky_item_chance},
{layout.dead_ends},
{layout.secondary_terrain},
MappaFloorTerrainSettingsStub({p_floor_terrain_settings(layout.terrain_settings)}),
{layout.unk_e},
{layout.item_density},
{layout.trap_density},
{layout.floor_number},
{layout.fixed_floor_id},
{layout.extra_hallway_density},
{layout.buried_item_density},
{layout.water_density},
{layout.darkness_level},
{layout.max_coin_amount},
{layout.kecleon_shop_item_positions},
{layout.empty_monster_house_chance},
{layout.unk_hidden_stairs},
{layout.hidden_stairs_spawn_chance},
{layout.enemy_iq},
i16({layout.iq_booster_boost})
""".replace(
        "\n", ""
    )


def p_floor_terrain_settings(settings: MappaFloorTerrainSettings):
    return f"""{settings.has_secondary_terrain},
{settings.unk1},
{settings.generate_imperfect_rooms},
{settings.unk3},
{settings.unk4},
{settings.unk5},
{settings.unk6},
{settings.unk7}
""".replace(
        "\n", ""
    )


def p_monster(monster: MappaMonster) -> str:
    return f"""{monster.level},
{monster.weight},
{monster.weight2},
{monster.md_index}
""".replace(
        "\n", ""
    )


def p_trap_list(trap_list: MappaTrapList) -> str:
    return f"{repr(trap_list.weights)}"


def p_item_list(item_list: MappaItemList) -> str:
    return f"{repr(item_list.categories)},{repr(item_list.items)}"


if __name__ == "__main__":
    floor_layouts = []
    monster_lists = []
    trap_lists = []
    item_lists = []
    terrain_settings_lists = []

    for _ in range(0, 150):
        floor_layouts.append(randomize_floor_layout_protocol())

    for _ in range(0, 150):
        monster_lists.append(randomize_monster_list_protocol())

    for _ in range(0, 150):
        trap_lists.append(randomize_trap_list_protocol())

    for i in range(0, 150):
        ilist = randomize_item_list_protocol()
        item_lists.append(ilist)

        if i < 10:
            with open(f'item_list{i}.bin', 'wb') as f:
                f.write(ilist.to_bytes())

    for _ in range(0, 10):
        terrain_settings_lists.append(randomize_terrain_settings_protocol())

    floor_lists: List[List[MappaFloor]] = []
    for _ in range(0, 48):
        floor_list: List[MappaFloor] = []
        floor_lists.append(floor_list)
        for __ in range(4, random.randint(5, 99)):
            floor_list.append(
                MappaFloor(
                    random.choice(floor_layouts),
                    random.choice(monster_lists),
                    random.choice(trap_lists),
                    random.choice(item_lists),
                    random.choice(item_lists),
                    random.choice(item_lists),
                    random.choice(item_lists),
                    random.choice(item_lists),
                    random.choice(item_lists),
                )
            )

    mappa = MappaBinHandler.load_python_model()(floor_lists)

    with open("./fixture.bin", "wb") as f:
        parts = mappa.sir0_serialize_parts()
        assert mappa == MappaBinHandler.load_python_model().sir0_unwrap(
            parts[0], parts[2]
        )
        f.write(Sir0Handler.serialize(Sir0Handler.wrap(*parts)))

    with open("./fixture.bin", "rb") as f:
        in_s = Sir0Handler.deserialize(f.read())
        assert mappa == MappaBinHandler.load_python_model().sir0_unwrap(
            in_s.content, in_s.data_pointer
        )

    print("# fmt: off")
    print("# pylint: disable-all")
    print("# nopycln: file")
    print("")
    print("from skytemple_files_test.dungeon_data.mappa_bin.fixture import *")
    print("")

    print("FIX_FLOOR_LAYOUTS = (")
    for layout in floor_layouts:
        print(f"    MappaFloorLayoutStub({p_floor_layout(layout)}),")
    print(")")
    print("")

    print("FIX_TERRAIN_SETTINGS_LISTS = (")
    for terrain_settings_list in terrain_settings_lists:
        print(f"    MappaFloorTerrainSettingsStub({p_floor_terrain_settings(terrain_settings_list)}),")
    print(")")
    print("")

    print("FIX_MONSTER_LISTS = (")
    for monster_list in monster_lists:
        print("    (")
        for monster in monster_list:
            print(f"        MappaMonsterStub({p_monster(monster)}),")
        print("    ),")
    print(")")
    print("")

    print("FIX_TRAP_LISTS = (")
    for trap_list in trap_lists:
        print(f"    MappaTrapListStub({p_trap_list(trap_list)}),")
    print(")")
    print("")

    print("FIX_ITEM_LISTS = (")
    for item_list in item_lists:
        print(f"    MappaItemListStub({p_item_list(item_list)}),")
    print(")")
    print("")

    print("FIX_FLOOR_LISTS = (")
    for fli in floor_lists:
        print("    (")
        for fl in fli:
            print("        MappaFloorStub(")
            print(
                f"            MappaFloorLayoutStub({p_floor_layout(fl.layout)}),",
            )
            print("            [")
            for monster in fl.monsters:
                print(f"                MappaMonsterStub({p_monster(monster)}),")
            print("            ],")
            print(f"            MappaTrapListStub({p_trap_list(fl.traps)}),")
            print(f"            MappaItemListStub({p_item_list(fl.floor_items)}),")
            print(f"            MappaItemListStub({p_item_list(fl.shop_items)}),")
            print(
                f"            MappaItemListStub({p_item_list(fl.monster_house_items)}),",
            )
            print(
                f"            MappaItemListStub({p_item_list(fl.buried_items)}),",
            )
            print(f"            MappaItemListStub({p_item_list(fl.unk_items1)}),")
            print(f"            MappaItemListStub({p_item_list(fl.unk_items2)})")
            print("        ),")
        print("    ),")
    print(")")
    print("")

    print("FIX_FLOORS = tuple(FIX_FLOOR_LISTS[0] + FIX_FLOOR_LISTS[1])")
