"""Converts Ssa models back into the binary format used by the game"""
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

from skytemple_files.common.util import *
from skytemple_files.script.ssa_sse_sss.model import Ssa


LEN_HEADER = 0x12
TRIGGER_LEN = 0x08


class SsaWriter:
    def __init__(self, model: Ssa):
        self.model = model
        self.data = None
        self.bytes_written = 0

    def write(self) -> bytes:
        # Stored order:
        # - Header
        # - Trigger
        # - Actor
        # - Object
        # - Performers
        # - Events
        # - Position Markers
        # - Unk10
        # - Layer List

        # Collect Trigger
        trigger_bytes = bytearray()
        trigger_start = int(LEN_HEADER / 2)
        for trigger in self.model.triggers:
            trigger_bytes += self.uint16(trigger.coroutine.id)
            trigger_bytes += self.uint16(trigger.unk2)
            trigger_bytes += self.uint16(trigger.unk3)
            trigger_bytes += self.uint16(trigger.script_id)

        # Collect all the data that is referenced by layers
        actor_bytes = bytearray()
        object_bytes = bytearray()
        performer_bytes = bytearray()
        event_bytes = bytearray()
        unk10_bytes = bytearray()
        layer_bytes = bytearray()
        for layer in self.model.layer_list:
            actor_start = len(actor_bytes)
            object_start = len(object_bytes)
            performer_start = len(performer_bytes)
            event_start = len(event_bytes)
            unk10_start = len(unk10_bytes)

            # Actors
            for actor in layer.actors:
                actor_bytes += self.uint16(actor.actor.id)
                actor_bytes += self.uint16(actor.pos.direction.id)
                actor_bytes += self.uint16(actor.pos.x_relative)
                actor_bytes += self.uint16(actor.pos.y_relative)
                actor_bytes += self.uint16(actor.pos.x_offset)
                actor_bytes += self.uint16(actor.pos.y_offset)
                actor_bytes += self.sint16(actor.script_id)
                actor_bytes += self.sint16(actor.unkE)

            # Objects
            for obj in layer.objects:
                object_bytes += self.uint16(obj.object.id)
                object_bytes += self.uint16(obj.pos.direction.id)
                object_bytes += self.sint16(obj.hitbox_w)
                object_bytes += self.sint16(obj.hitbox_h)
                object_bytes += self.uint16(obj.pos.x_relative)
                object_bytes += self.uint16(obj.pos.y_relative)
                object_bytes += self.uint16(obj.pos.x_offset)
                object_bytes += self.uint16(obj.pos.y_offset)
                object_bytes += self.sint16(obj.script_id)
                object_bytes += self.sint16(obj.unk12)

            # Performer
            for prf in layer.performers:
                performer_bytes += self.uint16(prf.type)
                performer_bytes += self.uint16(prf.pos.direction.id)
                performer_bytes += self.sint16(prf.hitbox_w)
                performer_bytes += self.sint16(prf.hitbox_h)
                performer_bytes += self.uint16(prf.pos.x_relative)
                performer_bytes += self.uint16(prf.pos.y_relative)
                performer_bytes += self.uint16(prf.pos.x_offset)
                performer_bytes += self.uint16(prf.pos.y_offset)
                performer_bytes += self.sint16(prf.unk10)
                performer_bytes += self.sint16(prf.unk12)

            # Event
            for evt in layer.events:
                event_bytes += self.uint16(evt.trigger_width)
                event_bytes += self.uint16(evt.trigger_height)
                event_bytes += self.uint16(evt.pos.x_relative)
                event_bytes += self.uint16(evt.pos.y_relative)
                event_bytes += self.uint16(evt.pos.x_offset)
                event_bytes += self.uint16(evt.pos.y_offset)
                event_bytes += self.uint16(trigger_start + evt.trigger_id * int(TRIGGER_LEN / 2))
                event_bytes += self.uint16(evt.unkE)

            # unk10
            for unk10 in layer.unk10s:
                unk10_bytes += self.sint16(unk10.unk0)
                unk10_bytes += self.sint16(unk10.unk2)
                unk10_bytes += self.sint16(unk10.unk4)
                unk10_bytes += self.sint16(unk10.unk6)

            layer_bytes += self.uint16(len(layer.actors))
            # We write the relative words for now and will add the start of the lists to this!
            if len(layer.actors) > 0:
                layer_bytes += self.sint16(int(actor_start / 2))
            else:
                layer_bytes += self.sint16(-1)

            layer_bytes += self.uint16(len(layer.objects))
            if len(layer.objects) > 0:
                layer_bytes += self.uint16(int(object_start / 2))
            else:
                layer_bytes += self.sint16(-1)

            layer_bytes += self.uint16(len(layer.performers))
            if len(layer.performers) > 0:
                layer_bytes += self.uint16(int(performer_start / 2))
            else:
                layer_bytes += self.sint16(-1)

            layer_bytes += self.uint16(len(layer.events))
            if len(layer.events) > 0:
                layer_bytes += self.uint16(int(event_start / 2))
            else:
                layer_bytes += self.sint16(-1)

            layer_bytes += self.uint16(len(layer.unk10s))
            if len(layer.unk10s) > 0:
                layer_bytes += self.uint16(int(unk10_start / 2))
            else:
                layer_bytes += self.sint16(-1)

        # Collect Position Marks
        pos_mark_bytes = bytearray()
        for mark in self.model.position_markers:
            pos_mark_bytes += self.uint16(mark.pos.x_relative)
            pos_mark_bytes += self.uint16(mark.pos.y_relative)
            pos_mark_bytes += self.uint16(mark.pos.x_offset)
            pos_mark_bytes += self.uint16(mark.pos.y_offset)
            pos_mark_bytes += self.sint16(mark.unk8)
            pos_mark_bytes += self.sint16(mark.unkA)
            pos_mark_bytes += self.sint16(mark.unkC)
            pos_mark_bytes += self.sint16(mark.unkE)

        # Collect Header
        header = bytearray(LEN_HEADER)
        actor_list_start = trigger_start + int(len(trigger_bytes) / 2)
        object_list_start = actor_list_start + int(len(actor_bytes) / 2)
        performer_list_start = object_list_start + int(len(object_bytes) / 2)
        event_list_start = performer_list_start + int(len(performer_bytes) / 2)
        pos_mark_list_start = event_list_start + int(len(event_bytes) / 2)
        unk10_list_start = pos_mark_list_start + int(len(pos_mark_bytes) / 2)
        layer_list_start = unk10_list_start + int(len(unk10_bytes) / 2)
        write_uintle(header, len(self.model.layer_list), 0x00, 2)
        write_uintle(header, layer_list_start, 0x02, 2)
        write_uintle(header, int(LEN_HEADER / 2), 0x04, 2)
        write_uintle(header, actor_list_start, 0x06, 2)
        write_uintle(header, object_list_start, 0x08, 2)
        write_uintle(header, performer_list_start, 0x0A, 2)
        write_uintle(header, event_list_start, 0x0C, 2)
        write_uintle(header, pos_mark_list_start, 0x0E, 2)
        write_uintle(header, unk10_list_start, 0x10, 2)

        # Add the offsets to the lists to the layer list offsets
        for i, layer in enumerate(self.model.layer_list):
            write_uintle(layer_bytes, actor_list_start     + read_sintle(layer_bytes, (i * 0x14) + 0x02, 2), (i * 0x14) + 0x02, 2)
            write_uintle(layer_bytes, object_list_start    + read_sintle(layer_bytes, (i * 0x14) + 0x06, 2), (i * 0x14) + 0x06, 2)
            write_uintle(layer_bytes, performer_list_start + read_sintle(layer_bytes, (i * 0x14) + 0x0A, 2), (i * 0x14) + 0x0A, 2)
            write_uintle(layer_bytes, event_list_start     + read_sintle(layer_bytes, (i * 0x14) + 0x0E, 2), (i * 0x14) + 0x0E, 2)
            write_uintle(layer_bytes, unk10_list_start     + read_sintle(layer_bytes, (i * 0x14) + 0x12, 2), (i * 0x14) + 0x12, 2)

        # Build everything together and return
        return header + trigger_bytes + actor_bytes + object_bytes + performer_bytes + \
               event_bytes + pos_mark_bytes + unk10_bytes + layer_bytes

    def uint16(self, i: int) -> bytes:
        return i.to_bytes(2, byteorder='little', signed=False)

    def sint16(self, i: int) -> bytes:
        return i.to_bytes(2, byteorder='little', signed=True)
