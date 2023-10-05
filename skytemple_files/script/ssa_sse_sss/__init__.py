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

LEN_LAYER_ENTRY = 20
ACTOR_ENTRY_LEN = 16
OBJECT_ENTRY_LEN = 20
PERFORMERS_ENTRY_LEN = 20
EVENTS_ENTRY_LEN = 16
POS_MARKER_ENTRY_LEN = 16
UNK10_ENTRY_LEN = 8
TRIGGER_ENTRY_LEN = 8

XML_SCENE = "Scene"
XML_LAYERS = "Layers"
XML_LAYER = "Layer"
XML_POSITION = "Position"
XML_POSITION__DIRECTION = "direction"
XML_POSITION__DIRECTION__NONE = "NONE"
XML_POSITION__DIRECTION__DOWN = "DOWN"
XML_POSITION__DIRECTION__DOWN_RIGHT = "DOWN_RIGHT"
XML_POSITION__DIRECTION__RIGHT = "RIGHT"
XML_POSITION__DIRECTION__UP_RIGHT = "UP_RIGHT"
XML_POSITION__DIRECTION__UP = "UP"
XML_POSITION__DIRECTION__UP_LEFT = "UP_LEFT"
XML_POSITION__DIRECTION__LEFT = "LEFT"
XML_POSITION__DIRECTION__DOWN_LEFT = "DOWN_LEFT"
XML_POSITION__X_POS = "x_pos"
XML_POSITION__Y_POS = "y_pos"
XML_POSITION__X_OFFSET = "x_offset"
XML_POSITION__Y_OFFSET = "y_offset"
XML_ACTOR = "Actor"
XML_ACTOR__ACTOR_ID = "actor_id"
XML_ACTOR__SCRIPT_ID = "script_id"
XML_ACTOR__UNK_E = "unk_e"
XML_OBJECT = "Object"
XML_OBJECT__OBJECT_ID = "object_id"
XML_OBJECT__SCRIPT_ID = "script_id"
XML_OBJECT__HITBOX_WIDTH = "hitbox_width"
XML_OBJECT__HITBOX_HEIGHT = "hitbox_height"
XML_OBJECT__UNK_12 = "unk_12"
XML_PERFORMER = "Performer"
XML_PERFORMER__TYPE = "type"
XML_PERFORMER__HITBOX_WIDTH = "hitbox_width"
XML_PERFORMER__HITBOX_HEIGHT = "hitbox_height"
XML_PERFORMER__UNK_10 = "unk_10"
XML_PERFORMER__UNK_12 = "unk_12"
XML_TRIGGER = "Trigger"  # NOTE: These are called "events" in the model code. See docs.
XML_TRIGGER__WIDTH = "width"
XML_TRIGGER__HEIGHT = "height"
XML_TRIGGER__UNK_E = "unk_e"
XML_TRIGGER__EVENT_ID = "event_id"
XML_UNK10 = "Unk10"
XML_UNK10__UNK_0 = "unk_0"
XML_UNK10__UNK_2 = "unk_2"
XML_UNK10__UNK_4 = "unk_4"
XML_UNK10__UNK_6 = "unk_6"
XML_EVENTS = "Events"
XML_EVENT = "Event"  # NOTE: These are called "triggers" in the model code.
XML_EVENT__SCRIPT_ID = "script_id"
XML_EVENT__COROUTINE_ID = "coroutine_id"
XML_EVENT__UNK_2 = "unk_2"
XML_EVENT__UNK_3 = "unk_3"
XML_POS_MARKS = "PositionMarks"
XML_POS_MARK = "PositionMark"
XML_POS_MARK__UNK_8 = "unk_8"
XML_POS_MARK__UNK_A = "unk_a"
XML_POS_MARK__UNK_C = "unk_c"
XML_POS_MARK__UNK_E = "unk_e"
