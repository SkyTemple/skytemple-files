#  Copyright 2020-2025 Capypara and the SkyTemple Contributors
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
import unittest

from explorerscript.ssb_converting.ssb_data_types import SsbOperation

from skytemple_files.common.ppmdu_config.xml_reader import Pmd2XmlReader
from skytemple_files.script.ssb.script_compiler import ScriptCompiler

# This is the jump test from ExplorerScript ported to skytemple-files to also test offset rewriting.

LOOPING_SCRIPT = """
def 0 {
    @foo;
    me_Stop();
    jump @foo;
    end;
}
"""

SELF_LOOPING_SCRIPT = """
def 0 {
    @foo;
    jump @foo;
    end;
}
"""


class StringTestCase(unittest.TestCase):
    """
    Tests compilation of jumps.
    """

    def test_looping_exps(self) -> None:
        routine_ops = self.compile_exps(LOOPING_SCRIPT)
        self.assertEqual(1, len(routine_ops))
        routine = routine_ops[0]
        self.assertEqual(3, len(routine))

        for op in routine_ops[0]:
            print(op)

        # FIRST OP
        op_to_check = routine[0]
        self.assertEqual("me_Stop", op_to_check.op_code.name)
        self.assertEqual(5, op_to_check.offset)
        self.assertEqual(0, len(op_to_check.params))

        # SECOND OP
        op_to_check = routine[1]
        self.assertEqual("Jump", op_to_check.op_code.name)
        self.assertEqual(6, op_to_check.offset)
        self.assertEqual(1, len(op_to_check.params))
        self.assertIs(5, op_to_check.params[0])

        # THIRD OP
        op_to_check = routine[2]
        self.assertEqual("End", op_to_check.op_code.name)
        self.assertEqual(8, op_to_check.offset)
        self.assertEqual(0, len(op_to_check.params))

    def test_self_looping_exps(self) -> None:
        routine_ops = self.compile_exps(SELF_LOOPING_SCRIPT)

        self.assertEqual(1, len(routine_ops))
        routine = routine_ops[0]
        self.assertEqual(2, len(routine))

        # FIRST OP
        op_to_check = routine[0]
        self.assertEqual("Jump", op_to_check.op_code.name)
        self.assertEqual(5, op_to_check.offset)
        self.assertEqual(1, len(op_to_check.params))
        self.assertIs(5, op_to_check.params[0])

        # SECOND OP
        op_to_check = routine[1]
        self.assertEqual("End", op_to_check.op_code.name)
        self.assertEqual(7, op_to_check.offset)
        self.assertEqual(0, len(op_to_check.params))

    def compile_exps(self, src: str) -> list[list[SsbOperation]]:
        static_data = Pmd2XmlReader.load_default()
        compiler = ScriptCompiler(static_data)

        ssb_after = compiler.compile_explorerscript(src, "")[0]

        return ssb_after.routine_ops
