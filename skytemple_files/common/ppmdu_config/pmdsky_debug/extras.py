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

from typing import Protocol, List, Optional

from pmdsky_debug_py.eu import EuArm9Section, EuOverlay11Section
from pmdsky_debug_py.jp import JpArm9Section, JpOverlay11Section
from pmdsky_debug_py.na import NaArm9Section, NaOverlay11Section
from pmdsky_debug_py.protocol import Symbol, SectionProtocol


DEBUG_PRINT2_DESC = (
    "Would log a printf format string in the debug binary. A no-op in the final binary."
)
COMPRESSED_IQ_GROUP_SKILLS_DESC = (
    "Replaces IQ_GROUPS_SKILLS when the patch 'CompressIQData' is applied."
)
GUEST_MONSTER_DATA2_DESC = "Requires EditExtraPokemon patch."
EXTRA_DUNGEON_DATA_DESC = "Requires EditExtraPokemon patch."
MONSTER_GROUND_IDLE_ANIM_DESC = (
    "This table is added by the 'ChangePokemonGroundAnim' patch. "
    "See the patch description for details."
)
OV36_DESC = "This is End45's 'extra space' overlay. It requires the 'ExtraSpace' patch."


class ExtraArm9FunctionsProtocol(Protocol):
    DebugPrint2: Symbol[
        List[int],
        None,
    ]


class ExtraArm9DataProtocol(Protocol):
    COMPRESSED_IQ_GROUP_SKILLS: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    GUEST_MONSTER_DATA2: Symbol[
        Optional[List[int]],
        Optional[int],
    ]

    EXTRA_DUNGEON_DATA: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


class ExtraOverlay11FunctionsProtocol(Protocol):
    pass


class ExtraOverlay11DataProtocol(Protocol):
    MONSTER_GROUND_IDLE_ANIM: Symbol[
        Optional[List[int]],
        Optional[int],
    ]


class ExtraOverlay36FunctionsProtocol(Protocol):
    pass


class ExtraOverlay36DataProtocol(Protocol):
    pass


class ExtraAllSymbolsProtocol(Protocol):
    arm9: SectionProtocol[ExtraArm9FunctionsProtocol, ExtraArm9DataProtocol, int]
    overlay11: SectionProtocol[
        ExtraOverlay11FunctionsProtocol, ExtraOverlay11DataProtocol, int
    ]
    overlay36: Optional[
        SectionProtocol[
            ExtraOverlay36FunctionsProtocol, ExtraOverlay36DataProtocol, int
        ]
    ]


# ------------------------------
# ------------- EU -------------
# ------------------------------


class ExtraEuArm9Functions:
    # TODO: Is this really the same as DebugPrint0 for EU???
    DebugPrint2 = Symbol(
        [0x200C284 - EuArm9Section.loadaddress], [0x200C284], None, DEBUG_PRINT2_DESC
    )


class ExtraEuArm9Data:
    COMPRESSED_IQ_GROUP_SKILLS = Symbol(
        [0x20A2314 - EuArm9Section.loadaddress],
        [0x20A2314],
        0x90,
        COMPRESSED_IQ_GROUP_SKILLS_DESC,
    )
    GUEST_MONSTER_DATA2 = Symbol(
        [0x204F148 - EuArm9Section.loadaddress],
        [0x204F148],
        0x1D0,
        GUEST_MONSTER_DATA2_DESC,
    )
    EXTRA_DUNGEON_DATA = Symbol(
        [0x204EFE0 - EuArm9Section.loadaddress],
        [0x204EFE0],
        0x168,
        EXTRA_DUNGEON_DATA_DESC,
    )


class ExtraEuArm9Section:
    name = EuArm9Section.name
    description = EuArm9Section.description
    loadaddress = EuArm9Section.loadaddress
    length = EuArm9Section.length
    functions = ExtraEuArm9Functions
    data = ExtraEuArm9Data


class ExtraEuOverlay11Functions:
    pass


class ExtraEuOverlay11Data:
    MONSTER_GROUND_IDLE_ANIM = Symbol(
        [0x22F66F4 - EuOverlay11Section.loadaddress],
        [0x22F66F4],
        0x800,
        MONSTER_GROUND_IDLE_ANIM_DESC,
    )


class ExtraEuOverlay11Section:
    name = EuOverlay11Section.name
    description = EuOverlay11Section.description
    loadaddress = EuOverlay11Section.loadaddress
    length = EuOverlay11Section.length
    functions = ExtraEuOverlay11Functions
    data = ExtraEuOverlay11Data


class ExtraEuOverlay36Functions(Protocol):
    pass


class ExtraEuOverlay36Data(Protocol):
    pass


class ExtraEuOverlay36Section:
    name = "overlay36"
    description = OV36_DESC
    loadaddress = 0x23A7080
    length = 0x38F80
    functions = ExtraEuOverlay36Functions
    data = ExtraEuOverlay36Data


class ExtraEuSections:
    arm9 = ExtraEuArm9Section
    overlay11 = ExtraEuOverlay11Section
    overlay36 = ExtraEuOverlay36Section


# ------------------------------
# ------------- NA -------------
# ------------------------------


class ExtraNaArm9Functions:
    DebugPrint2 = Symbol(
        [0x200C30C - NaArm9Section.loadaddress], [0x200C30C], None, DEBUG_PRINT2_DESC
    )


class ExtraNaArm9Data:
    COMPRESSED_IQ_GROUP_SKILLS = Symbol(
        [0x20A1D90 - NaArm9Section.loadaddress],
        [0x20A1D90],
        0x90,
        COMPRESSED_IQ_GROUP_SKILLS_DESC,
    )
    GUEST_MONSTER_DATA2 = Symbol(
        [0x204EE10 - NaArm9Section.loadaddress],
        [0x204EE10],
        0x1D0,
        GUEST_MONSTER_DATA2_DESC,
    )
    EXTRA_DUNGEON_DATA = Symbol(
        [0x204ECA8 - NaArm9Section.loadaddress],
        [0x204ECA8],
        0x168,
        EXTRA_DUNGEON_DATA_DESC,
    )


class ExtraNaArm9Section:
    name = NaArm9Section.name
    description = NaArm9Section.description
    loadaddress = NaArm9Section.loadaddress
    length = NaArm9Section.length
    functions = ExtraNaArm9Functions
    data = ExtraNaArm9Data


class ExtraNaOverlay11Functions:
    pass


class ExtraNaOverlay11Data:
    MONSTER_GROUND_IDLE_ANIM = Symbol(
        [0x22F5D54 - NaOverlay11Section.loadaddress],
        [0x22F5D54],
        0x800,
        MONSTER_GROUND_IDLE_ANIM_DESC,
    )


class ExtraNaOverlay11Section:
    name = NaOverlay11Section.name
    description = NaOverlay11Section.description
    loadaddress = NaOverlay11Section.loadaddress
    length = NaOverlay11Section.length
    functions = ExtraNaOverlay11Functions
    data = ExtraNaOverlay11Data


class ExtraNaOverlay36Functions(Protocol):
    pass


class ExtraNaOverlay36Data(Protocol):
    pass


class ExtraNaOverlay36Section:
    name = "overlay36"
    description = OV36_DESC
    loadaddress = 0x23A7080
    length = 0x38F80
    functions = ExtraNaOverlay36Functions
    data = ExtraNaOverlay36Data


class ExtraNaSections:
    arm9 = ExtraNaArm9Section
    overlay11 = ExtraNaOverlay11Section
    overlay36 = ExtraNaOverlay36Section


# ------------------------------
# ------------- JP -------------
# ------------------------------


class ExtraJpArm9Functions:
    DebugPrint2 = Symbol(None, None, None, DEBUG_PRINT2_DESC)


class ExtraJpArm9Data:
    COMPRESSED_IQ_GROUP_SKILLS = Symbol(
        [0x20A3164 - JpArm9Section.loadaddress],
        [0x20A3164],
        0x90,
        COMPRESSED_IQ_GROUP_SKILLS_DESC,
    )
    GUEST_MONSTER_DATA2 = Symbol(
        [0x204F168 - JpArm9Section.loadaddress],
        [0x204F168],
        0x1D0,
        GUEST_MONSTER_DATA2_DESC,
    )
    EXTRA_DUNGEON_DATA = Symbol(
        [0x204F000 - JpArm9Section.loadaddress],
        [0x204F000],
        0x168,
        EXTRA_DUNGEON_DATA_DESC,
    )


class ExtraJpArm9Section:
    name = JpArm9Section.name
    description = JpArm9Section.description
    loadaddress = JpArm9Section.loadaddress
    length = JpArm9Section.length
    functions = ExtraJpArm9Functions
    data = ExtraJpArm9Data


class ExtraJpOverlay11Functions:
    pass


class ExtraJpOverlay11Data:
    MONSTER_GROUND_IDLE_ANIM = Symbol(
        [0x22F73D8 - JpOverlay11Section.loadaddress],
        [0x22F73D8],
        0x800,
        MONSTER_GROUND_IDLE_ANIM_DESC,
    )


class ExtraJpOverlay11Section:
    name = JpOverlay11Section.name
    description = JpOverlay11Section.description
    loadaddress = JpOverlay11Section.loadaddress
    length = JpOverlay11Section.length
    functions = ExtraJpOverlay11Functions
    data = ExtraJpOverlay11Data


class ExtraJpSections:
    arm9 = ExtraJpArm9Section
    overlay11 = ExtraJpOverlay11Section
    overlay36 = None
