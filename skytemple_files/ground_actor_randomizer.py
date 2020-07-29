#!/usr/bin/env python3
"""
This is a sample Python CLI script that uses SkyTemple Files to randomize the actors used in ground mode.
In addition portraits for the Pokémon the actors get randomized to are copied, if they don't have portraits for all the
emotions, and all text in the game referencing that Pokémon is replaced with the new Pokémon name.
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
from random import choice
from typing import Dict

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_ppmdu_config_for_rom, get_files_from_rom_with_extension
from skytemple_files.data.md.model import Gender
from skytemple_files.data.str.model import Str
from skytemple_files.graphics.kao.model import Kao, SUBENTRIES
from skytemple_files.list.actor.model import ActorListBin
from skytemple_files.patch.patches import Patcher
ALLOWED_ENTIDS = [*range(1, 537), *range(601, 1136)]


def randomize_actors(rom: NintendoDSRom, string_file, pokemon_string_data) -> Dict[int, int]:
    """Returns a dict that maps old entids -> new entids"""
    # noinspection PyTypeChecker
    # - Bug in PyCharm with bound TypeVars
    actor_list: ActorListBin = FileType.SIR0.unwrap_obj(
        FileType.SIR0.deserialize(rom.getFileByName('BALANCE/actor_list.bin')), ActorListBin
    )
    md = FileType.MD.deserialize(rom.getFileByName('BALANCE/monster.md'))

    mapped = {}
    # We want to map actors with the same name to the same ID
    mapped_for_names = {}
    old_entid_bases = [actor.entid % 600 for actor in actor_list.list]
    for actor in actor_list.list:
        if actor.entid > 0:
            old_name = get_name(string_file, actor.entid % 600, pokemon_string_data)
            if old_name in mapped_for_names.keys():
                new_entid = mapped_for_names[old_name]
            else:
                new_entid = choice(ALLOWED_ENTIDS)
                # Due to the way the string replacing works we don't want anything that previously existed.
                while md.get_by_index(new_entid).gender == Gender.INVALID or new_entid % 600 in old_entid_bases:
                    new_entid = choice(ALLOWED_ENTIDS)
            mapped[actor.entid] = new_entid
            mapped_for_names[old_name] = new_entid
            actor.entid = new_entid

    rom.setFileByName(
        'BALANCE/actor_list.bin', FileType.SIR0.serialize(FileType.SIR0.wrap_obj(actor_list))
    )
    return mapped


def get_name(string_file: Str, index: int, pokemon_string_data):
    """Returns a Pokémon name from the string file"""
    return string_file.strings[pokemon_string_data.begin + index]


def replace_strings(original: str, replacement_map: Dict[str, str]):
    """Replaces all strings from the replacement map in original and returns the new string"""
    string = original
    for old, new in replacement_map.items():
        string = string.replace(old, new)
    return string


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

    lang = None
    for l in config.string_index_data.languages:
        if l.locale == 'en-US':
            lang = l
            break
    # If we didn't find english, just take the first
    if lang is None:
        lang = config.string_index_data.languages[0]
    string_file = FileType.STR.deserialize(rom.getFileByName(f'MESSAGE/{lang.filename}'))
    pokemon_string_data = config.string_index_data.string_blocks["Pokemon Names"]

    print("Checking if patch needs to be applied...")
    patcher = Patcher(rom, config)
    if not patcher.is_applied('ActorAndLevelLoader'):
        print("Applying patch... - At time of writing this is only supported for US ROMs!")
        patcher.apply('ActorAndLevelLoader')

    print("Randomizing actor list...")
    mapped_actors = randomize_actors(rom, string_file, pokemon_string_data)

    print("Replacing all text in the main string file...")
    names_mapped = {}
    for old, new in mapped_actors.items():
        old_base = old % 600
        new_base = new % 600
        old_name = get_name(string_file, old_base, pokemon_string_data)
        new_name = get_name(string_file, new_base, pokemon_string_data)
        names_mapped[old_name] = new_name
    new_strings = []
    for idx, string in enumerate(string_file.strings):
        if idx < pokemon_string_data.begin or idx > pokemon_string_data.end:
            new_strings.append(replace_strings(string, names_mapped))
        else:
            new_strings.append(string)
    string_file.strings = new_strings
    rom.setFileByName(f'MESSAGE/{lang.filename}', FileType.STR.serialize(string_file))

    print("Replacing all text in the script files...")
    for file_path in get_files_from_rom_with_extension(rom, 'ssb'):
        script = FileType.SSB.deserialize(rom.getFileByName(file_path), config)
        script.constants = [replace_strings(string, names_mapped) for string in script.constants]
        for langname, strings in script.strings.items():
            script.strings[langname] = [replace_strings(string, names_mapped) for string in strings]
        rom.setFileByName(file_path, FileType.SSB.serialize(script, config))

    print("Cloning missing portraits...")
    kao = FileType.KAO.deserialize(rom.getFileByName('FONT/kaomado.kao'))
    for new in mapped_actors.values():
        new_base = new % 600
        clone_missing_portraits(kao, new_base - 1)
    rom.setFileByName('FONT/kaomado.kao', FileType.KAO.serialize(kao))

    print(f"Saving output ROM to {output_rom_path}...")
    rom.saveToFile(output_rom_path)

    print("Success!")


def main():
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(description="""Randomize the actors used in ground mode.

In addition portraits for the Pokémon the actors get randomized to are copied, if they don't have portraits for all the
emotions, and all text in the game referencing that Pokémon is replaced with the new Pokémon name.
        """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input_rom', metavar='INPUT_ROM',
                        help='Path to the input ROM file.')
    parser.add_argument('output_rom', metavar='OUTPUT_ROM',
                        help='Path where the randomized output ROM should be saved.')

    args = parser.parse_args()

    run_main(args.input_rom, args.output_rom)


if __name__ == '__main__':
    main()
