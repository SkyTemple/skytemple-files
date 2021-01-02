"""Testing script for ExplorerScript's execution graphs."""
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
import hashlib
import os
import warnings

from ndspy.rom import NintendoDSRom

from explorerscript.ssb_converting.decompiler.graph_building.graph_minimizer import SsbGraphMinimizer
from explorerscript.ssb_converting.decompiler.label_jump_to_resolver import OpsLabelJumpToResolver
from skytemple_files.common.util import get_files_from_rom_with_extension
from skytemple_files.script.ssb.handler import SsbHandler


RENDER = True


def main():
    output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output', 'graphs')
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

    rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

    total_count_labels_before = 0
    total_count_labels_after = 0

    for file_name in get_files_from_rom_with_extension(rom, 'ssb'):
        print(file_name)

        bin_before = rom.getFileByName(file_name)
        ssb = SsbHandler.deserialize(bin_before)

        routine_ops = ssb.get_filled_routine_ops()

        resolver = OpsLabelJumpToResolver(routine_ops)
        routine_ops = list(resolver)

        grapher = SsbGraphMinimizer(routine_ops)
        total_count_labels_before += grapher.count_labels()
        draw_graphs(grapher, file_name, output_dir, 'before_optimize')

        grapher.optimize_paths()
        draw_graphs(grapher, file_name, output_dir, 'after_optimize')

        #grapher._graphs = [ grapher._graphs[86] ]
        grapher.build_branches()
        draw_graphs(grapher, file_name, output_dir, 'after_branch_before_group')
        grapher.group_branches()
        grapher.invert_branches()
        draw_graphs(grapher, file_name, output_dir, 'after_branch')

        grapher.build_and_group_switch_cases()
        grapher.group_switch_cases()
        grapher.build_switch_fallthroughs()
        draw_graphs(grapher, file_name, output_dir, 'after_switch')

        grapher.build_loops()
        draw_graphs(grapher, file_name, output_dir, 'after_loops')

        grapher.remove_label_markers()
        draw_graphs(grapher, file_name, output_dir, 'done')

        total_count_labels_after += grapher.count_labels()

    print("Total number labels before: " + str(total_count_labels_before))
    print("Total number labels after:  " + str(total_count_labels_after))


def draw_graphs(grapher, file_name, output_dir, run_name):
    local_output_dir = os.path.abspath(os.path.join(output_dir, run_name, file_name))
    print(f">> {run_name}")
    if not RENDER:
        return
    os.makedirs(local_output_dir, exist_ok=True)
    for i, graph in enumerate(grapher._graphs):
        dot_name = os.path.join(local_output_dir, f'{i}.dot')
        hash_dotfile_before = None
        if os.path.exists(dot_name):
            with open(dot_name, 'r') as f:
                hash_dotfile_before = hashlib.md5(f.read().encode('utf-8')).hexdigest()
        with open(dot_name, 'w') as f:
            graph.write_dot(f)
        with open(dot_name, 'r') as f:
            hash_dotfile_same = hashlib.md5(f.read().encode('utf-8')).hexdigest() == hash_dotfile_before
        unconnected_vertices = []
        if not hash_dotfile_same:
            print("Writing svg for " + dot_name)
            try:
                os.remove(os.path.join(local_output_dir, f'{i}.dot.svg'))
            except FileNotFoundError:
                pass
            os.chdir(local_output_dir)
            os.system(f'dot -Tsvg -O {i}.dot')
            print("done.")
        for v in graph.vs:
            if len(list(v.all_edges())) < 1 and v['name'] != 0:
                unconnected_vertices.append(v['label'])
        if len(unconnected_vertices) > 0:
            warnings.warn(f"[{file_name}] Routine {i} has unconnected ops: {unconnected_vertices}")


if __name__ == '__main__':
    main()
