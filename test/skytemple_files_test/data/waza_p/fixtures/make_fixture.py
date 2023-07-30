import random

from range_typed_integers import u16, u8, u32

from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.data.md.protocol import PokeType

from skytemple_files.data.waza_p._model import LevelUpMove, MoveLearnset, WazaMove, WazaMoveRangeSettings
from skytemple_files.data.waza_p.handler import WazaPHandler
from skytemple_files.data.waza_p.protocol import WazaMoveCategory


def randomize_level_up_move() -> LevelUpMove:
    return LevelUpMove(
        u16(random.randint(1, 65_535)), u16(random.randint(1, 65_535))
    )


def randomize_move_learnset() -> MoveLearnset:
    level_up = []
    for _ in range(0, random.randint(0, 500)):
        level_up.append(randomize_level_up_move())
    tm_hm = []
    for _ in range(0, random.randint(0, 500)):
        tm_hm.append(u32(random.randint(1, 65_535)))
    egg = []
    for _ in range(0, random.randint(0, 500)):
        egg.append(u32(random.randint(1, 65_535)))
    return MoveLearnset(level_up, tm_hm, egg)


def randomize_move() -> WazaMove:
    move = WazaMove.__new__(WazaMove)
    move.base_power = u16(random.randint(0, 65_535))
    move.type = u8(random.choice(list(PokeType)).value)
    move.category = u8(random.choice(list(WazaMoveCategory)).value)
    move.settings_range = WazaMoveRangeSettings(random.randint(0, 65_535).to_bytes(2, 'little'))
    move.settings_range_ai = WazaMoveRangeSettings(random.randint(0, 65_535).to_bytes(2, 'little'))
    move.base_pp = u8(random.randint(0, 255))
    move.ai_weight = u8(random.randint(0, 255))
    move.miss_accuracy = u8(random.randint(0, 255))
    move.accuracy = u8(random.randint(0, 255))
    move.ai_condition1_chance = u8(random.randint(0, 255))
    move.number_chained_hits = u8(random.randint(0, 255))
    move.max_upgrade_level = u8(random.randint(0, 255))
    move.crit_chance = u8(random.randint(0, 255))
    move.affected_by_magic_coat = bool(random.randint(0, 1))
    move.is_snatchable = bool(random.randint(0, 1))
    move.uses_mouth = bool(random.randint(0, 1))
    move.ai_frozen_check = bool(random.randint(0, 1))
    move.ignores_taunted = bool(random.randint(0, 1))
    move.range_check_text = u8(random.randint(0, 255))
    move.move_id = u16(random.randint(0, 65_535))
    move.message_id = u8(random.randint(0, 255))
    return move


if __name__ == "__main__":
    waza_p = WazaPHandler.load_python_model().__new__(WazaPHandler.load_python_model())
    waza_p.moves = []
    waza_p.learnsets = []

    for _ in range(0, 559):
        waza_p.moves.append(randomize_move())

    for _ in range(0, 800):
        waza_p.learnsets.append(randomize_move_learnset())

    with open("./fixture.bin", "wb") as f:
        f.write(Sir0Handler.serialize(Sir0Handler.wrap(*waza_p.sir0_serialize_parts())))

    print("# fmt: off")
    print("# pylint: disable-all")
    print("# nopycln: file")
    print("")
    print("from skytemple_files_test.data.waza_p.fixture import *")
    print("")

    print("FIX_MOVES_BYTES = (")
    for entry in waza_p.moves:
        print(f"    {repr(entry.to_bytes())},")
    print(")")
    print("")
    print("FIX_MOVES = (")
    for entry in waza_p.moves:
        print(f"    WazaMoveStub.stub_new("
              f"u16({entry.base_power}), "
              f"u8({entry.type}), "
              f"u8({entry.category}), "
              f"{int(entry.settings_range)}, "
              f"{int(entry.settings_range_ai)}, "
              f"u8({entry.base_pp}), "
              f"u8({entry.ai_weight}), "
              f"u8({entry.miss_accuracy}), "
              f"u8({entry.accuracy}), "
              f"u8({entry.ai_condition1_chance}), "
              f"u8({entry.number_chained_hits}), "
              f"u8({entry.max_upgrade_level}), "
              f"u8({entry.crit_chance}), "
              f"{entry.affected_by_magic_coat}, "
              f"{entry.is_snatchable}, "
              f"{entry.uses_mouth}, "
              f"{entry.ai_frozen_check}, "
              f"{entry.ignores_taunted}, "
              f"u8({entry.range_check_text}), "
              f"u16({entry.move_id}), "
              f"u8({entry.message_id}), "
              f"),")
    print(")")
    print("")
    print("FIX_LEARNSETS = (")
    for entry in waza_p.learnsets:
        print(f"    WazaLearnsetStub.stub_new(\n"
              f"        [{', '.join([f'LevelUpMoveStub.stub_new({m.level_id}, {m.move_id})' for m in entry.level_up_moves])}],\n"
              f"        {repr(entry.tm_hm_moves)},\n"
              f"        {repr(entry.egg_moves)},\n"
              f"    ),")
    print(")")
