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

from typing import List

from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptData
from skytemple_files.common.util import (
    read_u16,
    read_i16,
    iter_bytes,
)
from skytemple_files.script.ssa_sse_sss import (
    ACTOR_ENTRY_LEN,
    EVENTS_ENTRY_LEN,
    LEN_LAYER_ENTRY,
    OBJECT_ENTRY_LEN,
    PERFORMERS_ENTRY_LEN,
    POS_MARKER_ENTRY_LEN,
    TRIGGER_ENTRY_LEN,
    UNK10_ENTRY_LEN,
)
from skytemple_files.script.ssa_sse_sss.actor import SsaActor
from skytemple_files.script.ssa_sse_sss.event import SsaEvent
from skytemple_files.script.ssa_sse_sss.header import SsaHeader
from skytemple_files.script.ssa_sse_sss.layer import SsaLayer
from skytemple_files.script.ssa_sse_sss.object import SsaObject
from skytemple_files.script.ssa_sse_sss.performer import SsaPerformer
from skytemple_files.script.ssa_sse_sss.position import SsaPosition
from skytemple_files.script.ssa_sse_sss.position_marker import SsaPositionMarker
from skytemple_files.script.ssa_sse_sss.trigger import SsaTrigger
from skytemple_files.script.ssa_sse_sss.unk10 import SsaUnk10


class Ssa:
    def __init__(self, scriptdata: Pmd2ScriptData, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        self._scriptdata = scriptdata

        self.header = self._init_header(data)
        self.layer_list: List[SsaLayer] = self._init_layer_list(data)

        self.triggers = self._init_triggers(data)
        self.position_markers = self._init_position_markers(data)

        actors = self._init_actors(data)
        objects = self._init_objects(data)
        performers = self._init_performers(data)
        events = self._init_events(data)
        unk10 = self._init_unk10(data)

        for layer in self.layer_list:
            layer.fill_data(actors, objects, performers, events, unk10)

    def _init_header(self, data):
        # All offsets/pointers must be multiplied by 2, since they're counting 16 bits words and not bytes!
        return SsaHeader(
            layer_count=read_u16(data, 0x0),
            layer_list_pointer=read_u16(data, 0x2) * 2,
            trigger_pointer=read_u16(data, 0x4) * 2,
            actor_pointer=read_u16(data, 0x6) * 2,
            object_pointer=read_u16(data, 0x8) * 2,
            performer_pointer=read_u16(data, 0xA) * 2,
            events_pointer=read_u16(data, 0xC) * 2,
            position_marker_pointer=read_u16(data, 0xE) * 2,
            unk10_pointer=read_u16(data, 0x10) * 2,
        )

    def _init_layer_list(self, data):
        lst = []
        for i in range(0, self.header.layer_count):
            offset = self.header.layer_list_pointer + (i * LEN_LAYER_ENTRY)
            # All pointers in this list are multiplied by 2, see _init_header info above why
            lst.append(
                SsaLayer(
                    header=self.header,
                    actors_count=read_u16(data, offset + 0x0),
                    actors_pointer=read_u16(data, offset + 0x2) * 2,
                    objects_count=read_u16(data, offset + 0x4),
                    objects_pointer=read_u16(data, offset + 0x6) * 2,
                    performers_count=read_u16(data, offset + 0x8),
                    performers_pointer=read_u16(data, offset + 0xA) * 2,
                    events_count=read_u16(data, offset + 0xC),
                    events_pointer=read_u16(data, offset + 0xE) * 2,
                    unk10_block_count=read_u16(data, offset + 0x10),
                    unk10_block_pointer=read_u16(data, offset + 0x12) * 2,
                )
            )
        return lst

    def _init_triggers(self, data):
        lst = []
        if self.header.trigger_pointer is not None:
            for entry in iter_bytes(
                data,
                TRIGGER_ENTRY_LEN,
                self.header.trigger_pointer,
                self.header.trigger_end_pointer,
            ):
                lst.append(
                    SsaTrigger(
                        scriptdata=self._scriptdata,
                        coroutine_id=read_u16(entry, 0x0),
                        unk2=read_u16(entry, 0x2),
                        unk3=read_u16(entry, 0x4),
                        script_id=read_u16(entry, 0x6),
                    )
                )
        return lst

    def _init_actors(self, data):
        lst = []
        if self.header.actor_pointer is not None:
            for entry in iter_bytes(
                data,
                ACTOR_ENTRY_LEN,
                self.header.actor_pointer,
                self.header.actor_end_pointer,
            ):
                lst.append(
                    SsaActor(
                        scriptdata=self._scriptdata,
                        actor_id=read_u16(entry, 0x0),
                        pos=SsaPosition(
                            scriptdata=self._scriptdata,
                            direction=read_u16(entry, 0x2),
                            x_pos=read_u16(entry, 0x4),
                            y_pos=read_u16(entry, 0x6),
                            x_offset=read_u16(entry, 0x8),
                            y_offset=read_u16(entry, 0xA),
                        ),
                        script_id=read_i16(entry, 0xC),
                        unkE=read_i16(entry, 0xE),
                    )
                )
        return lst

    def _init_objects(self, data):
        lst = []
        if self.header.object_pointer is not None:
            for entry in iter_bytes(
                data,
                OBJECT_ENTRY_LEN,
                self.header.object_pointer,
                self.header.object_end_pointer,
            ):
                lst.append(
                    SsaObject(
                        scriptdata=self._scriptdata,
                        object_id=read_u16(entry, 0x0),
                        htibox_w=read_i16(entry, 0x4),
                        hitbox_h=read_i16(entry, 0x6),
                        pos=SsaPosition(
                            scriptdata=self._scriptdata,
                            direction=read_u16(entry, 0x2),
                            x_pos=read_u16(entry, 0x8),
                            y_pos=read_u16(entry, 0xA),
                            x_offset=read_u16(entry, 0xC),
                            y_offset=read_u16(entry, 0xE),
                        ),
                        script_id=read_i16(entry, 0x10),
                        unk12=read_i16(entry, 0x12),
                    )
                )
        return lst

    def _init_performers(self, data):
        lst = []
        if self.header.performer_pointer is not None:
            for entry in iter_bytes(
                data,
                PERFORMERS_ENTRY_LEN,
                self.header.performer_pointer,
                self.header.performer_end_pointer,
            ):
                lst.append(
                    SsaPerformer(
                        type=read_u16(entry, 0x0),
                        hitbox_w=read_i16(entry, 0x4),
                        hitbox_h=read_i16(entry, 0x6),
                        pos=SsaPosition(
                            scriptdata=self._scriptdata,
                            direction=read_u16(entry, 0x2),
                            x_pos=read_u16(entry, 0x8),
                            y_pos=read_u16(entry, 0xA),
                            x_offset=read_u16(entry, 0xC),
                            y_offset=read_u16(entry, 0xE),
                        ),
                        unk10=read_i16(entry, 0x10),
                        unk12=read_i16(entry, 0x12),
                    )
                )
        return lst

    def _init_events(self, data):
        lst = []
        if self.header.events_pointer is not None:
            for entry in iter_bytes(
                data,
                EVENTS_ENTRY_LEN,
                self.header.events_pointer,
                self.header.events_end_pointer,
            ):
                lst.append(
                    SsaEvent(
                        trigger_width=read_u16(entry, 0x0),
                        trigger_height=read_u16(entry, 0x2),
                        trigger_pointer=read_u16(entry, 0xC) * 2,
                        trigger_table_start=self.header.trigger_pointer,
                        pos=SsaPosition(
                            scriptdata=self._scriptdata,
                            x_pos=read_u16(entry, 0x4),
                            y_pos=read_u16(entry, 0x6),
                            x_offset=read_u16(entry, 0x8),
                            y_offset=read_u16(entry, 0xA),
                        ),
                        unkE=read_u16(entry, 0xE),
                    )
                )
        return lst

    def _init_position_markers(self, data):
        lst = []
        if self.header.position_marker_pointer is not None:
            for entry in iter_bytes(
                data,
                POS_MARKER_ENTRY_LEN,
                self.header.position_marker_pointer,
                self.header.position_marker_end_pointer,
            ):
                lst.append(
                    SsaPositionMarker(
                        pos=SsaPosition(
                            scriptdata=self._scriptdata,
                            direction=None,
                            x_pos=read_u16(entry, 0x0),
                            y_pos=read_u16(entry, 0x2),
                            x_offset=read_u16(entry, 0x4),
                            y_offset=read_u16(entry, 0x6),
                        ),
                        unk8=read_i16(entry, 0x8),
                        unkA=read_i16(entry, 0xA),
                        unkC=read_i16(entry, 0xC),
                        unkE=read_i16(entry, 0xE),
                    )
                )
        return lst

    def _init_unk10(self, data):
        lst = []
        if self.header.unk10_pointer is not None:
            for entry in iter_bytes(
                data,
                UNK10_ENTRY_LEN,
                self.header.unk10_pointer,
                self.header.unk10_end_pointer,
            ):
                lst.append(
                    SsaUnk10(
                        unk0=read_i16(entry, 0x0),
                        unk2=read_i16(entry, 0x2),
                        unk4=read_i16(entry, 0x4),
                        unk6=read_i16(entry, 0x6),
                    )
                )
        return lst
