#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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
from __future__ import annotations

from collections.abc import Iterable

from skytemple_files.common.util import AutoString
from skytemple_files.script.ssa_sse_sss import (
    ACTOR_ENTRY_LEN,
    EVENTS_ENTRY_LEN,
    OBJECT_ENTRY_LEN,
    PERFORMERS_ENTRY_LEN,
    UNK10_ENTRY_LEN,
)
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

    def __init__(
        self,
        header: SsaHeader | None = None,
        actors_count: int | None = None,
        actors_pointer: int | None = None,
        objects_count: int | None = None,
        objects_pointer: int | None = None,
        performers_count: int | None = None,
        performers_pointer: int | None = None,
        events_count: int | None = None,
        events_pointer: int | None = None,
        unk10_block_count: int | None = None,
        unk10_block_pointer: int | None = None,
    ):
        self.actors: list[SsaActor] = []
        self.objects: list[SsaObject] = []
        self.performers: list[SsaPerformer] = []
        self.events: list[SsaEvent] = []
        self.unk10s: list[SsaUnk10] = []

        if header is None:
            # Empty layer
            return
        assert (
            actors_count is not None
            and objects_count is not None
            and performers_count is not None
            and events_count is not None
            and unk10_block_count is not None
        )
        assert (
            actors_pointer is not None
            and objects_pointer is not None
            and performers_pointer is not None
            and events_pointer is not None
            and unk10_block_pointer is not None
        )

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
        if (
            actors_pointer == 0
            and objects_pointer == 0
            and performers_pointer == 0
            and events_pointer == 0
            and unk10_block_pointer == 0
        ):
            return

        if self._actors_count > 0:
            assert header.actor_pointer is not None
            self._actors_first_offset = (
                actors_pointer - header.actor_pointer
            ) // ACTOR_ENTRY_LEN
        elif header.actor_pointer is not None:
            assert header.actor_pointer - 2 == actors_pointer

        if self._objects_count > 0:
            assert header.object_pointer is not None
            self._objects_first_offset = (
                objects_pointer - header.object_pointer
            ) // OBJECT_ENTRY_LEN
        elif header.object_pointer is not None:
            assert header.object_pointer - 2 == objects_pointer

        if self._performers_count > 0:
            assert header.performer_pointer is not None
            self._performers_first_offset = (
                performers_pointer - header.performer_pointer
            ) // PERFORMERS_ENTRY_LEN
        elif header.performer_pointer is not None:
            assert header.performer_pointer - 2 == performers_pointer

        if self._events_count > 0:
            assert header.events_pointer is not None
            self._events_first_offset = (
                events_pointer - header.events_pointer
            ) // EVENTS_ENTRY_LEN
        elif header.events_pointer is not None:
            assert header.events_pointer - 2 == events_pointer

        if self._unk10_block_count > 0:
            assert header.unk10_pointer is not None
            self._unk10_block_first_offset = (
                unk10_block_pointer - header.unk10_pointer
            ) // UNK10_ENTRY_LEN
        elif header.unk10_pointer is not None:
            assert header.unk10_pointer - 2 == unk10_block_pointer

    @classmethod
    def new(
        cls,
        all_actors: Iterable[SsaActor],
        all_objects: Iterable[SsaObject],
        all_performers: Iterable[SsaPerformer],
        all_events: Iterable[SsaEvent],
        all_unk10s: Iterable[SsaUnk10],
    ) -> SsaLayer:
        slf = cls.__new__(cls)
        slf.actors = list(all_actors)
        slf.objects = list(all_objects)
        slf.performers = list(all_performers)
        slf.events = list(all_events)
        slf.unk10s = list(all_unk10s)
        slf._actors_count = len(slf.actors)
        slf._objects_count = len(slf.objects)
        slf._performers_count = len(slf.performers)
        slf._events_count = len(slf.events)
        slf._unk10_block_count = len(slf.unk10s)
        slf._actors_first_offset = None
        slf._objects_first_offset = None
        slf._performers_first_offset = None
        slf._events_first_offset = None
        slf._unk10_block_first_offset = None
        return slf

    def fill_data(
        self, all_actors, all_objects, all_performers, all_events, all_unk10s
    ):
        if self._actors_count > 0:
            assert self._actors_first_offset is not None
            self.actors = all_actors[
                self._actors_first_offset : (
                    self._actors_first_offset + self._actors_count
                )
            ]
        if self._objects_count > 0:
            assert self._objects_first_offset is not None
            self.objects = all_objects[
                self._objects_first_offset : (
                    self._objects_first_offset + self._objects_count
                )
            ]
        if self._performers_count > 0:
            assert self._performers_first_offset is not None
            self.performers = all_performers[
                self._performers_first_offset : (
                    self._performers_first_offset + self._performers_count
                )
            ]
        if self._events_count > 0:
            assert self._events_first_offset is not None
            self.events = all_events[
                self._events_first_offset : (
                    self._events_first_offset + self._events_count
                )
            ]
        if self._unk10_block_count > 0:
            assert self._unk10_block_first_offset is not None
            self.unk10s = all_unk10s[
                self._unk10_block_first_offset : (
                    self._unk10_block_first_offset + self._unk10_block_count
                )
            ]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return (
            self.actors == other.actors
            and self.objects == other.objects
            and self.performers == other.performers
            and self.events == other.events
            and self.unk10s == other.unk10s
        )
