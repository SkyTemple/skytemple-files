"""
Specialized script to find offsets in the JP ROM based on the blocks in the EU ROM.
Uses the tools in pmdsky-debug.
I know it's a bit silly to use subprocess for this, since they are also just Python scripts
but I wanted a bit of a challenge, *shrugs*.

Parameters via env vars:
JP_ROM: Japanese ROM path
EU_ROM: European ROM path
"""

import os
import subprocess
import sys
from glob import glob
from tempfile import TemporaryDirectory
from typing import Tuple, Optional
import re

import yaml
from ndspy.rom import NintendoDSRom

INTERESTING_BLOCKS = [
    "CART_REMOVED_IMG_DATA",
    "DEFAULT_PARTNER_ID",
    "DEFAULT_HERO_ID",
    "PARTNER_START_LEVEL",
    "HERO_START_LEVEL",
    "SPECIAL_EPISODE_MAIN_CHARACTERS",
    "BURN_DAMAGE_COOLDOWN",
    "POISON_DAMAGE_COOLDOWN",
    "BAD_POISON_DAMAGE_COOLDOWN",
    "GINSENG_CHANCE_3",
    "BELLY_LOST_PER_TURN",
    "BELLY_DRAIN_IN_WALLS_INT",
    "BELLY_DRAIN_IN_WALLS_THOUSANDTHS",
    "MUSIC_ID_TABLE",
    "RANDOM_MUSIC_ID_TABLE",
    "DUNGEON_DATA_LIST",
    "DUNGEON_RESTRICTIONS",
    "SECONDARY_TERRAIN_TYPES",
    "MAP_MARKER_PLACEMENTS",
    "TILESET_PROPERTIES",
    "FIXED_ROOM_ITEM_SPAWN_TABLE",
    "FIXED_ROOM_ENTITY_SPAWN_TABLE",
    "FIXED_ROOM_TILE_SPAWN_TABLE",
    "FIXED_ROOM_REVISIT_OVERRIDES",
    "FIXED_ROOM_MONSTER_SPAWN_TABLE",
    "FIXED_ROOM_PROPERTIES_TABLE",
    "FIXED_ROOM_REVISIT_OVERRIDES",
    "LEVEL_TILEMAP_LIST",
    "LIFE_SEED_HP_BOOST",
    "SITRUS_BERRY_HP_RESTORATION",
    "ORAN_BERRY_HP_RESTORATION",
    "MIN_IQ_EXCLUSIVE_MOVE_USER",
    "MIN_IQ_ITEM_MASTER",
    "INTIMIDATOR_ACTIVATION_CHANCE",
    "IQ_GUMMI_GAIN_TABLE",
    "GUMMI_BELLY_RESTORE_TABLE",
    "WONDER_GUMMI_IQ_GAIN",
    "JUICE_BAR_NECTAR_IQ_GAIN",
    "NECTAR_IQ_BOOST",
    "IQ_SKILLS",
    "IQ_GROUP_SKILLS",
    "IQ_SKILL_RESTRICTIONS",
    "TOP_MENU_MUSIC_ID",
    "TOP_MENU_RETURN_MUSIC_ID",
    "MONSTER_SPRITE_DATA",
    "STARTERS_PARTNER_IDS",
    "STARTERS_HERO_IDS",
    "RANK_UP_TABLE",
    "RECRUITMENT_TABLE_SPECIES",
    "RECRUITMENT_TABLE_LOCATIONS",
    "RECRUITMENT_TABLE_LEVELS",
    "LEVEL_TILEMAP_LIST",
    "SPAWN_COOLDOWN",
    "SPAWN_COOLDOWN_THIEF_ALERT",
    "TACTICS_UNLOCK_LEVEL_TABLE",
    "TEXT_SPEED",
    "DUNGEON_PTR",
    "MEMORY_ALLOCATION_TABLE",
    "SCRIPT_VARS_VALUES",
    "GAME_STATE_VALUES",
    "LANGUAGE_INFO_DATA",
    "GAME_MODE",
    "DEBUG_SPECIAL_EPISODE_NUMBER",
    "NOTIFY_NOTE",
    "GROUND_STATE_MAP",
    "GROUND_STATE_PTRS",
    "UNIONALL_RAM_ADDRESS",
]

JP_ROM = os.getenv('JP_ROM', '/tmp/rom_jp.nds')
EU_ROM = os.getenv('EU_ROM', '/tmp/rom_eu.nds')
OFFSETS_REGEX = re.compile(r'0[xX]([\da-fA-F]+) \(absolute\): 0[xX]([\da-fA-F]+)')
ARM5FIND_REGEX = re.compile(r' {2}- \[(.*?)]: 0[xX]([\da-fA-F]+)\.\.0[xX]([\da-fA-F]+)')

THRESHOLD = 0x08


class RomDir:
    """Temporary directory context manager"""
    def __init__(self, rom_path: str):
        self.tempdir = TemporaryDirectory()
        self.rom = NintendoDSRom.fromFile(rom_path)

    def __enter__(self):
        self.tempdir.__enter__()
        with open(os.path.join(self.tempdir.name, 'arm9.bin'), 'wb') as f:
            f.write(self.rom.arm9)
        for ov_id, ov in self.rom.loadArm9Overlays().items():
            with open(os.path.join(self.tempdir.name, f'overlay{ov_id}.bin'), 'wb') as f:
                f.write(ov.data)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.tempdir.__exit__(exc_type, exc_val, exc_tb)

    def get(self, path: str) -> str:
        return os.path.join(self.tempdir.name, path + ".bin")


def path_to(path: str) -> str:
    """
    Return the path to the given file relative to this file.
    """
    return os.path.join(os.path.dirname(__file__), path)


def call(args: list[str]) -> Tuple[int, str]:
    """
    Call the command line tool with the given arguments and print
    out the command output.
    Returns both the return code and stdout.
    """
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret = result.stdout.decode('utf-8')
    #print("$ " + " ".join(args) + " -> " + str(result.returncode))
    #print(ret)
    #print(result.stderr.decode('utf-8'), file=sys.stderr)
    return result.returncode, ret


def call_checked(args: list[str]) -> str:
    code, ret = call(args)
    assert code == 0
    return ret


def run_offsets(version: str, binary: str, offset: int) -> int:
    """
    Run the offset finder for the given version and binary.
    """
    args = [
        'python',
        path_to('../skytemple_files/_resources/pmdsky-debug/tools/offsets.py'),
        '-v', version,
        '-b', binary,
        str(offset),
    ]
    result = call_checked(args)
    try:
        return int(OFFSETS_REGEX.match(result.splitlines()[-1]).group(2), 16)
    except Exception:
        print(f"Failed to find offset from output:\n{result}", file=sys.stderr)
        raise


def run_arm5find(offset: int, length: int, source: str, target: str) -> list[int]:
    args = [
        'python',
        path_to('../skytemple_files/_resources/pmdsky-debug/tools/arm5find.py'),
        '-d', str(offset), str(length),
        source, target
    ]
    res = call_checked(args)
    matches = []
    for line in res.splitlines():
        match = ARM5FIND_REGEX.match(line)
        if match:
            assert int(match.group(3), 16) - int(match.group(2), 16) == length
            matches.append(int(match.group(2), 16))
    return matches


def save_yml(path: str, data: dict):
    with open(path, 'w') as f:
        yaml.dump(data, f)
    call_checked([
        "cargo", "run", "--release",
        f"--manifest-path={path_to('../skytemple_files/_resources/pmdsky-debug/Cargo.toml')}",
        "fmt", path
    ])


def process(
        block_name: str, binary_name: str,
        addresses_dict: dict, length_dict: Optional[dict],
        eu_address: int, length: int,
        rom_dir_eu: RomDir, rom_dir_jp: RomDir,
        jp_binary_start_addr: int
):
    print(f">> {block_name} in {binary_name}")
    print(f"   Length: 0x{length:0x}")
    print(f"   EU adr: 0x{eu_address:0x}")

    # We might add padding in our search if the length is below a threshold.
    offset_in_search = 0
    orig_length = length
    if length < THRESHOLD:
        offset_in_search = THRESHOLD // 2
        eu_address -= offset_in_search
        length = THRESHOLD

    translated_search_offset = run_offsets('eu', binary_name, eu_address)
    found_offsets = run_arm5find(translated_search_offset, length, rom_dir_eu.get(binary_name), rom_dir_jp.get(binary_name))
    translated_found_offsets = [jp_binary_start_addr + x for x in found_offsets]

    if len(translated_found_offsets) < 1:
        print("-- No matches found.")
    elif len(translated_found_offsets) == 1:
        print(f"++ Found! 0x{translated_found_offsets[0]:0x}")
        addresses_dict["JP"] = jp_binary_start_addr + translated_found_offsets[0] + offset_in_search
        if length_dict is not None:
            length_dict["JP"] = orig_length
        return True
    else:
        print("?? Multiple matches found: " + ", ".join(f"0x{x:0x}" for x in translated_found_offsets))

    return False


def main():
    found = set()
    with RomDir(EU_ROM) as rom_dir_eu:
        with RomDir(JP_ROM) as rom_dir_jp:
            print(f"Pre-processing...")
            # We pre-process the JP offsets since the literal file doesn't contain them
            binary_jp_addresses = {}
            for yml_path in glob(path_to('../skytemple_files/_resources/pmdsky-debug/symbols/*.yml')):
                with open(yml_path) as f:
                    yml = yaml.load(f, Loader=yaml.SafeLoader)
                    for binary_name, binary in yml.items():
                        if "address" in binary and "JP" in binary["address"]:
                            binary_jp_addresses[binary_name] = binary["address"]["JP"]

            for yml_path in glob(path_to('../skytemple_files/_resources/pmdsky-debug/symbols/*.yml')):
                print(f"Processing {yml_path}...")
                with open(yml_path) as f:
                    yml = yaml.load(f, Loader=yaml.SafeLoader)
                    changed = False

                    for binary_name, binary in yml.items():
                        if "data" in binary:
                            for blk in binary["data"]:
                                if blk["name"] in INTERESTING_BLOCKS and "EU" in blk["address"]:
                                    eu_address = blk["address"]["EU"]
                                    if yml_path.endswith("ram.yml"):
                                        print(f">> {blk['name']} in {binary_name}")
                                        print("-- can not determine RAM values.")
                                        continue
                                    if "JP" in blk["address"]:
                                        print(f">> {blk['name']} in {binary_name}")
                                        found.add(blk["name"])
                                        print("-- skipped, already exists.")
                                        continue
                                    if "length" in blk:
                                        length = blk["length"]["EU"]
                                        if "NA" in blk["length"]:
                                            if blk["length"]["NA"] != blk["length"]["EU"]:
                                                print(f">> {blk['name']} in {binary_name}")
                                                print(f'-- Warning: Skipped: NA [{blk["length"]["NA"]}] '
                                                      f'and EU [{blk["length"]["EU"]}] length not the same.')
                                                continue
                                    else:
                                        length = 1
                                    processed = process(
                                        blk['name'], binary_name,
                                        blk["address"], blk["length"] if "length" in blk else None,
                                        eu_address, length,
                                        rom_dir_eu, rom_dir_jp,
                                        binary_jp_addresses[binary_name]
                                    )
                                    if processed:
                                        found.add(blk["name"])
                                    changed = changed or processed

                    if changed:
                        pass  # todo save_yml(yml_path, yml)

            print("Missed:")
            print(set(INTERESTING_BLOCKS) - found)


if __name__ == '__main__':
    main()
