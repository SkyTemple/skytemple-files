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
from skytemple_files.test.case import SkyTempleFilesTestCase, romtest


# TODO: Non romtests
class SmdlTestCase(SkyTempleFilesTestCase[SmdlHandler, SmdlProtocol]):
    handler = SmdlHandler

    @romtest(file_ext='smd', path='SOUND/BGM')
    def test_using_rom(self, _, file):
        before = self.handler.deserialize(file)
        after = self.handler.deserialize(self.handler.serialize(before))

        self.assertEqual(before.header.version, after.header.version)
        self.assertEqual(before.header.unk1, after.header.unk1)
        self.assertEqual(before.header.unk2, after.header.unk2)
        self.assertEqual(before.header.modified_date, after.header.modified_date)
        self.assertEqual(before.header.file_name, after.header.file_name)
        self.assertEqual(before.header.unk5, after.header.unk5)
        self.assertEqual(before.header.unk6, after.header.unk6)
        self.assertEqual(before.header.unk8, after.header.unk8)
        self.assertEqual(before.header.unk9, after.header.unk9)

        self.assertEqual(before.song.unk1, after.song.unk1)
        self.assertEqual(before.song.unk2, after.song.unk2)
        self.assertEqual(before.song.unk3, after.song.unk3)
        self.assertEqual(before.song.unk4, after.song.unk4)
        self.assertEqual(before.song.tpqn, after.song.tpqn)
        self.assertEqual(before.song.unk5, after.song.unk5)
        self.assertEqual(before.song.nbchans, after.song.nbchans)
        self.assertEqual(before.song.unk6, after.song.unk6)
        self.assertEqual(before.song.unk7, after.song.unk7)
        self.assertEqual(before.song.unk8, after.song.unk8)
        self.assertEqual(before.song.unk9, after.song.unk9)
        self.assertEqual(before.song.unk10, after.song.unk10)
        self.assertEqual(before.song.unk11, after.song.unk11)
        self.assertEqual(before.song.unk12, after.song.unk12)

        self.assertEqual(before.eoc.param1, after.eoc.param1)
        self.assertEqual(before.eoc.param2, after.eoc.param2)

        self.assertEqual(len(before.tracks), len(after.tracks))
        for b_track, a_track in zip(before.tracks, after.tracks):
            self.assertEqual(b_track.header.param1, a_track.header.param1)
            self.assertEqual(b_track.header.param2, a_track.header.param2)

            self.assertEqual(b_track.preamble.track_id, a_track.preamble.track_id)
            self.assertEqual(b_track.preamble.channel_id, a_track.preamble.channel_id)
            self.assertEqual(b_track.preamble.unk1, a_track.preamble.unk1)
            self.assertEqual(b_track.preamble.unk2, a_track.preamble.unk2)

            self.assertEqual(len(b_track.events), len(a_track.events))
            for b_event, a_event in zip(b_track.events, a_track.events):
                self.assertEqual(type(b_event), type(a_event))
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
