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
from typing import TYPE_CHECKING, List

from explorerscript.ssb_converting.decompiler.graph_building.graph_minimizer import SsbGraphMinimizer
from explorerscript.ssb_converting.decompiler.label_jump_to_resolver import OpsLabelJumpToResolver
from explorerscript.ssb_converting.ssb_data_types import SsbOperation, SsbOpCode, SsbCalcOperator
from explorerscript.ssb_converting.ssb_special_ops import OPS_WITH_JUMP_TO_MEM_OFFSET, OP_BRANCH_VARIATION, \
    SsbLabelJump, OPS_THAT_END_CONTROL_FLOW, OP_RETURN, OPS_FLAG__CALC_VALUE, OPS_FLAG__SET, OP_BRANCH_BIT, \
    OP_BRANCH_PERFORMANCE, SsbForeignLabel
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.script.ssb.constants import SsbConstant
from skytemple_files.script.ssb.model import Ssb

if TYPE_CHECKING:
    from igraph import Vertex


class SsbFlow:
    """
    Represents the flow of all Ssb routines as a graph. It can be compared with other graphs,
    to check if two Ssb models are logically the same.
    This uses the same base mechanisms / graphing logic as the ExplorerScript compiler.
    """
    def __init__(self, ssb: Ssb, static_data: Pmd2Data):
        self._named_routines = static_data.script_data.common_routine_info__by_id
        self._variables_by_name = static_data.script_data.game_variables__by_name
        routine_ops: List[List[SsbOperation]] = list(OpsLabelJumpToResolver(ssb.get_filled_routine_ops()))

        # Check if the last operation ends control flow, if it doesn't, insert a return for more accurate
        # checking with ExplorerScript opcode order changes.
        for r in routine_ops:
            if len(r) > 0:
                if r[-1].op_code.name not in OPS_THAT_END_CONTROL_FLOW:
                    r.append(SsbOperation(9999, SsbOpCode(-1, OP_RETURN), []))

        # Build and optimize execution graph
        self._grapher = SsbGraphMinimizer(routine_ops)
        self._grapher.optimize_paths()
        self._grapher.remove_all_labels_and_simple_jumps()

    def to_dot(self, directory_name: str):
        """Exports all graphs to directory_name as dot files. The directory is created, if it doesn't exist."""
        os.makedirs(directory_name, exist_ok=True)
        for i, g in enumerate(self.get_graphs()):
            g.write_dot(os.path.join(directory_name, f'{i}.dot'))

    def get_graphs(self):
        return self._grapher.get_graphs()

    def assert_equal(self, other, output_print=True):
        """Assert that self and other are equal. If they are not, the raised AssertionError will contain details."""
        if not isinstance(other, SsbFlow):
            raise AssertionError("other is not an SsbFlow.")
        for i, (g_self, g_other) in enumerate(zip(self.get_graphs(), other.get_graphs())):
            if output_print:
                print(f"Checking routine {i}...")
            if len(g_self.vs) == 0 or len(g_other.vs) == 0:
                assert len(g_self.vs) == len(g_other.vs), f"If one graph is empty, " \
                                                          f"the other must be too ({self._r_info(i)})"
                continue
            self_iter = iter(self.bfs_generator(g_self.vs[0]))
            other_iter = iter(self.bfs_generator(g_other.vs[0]))
            # iterators yield: (current vertex, distance from root, parent vertex)
            try:
                while True:
                    self_v, self_distance, self_parent = next(self_iter)
                    other_v, other_distance, other_parent = next(other_iter)
                    assert self_distance == other_distance, f"While running BFS, the distances changed unexpectedly " \
                                                            f"({self._r_info(i)})."
                    self._assert_same_vertex(i, self_v, other_v)
                    self._assert_same_vertex(i, self_parent, other_parent)
            except StopIteration:
                # Both need to be ended
                assert self._iter_is_at_end(self_iter), f"The other graph ended to early ({self._r_info(i)})."
                assert self._iter_is_at_end(other_iter), f"My graph ended to early ({self._r_info(i)})."

    def _assert_same_vertex(self, i, self_v: 'Vertex', other_v: 'Vertex'):
        if self_v is None or other_v is None:
            assert self_v == other_v, f"Both must be None {self._r_info(i)}"
            return

        self_op: SsbOperation = self_v['op']
        other_op: SsbOperation = other_v['op']
        # We can't really check foreign jumps
        if isinstance(self_op, SsbForeignLabel) or isinstance(other_op, SsbForeignLabel):
            assert isinstance(self_op, SsbForeignLabel) and isinstance(other_op, SsbForeignLabel), \
                f"If one is foreign label, both must be ({self._r_info(i)})."
            return
        # If this is a label jump, take root.
        if hasattr(self_op, 'root'):
            self_op = self_op.root
        if hasattr(other_op, 'root'):
            other_op = other_op.root
            
        # OPCODES EXCEPTIONS
        # We replace flag_CalcValue with the ASSIGN operator with flag_Set
        if self_op.op_code.name == OPS_FLAG__CALC_VALUE and self_op.params[1] == SsbCalcOperator.ASSIGN.value:
            self_op.op_code = SsbOpCode(-1, OPS_FLAG__SET)
            self_op.params = [self_op.params[0], self_op.params[2]]
        if other_op.op_code.name == OPS_FLAG__CALC_VALUE and other_op.params[1] == SsbCalcOperator.ASSIGN.value:
            other_op.op_code = SsbOpCode(-1, OPS_FLAG__SET)
            other_op.params = [other_op.params[0], other_op.params[2]]
        # We replace BranchBit + PERFORMANCE_PROGRESS_LIST with BranchPerformance
        if self_op.op_code.name == OP_BRANCH_BIT and self_op.params[0].name == SsbConstant.create_for(self._variables_by_name['PERFORMANCE_PROGRESS_LIST']).name:
            self_op.op_code.name = SsbOpCode(-1, OP_BRANCH_PERFORMANCE)
            self_op.params = [self_op.params[1], 1]
        if other_op.op_code.name == OP_BRANCH_BIT and other_op.params[0].name == SsbConstant.create_for(self._variables_by_name['PERFORMANCE_PROGRESS_LIST']).name:
            other_op.op_code.name = SsbOpCode(-1, OP_BRANCH_PERFORMANCE)
            other_op.params = [other_op.params[1], 1]

        assert self_op.op_code.name == other_op.op_code.name, f"Opcodes were not the same: {self_op.op_code.name} " \
                                                              f"vs. {other_op.op_code.name} [{self_v.index}," \
                                                              f"{other_v.index}] ({self._r_info(i)})."

        self_op_params = self_op.params
        other_op_params = other_op.params
        # PARAMETER EXCEPTIONS:
        # We force BranchVariation to be a boolean, because the game seems to treat it as such too.
        if self_op.op_code.name == OP_BRANCH_VARIATION:
            if self_op_params[0] > 1:
                self_op_params[0] = 1
            if other_op_params[0] > 1:
                other_op_params[0] = 1

        assert self_op_params == other_op_params, f"Parameters of opcode ({self_op.op_code.name}) [{self_v.index}," \
                                                  f"{other_v.index}] are not the same ({self._r_info(i)})."

    def __eq__(self, other):
        try:
            self.assert_equal(other, False)
        except AssertionError:
            return False
        return True

    @staticmethod
    def _iter_is_at_end(iterator):
        try:
            next(iterator)
        except StopIteration:
            return True
        return False

    def _r_info(self, i):
        return f"Routine {i} (coro name {self._named_routines[i]})"

    @staticmethod
    def bfs_generator(start: 'Vertex'):
        """
        Basically the same as graph.bfsiter with advanced (but as a generator).
        However the order of vertices honors the flow_level of it's in edge. It also takes special Ssb flow
        rules into account.
        """
        already_visited = set()
        next_vertices = [(start, 0, None)]
        while len(next_vertices) > 0:
            nxt, distance, parent = next_vertices.pop()

            yield nxt, distance, parent

            # Don't loop.
            if nxt.index in already_visited:
                continue
            already_visited.add(nxt.index)

            for e in sorted(nxt.out_edges(), key=lambda e: e['flow_level']):
                next_vertices.append((e.target_vertex, distance + 1, e.source_vertex))
