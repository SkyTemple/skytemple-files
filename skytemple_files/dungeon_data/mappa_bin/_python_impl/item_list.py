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

import logging
from typing import Dict, TYPE_CHECKING

from skytemple_files.common.util import (
    AutoString,
    read_u16,
)
from skytemple_files.dungeon_data.mappa_bin.protocol import (
    MappaItemListProtocol,
    Probability,
    _MappaItemCategory,
    _MappaItem,
    MAX_ITEM_ID,
    CMD_SKIP,
    GUARANTEED,
    MAX_CAT_IDS,
)

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin._python_impl.model import (
        MappaBinReadContainer,
    )
logger = logging.getLogger(__name__)


class MappaItemList(MappaItemListProtocol, AutoString):
    def __init__(
        self,
        categories: Dict[_MappaItemCategory, Probability],
        items: Dict[_MappaItem, Probability],
    ):
        self.categories = categories
        self.items = items

    @classmethod
    def from_mappa(cls, read: "MappaBinReadContainer", pointer: int):
        return cls.from_bytes(read.data, pointer)

    @classmethod
    def from_bytes(cls, data: bytes, pointer: int) -> "MappaItemList":
        processing_categories = True
        item_or_cat_id = 0
        orig_pointer = pointer
        len_read = 0

        items = {}
        categories = {}

        while item_or_cat_id <= MAX_ITEM_ID:
            val = read_u16(data, pointer)
            len_read += 2
            skip = val > CMD_SKIP and val != GUARANTEED

            if skip:
                item_or_cat_id += val - CMD_SKIP
            else:
                if val == GUARANTEED:
                    weight = GUARANTEED
                else:
                    weight = val
                if processing_categories:
                    categories[item_or_cat_id] = weight
                else:
                    items[item_or_cat_id] = weight
                item_or_cat_id += 1
            if item_or_cat_id >= MAX_CAT_IDS and processing_categories:
                processing_categories = False
                item_or_cat_id -= MAX_CAT_IDS + 1
            pointer += 2

        assert (
            data[orig_pointer : orig_pointer + len_read]
            == MappaItemList(categories, items).to_mappa()
        )

        return MappaItemList(categories, items)

    def to_mappa(self) -> bytes:
        data = bytearray()
        current_id = 0
        # Start with the categories
        for cat, val in sorted(self.categories.items(), key=lambda it: it[0]):
            id_cat = cat
            if current_id != id_cat:
                current_id = self._write_skip(data, current_id, id_cat)
            self._write_probability(data, val)
            current_id += 1
        # Continue with the items
        sorted_items = sorted(self.items.items(), key=lambda it: it[0])
        first_item_id = sorted_items[0][0] if len(sorted_items) > 0 else 0
        self._write_skip(data, current_id, MAX_CAT_IDS + 1 + first_item_id)
        current_id = first_item_id
        for item, val in sorted_items:
            if current_id != item:
                current_id = self._write_skip(data, current_id, item)
            self._write_probability(data, val)
            current_id += 1
        # Fill up to MAX_ITEM_ID + 1
        self._write_skip(data, current_id, MAX_ITEM_ID + 1)
        return data

    def to_bytes(self) -> bytes:
        return self.to_mappa()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MappaItemList):
            return False
        return self.categories == other.categories and self.items == other.items

    def _write_skip(self, data: bytearray, current_id: int, target_id: int):
        if current_id != target_id:
            data += (target_id - current_id + CMD_SKIP).to_bytes(
                2, "little", signed=False
            )
        return target_id

    def _write_probability(self, data: bytearray, probability: Probability):
        data += probability.to_bytes(2, "little", signed=False)
