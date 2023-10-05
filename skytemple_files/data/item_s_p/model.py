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

from enum import Enum, auto
from collections.abc import Sequence

from range_typed_integers import u16, u32

from skytemple_files.common.i18n_util import _
from skytemple_files.common.util import (
    AutoString,
    read_u16,
    write_u16,
)
from skytemple_files.container.sir0.sir0_serializable import Sir0Serializable
from skytemple_files.container.sir0.sir0_util import decode_sir0_pointer_offsets
from skytemple_files.data.item_s_p import ITEM_S_P_ENTRY_SIZE


class ItemSPExclusiveType(Enum):
    NONE = auto(), _("None")
    MONSTER = auto(), _("Pokémon")
    TYPE = auto(), _("Type")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, name_localized: str):
        self.name_localized = name_localized

    def __str__(self):
        return f"ItemSPExclusiveType.{self.name}"

    def __repr__(self):
        return str(self)


class ItemSPType(Enum):
    NONE = 0x00, "-", None, ItemSPExclusiveType.NONE, None
    TYPE_ONE_SLOT_ONE = 0x01, "*", 1, ItemSPExclusiveType.TYPE, None
    TYPE_ONE_SLOT_TWO = 0x02, "*", 2, ItemSPExclusiveType.TYPE, None
    TYPE_TWO = 0x03, "**", None, ItemSPExclusiveType.TYPE, None
    TYPE_THREE = 0x04, "***", None, ItemSPExclusiveType.TYPE, None
    POKE_ONE_SLOT_ONE = 0x05, "*", 1, ItemSPExclusiveType.MONSTER, None
    POKE_ONE_SLOT_TWO = 0x06, "*", 2, ItemSPExclusiveType.MONSTER, None
    POKE_TWO = 0x07, "**", None, ItemSPExclusiveType.MONSTER, None
    POKE_THREE = 0x08, "***", None, ItemSPExclusiveType.MONSTER, None
    POKE_HATCH = (
        0x09,
        "***",
        None,
        ItemSPExclusiveType.MONSTER,
        _("The Pokemon may hatch holding the item."),
    )
    POKE_SPECIAL = (
        0x0A,
        "***",
        None,
        ItemSPExclusiveType.MONSTER,
        _(
            "? (Only all the Eeveelutions, and the Tyrogue line have items with this type!)"
        ),
    )

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
        self,
        _: int,
        rarity: str,
        slot: int | None,
        exclusive_to: ItemSPExclusiveType,
        extra_trait_desc: str | None,
    ):
        self.rarity = rarity
        self.slot = slot
        self.exclusive_to = exclusive_to
        self.extra_trait_desc = extra_trait_desc

    @property
    def print_name(self):
        return (
            f'{self.exclusive_to.name_localized} - {self.rarity} ({_("Slot")} {"n/a" if self.slot is None else self.slot})'
            f'{(" - " + self.extra_trait_desc) if self.extra_trait_desc is not None else ""}'
        )

    def __str__(self):
        return f"ItemSPType.{self.name}"

    def __repr__(self):
        return str(self)


class ItemSPEntry(AutoString):
    type: ItemSPType
    parameter: u16

    def __init__(self, data: bytes):
        self.type = ItemSPType(read_u16(data, 0))  # type: ignore
        self.parameter = read_u16(data, 2)

    def to_bytes(self) -> bytes:
        data = bytearray(ITEM_S_P_ENTRY_SIZE)
        write_u16(data, u16(self.type.value), 0)
        write_u16(data, self.parameter, 2)
        return bytes(data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ItemSPEntry):
            return False
        return self.type == other.type and self.parameter == other.parameter


class ItemSP(Sir0Serializable, AutoString):
    def __init__(self, data: bytes, header_pointer: int):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.item_list = []
        for x in range(0, len(data), ITEM_S_P_ENTRY_SIZE):
            self.item_list.append(ItemSPEntry(data[x : x + ITEM_S_P_ENTRY_SIZE]))

    @classmethod
    def sir0_unwrap(
        cls,
        content_data: bytes,
        data_pointer: u32,
    ) -> Sir0Serializable:
        return cls(content_data, data_pointer)

    def sir0_serialize_parts(self) -> tuple[bytes, list[u32], u32 | None]:
        from skytemple_files.data.item_s_p.writer import ItemSPWriter

        return ItemSPWriter(self).write()  # type: ignore

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ItemSP):
            return False
        return self.item_list == other.item_list

    @staticmethod
    def _decode_ints(data: bytes, pnt_start: u32) -> Sequence[u32]:
        return decode_sir0_pointer_offsets(data, pnt_start, False)
