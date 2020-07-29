#!/usr/bin/env python3
"""
This is a sample Python CLI script that uses SkyTemple Files to randomize starters.

This is also an example on how to modify hardcoded data and strings.

Based on mdrngzer.
"""
#  Copyright 2020 Parakoopa
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
import argparse
from decimal import Decimal
from random import randrange, choice
from typing import List

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu, set_binary_in_rom_ppmdu
from skytemple_files.data.md.model import NUM_ENTITIES

# 383, 384 -> Kecleons
from skytemple_files.data.str.model import Str
from skytemple_files.graphics.kao.model import SUBENTRIES, Kao
from skytemple_files.hardcoded.personality_test_starters import HardcodedPersonalityTestStarters

ALLOWED_MD_IDS = [x for x in range(1, 537) if x not in [383, 384]]


def random_gender(orig_value):
    """50% male (nothing added to index), 50% female (+600 added to index)"""
    if choice([True, False]):
        return orig_value + NUM_ENTITIES
    return orig_value


def get_name(string_file: Str, index: int, pokemon_string_data):
    """Returns a Pokémon name from the string file"""
    return string_file.strings[pokemon_string_data.begin + index]


def clone_missing_portraits(kao: Kao, index: int):
    """Fills all missing kao subindex slots for index with the first portrait."""
    cloned = kao.get(index, 0)
    # Skip mirrored slots.
    for i in range(2, SUBENTRIES, 2):
        if kao.get(index, i) is None:
            kao.set(index, i, cloned)


def run_main(rom_path, output_rom_path):
    print("Loading ROM...")
    rom = NintendoDSRom.fromFile(rom_path)
    config = get_ppmdu_config_for_rom(rom)

    overlay13 = get_binary_from_rom_ppmdu(rom, config.binaries['overlay/overlay_0013.bin'])
    lang = None
    for l in config.string_index_data.languages:
        if l.locale == 'en-US':
            lang = l
            break
    # If we didn't find english, just take the first
    if lang is None:
        lang = config.string_index_data.languages[0]
    pokemon_string_data = config.string_index_data.string_blocks["Pokemon Names"]
    string_file = FileType.STR.deserialize(rom.getFileByName(f'MESSAGE/{lang.filename}'))

    print("Randomizing partner...")
    orig_partner_ids = HardcodedPersonalityTestStarters.get_partner_md_ids(overlay13, config)
    new_partner_ids = [random_gender(choice(ALLOWED_MD_IDS)) for _ in range(0, len(orig_partner_ids))]
    HardcodedPersonalityTestStarters.set_partner_md_ids(new_partner_ids, overlay13, config)

    print("Randomizing player...")
    # The player options are put into two-pairs for each nature, first male then female.
    orig_player_ids = HardcodedPersonalityTestStarters.get_player_md_ids(overlay13, config)
    new_player_ids = []
    k = 0  # Index of text for "Will be..."
    for i in range(0, len(orig_player_ids)):
        new_id = choice(ALLOWED_MD_IDS)
        if k % 3 == 0:
            k += 1
        personality_message = f"Will be a [CS:K]{get_name(string_file, new_id, pokemon_string_data)}[CR]!"
        assert "Will be a" in string_file.strings[0x67C + k]
        string_file.strings[0x67C + k] = personality_message
        if i % 2 == 1:
            new_id += NUM_ENTITIES
        new_player_ids.append(new_id)
        k += 1
    HardcodedPersonalityTestStarters.set_player_md_ids(new_player_ids, overlay13, config)

    print("Cloning missing portraits...")
    kao = FileType.KAO.deserialize(rom.getFileByName('FONT/kaomado.kao'))
    for new in new_player_ids + new_partner_ids:
        new_base = new % 600
        clone_missing_portraits(kao, new_base - 1)

    print("Saving to ROM...")
    set_binary_in_rom_ppmdu(rom, config.binaries['overlay/overlay_0013.bin'], overlay13)
    rom.setFileByName(f'MESSAGE/{lang.filename}', FileType.STR.serialize(string_file))
    rom.setFileByName('FONT/kaomado.kao', FileType.KAO.serialize(kao))

    print(f"Saving output ROM to {output_rom_path}...")
    rom.saveToFile(output_rom_path)

    print("Success!")


def main():
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(description="""Randomize the starters in PMD EoS.

    Currently there are no settings. Both player and partner options are randomized""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input_rom', metavar='INPUT_ROM',
                        help='Path to the input ROM file.')
    parser.add_argument('output_rom', metavar='OUTPUT_ROM',
                        help='Path where the randomized output ROM should be saved.')

    args = parser.parse_args()

    run_main(args.input_rom, args.output_rom)


if __name__ == '__main__':
    main()
