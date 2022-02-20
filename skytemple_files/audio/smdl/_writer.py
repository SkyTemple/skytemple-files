"""Converts Smdl models back into the binary format used by the game"""
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
from typing import List, Sequence

from skytemple_files.audio.smdl._model import Smdl, SmdlEvent, SmdlEventSpecial, SmdlEventPlayNote, SmdlEventPause


class SmdlWriter:
    def write(self, model: Smdl) -> bytes:
        data = bytearray(128)
        # Tracks
        for track in model.tracks:
            events = self._events_to_bytes(track.events)
            preamble: bytes = track.preamble.to_bytes()
            data += track.header.to_bytes(len(preamble) + len(events))
            data += preamble
            data += events
            # padding
            if len(data) % 4 != 0:
                data += bytes([0x98] * (4 - len(data) % 4))
        # EOC
        data += model.eoc.to_bytes()
        # Header 64 bytes
        data[0:64] = model.header.to_bytes(len(data))
        # Song header 64 bytes
        data[64:128] = model.song.to_bytes(len(model.tracks))

        return data

    @staticmethod
    def _events_to_bytes(events: Sequence[SmdlEvent]) -> bytearray:
        buffer = bytearray()
        for event in events:
            if isinstance(event, SmdlEventPlayNote):
                buffer.append(event.velocity)
                note = event.note
                octmod = event.octave_mod
                if event.key_down_duration is None:
                    n_p = 0
                elif event.key_down_duration > 0xFFFFFF:
                    raise ValueError("Key down duration too large to encode.")
                elif event.key_down_duration > 0xFFFF:
                    n_p = 3
                elif event.key_down_duration > 0xFF:
                    n_p = 2
                else:
                    n_p = 1
                note_data = note & 0xF
                note_data += ((octmod + 2) & 0x3) << 4
                note_data += (n_p & 0x3) << 6
                buffer.append(note_data)
                if n_p > 0:
                    assert event.key_down_duration is not None
                    i = int.to_bytes(event.key_down_duration, n_p, byteorder='big', signed=False)
                    assert len(i) == n_p
                    buffer += i
            elif isinstance(event, SmdlEventPause):
                buffer.append(event.value)
            elif isinstance(event, SmdlEventSpecial):
                buffer.append(event.op)
                for param in event.params:
                    if param > 0xFF or param < 0:
                        raise ValueError("An SMDL special event parameter must be unsigned 0-255.")
                    buffer.append(param)
            else:
                raise TypeError(f"Invalid event type: {type(event)}")
        return buffer
