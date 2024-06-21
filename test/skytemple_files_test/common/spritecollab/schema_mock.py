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
from __future__ import annotations

import typing
from typing import Dict, List, Optional, Tuple

from graphql import (
    GraphQLArgument,
    GraphQLBoolean,
    GraphQLEnumType,
    GraphQLField,
    GraphQLInt,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    GraphQLString,
    GraphQLUnionType,
)

from skytemple_files.common.spritecollab.schema import (
    PHASE_EXISTS,
    PHASE_FULL,
    PHASE_UNKNOWN,
    Config,
    Credit,
    Monster_Metadata,
    MonsterForm,
    MonsterFormPortraits_Emotions,
    MonsterFormSprites_Actions,
)
from skytemple_files_test.common.spritecollab.sc_offline_fixtures import CONFIG_FIX


def mock_search_monster(_monster_name: str) -> List[Monster_Metadata]:
    raise NotImplementedError("mock_search_monster not implemented for the test mocks.")


def mock_monster(filter: Optional[List[int]]) -> List[Monster_Metadata]:
    index: Dict[int, Monster_Metadata] = {
        9998: {"id": 9998, "rawId": "9998", "name": "Dummy 9998"},
        9999: {"id": 9999, "rawId": "9999", "name": "Dummy 9999"},
    }

    result = []
    for key, value in index.items():
        if filter is None or key in filter:
            result.append(value)
    return result


def mock_search_credit(_query: str) -> List[Credit]:
    raise NotImplementedError("This is not implemented for the test mocks.")


def mock_credit() -> List[Credit]:
    raise NotImplementedError("This is not implemented for the test mocks.")


def mock_config() -> Config:
    return CONFIG_FIX


@typing.no_type_check
def mock_monster____all_forms(
    source: Monster_Metadata,
) -> Dict[Tuple[str, Tuple[int, bool, bool]], MonsterForm]:
    if source["id"] == 9998:
        return {
            ("", (0, False, False)): {
                "monsterId": 9998,
                "path": "",
                "fullPath": "9998",
                "name": "Dummy 9998",
                "fullName": "",
                "isShiny": False,
                "isFemale": False,
                "canon": False,
                "portraits": {
                    "required": True,
                    "bounty": [],
                    "phase": PHASE_EXISTS,
                    "phaseRaw": 1,
                    "creditPrimary": None,
                    "creditSecondary": [],
                    "sheetUrl": "test-portrait-sheet:0",
                    "recolorSheetUrl": "dummy",
                    "modifiedDate": "2000-12-01T13:14:15.000010+00:00",
                    "emotions": [
                        {
                            "emotion": "Normal",
                            "url": "dummy",
                        }
                    ],
                    "emotionsFlipped": [],
                    "previewEmotion": {
                        "emotion": "previewdummy",
                        "locked": False,
                        "url": "test-portrait:Special3.png",
                    },
                    "history": [],
                    "historyUrl": "dummy-1",
                },
                "sprites": {
                    "required": True,
                    "bounty": [],
                    "phase": PHASE_UNKNOWN,
                    "phaseRaw": -1,
                    "creditPrimary": None,
                    "creditSecondary": [],
                    "animDataXml": "dummy",
                    "zipUrl": "test-sprite-zip:0",
                    "recolorSheetUrl": "dummy",
                    "modifiedDate": "2001-03-02T04:12:03.000098+00:00",
                    "actions": [],
                    "history": [],
                    "historyUrl": "dummy-2",
                },
            },
        }
    if source["id"] == 9999:
        return {
            ("", (0, True, False)): {
                "monsterId": 9999,
                "path": "",
                "fullPath": "9999",
                "name": "Dummy 9999",
                "fullName": "",
                "isShiny": False,
                "isFemale": True,
                "canon": True,
                "portraits": {
                    "required": True,
                    "bounty": [],
                    "phase": PHASE_FULL,
                    "phaseRaw": 1,
                    "creditPrimary": {
                        "id": "CREDIT1",
                        "name": None,
                        "contact": None,
                        "discordHandle": None,
                    },
                    "creditSecondary": [
                        {
                            "id": "CREDIT2",
                            "name": "Credit 2",
                            "contact": "Credit 2 Contact",
                            "discordHandle": None,
                        },
                        {
                            "id": "CREDIT3",
                            "name": None,
                            "contact": None,
                            "discordHandle": "Discord Handle",
                        },
                    ],
                    "sheetUrl": "test-portrait-sheet:1",
                    "recolorSheetUrl": "dummy",
                    "modifiedDate": "3000-03-01T13:12:15.000010+00:00",
                    "emotions": [
                        {
                            "emotion": "Special3",
                            "locked": False,
                            "url": "test-portrait:Special3.png",
                        },
                        {
                            "emotion": "Special1",
                            "locked": False,
                            "url": "test-portrait:Special1.png",
                        },
                        {
                            "emotion": "Shouting",
                            "locked": False,
                            "url": "test-portrait:Shouting.png",
                        },
                        {
                            "emotion": "Stunned",
                            "locked": False,
                            "url": "test-portrait:Stunned.png",
                        },
                        {
                            "emotion": "Happy",
                            "locked": False,
                            "url": "test-portrait:Happy.png",
                        },
                        {
                            "emotion": "Surprised",
                            "locked": False,
                            "url": "test-portrait:Surprised.png",
                        },
                        {
                            "emotion": "Crying",
                            "locked": False,
                            "url": "test-portrait:Crying.png",
                        },
                        {
                            "emotion": "Sigh",
                            "locked": False,
                            "url": "test-portrait:Sigh.png",
                        },
                        {
                            "emotion": "Teary-Eyed",
                            "locked": False,
                            "url": "test-portrait:Teary-Eyed.png",
                        },
                        {
                            "emotion": "Inspired",
                            "locked": False,
                            "url": "test-portrait:Inspired.png",
                        },
                        {
                            "emotion": "Angry",
                            "locked": False,
                            "url": "test-portrait:Angry.png",
                        },
                        {
                            "emotion": "Special0",
                            "locked": False,
                            "url": "test-portrait:Special0.png",
                        },
                        {
                            "emotion": "Normal",
                            "locked": False,
                            "url": "test-portrait:Normal.png",
                        },
                        {
                            "emotion": "Joyous",
                            "locked": False,
                            "url": "test-portrait:Joyous.png",
                        },
                        {
                            "emotion": "Determined",
                            "locked": False,
                            "url": "test-portrait:Determined.png",
                        },
                        {
                            "emotion": "Dizzy",
                            "locked": False,
                            "url": "test-portrait:Dizzy.png",
                        },
                        {
                            "emotion": "Special2",
                            "locked": False,
                            "url": "test-portrait:Special2.png",
                        },
                        {
                            "emotion": "Sad",
                            "locked": False,
                            "url": "test-portrait:Sad.png",
                        },
                        {
                            "emotion": "Pain",
                            "locked": False,
                            "url": "test-portrait:Pain.png",
                        },
                        {
                            "emotion": "Worried",
                            "locked": False,
                            "url": "test-portrait:Worried.png",
                        },
                    ],
                    "emotionsFlipped": [
                        {
                            "emotion": "Special3^",
                            "locked": False,
                            "url": "test-portrait:Special3^.png",
                        },
                        {
                            "emotion": "Special1^",
                            "locked": False,
                            "url": "test-portrait:Special1^.png",
                        },
                        {
                            "emotion": "Shouting^",
                            "locked": False,
                            "url": "test-portrait:Shouting^.png",
                        },
                        {
                            "emotion": "Stunned^",
                            "locked": False,
                            "url": "test-portrait:Stunned^.png",
                        },
                        {
                            "emotion": "Happy^",
                            "locked": False,
                            "url": "test-portrait:Happy^.png",
                        },
                        {
                            "emotion": "Surprised^",
                            "locked": False,
                            "url": "test-portrait:Surprised^.png",
                        },
                        {
                            "emotion": "Crying^",
                            "locked": False,
                            "url": "test-portrait:Crying^.png",
                        },
                        {
                            "emotion": "Sigh^",
                            "locked": False,
                            "url": "test-portrait:Sigh^.png",
                        },
                        {
                            "emotion": "Teary-Eyed^",
                            "locked": False,
                            "url": "test-portrait:Teary-Eyed^.png",
                        },
                        {
                            "emotion": "Inspired^",
                            "locked": False,
                            "url": "test-portrait:Inspired^.png",
                        },
                        {
                            "emotion": "Angry^",
                            "locked": False,
                            "url": "test-portrait:Angry^.png",
                        },
                        {
                            "emotion": "Special0^",
                            "locked": False,
                            "url": "test-portrait:Special0^.png",
                        },
                        {
                            "emotion": "Normal^",
                            "locked": False,
                            "url": "test-portrait:Normal^.png",
                        },
                        {
                            "emotion": "Joyous^",
                            "locked": False,
                            "url": "test-portrait:Joyous^.png",
                        },
                        {
                            "emotion": "Determined^",
                            "locked": False,
                            "url": "test-portrait:Determined^.png",
                        },
                        {
                            "emotion": "Dizzy^",
                            "locked": False,
                            "url": "test-portrait:Dizzy^.png",
                        },
                        {
                            "emotion": "Special2^",
                            "locked": False,
                            "url": "test-portrait:Special2^.png",
                        },
                        {
                            "emotion": "Sad^",
                            "locked": False,
                            "url": "test-portrait:Sad^.png",
                        },
                        {
                            "emotion": "Pain^",
                            "locked": False,
                            "url": "test-portrait:Pain^.png",
                        },
                        {
                            "emotion": "Worried^",
                            "locked": False,
                            "url": "test-portrait:Worried^.png",
                        },
                    ],
                    "previewEmotion": {
                        "emotion": "previewdummy",
                        "locked": False,
                        "url": "test-portrait:Normal.png",
                    },
                    "history": [
                        {
                            "credit": {
                                "id": "CREDIT1",
                                "name": None,
                                "contact": None,
                                "discordHandle": None,
                            },
                            "modifiedDate": "2020-10-07T17:58:43.588731+00:00",
                            "modifications": ["NORMAL"],
                            "obsolete": True,
                            "license": {"license": "UNSPECIFIED"},
                        },
                        {
                            "credit": {
                                "id": "CREDIT2",
                                "name": "Credit 2",
                                "contact": "Credit 2 Contact",
                                "discordHandle": None,
                            },
                            "modifiedDate": "2021-10-07T17:58:43.588731+00:00",
                            "modifications": ["HAPPY"],
                            "obsolete": False,
                            "license": {"license": "CC_BY_NC4"},
                        },
                        {
                            "credit": {
                                "id": "CREDIT3",
                                "name": None,
                                "contact": None,
                                "discordHandle": None,
                            },
                            "modifiedDate": "2022-10-07T17:58:43.588731+00:00",
                            "modifications": ["NORMAL"],
                            "obsolete": False,
                            "license": {"name": "Test"},
                        },
                    ],
                    "historyUrl": "dummy-3",
                },
                "sprites": {
                    "required": True,
                    "bounty": [],
                    "phase": PHASE_UNKNOWN,
                    "phaseRaw": -1,
                    "creditPrimary": None,
                    "creditSecondary": [],
                    "animDataXml": "dummy",
                    "zipUrl": "test-sprite-zip:1",
                    "recolorSheetUrl": "dummy",
                    "modifiedDate": "2021-03-01T05:11:03.000004+00:00",
                    "actions": [
                        {
                            "action": "Charge",
                            "locked": False,
                            "animUrl": "test-sprite:1:Charge-Anim.png",
                            "offsetsUrl": "test-sprite:1:Charge-Offsets.png",
                            "shadowsUrl": "test-sprite:1:Charge-Shadow.png",
                        },
                        {
                            "action": "Idle",
                            "locked": False,
                            "animUrl": "test-sprite:1:Idle-Anim.png",
                            "offsetsUrl": "test-sprite:1:Idle-Offsets.png",
                            "shadowsUrl": "test-sprite:1:Idle-Shadow.png",
                        },
                        {
                            "action": "Rotate",
                            "locked": False,
                            "animUrl": "test-sprite:1:Rotate-Anim.png",
                            "offsetsUrl": "test-sprite:1:Rotate-Offsets.png",
                            "shadowsUrl": "test-sprite:1:Rotate-Shadow.png",
                        },
                        {
                            "action": "Walk",
                            "locked": False,
                            "animUrl": "test-sprite:1:Walk-Anim.png",
                            "offsetsUrl": "test-sprite:1:Walk-Offsets.png",
                            "shadowsUrl": "test-sprite:1:Walk-Shadow.png",
                        },
                        {
                            "action": "Double",
                            "locked": False,
                            "animUrl": "test-sprite:1:Double-Anim.png",
                            "offsetsUrl": "test-sprite:1:Double-Offsets.png",
                            "shadowsUrl": "test-sprite:1:Double-Shadow.png",
                        },
                        {
                            "action": "Hurt",
                            "locked": False,
                            "animUrl": "test-sprite:1:Hurt-Anim.png",
                            "offsetsUrl": "test-sprite:1:Hurt-Offsets.png",
                            "shadowsUrl": "test-sprite:1:Hurt-Shadow.png",
                        },
                        {
                            "action": "Swing",
                            "locked": False,
                            "animUrl": "test-sprite:1:Swing-Anim.png",
                            "offsetsUrl": "test-sprite:1:Swing-Offsets.png",
                            "shadowsUrl": "test-sprite:1:Swing-Shadow.png",
                        },
                        {
                            "action": "Hop",
                            "locked": False,
                            "animUrl": "test-sprite:1:Hop-Anim.png",
                            "offsetsUrl": "test-sprite:1:Hop-Offsets.png",
                            "shadowsUrl": "test-sprite:1:Hop-Shadow.png",
                        },
                        {
                            "action": "Sleep",
                            "locked": False,
                            "animUrl": "test-sprite:1:Sleep-Anim.png",
                            "offsetsUrl": "test-sprite:1:Sleep-Offsets.png",
                            "shadowsUrl": "test-sprite:1:Sleep-Shadow.png",
                        },
                        {
                            "action": "Attack",
                            "locked": False,
                            "animUrl": "test-sprite:1:Attack-Anim.png",
                            "offsetsUrl": "test-sprite:1:Attack-Offsets.png",
                            "shadowsUrl": "test-sprite:1:Attack-Shadow.png",
                        },
                        {
                            "action": "Pose",
                            "locked": False,
                            "copyOf": "Idle",
                        },
                        {
                            "action": "EventSleep",
                            "locked": False,
                            "copyOf": "Sleep",
                        },
                    ],
                    "history": [],
                    "historyUrl": "dummy-4",
                },
            },
            ("9999/9999", (9999, False, True)): {
                "monsterId": 9999,
                "path": "9999/9999",
                "fullPath": "9999/9999/9999",
                "name": "(Form 9999) (Form 9999)",
                "fullName": "(Form 9999) (Form 9999)",
                "isShiny": True,
                "isFemale": False,
                "canon": False,
                "portraits": {
                    "required": True,
                    "bounty": [],
                    "phase": PHASE_EXISTS,
                    "phaseRaw": 1,
                    "creditPrimary": None,
                    "creditSecondary": [],
                    "sheetUrl": "test-portrait-sheet:2",
                    "recolorSheetUrl": "dummy",
                    "modifiedDate": "1994-05-05T13:12:15.000010+00:00",
                    "emotions": [
                        {
                            "emotion": "Special1",
                            "locked": False,
                            "url": "test-portrait:Happy.png",
                        },
                        {
                            "emotion": "Happy",
                            "locked": False,
                            "url": "test-portrait:Happy.png",
                        },
                        {
                            "emotion": "Angry",
                            "locked": False,
                            "url": "test-portrait:Happy.png",
                        },
                    ],
                    "emotionsFlipped": [],
                    "previewEmotion": None,
                    "history": [],
                    "historyUrl": "dummy-5",
                },
                "sprites": {
                    "required": True,
                    "bounty": [],
                    "phase": PHASE_EXISTS,
                    "phaseRaw": -1,
                    "creditPrimary": None,
                    "creditSecondary": [],
                    "animDataXml": "dummy",
                    "zipUrl": "test-sprite-zip:2",
                    "recolorSheetUrl": "dummy",
                    "modifiedDate": "2021-03-02T05:11:03.000004+00:00",
                    "actions": [
                        {
                            "action": "Idle",
                            "locked": False,
                            "animUrl": "test-sprite:2:Idle-Anim.png",
                            "offsetsUrl": "test-sprite:2:Idle-Offsets.png",
                            "shadowsUrl": "test-sprite:2:Idle-Shadow.png",
                        }
                    ],
                    "history": [],
                    "historyUrl": "dummy-6",
                },
            },
        }
    raise NotImplementedError(f"This mock is not implemented for monster {source['id']}.")


def mock_monster__forms(source: Monster_Metadata) -> List[MonsterForm]:
    return list(mock_monster____all_forms(source).values())


def mock_monster__get(source: Monster_Metadata, form_id: int, shiny: bool, female: bool) -> Optional[MonsterForm]:
    all_forms = mock_monster____all_forms(source)
    for (_, key_get), value in all_forms.items():
        if (form_id, shiny, female) == key_get:
            return value
    return None


def mock_monster__manual(source: Monster_Metadata, path: str) -> Optional[MonsterForm]:
    all_forms = mock_monster____all_forms(source)
    for (key_manual, _), value in all_forms.items():
        if path == key_manual:
            return value
    return None


def mock_emotion(source: MonsterFormPortraits_Emotions, emotion, flipped):
    if flipped:
        emotion = emotion + "^"
    for entry in source["emotions"]:
        if entry["emotion"] == emotion:
            return entry
    return None


def mock_action(source: MonsterFormSprites_Actions, action):
    for entry in source["actions"]:
        if entry["action"] == action:
            return entry
    return None


# """An action mapped uniquely to an ID."""
# type ActionId {
#   id: Int!
#   name: String!
# }
action_id_type = GraphQLObjectType(
    "ActionId",
    lambda: {
        "id": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "name": GraphQLField(GraphQLNonNull(GraphQLString)),
    },
)

# """Configuration for this instance of SpriteCollab."""
# type Config {
#   """The portrait width and height in pixels."""
#   portraitSize: Int!
#
#   """How many portraits per row a portrait sheet contains."""
#   portraitTileX: Int!
#
#   """How many rows a portrait sheet contains."""
#   portraitTileY: Int!
#
#   """A list of known emotions. The position is the ID of the emotion."""
#   emotions: [String!]!
#
#   """A list of known action. The position is the ID of the action."""
#   actions: [String!]!
#
#   """
#   Returns a list, that for each phase contains a list of emotions (by index)
#   that need to exist for this phase to be considered completed.
#   """
#   completionEmotions: [[Int!]!]!
#
#   """
#   Returns a list, that for each phase contains a list of actions (by index) that
#   need to exist for this phase to be considered completed.
#   """
#   completionActions: [[Int!]!]!
#
#   """A mapping of actions to EoS action indices."""
#   actionMap: [ActionId!]!
# }
config_type = GraphQLObjectType(
    "Config",
    lambda: {
        "portraitSize": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "portraitTileX": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "portraitTileY": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "emotions": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLString)))),
        "actions": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLString)))),
        "completionEmotions": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLInt)))))
        ),
        "completionActions": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLInt)))))
        ),
        "actionMap": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(action_id_type)))),
    },
)

# """A sprite, which is a copy of another sprite."""
# type CopyOf {
#   """Action of this sprite."""
#   action: String!
#
#   """
#   Whether or not this sprite is locked and requires special permissions to be updated.
#   """
#   locked: Boolean!
#
#   """Which action this sprite is a copy of."""
#   copyOf: String!
# }
copy_of_type = GraphQLObjectType(
    "CopyOf",
    lambda: {
        "action": GraphQLField(GraphQLNonNull(GraphQLString)),
        "locked": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "copyOf": GraphQLField(GraphQLNonNull(GraphQLString)),
    },
)

# type Credit {
#   """Discord ID or absentee ID. Guaranteed to be an ASCII string."""
#   id: String!
#
#   """
#   The human-readable name of the author. Guaranteed to be an ASCII string.
#   """
#   name: String
#
#   """Contact information for this author."""
#   contact: String
#
#   """
#   Discord name and discriminator in the form Name#Discriminator (eg.
#   Capypara#7887), if this is a credit for a Discord profile, and the server can
#   resolve the ID to a Discord profile.
#   """
#   discordHandle: String
# }
credit_type = GraphQLObjectType(
    "Credit",
    lambda: {
        "id": GraphQLField(GraphQLNonNull(GraphQLString)),
        "name": GraphQLField(GraphQLString),
        "contact": GraphQLField(GraphQLString),
        "discordHandle": GraphQLField(GraphQLString),
    },
)

# """DateTime"""
# scalar DateTimeUtc
date_time_utc_type = GraphQLScalarType("DateTimeUtc")

# """An unknown license. The name is the identifier for the license."""
# type OtherLicense {
#   name: String!
# }
other_license_type = GraphQLObjectType(
    "OtherLicense",
    lambda: {
        "name": GraphQLField(GraphQLNonNull(GraphQLString)),
    },
)

# """A known license from a common list of options."""
# enum KnownLicenseType {
#   """The license could not be determined."""
#   UNKNOWN
#
#   """The license is not specified / the work is unlicensed."""
#   UNSPECIFIED
#
#   """Original license: When using, you must credit the contributors."""
#   PMDCOLLAB1
#
#   """
#   License for works between May 2023 - March 2024: You are free to use, copy
#   redistribute or modify sprites and portraits from this repository for your own
#   projects and contributions. When using portraits or sprites from this
#   repository, you must credit the contributors for each portrait and sprite you use.
#   """
#   PMDCOLLAB2
#
#   """
#   Licensed under Creative Commons Attribution-NonCommercial 4.0 International
#   """
#   CC_BY_NC4
# }
known_license_type_type = GraphQLEnumType(
    "KnownLicenseType",
    {
        "UNKNOWN": None,
        "UNSPECIFIED": None,
        "PMDCOLLAB1": None,
        "PMDCOLLAB2": None,
        "CC_BY_NC4": None,
    },
    names_as_values=True,
)

# """A known license from a common list of options."""
# type KnownLicense {
#   license: KnownLicenseType!
# }
known_license_type = GraphQLObjectType(
    "KnownLicense",
    lambda: {
        "license": GraphQLField(GraphQLNonNull(known_license_type_type)),
    },
)

# """
# The license that applies to the image of a sprite action or portrait emotion.
# """
# union License = KnownLicense | OtherLicense
license_union_type = GraphQLUnionType(
    "License",
    [known_license_type, other_license_type],
    resolve_type=lambda value, _, __: "KnownLicense" if "license" in value.keys() else "OtherLicense",
)

# type MonsterHistory {
#   """The author that contributed for this history entry."""
#   credit: Credit
#
#   """The date of the history entry submission."""
#   modifiedDate: DateTimeUtc!
#
#   """A list of emotions or actions that were changed in this history entry."""
#   modifications: [String!]!
#
#   """
#   True if the credit for this history entry was marked as no longer relevant for the current portraits or sprites.
#   """
#   obsolete: Boolean!
#
#   """The license applying to this modification."""
#   license: License!
# }
monster_history_type = GraphQLObjectType(
    "MonsterHistory",
    lambda: {
        "credit": GraphQLField(credit_type),
        "modifiedDate": GraphQLField(GraphQLNonNull(date_time_utc_type)),
        "modifications": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLString)))),
        "obsolete": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "license": GraphQLField(GraphQLNonNull(license_union_type)),
    },
)

# """The current phase of the sprite or portrait."""
# enum Phase {
#   INCOMPLETE
#   EXISTS
#   FULL
#
#   """
#   Returned if the phase value is non-standard. Use phaseRaw to get the raw ID.
#   """
#   UNKNOWN
# }
phase_type = GraphQLEnumType(
    "Phase",
    {
        "INCOMPLETE": None,
        "EXISTS": None,
        "FULL": None,
        "UNKNOWN": None,
    },
    names_as_values=True,
)

# """A single portrait for a single emotion."""
# type Portrait {
#   """Name of the emotion."""
#   emotion: String!
#
#   """
#   Whether or not this sprite is locked and requires special permissions to be updated.
#   """
#   locked: Boolean!
#
#   """URL to the portraits."""
#   url: String!
# }
portrait_type = GraphQLObjectType(
    "Portrait",
    lambda: {
        "emotion": GraphQLField(GraphQLNonNull(GraphQLString)),
        "locked": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "url": GraphQLField(GraphQLNonNull(GraphQLString)),
    },
)

# """A single sprite for a single action."""
# type Sprite {
#   """Action of this sprite."""
#   action: String!
#
#   """
#   Whether or not this sprite is locked and requires special permissions to be updated.
#   """
#   locked: Boolean!
#
#   """
#   URL to the sprite sheet containing the actual frames for the animation.
#   """
#   animUrl: String!
#
#   """
#   URL to the sprite sheet containing the sprite offset pixels for each frame.
#   """
#   offsetsUrl: String!
#
#   """
#   URL to the sprite sheet containing the shadow placeholders for each frame.
#   """
#   shadowsUrl: String!
# }
sprite_type = GraphQLObjectType(
    "Sprite",
    lambda: {
        "action": GraphQLField(GraphQLNonNull(GraphQLString)),
        "locked": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "animUrl": GraphQLField(GraphQLNonNull(GraphQLString)),
        "offsetsUrl": GraphQLField(GraphQLNonNull(GraphQLString)),
        "shadowsUrl": GraphQLField(GraphQLNonNull(GraphQLString)),
    },
)

# """
# A single sprite for a single action that is either a copy of another sprite (as
# defined in the AnimData.xml) or has it's own sprite data.
# """
# union SpriteUnion = Sprite | CopyOf
sprite_union_type = GraphQLUnionType(
    "SpriteUnion",
    [sprite_type, copy_of_type],
    resolve_type=lambda value, _, __: "CopyOf" if "copyOf" in value.keys() else "Sprite",
)

# """A bounty for a non-standard phase."""
# type OtherBounty {
#   phase: Int!
#   bounty: Int!
# }
other_bounty_type = GraphQLObjectType(
    "OtherBounty",
    lambda: {
        "phase": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "bounty": GraphQLField(GraphQLNonNull(GraphQLInt)),
    },
)

# """
# A SkyTemple Discord Server Guild Point bounty that will be rewarded, if the
# portrait or sprite has transitioned into a phase.
# """
# type MonsterBounty {
#   """
#   If true, SpriteBot will not automatically hand out the Guild Point bounty.
#   """
#   modreward: Boolean!
#
#   """Amount of points to reward if the phase changes to Incomplete."""
#   incomplete: Int
#
#   """Amount of points to reward if the phase changes to Exists."""
#   exists: Int
#
#   """Amount of points to reward if the phase changes to Full."""
#   full: Int
#   other: [OtherBounty!]!
# }
monster_bounty_type = GraphQLObjectType(
    "MonsterBounty",
    lambda: {
        "modreward": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "incomplete": GraphQLField(GraphQLInt),
        "exists": GraphQLField(GraphQLInt),
        "full": GraphQLField(GraphQLInt),
        "other": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(other_bounty_type)))),
    },
)

# type MonsterFormPortraits {
#   """Whether or not this form should have portraits."""
#   required: Boolean!
#
#   """Guild Point bounty for this portrait set."""
#   bounty: MonsterBounty!
#
#   """Current completion phase of the portraits."""
#   phase: Phase!
#
#   """Current completion phase of the portraits (raw ID)."""
#   phaseRaw: Int!
#
#   """Primary artist credits."""
#   creditPrimary: Credit
#
#   """All other artists credited."""
#   creditSecondary: [Credit!]!
#
#   """URL to a SpriteBot format sheet of all portraits."""
#   sheetUrl: String!
#
#   """URL to a SpriteBot format recolor sheet."""
#   recolorSheetUrl: String!
#
#   """A list of all existing portraits for the emotions."""
#   emotions: [Portrait!]!
#
#   """A single portrait for a given emotion."""
#   emotion(emotion: String!): Portrait
#
#   """
#   A single portrait. Return the 'Normal' portrait if avalaible, but may return another one if not present.
#   """
#   previewEmotion: Portrait
#
#   """A list of all existing flipped portraits for the emotions."""
#   emotionsFlipped: [Portrait!]!
#
#   """A single flipped portrait for a given emotion."""
#   emotionFlipped(emotion: String!): Portrait
#
#   """The date and time this portrait set was last updated."""
#   modifiedDate: DateTimeUtc
#
#   """List of all modifications made to those portraits since its creation."""
#   history: [MonsterHistory!]!
#
#   """
#   Returns a URL to retrieve the credits text file for the portraits for this form.
#   """
#   historyUrl: String
# }
monster_form_portraits_type = GraphQLObjectType(
    "MonsterFormPortraits",
    lambda: {
        "required": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "bounty": GraphQLField(GraphQLNonNull(monster_bounty_type)),
        "phase": GraphQLField(GraphQLNonNull(phase_type)),
        "phaseRaw": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "creditPrimary": GraphQLField(credit_type),
        "creditSecondary": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(credit_type)))),
        "sheetUrl": GraphQLField(GraphQLNonNull(GraphQLString)),
        "recolorSheetUrl": GraphQLField(GraphQLNonNull(GraphQLString)),
        "emotions": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(portrait_type)))),
        "emotion": GraphQLField(
            portrait_type,
            args={
                "emotion": GraphQLArgument(GraphQLNonNull(GraphQLString)),
            },
            resolve=lambda source, _info, emotion: mock_emotion(source, emotion, False),
        ),
        "emotionsFlipped": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(portrait_type)))),
        "emotionFlipped": GraphQLField(
            portrait_type,
            args={
                "emotion": GraphQLArgument(GraphQLNonNull(GraphQLString)),
            },
            resolve=lambda source, _info, emotion: mock_emotion(source, emotion, True),
        ),
        "previewEmotion": GraphQLField(portrait_type),
        "modifiedDate": GraphQLField(date_time_utc_type),
        "history": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(monster_history_type)))),
        "historyUrl": GraphQLField(GraphQLString),
    },
)

# type MonsterFormSprites {
#   """Whether or not this form should have sprites."""
#   required: Boolean!
#
#   """Guild Point bounty for this sprite set."""
#   bounty: MonsterBounty!
#
#   """Current completion phase of the sprites."""
#   phase: Phase!
#
#   """Current completion phase of the sprites (raw ID)."""
#   phaseRaw: Int!
#
#   """Primary artist credits."""
#   creditPrimary: Credit
#
#   """All other artists credited."""
#   creditSecondary: [Credit!]!
#
#   """URL to the AnimData XML file for this sprite set."""
#   animDataXml: String
#
#   """URL to a SpriteBot format ZIP archive of all sprites."""
#   zipUrl: String
#
#   """URL to a SpriteBot format recolor sheet."""
#   recolorSheetUrl: String
#
#   """A list of all existing sprites for the actions."""
#   actions: [SpriteUnion!]!
#
#   """A single sprite for a given action."""
#   action(action: String!): SpriteUnion
#
#   """The date and time this sprite set was last updated."""
#   modifiedDate: DateTimeUtc
#
#   """List of all modifications made to those sprites since its creation."""
#   history: [MonsterHistory!]!
#
#   """
#   Returns a URL to retrieve the credits text file for the sprites for this form.
#   """
#   historyUrl: String
# }
monster_form_sprites_type = GraphQLObjectType(
    "MonsterFormSprites",
    lambda: {
        "required": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "bounty": GraphQLField(GraphQLNonNull(monster_bounty_type)),
        "phase": GraphQLField(GraphQLNonNull(phase_type)),
        "phaseRaw": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "creditPrimary": GraphQLField(credit_type),
        "creditSecondary": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(credit_type)))),
        "animDataXml": GraphQLField(GraphQLString),
        "zipUrl": GraphQLField(GraphQLString),
        "recolorSheetUrl": GraphQLField(GraphQLString),
        "actions": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(sprite_union_type)))),
        "action": GraphQLField(
            sprite_union_type,
            args={
                "action": GraphQLArgument(GraphQLNonNull(GraphQLString)),
            },
            resolve=lambda source, _info, action: mock_action(source, action),
        ),
        "modifiedDate": GraphQLField(date_time_utc_type),
        "history": GraphQLField(GraphQLNonNull(GraphQLList(GraphQLNonNull(monster_history_type)))),
        "historyUrl": GraphQLField(GraphQLString),
    },
)

# type MonsterForm {
#   """The ID of the monster, that this form belongs to."""
#   monsterId: Int!
#
#   """
#   The path to this form (without the monster ID) as it's specified in the
#   SpriteCollab tracker.json file and repository file structure.
#   """
#   path: String!
#
#   """
#   The path to this form (including the monster ID) as it's specified in the
#   SpriteCollab tracker.json file and repository file structure.
#   """
#   fullPath: String!
#
#   """Human-readable name of this form."""
#   name: String!
#
#   """
#   Human-readable full name of this form (excluding the monster name itself).
#   """
#   fullName: String!
#
#   """Whether or not this form is considered for a shiny."""
#   isShiny: Boolean!
#
#   """Whether or not this form is considered for a female monsters."""
#   isFemale: Boolean!
#
#   """Whether or not this form is canon."""
#   canon: Boolean!
#
#   """Portraits for this form."""
#   portraits: MonsterFormPortraits!
#
#   """Sprites for this form."""
#   sprites: MonsterFormSprites!
# }
monster_form_type = GraphQLObjectType(
    "MonsterForm",
    lambda: {
        "monsterId": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "path": GraphQLField(GraphQLNonNull(GraphQLString)),
        "fullPath": GraphQLField(GraphQLNonNull(GraphQLString)),
        "name": GraphQLField(GraphQLNonNull(GraphQLString)),
        "fullName": GraphQLField(GraphQLNonNull(GraphQLString)),
        "isShiny": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "isFemale": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "canon": GraphQLField(GraphQLNonNull(GraphQLBoolean)),
        "portraits": GraphQLField(GraphQLNonNull(monster_form_portraits_type)),
        "sprites": GraphQLField(GraphQLNonNull(monster_form_sprites_type)),
    },
)

# type Monster {
#   """ID of this monster."""
#   id: Int!
#
#   """
#   Raw ID of this monster, as a string. This is a 4-character numeric string, padded with leading zeroes.
#   """
#   rawId: String!
#
#   """Human-readable name of this monster."""
#   name: String!
#
#   """All forms that exist for this monster."""
#   forms: [MonsterForm!]!
#
#   """Get a specific form for this monster."""
#   get(formId: Int!, shiny: Boolean!, female: Boolean!): MonsterForm
#
#   """
#   Manually enter the path to a monster, seperated by /. This should match the
#   path as it is stored in SpriteCollab, however the path passed in might be
#   collapsed until a unique form is found.
#   """
#   manual(path: String!): MonsterForm
# }
monster_type = GraphQLObjectType(
    "Monster",
    lambda: {
        "id": GraphQLField(GraphQLNonNull(GraphQLInt)),
        "rawId": GraphQLField(GraphQLNonNull(GraphQLString)),
        "name": GraphQLField(GraphQLNonNull(GraphQLString)),
        "forms": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(monster_form_type))),
            resolve=lambda source, _info: mock_monster__forms(source),
        ),
        "get": GraphQLField(
            monster_form_type,
            args={
                "formId": GraphQLArgument(GraphQLNonNull(GraphQLInt)),
                "shiny": GraphQLArgument(GraphQLNonNull(GraphQLBoolean)),
                "female": GraphQLArgument(GraphQLNonNull(GraphQLBoolean)),
            },
            resolve=lambda source, _info, form_id, shiny, female: mock_monster__get(source, form_id, shiny, female),
        ),
        "manual": GraphQLField(
            monster_form_type,
            args={
                "path": GraphQLArgument(GraphQLNonNull(GraphQLString)),
            },
            resolve=lambda source, _info, path: mock_monster__manual(source, path),
        ),
    },
)

# type Query {
#   """Version of this API."""
#   apiVersion: String!
#
#   """
#   Search for a monster by (parts) of its name. Results are sorted by best match.
#   """
#   searchMonster(monsterName: String!): [Monster!]!
#
#   """Retrieve a list of monsters."""
#   monster(
#     """Monster IDs to limit the request to."""
#     filter: [Int!]
#   ): [Monster!]!
#
#   """
#   Search for a credit entry by (parts) of the ID, the author name or the contact info. Results are sorted by best match.
#   """
#   searchCredit(query: String!): [Credit!]!
#
#   """Retrieve a list of credits."""
#   credit: [Credit!]!
#
#   """Configuration for this instance of SpriteCollab."""
#   config: Config!
# }
#
# noinspection PyPep8Naming
query_type = GraphQLObjectType(
    "Query",
    lambda: {
        "apiVersion": GraphQLField(
            GraphQLNonNull(GraphQLString),
            resolve=lambda _source, _info: "dummy",
        ),
        "searchMonster": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(monster_type))),
            args={
                "monsterName": GraphQLArgument(GraphQLNonNull(GraphQLString)),
            },
            resolve=lambda _source, _info, monsterName: mock_search_monster(monsterName),
        ),
        "monster": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(monster_type))),
            args={
                "filter": GraphQLArgument(GraphQLList(GraphQLNonNull(GraphQLInt))),
            },
            resolve=lambda _source, _info, filter=None: mock_monster(filter),
        ),
        "searchCredit": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(credit_type))),
            args={
                "query": GraphQLArgument(GraphQLNonNull(GraphQLString)),
            },
            resolve=lambda _source, _info, query: mock_search_credit(query),
        ),
        "credit": GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(credit_type))),
            resolve=lambda _source, _info: mock_credit(),
        ),
        "config": GraphQLField(
            GraphQLNonNull(config_type),
            resolve=lambda _source, _info: mock_config(),
        ),
    },
)

SprieCollabLocalSchema = GraphQLSchema(
    query=query_type,
    types=[
        action_id_type,
        config_type,
        copy_of_type,
        credit_type,
        date_time_utc_type,
        monster_type,
        monster_bounty_type,
        monster_form_type,
        monster_form_portraits_type,
        monster_form_sprites_type,
        other_bounty_type,
        phase_type,
        portrait_type,
        sprite_type,
        sprite_union_type,
        query_type,
    ],
)
