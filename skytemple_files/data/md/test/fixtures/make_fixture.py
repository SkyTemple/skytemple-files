import random

from ndspy.rom import NintendoDSRom
from range_typed_integers import u16, i16, u8, i8

from skytemple_files.data.md.handler import MdHandler
from skytemple_files.data.md.protocol import MdEntryProtocol


def randomize_md_entry(entry: MdEntryProtocol):
    entry.unk31 = u16(random.randint(0, 65_535))
    entry.national_pokedex_number = u16(random.randint(0, 65_535))
    entry.base_movement_speed = u16(random.randint(0, 65_535))
    entry.pre_evo_index = u16(random.randint(0, 65_535))
    entry.evo_method = u16(random.randint(0, 5))
    entry.evo_param1 = u16(random.randint(0, 65_535))
    entry.evo_param2 = u16(random.randint(0, 15))
    entry.sprite_index = i16(random.randint(-32_768, 32_767))
    entry.gender = u8(random.randint(0, 2))
    entry.body_size = u8(random.randint(0, 255))
    entry.type_primary = u8(random.randint(0, 18))
    entry.type_secondary = u8(random.randint(0, 18))
    entry.movement_type = u8(random.randint(0, 5))
    entry.iq_group = u8(random.randint(0, 15))
    entry.ability_primary = u8(random.randint(0, 0x7B))
    entry.ability_secondary = u8(random.randint(0, 0x7B))
    entry.exp_yield = u16(random.randint(0, 65_535))
    entry.recruit_rate1 = i16(random.randint(-32_768, 32_767))
    entry.base_hp = u16(random.randint(0, 15))
    entry.recruit_rate2 = i16(random.randint(-32_768, 32_767))
    entry.base_atk = u8(random.randint(0, 255))
    entry.base_sp_atk = u8(random.randint(0, 255))
    entry.base_def = u8(random.randint(0, 255))
    entry.base_sp_def = u8(random.randint(0, 255))
    entry.weight = i16(random.randint(-32_768, 32_767))
    entry.size = i16(random.randint(-32_768, 32_767))
    entry.unk17 = u8(random.randint(0, 255))
    entry.unk18 = u8(random.randint(0, 255))
    entry.shadow_size = i8(random.randint(0, 2))
    entry.chance_spawn_asleep = i8(random.randint(-128, 127))
    entry.hp_regeneration = u8(random.randint(0, 255))
    entry.unk21_h = i8(random.randint(-128, 127))
    entry.base_form_index = i16(random.randint(-32_768, 32_767))
    entry.exclusive_item1 = i16(random.randint(-32_768, 32_767))
    entry.exclusive_item2 = i16(random.randint(-32_768, 32_767))
    entry.exclusive_item3 = i16(random.randint(-32_768, 32_767))
    entry.exclusive_item4 = i16(random.randint(-32_768, 32_767))
    entry.unk27 = i16(random.randint(-32_768, 32_767))
    entry.unk28 = i16(random.randint(-32_768, 32_767))
    entry.unk29 = i16(random.randint(-32_768, 32_767))
    entry.unk30 = i16(random.randint(-32_768, 32_767))
    entry.bitfield1_0 = bool(random.randint(0, 1))
    entry.bitfield1_1 = bool(random.randint(0, 1))
    entry.bitfield1_2 = bool(random.randint(0, 1))
    entry.bitfield1_3 = bool(random.randint(0, 1))
    entry.can_move = bool(random.randint(0, 1))
    entry.bitfield1_5 = bool(random.randint(0, 1))
    entry.can_evolve = bool(random.randint(0, 1))
    entry.item_required_for_spawning = bool(random.randint(0, 1))


if __name__ == "__main__":
    rom = NintendoDSRom.fromFile("/tmp/rom.nds")

    md = MdHandler.load_python_model()(rom.getFileByName("BALANCE/monster.md"))

    entry0 = md.entries[0]
    entry6 = md.entries[600]
    assert entry0.md_index_base == 0
    assert entry6.md_index_base == 0
    assert entry0.entid == 0
    assert entry6.entid == 0
    entry1 = md.entries[1]
    entry7 = md.entries[601]
    assert entry1.md_index_base == 1
    assert entry7.md_index_base == 1
    assert entry1.entid == 1
    assert entry7.entid == 1
    entry2 = md.entries[2]
    entry8 = md.entries[602]
    assert entry2.md_index_base == 2
    assert entry8.md_index_base == 2
    assert entry2.entid == 2
    assert entry8.entid == 2
    entry3 = md.entries[3]
    entry9 = md.entries[603]
    assert entry3.md_index_base == 3
    assert entry9.md_index_base == 3
    assert entry3.entid == 3
    assert entry9.entid == 3
    entry4 = md.entries[4]
    assert entry4.md_index_base == 4
    assert entry4.entid == 4
    entry5 = md.entries[5]
    assert entry5.md_index_base == 5
    assert entry5.entid == 5

    randomize_md_entry(entry1)
    randomize_md_entry(entry2)
    randomize_md_entry(entry3)
    randomize_md_entry(entry4)
    randomize_md_entry(entry5)
    randomize_md_entry(entry7)
    randomize_md_entry(entry8)
    randomize_md_entry(entry9)

    md.entries = [
        entry0,
        entry1,
        entry2,
        entry3,
        entry4,
        entry5,
        entry6,
        entry7,
        entry8,
        entry9,
    ]

    with open("./fixture.md", "wb") as f:
        f.write(MdHandler.load_python_writer()().write(md))

    for md_index, entry in enumerate(md.entries):
        print(
            f"ExpectedMdEntry("
            f"u32({md_index}), "
            f"u16({entry.entid}), "
            f"u16({entry.unk31}), "
            f"u16({entry.national_pokedex_number}), "
            f"u16({entry.base_movement_speed}), "
            f"u16({entry.pre_evo_index}), "
            f"u16({entry.evo_method}), "
            f"u16({entry.evo_param1}), "
            f"u16({entry.evo_param2}), "
            f"i16({entry.sprite_index}), "
            f"u8({entry.gender}), "
            f"u8({entry.body_size}), "
            f"u8({entry.type_primary}), "
            f"u8({entry.type_secondary}), "
            f"u8({entry.movement_type}), "
            f"u8({entry.iq_group}), "
            f"u8({entry.ability_primary}), "
            f"u8({entry.ability_secondary}), "
            f"u16({entry.exp_yield}), "
            f"i16({entry.recruit_rate1}), "
            f"u16({entry.base_hp}), "
            f"i16({entry.recruit_rate2}), "
            f"u8({entry.base_atk}), "
            f"u8({entry.base_sp_atk}), "
            f"u8({entry.base_def}), "
            f"u8({entry.base_sp_def}), "
            f"i16({entry.weight}), "
            f"i16({entry.size}), "
            f"u8({entry.unk17}), "
            f"u8({entry.unk18}), "
            f"i8({entry.shadow_size}), "
            f"i8({entry.chance_spawn_asleep}), "
            f"u8({entry.hp_regeneration}), "
            f"i8({entry.unk21_h}), "
            f"i16({entry.base_form_index}), "
            f"i16({entry.exclusive_item1}), "
            f"i16({entry.exclusive_item2}), "
            f"i16({entry.exclusive_item3}), "
            f"i16({entry.exclusive_item4}), "
            f"i16({entry.unk27}), "
            f"i16({entry.unk28}), "
            f"i16({entry.unk29}), "
            f"i16({entry.unk30}), "
            f"bool({entry.bitfield1_0}), "
            f"bool({entry.bitfield1_1}), "
            f"bool({entry.bitfield1_2}), "
            f"bool({entry.bitfield1_3}), "
            f"bool({entry.can_move}), "
            f"bool({entry.bitfield1_5}), "
            f"bool({entry.can_evolve}), "
            f"bool({entry.item_required_for_spawning}), "
            f")"
        )
