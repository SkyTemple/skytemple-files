"""
Types of the GraphQL schema represented as python types.

Types with expensive fields are split-off into partial types..
"""
from __future__ import annotations

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
from typing import Literal, TypedDict, Union


# noinspection PyPep8Naming
class Credit_Basic(TypedDict):
    id: str
    name: str | None
    contact: str | None


# noinspection PyPep8Naming
class Credit_DiscordHandle(TypedDict):
    discordHandle: str | None


class Credit(Credit_Basic, Credit_DiscordHandle):
    pass


def credit_canonical_name(this: Credit) -> str:
    if this["name"] is not None:
        return this["name"]
    if this["discordHandle"] is not None:
        return this["discordHandle"]
    return this["id"]


PHASE_INCOMPLETE: Literal["INCOMPLETE"] = "INCOMPLETE"
PHASE_EXISTS: Literal["EXISTS"] = "EXISTS"
PHASE_FULL: Literal["FULL"] = "FULL"
PHASE_UNKNOWN: Literal["UNKNOWN"] = "UNKNOWN"
Phase = Union[
    Literal["INCOMPLETE"],
    Literal["EXISTS"],
    Literal["FULL"],
    Literal["UNKNOWN"],
]


class OtherBounty(TypedDict):
    phase: int
    bounty: int


class MonsterBounty(TypedDict):
    modreward: bool
    incomplete: int | None
    exists: int | None
    full: int | None
    other: list[OtherBounty]


class ActionId(TypedDict):
    id: int
    name: str


class CopyOf(TypedDict):
    action: str
    locked: bool
    copyOf: str


class Sprite(TypedDict):
    action: str
    locked: bool
    animUrl: str
    offsetsUrl: str
    shadowsUrl: str


SpriteUnion = Union[Sprite, CopyOf]
OptionalSpriteUnion = Union[None, Sprite, CopyOf]


class Portrait(TypedDict):
    emotion: str
    locked: bool
    url: str


# noinspection PyPep8Naming
class MonsterFormSprites_Metadata(TypedDict):
    required: bool
    bounty: MonsterBounty
    phase: Phase
    phaseRaw: int
    creditPrimary: Credit | None
    creditSecondary: list[Credit]
    animDataXml: str | None
    zipUrl: str | None
    recolorSheetUrl: str | None
    modifiedDate: str


# noinspection PyPep8Naming
class MonsterFormSprites_Actions(TypedDict):
    actions: list[SpriteUnion]


# noinspection PyPep8Naming
class MonsterFormSprites_Action(TypedDict):
    action: OptionalSpriteUnion


class MonsterFormSprites(
    MonsterFormSprites_Metadata, MonsterFormSprites_Actions, MonsterFormSprites_Action
):
    pass


# noinspection PyPep8Naming
class MonsterFormPortraits_Metadata(TypedDict):
    required: bool
    bounty: MonsterBounty
    phase: Phase
    phaseRaw: int
    creditPrimary: Credit | None
    creditSecondary: list[Credit]
    sheetUrl: str
    recolorSheetUrl: str
    modifiedDate: str


# noinspection PyPep8Naming
class MonsterFormPortraits_PreviewEmotion(TypedDict):
    previewEmotion: Portrait | None


# noinspection PyPep8Naming
class MonsterFormPortraits_Emotions(TypedDict):
    emotions: list[Portrait]
    emotionsFlipped: list[Portrait]


# noinspection PyPep8Naming
class MonsterFormPortraits_Emotion(TypedDict):
    emotion: Portrait | None
    emotionFlipped: Portrait | None


class MonsterFormPortraits(
    MonsterFormPortraits_Metadata,
    MonsterFormPortraits_PreviewEmotion,
    MonsterFormPortraits_Emotions,
    MonsterFormPortraits_Emotion,
):
    pass


# noinspection PyPep8Naming
class MonsterForm_Metadata(TypedDict):
    monsterId: int
    path: str
    fullPath: str
    name: str
    fullName: str
    isShiny: bool
    isFemale: bool
    canon: bool


# noinspection PyPep8Naming
class MonsterForm_Portraits(TypedDict):
    portraits: MonsterFormPortraits


# noinspection PyPep8Naming
class MonsterForm_Sprites(TypedDict):
    sprites: MonsterFormSprites


class MonsterForm(MonsterForm_Metadata, MonsterForm_Portraits, MonsterForm_Sprites):
    pass


class Config(TypedDict):
    portraitSize: int
    portraitTileX: int
    portraitTileY: int
    emotions: list[str]
    actions: list[str]
    completionEmotions: list[list[int]]
    completionActions: list[list[int]]
    actionMap: list[ActionId]


# noinspection PyPep8Naming
class Monster_Metadata(TypedDict):
    id: int
    rawId: str
    name: str


# noinspection PyPep8Naming
class Monster_Forms(TypedDict):
    forms: list[MonsterForm]


# noinspection PyPep8Naming
class Monster_Get(TypedDict):
    get: MonsterForm | None


# noinspection PyPep8Naming
class Monster_Manual(TypedDict):
    manual: MonsterForm | None


class Monster(Monster_Metadata, Monster_Forms, Monster_Get, Monster_Manual):
    pass


# noinspection PyPep8Naming
class Query_ApiVersion(TypedDict):
    apiVersion: str


# noinspection PyPep8Naming
class Query_SearchMonster(TypedDict):
    searchMonster: list[Monster]


# noinspection PyPep8Naming
class Query_Monster(TypedDict):
    monster: list[Monster]


# noinspection PyPep8Naming
class Query_SearchCredit(TypedDict):
    searchCredit: list[Credit]


# noinspection PyPep8Naming
class Query_Credit(TypedDict):
    credit: list[Credit]


# noinspection PyPep8Naming
class Query_Config(TypedDict):
    config: Config


class Query(
    Query_ApiVersion,
    Query_SearchMonster,
    Query_Monster,
    Query_SearchCredit,
    Query_Credit,
    Query_Config,
):
    pass
