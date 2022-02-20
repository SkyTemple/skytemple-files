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
from skytemple_files.audio.smdl.handler import SmdlHandler
from skytemple_files.audio.smdl.protocol import SmdlProtocol
from skytemple_files.common.impl_cfg import env_use_native
from skytemple_files.test.case import SkyTempleFilesTestCase, romtest


# TODO: Non romtests
class SmdlTestCase(SkyTempleFilesTestCase[SmdlHandler, SmdlProtocol]):
    handler = SmdlHandler

    @romtest(file_ext='smd', path='SOUND/BGM')
    def test_against_pyimpl(self, _, file):
        if not env_use_native():
            self.skipTest("This test is only enabled when the native implementations are tested.")
        py = self.handler.load_python_model()(file)
        rst = self.handler.load_native_model()(file)
        self.do_tests(py, rst, skip_filename=True)

    @romtest(file_ext='smd', path='SOUND/BGM')
    def test_using_rom(self, _, file):
        before = self.handler.deserialize(file)
        after = self.handler.deserialize(self.handler.serialize(before))

    def do_tests(self, expected, to_test, skip_filename=False):
        self.assertEqual(expected.header.version, to_test.header.version)
        self.assertEqual(expected.header.unk1, to_test.header.unk1)
        self.assertEqual(expected.header.unk2, to_test.header.unk2)
        self.assertEqual(expected.header.modified_date, to_test.header.modified_date)
        if not skip_filename:
            self.assertEqual(expected.header.file_name, to_test.header.file_name)
        self.assertEqual(expected.header.unk5, to_test.header.unk5)
        self.assertEqual(expected.header.unk6, to_test.header.unk6)
        self.assertEqual(expected.header.unk8, to_test.header.unk8)
        self.assertEqual(expected.header.unk9, to_test.header.unk9)

        self.assertEqual(expected.song.unk1, to_test.song.unk1)
        self.assertEqual(expected.song.unk2, to_test.song.unk2)
        self.assertEqual(expected.song.unk3, to_test.song.unk3)
        self.assertEqual(expected.song.unk4, to_test.song.unk4)
        self.assertEqual(expected.song.tpqn, to_test.song.tpqn)
        self.assertEqual(expected.song.unk5, to_test.song.unk5)
        self.assertEqual(expected.song.nbchans, to_test.song.nbchans)
        self.assertEqual(expected.song.unk6, to_test.song.unk6)
        self.assertEqual(expected.song.unk7, to_test.song.unk7)
        self.assertEqual(expected.song.unk8, to_test.song.unk8)
        self.assertEqual(expected.song.unk9, to_test.song.unk9)
        self.assertEqual(expected.song.unk10, to_test.song.unk10)
        self.assertEqual(expected.song.unk11, to_test.song.unk11)
        self.assertEqual(expected.song.unk12, to_test.song.unk12)

        self.assertEqual(expected.eoc.param1, to_test.eoc.param1)
        self.assertEqual(expected.eoc.param2, to_test.eoc.param2)

        self.assertEqual(len(expected.tracks), len(to_test.tracks))
        for b_track, a_track in zip(expected.tracks, to_test.tracks):
            self.assertEqual(b_track.header.param1, a_track.header.param1)
            self.assertEqual(b_track.header.param2, a_track.header.param2)

            self.assertEqual(b_track.preamble.track_id, a_track.preamble.track_id)
            self.assertEqual(b_track.preamble.channel_id, a_track.preamble.channel_id)
            self.assertEqual(b_track.preamble.unk1, a_track.preamble.unk1)
            self.assertEqual(b_track.preamble.unk2, a_track.preamble.unk2)

            self.assertEqual(len(b_track.events), len(a_track.events))
            for b_event, a_event in zip(b_track.events, a_track.events):
                # we do it like this to allow easy cross-check of py/rst types, not ideal,
                # but i don't think runtime checkable protocols would help here
                self.assertEqual(type(b_event).__name__, type(a_event).__name__)
                if hasattr(b_event, "op"):  # SmdlEventSpecialProtocol
                    self.assertEqual(b_event.op, a_event.op)
                    self.assertEqual(b_event.params, a_event.params)
                elif hasattr(b_event, "value"):  # SmdlEventPauseProtocol
                    self.assertEqual(b_event.value, a_event.value)
                elif hasattr(b_event, "velocity"):  # SmdlEventPlayNoteProtocol
                    self.assertEqual(b_event.velocity, a_event.velocity)
                    self.assertEqual(b_event.octave_mod, a_event.octave_mod)
                    self.assertEqual(b_event.note, a_event.note)
                    self.assertEqual(b_event.key_down_duration, a_event.key_down_duration)
                else:
                    self.fail(f"Unknown event type for {b_event!r} & {a_event!r}")
