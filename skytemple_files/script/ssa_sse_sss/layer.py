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
from typing import List

from skytemple_files.common.util import AutoString
from skytemple_files.script.ssa_sse_sss import ACTOR_ENTRY_LEN, OBJECT_ENTRY_LEN, PERFORMERS_ENTRY_LEN, \
    EVENTS_ENTRY_LEN, UNK10_ENTRY_LEN
from skytemple_files.script.ssa_sse_sss.actor import SsaActor
from skytemple_files.script.ssa_sse_sss.event import SsaEvent
from skytemple_files.script.ssa_sse_sss.header import SsaHeader
from skytemple_files.script.ssa_sse_sss.object import SsaObject
from skytemple_files.script.ssa_sse_sss.performer import SsaPerformer
from skytemple_files.script.ssa_sse_sss.unk10 import SsaUnk10


class SsaLayer(AutoString):
    """
    A single layer of an SSA file.
    """
    def __init__(self,
                 header: SsaHeader = None,
                 actors_count=None, actors_pointer=None,
                 objects_count=None, objects_pointer=None,
                 performers_count=None, performers_pointer=None,
                 events_count=None, events_pointer=None,
                 unk10_block_count=None, unk10_block_pointer=None):

        self.actors: List[SsaActor] = []
        self.objects: List[SsaObject] = []
        self.performers: List[SsaPerformer] = []
        self.events: List[SsaEvent] = []
        self.unk10s: List[SsaUnk10] = []

        if header is None:
            # Empty layer
            return

        # These fields are only used to build the layer data in self.fill_data.
        # If a value is (start offset of data block - 2), then it's count is 0.
        self._actors_count = actors_count
        self._objects_count = objects_count
        self._performers_count = performers_count
        self._events_count = events_count
        self._unk10_block_count = unk10_block_count
        self._actors_first_offset = None
        self._objects_first_offset = None
        self._performers_first_offset = None
        self._events_first_offset = None
        self._unk10_block_first_offset = None

        # It's also possible everything is just 0.
        if actors_pointer == 0 and objects_pointer == 0 and performers_pointer == 0 and events_pointer == 0 and unk10_block_pointer == 0:
            return

        if self._actors_count > 0:
            self._actors_first_offset = int((actors_pointer - header.actor_pointer) / ACTOR_ENTRY_LEN)
        elif header.actor_pointer is not None:
            assert header.actor_pointer - 2 == actors_pointer

        if self._objects_count > 0:
            self._objects_first_offset = int((objects_pointer - header.object_pointer) / OBJECT_ENTRY_LEN)
        elif header.object_pointer is not None:
            assert header.object_pointer - 2 == objects_pointer

        if self._performers_count > 0:
            self._performers_first_offset = int((performers_pointer - header.performer_pointer) / PERFORMERS_ENTRY_LEN)
        elif header.performer_pointer is not None:
            assert header.performer_pointer - 2 == performers_pointer

        if self._events_count > 0:
            self._events_first_offset = int((events_pointer - header.events_pointer) / EVENTS_ENTRY_LEN)
        elif header.events_pointer is not None:
            assert header.events_pointer - 2 == events_pointer

        if self._unk10_block_count > 0:
            self._unk10_block_first_offset = int((unk10_block_pointer - header.unk10_pointer) / UNK10_ENTRY_LEN)
        elif header.unk10_pointer is not None:
            assert header.unk10_pointer - 2 == unk10_block_pointer

    def fill_data(self, all_actors, all_objects, all_performers, all_events, all_unk10s):
        if self._actors_count > 0:
            self.actors = all_actors[self._actors_first_offset:(self._actors_first_offset+self._actors_count)]
        if self._objects_count > 0:
            self.objects = all_objects[self._objects_first_offset:(self._objects_first_offset+self._objects_count)]
        if self._performers_count > 0:
            self.performers = all_performers[self._performers_first_offset:(self._performers_first_offset+self._performers_count)]
        if self._events_count > 0:
            self.events = all_events[self._events_first_offset:(self._events_first_offset+self._events_count)]
        if self._unk10_block_count > 0:
            self.unk10s = all_unk10s[self._unk10_block_first_offset:(self._unk10_block_first_offset + self._unk10_block_count)]
