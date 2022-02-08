#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
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
from skytemple_files.audio.swdl.handler import SwdlHandler
from skytemple_files.audio.swdl.protocol import SwdlProtocol
from skytemple_files.test.case import SkyTempleFilesTestCase, romtest


# TODO: Non romtests
class SwdlTestCase(SkyTempleFilesTestCase[SwdlHandler, SwdlProtocol]):
    handler = SwdlHandler

    @romtest(file_ext='swd', path='SOUND/BGM')
    def test_using_rom(self, _, file):
        before = self.handler.deserialize(file)
        after = self.handler.deserialize(self.handler.serialize(before))

        self.assertEqual(before.header.version, after.header.version)
        self.assertEqual(before.header.unk1, after.header.unk1)
        self.assertEqual(before.header.unk2, after.header.unk2)
        self.assertEqual(before.header.modified_date, after.header.modified_date)
        self.assertEqual(before.header.file_name, after.header.file_name)
        self.assertEqual(before.header.unk13, after.header.unk13)
        self.assertEqual(before.header.pcmdlen.ref, after.header.pcmdlen.ref)
        self.assertEqual(before.header.pcmdlen.external, after.header.pcmdlen.external)
        self.assertEqual(before.header.unk17, after.header.unk17)

        self.assertEqual(len(before.wavi.sample_info_table), len(after.wavi.sample_info_table))
        for b_site, a_site in zip(before.wavi.sample_info_table, after.wavi.sample_info_table):
            if b_site is None:
                self.assertIsNone(a_site)
            else:
                self.assertIsNotNone(a_site)
                self.assertEqual(b_site.id, a_site.id)
                self.assertEqual(b_site.ftune, a_site.ftune)
                self.assertEqual(b_site.ctune, a_site.ctune)
                self.assertEqual(b_site.rootkey, a_site.rootkey)
                self.assertEqual(b_site.ktps, a_site.ktps)
                self.assertEqual(b_site.volume, a_site.volume)
                self.assertEqual(b_site.pan, a_site.pan)
                self.assertEqual(b_site.unk5, a_site.unk5)
                self.assertEqual(b_site.unk58, a_site.unk58)
                self.assertEqual(b_site.sample_format, a_site.sample_format)
                self.assertEqual(b_site.unk9, a_site.unk9)
                self.assertEqual(b_site.loop, a_site.loop)
                self.assertEqual(b_site.unk10, a_site.unk10)
                self.assertEqual(b_site.unk11, a_site.unk11)
                self.assertEqual(b_site.unk12, a_site.unk12)
                self.assertEqual(b_site.unk13, a_site.unk13)
                self.assertEqual(b_site.sample_rate, a_site.sample_rate)
                if b_site.sample is None:
                    self.assertIsNone(a_site.sample)
                else:
                    self.assertIsNotNone(a_site.sample)
                    self.assertEqual(b_site.sample.offset, a_site.sample.offset)
                    self.assertEqual(b_site.sample.length, a_site.sample.length)
                    if b_site.sample.pcmd is None:
                        self.assertIsNone(a_site.sample.pcmd)
                    else:
                        self.assertIsNotNone(a_site.sample.pcmd)
                        self.assertEqual(b_site.sample.pcmd.chunk_data, a_site.sample.pcmd.chunk_data)
                self.assertEqual(b_site.loop_begin_pos, a_site.loop_begin_pos)
                self.assertEqual(b_site.loop_length, a_site.loop_length)
                self.assertEqual(b_site.envelope, a_site.envelope)
                self.assertEqual(b_site.envelope_multiplier, a_site.envelope_multiplier)
                self.assertEqual(b_site.unk19, a_site.unk19)
                self.assertEqual(b_site.unk20, a_site.unk20)
                self.assertEqual(b_site.unk21, a_site.unk21)
                self.assertEqual(b_site.unk22, a_site.unk22)
                self.assertEqual(b_site.attack_volume, a_site.attack_volume)
                self.assertEqual(b_site.attack, a_site.attack)
                self.assertEqual(b_site.decay, a_site.decay)
                self.assertEqual(b_site.sustain, a_site.sustain)
                self.assertEqual(b_site.hold, a_site.hold)
                self.assertEqual(b_site.decay2, a_site.decay2)
                self.assertEqual(b_site.release, a_site.release)
                self.assertEqual(b_site.unk57, a_site.unk57)

        if before.pcmd is None:
            self.assertIsNone(after.pcmd)
        else:
            self.assertIsNotNone(after.pcmd)
            self.assertEqual(before.pcmd.chunk_data, after.pcmd.chunk_data)


        if before.prgi is None:
            self.assertIsNone(after.prgi)
        else:
            self.assertIsNotNone(after.prgi)
            self.assertEqual(len(before.prgi.program_table), len(after.prgi.program_table))
            for b_program, a_program in zip(before.prgi.program_table, after.prgi.program_table):
                if b_program is None:
                    self.assertIsNone(a_program)
                else:
                    self.assertIsNotNone(a_program)
                    self.assertEqual(b_program.id, a_program.id)
                    self.assertEqual(b_program.prg_volume, a_program.prg_volume)
                    self.assertEqual(b_program.prg_pan, a_program.prg_pan)
                    self.assertEqual(b_program.unk3, a_program.unk3)
                    self.assertEqual(b_program.that_f_byte, a_program.that_f_byte)
                    self.assertEqual(b_program.unk4, a_program.unk4)
                    self.assertEqual(b_program.unk5, a_program.unk5)
                    self.assertEqual(b_program.unk7, a_program.unk7)
                    self.assertEqual(b_program.unk8, a_program.unk8)
                    self.assertEqual(b_program.unk9, a_program.unk9)
                    self.assertEqual(len(b_program.lfos), len(a_program.lfos))
                    for b_lfo, a_lfo in zip(b_program.lfos, a_program.lfos):
                        self.assertEqual(b_lfo.unk34, a_lfo.unk34)
                        self.assertEqual(b_lfo.unk52, a_lfo.unk52)
                        self.assertEqual(b_lfo.dest, a_lfo.dest)
                        self.assertEqual(b_lfo.wshape, a_lfo.wshape)
                        self.assertEqual(b_lfo.rate, a_lfo.rate)
                        self.assertEqual(b_lfo.unk29, a_lfo.unk29)
                        self.assertEqual(b_lfo.depth, a_lfo.depth)
                        self.assertEqual(b_lfo.delay, a_lfo.delay)
                        self.assertEqual(b_lfo.unk32, a_lfo.unk32)
                        self.assertEqual(b_lfo.unk33, a_lfo.unk33)
                    self.assertEqual(len(b_program.splits), len(a_program.splits))
                    for b_split, a_split in zip(b_program.splits, a_program.splits):
                        self.assertEqual(b_split.id, a_split.id)
                        self.assertEqual(b_split.unk11, a_split.unk11)
                        self.assertEqual(b_split.unk25, a_split.unk25)
                        self.assertEqual(b_split.lowkey, a_split.lowkey)
                        self.assertEqual(b_split.hikey, a_split.hikey)
                        self.assertEqual(b_split.lolevel, a_split.lolevel)
                        self.assertEqual(b_split.hilevel, a_split.hilevel)
                        self.assertEqual(b_split.unk16, a_split.unk16)
                        self.assertEqual(b_split.unk17, a_split.unk17)
                        self.assertEqual(b_split.sample_id, a_split.sample_id)
                        self.assertEqual(b_split.ftune, a_split.ftune)
                        self.assertEqual(b_split.ctune, a_split.ctune)
                        self.assertEqual(b_split.rootkey, a_split.rootkey)
                        self.assertEqual(b_split.ktps, a_split.ktps)
                        self.assertEqual(b_split.sample_volume, a_split.sample_volume)
                        self.assertEqual(b_split.sample_pan, a_split.sample_pan)
                        self.assertEqual(b_split.keygroup_id, a_split.keygroup_id)
                        self.assertEqual(b_split.unk22, a_split.unk22)
                        self.assertEqual(b_split.unk23, a_split.unk23)
                        self.assertEqual(b_split.unk24, a_split.unk24)
                        self.assertEqual(b_split.envelope, a_split.envelope)
                        self.assertEqual(b_split.envelope_multiplier, a_split.envelope_multiplier)
                        self.assertEqual(b_split.unk37, a_split.unk37)
                        self.assertEqual(b_split.unk38, a_split.unk38)
                        self.assertEqual(b_split.unk39, a_split.unk39)
                        self.assertEqual(b_split.unk40, a_split.unk40)
                        self.assertEqual(b_split.attack_volume, a_split.attack_volume)
                        self.assertEqual(b_split.attack, a_split.attack)
                        self.assertEqual(b_split.decay, a_split.decay)
                        self.assertEqual(b_split.sustain, a_split.sustain)
                        self.assertEqual(b_split.hold, a_split.hold)
                        self.assertEqual(b_split.decay2, a_split.decay2)
                        self.assertEqual(b_split.release, a_split.release)
                        self.assertEqual(b_split.unk53, a_split.unk53)

        if before.kgrp is None:
            self.assertIsNone(after.kgrp)
        else:
            self.assertIsNotNone(after.kgrp)
            self.assertEqual(len(before.kgrp.keygroups), len(after.kgrp.keygroups))
            for b_kgrp, a_kgrp in zip(before.kgrp.keygroups, after.kgrp.keygroups):
                self.assertEqual(b_kgrp.id, a_kgrp.id)
                self.assertEqual(b_kgrp.poly, a_kgrp.poly)
                self.assertEqual(b_kgrp.priority, a_kgrp.priority)
                self.assertEqual(b_kgrp.vclow, a_kgrp.vclow)
                self.assertEqual(b_kgrp.vchigh, a_kgrp.vchigh)
                self.assertEqual(b_kgrp.unk50, a_kgrp.unk50)
                self.assertEqual(b_kgrp.unk51, a_kgrp.unk51)
