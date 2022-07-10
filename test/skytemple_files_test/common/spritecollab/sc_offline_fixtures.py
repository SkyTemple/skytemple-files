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

import datetime
from typing import List

from skytemple_files.common.spritecollab.client import (
    MonsterFormDetails,
    MonsterFormInfo,
    MonsterFormInfoWithPortrait,
    SpriteUrls,
)
from skytemple_files.common.spritecollab.schema import (
    PHASE_EXISTS,
    PHASE_FULL,
    PHASE_UNKNOWN,
    Config,
)
from skytemple_files_test.common.spritecollab.requests_mock import AioRequestAdapterMock

CONFIG_FIX: Config = {
    "portraitSize": 40,
    "portraitTileX": 5,
    "portraitTileY": 8,
    "emotions": [
        "Normal",
        "Happy",
        "Pain",
        "Angry",
        "Worried",
        "Sad",
        "Crying",
        "Shouting",
        "Teary-Eyed",
        "Determined",
        "Joyous",
        "Inspired",
        "Surprised",
        "Dizzy",
        "Special0",
        "Special1",
        "Sigh",
        "Stunned",
        "Special2",
        "Special3",
    ],
    "actions": [
        "Idle",
        "Walk",
        "Sleep",
        "Hurt",
        "Attack",
        "Charge",
        "Shoot",
        "Strike",
        "Chop",
        "Scratch",
        "Punch",
        "Slap",
        "Slice",
        "MultiScratch",
        "MultiStrike",
        "Uppercut",
        "Ricochet",
        "Bite",
        "Shake",
        "Jab",
        "Kick",
        "Lick",
        "Slam",
        "Stomp",
        "Appeal",
        "Dance",
        "Twirl",
        "TailWhip",
        "Sing",
        "Sound",
        "Rumble",
        "FlapAround",
        "Gas",
        "Shock",
        "Emit",
        "SpAttack",
        "Withdraw",
        "RearUp",
        "Swell",
        "Swing",
        "Double",
        "Rotate",
        "Hop",
        "Hover",
        "QuickStrike",
        "EventSleep",
        "Wake",
        "Eat",
        "Tumble",
        "Pose",
        "Pull",
        "Pain",
        "Float",
        "DeepBreath",
        "Nod",
        "Sit",
        "LookUp",
        "Sink",
        "Trip",
        "Laying",
        "LeapForth",
        "Head",
        "Cringe",
        "LostBalance",
        "TumbleBack",
        "HitGround",
        "Faint",
        "Fainted",
        "StandingUp",
        "DigIn",
        "DigOut",
        "Wiggle",
        "Yawn",
        "RaiseArms",
        "CarefulWalk",
        "Injured",
        "Jump",
        "Roar",
        "Wave",
        "Cry",
        "Bow",
        "Special0",
        "Special1",
        "Special2",
        "Special3",
        "Special4",
        "Special5",
        "Special6",
        "Special7",
        "Special8",
        "Special9",
        "Special10",
        "Special11",
        "Special12",
        "Special13",
        "Special14",
        "Special15",
        "Special16",
        "Special17",
        "Special18",
        "Special19",
        "Special20",
        "Special21",
        "Special22",
        "Special23",
        "Special24",
        "Special25",
        "Special26",
        "Special27",
        "Special28",
        "Special29",
        "Special30",
        "Special31",
    ],
    "completionEmotions": [
        [0],
        [0],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17],
    ],
    "completionActions": [
        [0, 1],
        [0, 1, 2, 3, 4, 5, 39, 40, 41, 42],
        [
            0,
            1,
            2,
            3,
            4,
            5,
            39,
            40,
            41,
            42,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
            64,
            65,
            66,
        ],
    ],
    "actionMap": [
        {"id": 1, "name": "Attack"},
        {"id": 7, "name": "Idle"},
        {"id": 9, "name": "Double"},
        {"id": 8, "name": "Swing"},
        {"id": 0, "name": "Walk"},
        {"id": 10, "name": "Hop"},
        {"id": 6, "name": "Hurt"},
        {"id": 12, "name": "Rotate"},
        {"id": 5, "name": "Sleep"},
        {"id": 11, "name": "Charge"},
    ],
}

LIST_MONSTER_FORMS_NO_PORTRAITS_FIX: List[MonsterFormInfo] = [
    MonsterFormInfo(
        _request_adapter=AioRequestAdapterMock(),
        monster_id=9998,
        form_path="",
        monster_name="Dummy 9998",
        full_form_name="Dummy 9998",
        shiny=False,
        female=False,
        canon=False,
        portraits_phase=PHASE_EXISTS,
        sprites_phase=PHASE_UNKNOWN,
        portraits_modified_date=datetime.datetime(
            2000, 12, 1, 13, 14, 15, 10, tzinfo=datetime.timezone.utc
        ),
        sprites_modified_date=datetime.datetime(
            2001, 3, 2, 4, 12, 3, 98, tzinfo=datetime.timezone.utc
        ),
    ),
    MonsterFormInfo(
        _request_adapter=AioRequestAdapterMock(),
        monster_id=9999,
        form_path="",
        monster_name="Dummy 9999",
        full_form_name="Dummy 9999",
        shiny=False,
        female=True,
        canon=True,
        portraits_phase=PHASE_FULL,
        sprites_phase=PHASE_UNKNOWN,
        portraits_modified_date=datetime.datetime(
            3000, 3, 1, 13, 12, 15, 10, tzinfo=datetime.timezone.utc
        ),
        sprites_modified_date=datetime.datetime(
            2021, 3, 1, 5, 11, 3, 4, tzinfo=datetime.timezone.utc
        ),
    ),
    MonsterFormInfo(
        _request_adapter=AioRequestAdapterMock(),
        monster_id=9999,
        form_path="9999/9999",
        monster_name="Dummy 9999",
        full_form_name="Dummy 9999 (Form 9999) (Form 9999)",
        shiny=True,
        female=False,
        canon=False,
        portraits_phase=PHASE_EXISTS,
        sprites_phase=PHASE_EXISTS,
        portraits_modified_date=datetime.datetime(
            1994, 5, 5, 13, 12, 15, 10, tzinfo=datetime.timezone.utc
        ),
        sprites_modified_date=datetime.datetime(
            2021, 3, 2, 5, 11, 3, 4, tzinfo=datetime.timezone.utc
        ),
    ),
]

LIST_MONSTER_FORMS_WITH_PORTRAITS_FIX: List[MonsterFormInfoWithPortrait] = [
    MonsterFormInfoWithPortrait(
        _request_adapter=AioRequestAdapterMock(),
        monster_id=9998,
        form_path="",
        monster_name="Dummy 9998",
        full_form_name="Dummy 9998",
        shiny=False,
        female=False,
        canon=False,
        portraits_phase=PHASE_EXISTS,
        sprites_phase=PHASE_UNKNOWN,
        portraits_modified_date=datetime.datetime(
            2000, 12, 1, 13, 14, 15, 10, tzinfo=datetime.timezone.utc
        ),
        sprites_modified_date=datetime.datetime(
            2001, 3, 2, 4, 12, 3, 98, tzinfo=datetime.timezone.utc
        ),
        preview_portrait="test-portrait:Special3.png",
    ),
    MonsterFormInfoWithPortrait(
        _request_adapter=AioRequestAdapterMock(),
        monster_id=9999,
        form_path="",
        monster_name="Dummy 9999",
        full_form_name="Dummy 9999",
        shiny=False,
        female=True,
        canon=True,
        portraits_phase=PHASE_FULL,
        sprites_phase=PHASE_UNKNOWN,
        portraits_modified_date=datetime.datetime(
            3000, 3, 1, 13, 12, 15, 10, tzinfo=datetime.timezone.utc
        ),
        sprites_modified_date=datetime.datetime(
            2021, 3, 1, 5, 11, 3, 4, tzinfo=datetime.timezone.utc
        ),
        preview_portrait="test-portrait:Normal.png",
    ),
    MonsterFormInfoWithPortrait(
        _request_adapter=AioRequestAdapterMock(),
        monster_id=9999,
        form_path="9999/9999",
        monster_name="Dummy 9999",
        full_form_name="Dummy 9999 (Form 9999) (Form 9999)",
        shiny=True,
        female=False,
        canon=False,
        portraits_phase=PHASE_EXISTS,
        sprites_phase=PHASE_EXISTS,
        portraits_modified_date=datetime.datetime(
            1994, 5, 5, 13, 12, 15, 10, tzinfo=datetime.timezone.utc
        ),
        sprites_modified_date=datetime.datetime(
            2021, 3, 2, 5, 11, 3, 4, tzinfo=datetime.timezone.utc
        ),
        preview_portrait=None,
    ),
]

MONSTER_FORM_DETAILS_FIX: List[MonsterFormDetails] = [
    MonsterFormDetails(
        _request_adapter=AioRequestAdapterMock(),
        monster_id=9999,
        form_path="",
        monster_name="Dummy 9999",
        full_form_name="Dummy 9999",
        shiny=False,
        female=True,
        canon=True,
        portraits_phase=PHASE_FULL,
        sprites_phase=PHASE_UNKNOWN,
        portraits_modified_date=datetime.datetime(
            3000, 3, 1, 13, 12, 15, 10, tzinfo=datetime.timezone.utc
        ),
        sprites_modified_date=datetime.datetime(
            2021, 3, 1, 5, 11, 3, 4, tzinfo=datetime.timezone.utc
        ),
        portraits={
            "Special3": "test-portrait:Special3.png",
            "Special1": "test-portrait:Special1.png",
            "Shouting": "test-portrait:Shouting.png",
            "Stunned": "test-portrait:Stunned.png",
            "Happy": "test-portrait:Happy.png",
            "Surprised": "test-portrait:Surprised.png",
            "Crying": "test-portrait:Crying.png",
            "Sigh": "test-portrait:Sigh.png",
            "Teary-Eyed": "test-portrait:Teary-Eyed.png",
            "Inspired": "test-portrait:Inspired.png",
            "Angry": "test-portrait:Angry.png",
            "Special0": "test-portrait:Special0.png",
            "Normal": "test-portrait:Normal.png",
            "Joyous": "test-portrait:Joyous.png",
            "Determined": "test-portrait:Determined.png",
            "Dizzy": "test-portrait:Dizzy.png",
            "Special2": "test-portrait:Special2.png",
            "Sad": "test-portrait:Sad.png",
            "Pain": "test-portrait:Pain.png",
            "Worried": "test-portrait:Worried.png",
            "Special3^": "test-portrait:Special3^.png",
            "Special1^": "test-portrait:Special1^.png",
            "Shouting^": "test-portrait:Shouting^.png",
            "Stunned^": "test-portrait:Stunned^.png",
            "Happy^": "test-portrait:Happy^.png",
            "Surprised^": "test-portrait:Surprised^.png",
            "Crying^": "test-portrait:Crying^.png",
            "Sigh^": "test-portrait:Sigh^.png",
            "Teary-Eyed^": "test-portrait:Teary-Eyed^.png",
            "Inspired^": "test-portrait:Inspired^.png",
            "Angry^": "test-portrait:Angry^.png",
            "Special0^": "test-portrait:Special0^.png",
            "Normal^": "test-portrait:Normal^.png",
            "Joyous^": "test-portrait:Joyous^.png",
            "Determined^": "test-portrait:Determined^.png",
            "Dizzy^": "test-portrait:Dizzy^.png",
            "Special2^": "test-portrait:Special2^.png",
            "Sad^": "test-portrait:Sad^.png",
            "Pain^": "test-portrait:Pain^.png",
            "Worried^": "test-portrait:Worried^.png",
        },
        portrait_sheet="test-portrait-sheet:1",
        sprites={
            "Charge": SpriteUrls(
                anim="test-sprite:1:Charge-Anim.png",
                shadows="test-sprite:1:Charge-Shadow.png",
                offsets="test-sprite:1:Charge-Offsets.png",
            ),
            "Idle": SpriteUrls(
                anim="test-sprite:1:Idle-Anim.png",
                shadows="test-sprite:1:Idle-Shadow.png",
                offsets="test-sprite:1:Idle-Offsets.png",
            ),
            "Rotate": SpriteUrls(
                anim="test-sprite:1:Rotate-Anim.png",
                shadows="test-sprite:1:Rotate-Shadow.png",
                offsets="test-sprite:1:Rotate-Offsets.png",
            ),
            "Walk": SpriteUrls(
                anim="test-sprite:1:Walk-Anim.png",
                shadows="test-sprite:1:Walk-Shadow.png",
                offsets="test-sprite:1:Walk-Offsets.png",
            ),
            "Double": SpriteUrls(
                anim="test-sprite:1:Double-Anim.png",
                shadows="test-sprite:1:Double-Shadow.png",
                offsets="test-sprite:1:Double-Offsets.png",
            ),
            "Hurt": SpriteUrls(
                anim="test-sprite:1:Hurt-Anim.png",
                shadows="test-sprite:1:Hurt-Shadow.png",
                offsets="test-sprite:1:Hurt-Offsets.png",
            ),
            "Swing": SpriteUrls(
                anim="test-sprite:1:Swing-Anim.png",
                shadows="test-sprite:1:Swing-Shadow.png",
                offsets="test-sprite:1:Swing-Offsets.png",
            ),
            "Hop": SpriteUrls(
                anim="test-sprite:1:Hop-Anim.png",
                shadows="test-sprite:1:Hop-Shadow.png",
                offsets="test-sprite:1:Hop-Offsets.png",
            ),
            "Sleep": SpriteUrls(
                anim="test-sprite:1:Sleep-Anim.png",
                shadows="test-sprite:1:Sleep-Shadow.png",
                offsets="test-sprite:1:Sleep-Offsets.png",
            ),
            "Attack": SpriteUrls(
                anim="test-sprite:1:Attack-Anim.png",
                shadows="test-sprite:1:Attack-Shadow.png",
                offsets="test-sprite:1:Attack-Offsets.png",
            ),
        },
        sprite_zip="test-sprite-zip:1",
        sprites_copy_of={
            "Pose": "Idle",
            "EventSleep": "Sleep",
        },
        portrait_credits=[
            {"id": "CREDIT1", "name": None, "contact": None, "discordHandle": None},
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
        sprite_credits=[],
    ),
    MonsterFormDetails(
        _request_adapter=AioRequestAdapterMock(),
        monster_id=9999,
        form_path="9999/9999",
        monster_name="Dummy 9999",
        full_form_name="Dummy 9999 (Form 9999) (Form 9999)",
        shiny=True,
        female=False,
        canon=False,
        portraits_phase=PHASE_EXISTS,
        sprites_phase=PHASE_EXISTS,
        portraits_modified_date=datetime.datetime(
            1994, 5, 5, 13, 12, 15, 10, tzinfo=datetime.timezone.utc
        ),
        sprites_modified_date=datetime.datetime(
            2021, 3, 2, 5, 11, 3, 4, tzinfo=datetime.timezone.utc
        ),
        portraits={
            "Special1": "test-portrait:Happy.png",
            "Happy": "test-portrait:Happy.png",
            "Angry": "test-portrait:Happy.png",
        },
        portrait_sheet="test-portrait-sheet:2",
        sprites={
            "Idle": SpriteUrls(
                anim="test-sprite:2:Idle-Anim.png",
                shadows="test-sprite:2:Idle-Shadow.png",
                offsets="test-sprite:2:Idle-Offsets.png",
            )
        },
        sprite_zip="test-sprite-zip:2",
        sprites_copy_of={},
        portrait_credits=[],
        sprite_credits=[],
    ),
]

MONSTER_FORM_DETAILS_FIX_MULTI_MON = [
    MonsterFormDetails(
        _request_adapter=AioRequestAdapterMock(),
        monster_id=9998,
        form_path="",
        monster_name="Dummy 9998",
        full_form_name="Dummy 9998",
        shiny=False,
        female=False,
        canon=False,
        portraits_phase=PHASE_EXISTS,
        sprites_phase=PHASE_UNKNOWN,
        portraits_modified_date=datetime.datetime(
            2000, 12, 1, 13, 14, 15, 10, tzinfo=datetime.timezone.utc
        ),
        sprites_modified_date=datetime.datetime(
            2001, 3, 2, 4, 12, 3, 98, tzinfo=datetime.timezone.utc
        ),
        portraits={
            "Normal": "dummy",
        },
        portrait_sheet="test-portrait-sheet:0",
        sprites={},
        sprite_zip="test-sprite-zip:0",
        sprites_copy_of={},
        portrait_credits=[],
        sprite_credits=[],
    ),
] + MONSTER_FORM_DETAILS_FIX

QUERY_API_VERSION_FIX = {
    "apiVersion": "dummy",
}
