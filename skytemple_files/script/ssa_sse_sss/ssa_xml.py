"""
Imports and exports SSA models from/to XML.
"""
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

from range_typed_integers import u16_checked, u16, i16_checked

from skytemple_files.common.i18n_util import _
from skytemple_files.common.ppmdu_config.script_data import (
    Pmd2ScriptDirection,
    Pmd2ScriptData,
)
from skytemple_files.common.xml_util import (
    validate_xml_tag,
    XmlValidateError,
    validate_xml_attribs,
)
from skytemple_files.script.ssa_sse_sss import (
    XML_SCENE,
    XML_LAYERS,
    XML_EVENTS,
    XML_POS_MARKS,
    XML_LAYER,
    XML_ACTOR,
    XML_OBJECT,
    XML_PERFORMER,
    XML_TRIGGER,
    XML_UNK10,
    XML_EVENT,
    XML_POS_MARK,
    XML_POSITION,
    XML_POSITION__DIRECTION,
    XML_POSITION__X_POS,
    XML_POSITION__Y_POS,
    XML_POSITION__X_OFFSET,
    XML_POSITION__Y_OFFSET,
    XML_POS_MARK__UNK_8,
    XML_POS_MARK__UNK_A,
    XML_POS_MARK__UNK_C,
    XML_POS_MARK__UNK_E,
    XML_TRIGGER__WIDTH,
    XML_TRIGGER__HEIGHT,
    XML_TRIGGER__UNK_E,
    XML_TRIGGER__EVENT_ID,
    XML_UNK10__UNK_0,
    XML_UNK10__UNK_2,
    XML_UNK10__UNK_4,
    XML_UNK10__UNK_6,
    XML_EVENT__COROUTINE_ID,
    XML_EVENT__SCRIPT_ID,
    XML_EVENT__UNK_2,
    XML_EVENT__UNK_3,
    XML_PERFORMER__TYPE,
    XML_PERFORMER__HITBOX_WIDTH,
    XML_PERFORMER__HITBOX_HEIGHT,
    XML_PERFORMER__UNK_10,
    XML_PERFORMER__UNK_12,
    XML_OBJECT__OBJECT_ID,
    XML_OBJECT__SCRIPT_ID,
    XML_OBJECT__HITBOX_WIDTH,
    XML_OBJECT__HITBOX_HEIGHT,
    XML_OBJECT__UNK_12,
    XML_ACTOR__ACTOR_ID,
    XML_ACTOR__SCRIPT_ID,
    XML_ACTOR__UNK_E,
    XML_POSITION__DIRECTION__DOWN,
    XML_POSITION__DIRECTION__DOWN_RIGHT,
    XML_POSITION__DIRECTION__RIGHT,
    XML_POSITION__DIRECTION__UP_RIGHT,
    XML_POSITION__DIRECTION__UP,
    XML_POSITION__DIRECTION__UP_LEFT,
    XML_POSITION__DIRECTION__LEFT,
    XML_POSITION__DIRECTION__DOWN_LEFT,
    XML_POSITION__DIRECTION__NONE,
)
from skytemple_files.script.ssa_sse_sss.actor import SsaActor
from skytemple_files.script.ssa_sse_sss.event import SsaEvent
from skytemple_files.script.ssa_sse_sss.layer import SsaLayer
from skytemple_files.script.ssa_sse_sss.object import SsaObject
from skytemple_files.script.ssa_sse_sss.performer import SsaPerformer
from skytemple_files.script.ssa_sse_sss.position import SsaPosition
from skytemple_files.script.ssa_sse_sss.position_marker import SsaPositionMarker
from skytemple_files.script.ssa_sse_sss.trigger import SsaTrigger
from skytemple_files.script.ssa_sse_sss.model import Ssa
from xml.etree.ElementTree import Element

from skytemple_files.script.ssa_sse_sss.unk10 import SsaUnk10


ERR_UNKNOWN = _("Unknown or extra XML element '{}' in scene data.")
ERR_MISSING = _("'{}' missing in scene data.")


def ssa_to_xml(ssa: Ssa) -> Element:
    """Exports the given scene to XML."""
    scene_xml = Element(XML_SCENE)
    scene_xml.append(layer_list_to_xml(ssa.layer_list))
    scene_xml.append(events_to_xml(ssa.triggers))
    scene_xml.append(position_markers_to_xml(ssa.position_markers))
    return scene_xml


def layer_list_to_xml(layers: Iterable[SsaLayer]) -> Element:
    layer_list = Element(XML_LAYERS)
    for layer in layers:
        layer_list.append(layer_to_xml(layer))
    return layer_list


def events_to_xml(events: Iterable[SsaTrigger]) -> Element:
    # NOTE: "Triggers" are called "events" in the model code and vice-versa. See docs.
    event_list = Element(XML_EVENTS)
    for event in events:
        event_list.append(event_to_xml(event))
    return event_list


def position_markers_to_xml(pos_marks: Iterable[SsaPositionMarker]) -> Element:
    pos_mark_list = Element(XML_POS_MARKS)
    for pos_mark in pos_marks:
        pos_mark_list.append(position_marker_to_xml(pos_mark))
    return pos_mark_list


def layer_to_xml(layer: SsaLayer) -> Element:
    layer_xml = Element(XML_LAYER)
    for actor in layer.actors:
        layer_xml.append(actor_to_xml(actor))
    for object in layer.objects:
        layer_xml.append(object_to_xml(object))
    for performer in layer.performers:
        layer_xml.append(performer_to_xml(performer))
    for trigger in layer.events:
        # NOTE: "Triggers" are called "events" in the model code and vice-versa. See docs.
        layer_xml.append(trigger_to_xml(trigger))
    for unk10 in layer.unk10s:
        layer_xml.append(unk10_to_xml(unk10))
    return layer_xml


def actor_to_xml(actor: SsaActor) -> Element:
    xml = Element(XML_ACTOR)
    xml.attrib[XML_ACTOR__ACTOR_ID] = str(actor.actor.id)
    xml.attrib[XML_ACTOR__SCRIPT_ID] = str(actor.script_id)
    xml.attrib[XML_ACTOR__UNK_E] = str(actor.unkE)
    xml.append(position_to_xml(actor.pos))
    return xml


def object_to_xml(object: SsaObject) -> Element:
    xml = Element(XML_OBJECT)
    xml.attrib[XML_OBJECT__OBJECT_ID] = str(object.object.id)
    xml.attrib[XML_OBJECT__SCRIPT_ID] = str(object.script_id)
    xml.attrib[XML_OBJECT__HITBOX_WIDTH] = str(object.hitbox_w)
    xml.attrib[XML_OBJECT__HITBOX_HEIGHT] = str(object.hitbox_h)
    xml.attrib[XML_OBJECT__UNK_12] = str(object.unk12)
    xml.append(position_to_xml(object.pos))
    return xml


def performer_to_xml(performer: SsaPerformer) -> Element:
    xml = Element(XML_PERFORMER)
    xml.attrib[XML_PERFORMER__TYPE] = str(performer.type)
    xml.attrib[XML_PERFORMER__HITBOX_WIDTH] = str(performer.hitbox_w)
    xml.attrib[XML_PERFORMER__HITBOX_HEIGHT] = str(performer.hitbox_h)
    xml.attrib[XML_PERFORMER__UNK_10] = str(performer.unk10)
    xml.attrib[XML_PERFORMER__UNK_12] = str(performer.unk12)
    xml.append(position_to_xml(performer.pos))
    return xml


def trigger_to_xml(trigger: SsaEvent) -> Element:
    # NOTE: "Triggers" are called "events" in the model code and vice-versa. See docs.
    xml = Element(XML_TRIGGER)
    xml.attrib[XML_TRIGGER__WIDTH] = str(trigger.trigger_width)
    xml.attrib[XML_TRIGGER__HEIGHT] = str(trigger.trigger_height)
    xml.attrib[XML_TRIGGER__UNK_E] = str(trigger.unkE)
    xml.attrib[XML_TRIGGER__EVENT_ID] = str(trigger.trigger_id)
    xml.append(position_to_xml(trigger.pos))
    return xml


def unk10_to_xml(unk10: SsaUnk10) -> Element:
    xml = Element(XML_UNK10)
    xml.attrib[XML_UNK10__UNK_0] = str(unk10.unk0)
    xml.attrib[XML_UNK10__UNK_2] = str(unk10.unk2)
    xml.attrib[XML_UNK10__UNK_4] = str(unk10.unk4)
    xml.attrib[XML_UNK10__UNK_6] = str(unk10.unk6)
    return xml


def event_to_xml(event: SsaTrigger) -> Element:
    # NOTE: "Triggers" are called "events" in the model code and vice-versa. See docs.
    xml = Element(XML_EVENT)
    xml.attrib[XML_EVENT__COROUTINE_ID] = str(event.coroutine.id)
    xml.attrib[XML_EVENT__SCRIPT_ID] = str(event.script_id)
    xml.attrib[XML_EVENT__UNK_2] = str(event.unk2)
    xml.attrib[XML_EVENT__UNK_3] = str(event.unk3)
    return xml


def position_marker_to_xml(pos_mark: SsaPositionMarker) -> Element:
    xml = Element(XML_POS_MARK)
    xml.attrib[XML_POS_MARK__UNK_8] = str(pos_mark.unk8)
    xml.attrib[XML_POS_MARK__UNK_A] = str(pos_mark.unkA)
    xml.attrib[XML_POS_MARK__UNK_C] = str(pos_mark.unkC)
    xml.attrib[XML_POS_MARK__UNK_E] = str(pos_mark.unkE)
    xml.append(position_to_xml(pos_mark.pos))
    return xml


def position_to_xml(pos_mark: SsaPosition) -> Element:
    xml = Element(XML_POSITION)
    xml.attrib[XML_POSITION__DIRECTION] = direction_to_xml(pos_mark.direction)
    xml.attrib[XML_POSITION__X_POS] = str(pos_mark.x_relative)
    xml.attrib[XML_POSITION__Y_POS] = str(pos_mark.y_relative)
    xml.attrib[XML_POSITION__X_OFFSET] = str(pos_mark.x_offset)
    xml.attrib[XML_POSITION__Y_OFFSET] = str(pos_mark.y_offset)
    return xml


def direction_to_xml(direction: Pmd2ScriptDirection | None) -> str:
    if direction is None:
        return XML_POSITION__DIRECTION__NONE
    if direction.ssa_id == 1:
        return XML_POSITION__DIRECTION__DOWN
    elif direction.ssa_id == 2:
        return XML_POSITION__DIRECTION__DOWN_RIGHT
    elif direction.ssa_id == 3:
        return XML_POSITION__DIRECTION__RIGHT
    elif direction.ssa_id == 4:
        return XML_POSITION__DIRECTION__UP_RIGHT
    elif direction.ssa_id == 5:
        return XML_POSITION__DIRECTION__UP
    elif direction.ssa_id == 6:
        return XML_POSITION__DIRECTION__UP_LEFT
    elif direction.ssa_id == 7:
        return XML_POSITION__DIRECTION__LEFT
    elif direction.ssa_id == 8:
        return XML_POSITION__DIRECTION__DOWN_LEFT
    raise ValueError("Unknown SSA direction ID.")


def ssa_from_xml(ele: Element, scriptdata: Pmd2ScriptData) -> Ssa:
    """
    Creates a new scene from the given XML element.
    May raise an exception if a trigger has an invalid event assigned or the
    XML structure is otherwise invalid.
    """
    validate_xml_tag(ele, XML_SCENE)
    layer_list: list[SsaLayer] | None = None
    # NOTE: "Triggers" are called "events" in the model code and vice-versa. See docs.
    events: list[SsaTrigger] | None = None
    pos_marks: list[SsaPositionMarker] | None = None
    for child in ele:
        if child.tag == XML_LAYERS:
            pass  # done in second pass
        elif child.tag == XML_EVENTS:
            events = events_from_xml(child, scriptdata)
        elif child.tag == XML_POS_MARKS:
            pos_marks = position_markers_from_xml(child, scriptdata)
        else:
            raise XmlValidateError(ERR_UNKNOWN.format(child.tag))

    if events is None:
        raise XmlValidateError(ERR_MISSING.format(XML_EVENTS))

    if pos_marks is None:
        raise XmlValidateError(ERR_MISSING.format(XML_POS_MARKS))

    # 2nd pass
    for child in ele:
        if child.tag == XML_LAYERS:
            layer_list = layer_list_from_xml(child, len(events), scriptdata)

    if layer_list is None:
        raise XmlValidateError(ERR_MISSING.format(XML_LAYERS))

    return Ssa.new(scriptdata, layer_list, events, pos_marks)


def layer_list_from_xml(
    ele: Element, length_event_list: int, scriptdata: Pmd2ScriptData
) -> list[SsaLayer]:
    validate_xml_tag(ele, XML_LAYERS)
    return [layer_from_xml(c, length_event_list, scriptdata) for c in ele]


def events_from_xml(ele: Element, scriptdata: Pmd2ScriptData) -> list[SsaTrigger]:
    validate_xml_tag(ele, XML_EVENTS)
    return [event_from_xml(c, scriptdata) for c in ele]


def position_markers_from_xml(
    ele: Element, scriptdata: Pmd2ScriptData
) -> list[SsaPositionMarker]:
    validate_xml_tag(ele, XML_POS_MARKS)
    return [position_marker_from_xml(c, scriptdata) for c in ele]


def layer_from_xml(
    ele: Element, length_event_list: int, scriptdata: Pmd2ScriptData
) -> SsaLayer:
    validate_xml_tag(ele, XML_LAYER)
    actors: list[SsaActor] = []
    objects: list[SsaObject] = []
    performers: list[SsaPerformer] = []
    triggers: list[SsaEvent] = []
    unk10s: list[SsaUnk10] = []

    for child in ele:
        if child.tag == XML_ACTOR:
            actors.append(actor_from_xml(child, scriptdata))
        elif child.tag == XML_OBJECT:
            objects.append(object_from_xml(child, scriptdata))
        elif child.tag == XML_PERFORMER:
            performers.append(performer_from_xml(child, scriptdata))
        elif child.tag == XML_TRIGGER:
            triggers.append(trigger_from_xml(child, length_event_list, scriptdata))
        elif child.tag == XML_UNK10:
            unk10s.append(unk10_from_xml(child))
        else:
            raise XmlValidateError(ERR_UNKNOWN.format(child.tag))

    return SsaLayer.new(actors, objects, performers, triggers, unk10s)


def event_from_xml(ele: Element, scriptdata: Pmd2ScriptData) -> SsaTrigger:
    validate_xml_tag(ele, XML_EVENT)
    validate_xml_attribs(
        ele,
        [
            XML_EVENT__SCRIPT_ID,
            XML_EVENT__COROUTINE_ID,
            XML_EVENT__UNK_2,
            XML_EVENT__UNK_3,
        ],
    )
    return SsaTrigger(
        scriptdata=scriptdata,
        coroutine_id=u16_checked(int(ele.attrib[XML_EVENT__COROUTINE_ID])),
        unk2=u16_checked(int(ele.attrib[XML_EVENT__UNK_2])),
        unk3=u16_checked(int(ele.attrib[XML_EVENT__UNK_3])),
        script_id=u16_checked(int(ele.attrib[XML_EVENT__SCRIPT_ID])),
    )


def position_marker_from_xml(
    ele: Element, scriptdata: Pmd2ScriptData
) -> SsaPositionMarker:
    validate_xml_tag(ele, XML_POS_MARK)
    validate_xml_attribs(
        ele,
        [
            XML_POS_MARK__UNK_8,
            XML_POS_MARK__UNK_A,
            XML_POS_MARK__UNK_C,
            XML_POS_MARK__UNK_E,
        ],
    )
    return SsaPositionMarker(
        unk8=i16_checked(int(ele.attrib[XML_POS_MARK__UNK_8])),
        unkA=i16_checked(int(ele.attrib[XML_POS_MARK__UNK_A])),
        unkC=i16_checked(int(ele.attrib[XML_POS_MARK__UNK_C])),
        unkE=i16_checked(int(ele.attrib[XML_POS_MARK__UNK_E])),
        pos=_extract_position(ele, scriptdata),
    )


def actor_from_xml(ele: Element, scriptdata: Pmd2ScriptData) -> SsaActor:
    validate_xml_tag(ele, XML_ACTOR)
    validate_xml_attribs(
        ele,
        [
            XML_ACTOR__ACTOR_ID,
            XML_ACTOR__SCRIPT_ID,
            XML_ACTOR__UNK_E,
        ],
    )
    return SsaActor(
        scriptdata=scriptdata,
        actor_id=u16_checked(int(ele.attrib[XML_ACTOR__ACTOR_ID])),
        pos=_extract_position(ele, scriptdata),
        script_id=i16_checked(int(ele.attrib[XML_ACTOR__SCRIPT_ID])),
        unkE=i16_checked(int(ele.attrib[XML_ACTOR__UNK_E])),
    )


def object_from_xml(ele: Element, scriptdata: Pmd2ScriptData) -> SsaObject:
    validate_xml_tag(ele, XML_OBJECT)
    validate_xml_attribs(
        ele,
        [
            XML_OBJECT__OBJECT_ID,
            XML_OBJECT__SCRIPT_ID,
            XML_OBJECT__HITBOX_WIDTH,
            XML_OBJECT__HITBOX_HEIGHT,
            XML_OBJECT__UNK_12,
        ],
    )
    return SsaObject(
        scriptdata=scriptdata,
        object_id=u16_checked(int(ele.attrib[XML_OBJECT__OBJECT_ID])),
        htibox_w=i16_checked(int(ele.attrib[XML_OBJECT__HITBOX_WIDTH])),
        hitbox_h=i16_checked(int(ele.attrib[XML_OBJECT__HITBOX_HEIGHT])),
        pos=_extract_position(ele, scriptdata),
        script_id=i16_checked(int(ele.attrib[XML_OBJECT__SCRIPT_ID])),
        unk12=i16_checked(int(ele.attrib[XML_OBJECT__UNK_12])),
    )


def performer_from_xml(ele: Element, scriptdata: Pmd2ScriptData) -> SsaPerformer:
    validate_xml_tag(ele, XML_PERFORMER)
    validate_xml_attribs(
        ele,
        [
            XML_PERFORMER__TYPE,
            XML_PERFORMER__HITBOX_WIDTH,
            XML_PERFORMER__HITBOX_HEIGHT,
            XML_PERFORMER__UNK_10,
            XML_PERFORMER__UNK_12,
        ],
    )
    return SsaPerformer(
        type=u16_checked(int(ele.attrib[XML_PERFORMER__TYPE])),
        hitbox_w=i16_checked(int(ele.attrib[XML_PERFORMER__HITBOX_WIDTH])),
        hitbox_h=i16_checked(int(ele.attrib[XML_PERFORMER__HITBOX_HEIGHT])),
        pos=_extract_position(ele, scriptdata),
        unk10=i16_checked(int(ele.attrib[XML_PERFORMER__UNK_10])),
        unk12=i16_checked(int(ele.attrib[XML_PERFORMER__UNK_12])),
    )


def trigger_from_xml(
    ele: Element, length_event_list: int, scriptdata: Pmd2ScriptData
) -> SsaEvent:
    validate_xml_tag(ele, XML_TRIGGER)
    validate_xml_attribs(
        ele,
        [
            XML_TRIGGER__WIDTH,
            XML_TRIGGER__HEIGHT,
            XML_TRIGGER__UNK_E,
            XML_TRIGGER__EVENT_ID,
        ],
    )
    event_id = u16_checked(int(ele.attrib[XML_TRIGGER__EVENT_ID]))
    if event_id >= length_event_list:
        raise XmlValidateError(
            _(
                "The event ID {} is out of bounds for one of the triggers.".format(
                    event_id
                )
            )
        )
    return SsaEvent(
        trigger_width=u16_checked(int(ele.attrib[XML_TRIGGER__WIDTH])),
        trigger_height=u16_checked(int(ele.attrib[XML_TRIGGER__HEIGHT])),
        trigger_pointer=event_id,
        trigger_table_start=u16(0),
        pos=_extract_position(ele, scriptdata),
        unkE=u16_checked(int(ele.attrib[XML_TRIGGER__UNK_E])),
    )


def unk10_from_xml(ele: Element) -> SsaUnk10:
    validate_xml_tag(ele, XML_UNK10)
    validate_xml_attribs(
        ele,
        [
            XML_UNK10__UNK_0,
            XML_UNK10__UNK_2,
            XML_UNK10__UNK_4,
            XML_UNK10__UNK_6,
        ],
    )
    return SsaUnk10(
        unk0=i16_checked(int(ele.attrib[XML_UNK10__UNK_0])),
        unk2=i16_checked(int(ele.attrib[XML_UNK10__UNK_2])),
        unk4=i16_checked(int(ele.attrib[XML_UNK10__UNK_4])),
        unk6=i16_checked(int(ele.attrib[XML_UNK10__UNK_6])),
    )


def _extract_position(ele: Element, scriptdata: Pmd2ScriptData) -> SsaPosition:
    pos = None
    for child in ele:
        if child.tag == XML_POSITION:
            if pos is not None:
                raise XmlValidateError(ERR_UNKNOWN.format(child.tag))
            pos = position_from_xml(child, scriptdata)
        else:
            raise XmlValidateError(ERR_UNKNOWN.format(child.tag))
    if pos is None:
        raise XmlValidateError(ERR_MISSING.format(XML_POSITION))
    return pos


def position_from_xml(ele: Element, scriptdata: Pmd2ScriptData) -> SsaPosition:
    validate_xml_tag(ele, XML_POSITION)
    validate_xml_attribs(
        ele,
        [
            XML_POSITION__X_POS,
            XML_POSITION__Y_POS,
            XML_POSITION__X_OFFSET,
            XML_POSITION__Y_OFFSET,
        ],
    )
    return SsaPosition(
        scriptdata=scriptdata,
        x_pos=u16_checked(int(ele.attrib[XML_POSITION__X_POS])),
        y_pos=u16_checked(int(ele.attrib[XML_POSITION__Y_POS])),
        x_offset=u16_checked(int(ele.attrib[XML_POSITION__X_OFFSET])),
        y_offset=u16_checked(int(ele.attrib[XML_POSITION__Y_OFFSET])),
        direction=direction_from_xml(ele.attrib[XML_POSITION__DIRECTION]),
    )


def direction_from_xml(value: str) -> u16 | None:
    if value == XML_POSITION__DIRECTION__NONE:
        return None
    if value == XML_POSITION__DIRECTION__DOWN:
        return u16(1)
    elif value == XML_POSITION__DIRECTION__DOWN_RIGHT:
        return u16(2)
    elif value == XML_POSITION__DIRECTION__RIGHT:
        return u16(3)
    elif value == XML_POSITION__DIRECTION__UP_RIGHT:
        return u16(4)
    elif value == XML_POSITION__DIRECTION__UP:
        return u16(5)
    elif value == XML_POSITION__DIRECTION__UP_LEFT:
        return u16(6)
    elif value == XML_POSITION__DIRECTION__LEFT:
        return u16(7)
    elif value == XML_POSITION__DIRECTION__DOWN_LEFT:
        return u16(8)
    raise XmlValidateError(_("Unknown direction value."))


def ssa_xml_import(ele: Element, ssa: Ssa):
    """Imports the data from the XML element into the existing provided Ssa. See `ssa_from_xml`."""
    # noinspection PyProtectedMember
    new_ssa = ssa_from_xml(ele, ssa._scriptdata)
    ssa.layer_list = new_ssa.layer_list
    ssa.triggers = new_ssa.triggers
    ssa.position_markers = new_ssa.position_markers
