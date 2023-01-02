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
# mypy: ignore-errors
from __future__ import annotations

import sys

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_ppmdu_config_for_rom
from skytemple_files.hardcoded.guest_pokemon import (
    ExtraDungeonDataList,
    GuestPokemon,
    GuestPokemonList,
)


def main():
    rom_path = sys.argv[1]
    rom = NintendoDSRom.fromFile(rom_path)
    config = get_ppmdu_config_for_rom(rom)
    arm9 = rom.arm9
    original_arm9 = arm9[0 : len(arm9)]

    extra_dungeon_data = ExtraDungeonDataList.read(arm9, config)
    guest_pokemon_data = GuestPokemonList.read(arm9, config)

    ExtraDungeonDataList.write(extra_dungeon_data, arm9, config)
    GuestPokemonList.write(guest_pokemon_data, arm9, config)

    extra_dungeon_data2 = ExtraDungeonDataList.read(arm9, config)
    guest_pokemon_data2 = GuestPokemonList.read(arm9, config)

    assert extra_dungeon_data == extra_dungeon_data2
    assert guest_pokemon_data == guest_pokemon_data2

    guest_pokemon_data.append(
        GuestPokemon(0, 64, 0, [1, 2, 3, 4], 901, 50, 255, 100, 102, 77, 88, 0, 0)
    )
    GuestPokemonList.write(guest_pokemon_data, arm9, config)
    guest_pokemon_data2 = GuestPokemonList.read(arm9, config)
    assert guest_pokemon_data == guest_pokemon_data2

    guest_pokemon_data2.pop(-1)
    GuestPokemonList.write(guest_pokemon_data2, arm9, config)
    assert original_arm9 == arm9


if __name__ == "__main__":
    main()
