#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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
import os
import sys

from ndspy.rom import NintendoDSRom
from skytemple_rust.pmd_wan import AnimationFrame

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_files_from_rom_with_extension

output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

# Object sprites
for path in get_files_from_rom_with_extension(rom, 'wan'):
    if path.startswith('FONT'):
        continue
    print(path)
    basename = os.path.basename(path)

    try:
        wan_bin = rom.getFileByName(path)
        wan_model = FileType.WAN.deserialize(wan_bin)
    except ValueError as e:
        print(f"FATAL Error for {basename}: {e}", file=sys.stderr)
        continue

    os.makedirs(os.path.join(output_dir, basename), exist_ok=True)
    for ag_i, group in enumerate(wan_model.anim_groups):
        if group is None:
            continue
        for ani_i, ani in enumerate(wan_model.get_animations_for_group(group)):
            mfg_id = wan_model.frame_groups[ani.frames[0].frame_id]
            try:
                img, (cx, cy) = wan_model.render_frame_group(mfg_id)
                img.save(os.path.join(output_dir, basename, f'{ag_i}_{ani_i}.png'))
            except ValueError as e:
                print(f"Error for {basename}/{ag_i}_{ani_i}: {e}", file=sys.stderr)

# Actor Sprites
pack_file = rom.getFileByName('MONSTER/monster.bin')
bin_pack = FileType.BIN_PACK.deserialize(pack_file)
for s_i, sprite in enumerate(bin_pack):
    print(f"Actor kind {s_i}")
    sprite_bin_decompressed = FileType.COMMON_AT.deserialize(sprite).decompress()
    wan_model = FileType.WAN.deserialize(sprite_bin_decompressed)
    basename = f'actor_{s_i}'

    os.makedirs(os.path.join(output_dir, basename), exist_ok=True)
    for ag_i, group in enumerate(wan_model.anim_groups):
        if group is None:
            continue
        for ani_i, ani in enumerate(wan_model.get_animations_for_group(group)):
            mfg_id = wan_model.frame_groups[ani.frames[0].frame_id]
            try:
                img, (cx, cy) = wan_model.render_frame_group(mfg_id)
                img.save(os.path.join(output_dir, basename, f'{ag_i}_{ani_i}.png'))
            except ValueError as e:
                print(f"Error for {basename}/{ag_i}_{ani_i}: {e}", file=sys.stderr)
