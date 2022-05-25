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
from typing import Optional

from range_typed_integers import u16

from skytemple_files.common.util import AutoString, CheckedIntWrites


class SsaHeader(AutoString, CheckedIntWrites):
    """
    The header of a read SSA file.
    Only contains information used during read-in of the data. Not used for saving.
    """
    layer_count: u16
    layer_list_pointer: Optional[u16]
    trigger_pointer: Optional[u16]
    actor_pointer: Optional[u16]
    object_pointer: Optional[u16]
    performer_pointer: Optional[u16]
    events_pointer: Optional[u16]
    position_marker_pointer: Optional[u16]
    unk10_pointer: Optional[u16]

    def __init__(self, layer_count: u16, layer_list_pointer: u16,
                 trigger_pointer: u16, actor_pointer: u16,
                 object_pointer: u16, performer_pointer: u16,
                 events_pointer: u16, position_marker_pointer: u16, unk10_pointer: u16):

        # If the pointer of the following entry is the same, then this layer doesn't actually exist.
        self.layer_count = layer_count
        self.layer_list_pointer = layer_list_pointer if layer_list_pointer != trigger_pointer else None

        self.trigger_pointer = trigger_pointer if trigger_pointer != actor_pointer else None
        if self.layer_list_pointer is not None:
            self.trigger_end_pointer = actor_pointer

        self.actor_pointer = actor_pointer if actor_pointer != object_pointer else None
        if self.actor_pointer is not None:
            self.actor_end_pointer = object_pointer

        self.object_pointer = object_pointer if object_pointer != performer_pointer else None
        if self.object_pointer is not None:
            self.object_end_pointer = performer_pointer

        self.performer_pointer = performer_pointer if performer_pointer != events_pointer else None
        if self.performer_pointer is not None:
            self.performer_end_pointer = events_pointer

        self.events_pointer = events_pointer if events_pointer != position_marker_pointer else None
        if self.events_pointer is not None:
            self.events_end_pointer = position_marker_pointer

        self.position_marker_pointer = position_marker_pointer if position_marker_pointer != unk10_pointer else None
        if self.position_marker_pointer is not None:
            self.position_marker_end_pointer = unk10_pointer

        self.unk10_pointer = unk10_pointer if unk10_pointer != layer_list_pointer else None
        if self.unk10_pointer is not None:
            self.unk10_end_pointer = layer_list_pointer
