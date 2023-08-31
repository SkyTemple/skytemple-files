"""Module for editing the hardcoded table mapping of ground levels to dungeon tilesets."""
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

from typing import cast, List, Optional, Tuple

from range_typed_integers import i16, u8, u32

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.ppmdu_config.script_data import (
    Pmd2ScriptLevel,
    Pmd2ScriptLevelMapType,
)
from skytemple_files.common.util import AutoString, read_u8, read_i16, read_u32
from skytemple_files.container.dungeon_bin.model import DungeonBinPack
from skytemple_files.dungeon_data.fixed_bin.model import FixedBin, FixedFloor
from skytemple_files.dungeon_data.mappa_bin.protocol import MappaBinProtocol
from skytemple_files.graphics.dma.protocol import DmaProtocol
from skytemple_files.graphics.dpc.protocol import DpcProtocol
from skytemple_files.graphics.dpci.protocol import DpciProtocol
from skytemple_files.graphics.dpl.protocol import DplProtocol
from skytemple_files.graphics.dpla.protocol import DplaProtocol
from skytemple_files.hardcoded.dungeons import DungeonDefinition


class GroundTilesetMapping(AutoString):
    ground_level: i16
    dungeon_tileset: u8
    floor_id: u8
    unk3: u32

    def __init__(self, ground_level: i16, dungeon_tileset: u8, floor_id: u8, unk3: u32):
        self.ground_level = ground_level
        self.dungeon_id = dungeon_tileset
        self.floor_id = floor_id
        self.unk3 = unk3

    # Compat
    @property
    def unk2(self) -> u8:
        return self.floor_id

    @unk2.setter
    def unk2(self, value: u8) -> None:
        self.floor_id = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GroundTilesetMapping):
            return False
        return (
            self.ground_level == other.ground_level
            and self.dungeon_id == other.dungeon_id
            and self.unk2 == other.unk2
            and self.unk3 == other.unk3
        )

    def to_bytes(self) -> bytes:
        return (
            self.ground_level.to_bytes(2, "little", signed=True)
            + self.dungeon_id.to_bytes(1, "little", signed=False)
            + self.unk2.to_bytes(1, "little", signed=False)
            + self.unk3.to_bytes(4, "little", signed=False)
        )


class HardcodedGroundDungeonTilesets:
    @staticmethod
    def get_ground_dungeon_tilesets(
        overlay11bin: bytes, config: Pmd2Data
    ) -> List[GroundTilesetMapping]:
        """Returns the list."""
        block = config.bin_sections.overlay11.data.LEVEL_TILEMAP_LIST
        lst = []
        for i in range(block.address, block.address + block.length, 8):
            lst.append(
                GroundTilesetMapping(
                    read_i16(overlay11bin, i),
                    read_u8(overlay11bin, i + 2),
                    read_u8(overlay11bin, i + 3),
                    read_u32(overlay11bin, i + 4),
                )
            )
        return lst

    @staticmethod
    def set_ground_dungeon_tilesets(
        value: List[GroundTilesetMapping], overlay11bin: bytearray, config: Pmd2Data
    ) -> None:
        """
        Sets the  list.
        The length of the list must exactly match the original ROM's length (see get_dungeon_list).
        """
        block = config.bin_sections.overlay11.data.LEVEL_TILEMAP_LIST
        assert block.length is not None
        expected_length = int(block.length / 8)
        if len(value) != expected_length:
            raise ValueError(
                f"The list must have exactly the length of {expected_length} entries."
            )
        for i, entry in enumerate(value):
            overlay11bin[
                block.address + i * 8 : block.address + (i + 1) * 8
            ] = entry.to_bytes()


def resolve_mapping_for_level(
    level: Pmd2ScriptLevel,
    tileset_mappings: List[GroundTilesetMapping],
    mappa: MappaBinProtocol,
    fixed: FixedBin,
    dungeon_bin: DungeonBinPack,
    dungeons: List[DungeonDefinition],
) -> Optional[
    Tuple[
        DmaProtocol,
        DpcProtocol,
        DpciProtocol,
        DplProtocol,
        DplaProtocol,
        Optional[FixedFloor],
    ]
]:
    """Returns tileset data and fixed floor data (if applicable) for the given level"""
    if (
        level.mapty_enum != Pmd2ScriptLevelMapType.FIXED_ROOM
        and level.mapty_enum != Pmd2ScriptLevelMapType.TILESET
    ):
        return None
    dungeon_id, floor_id = None, None
    for mapping in tileset_mappings:
        if mapping.ground_level == level.id:
            dungeon_id, floor_id = mapping.dungeon_id, mapping.floor_id
            break
    if not dungeon_id:
        return None
    assert dungeon_id is not None
    assert floor_id is not None
    mappa_idx = dungeons[dungeon_id].mappa_index
    start_offset = dungeons[dungeon_id].start_after
    length = dungeons[dungeon_id].number_floors
    floor_id = cast(u8, min(length - 1, floor_id - 1))  # type: ignore
    layout = mappa.floor_lists[mappa_idx][start_offset + floor_id].layout
    tileset_id = layout.tileset_id
    if tileset_id > 169:
        tileset_id = u8(0)
    dma: DmaProtocol = dungeon_bin.get(f"dungeon{tileset_id}.dma")
    dpl: DplProtocol = dungeon_bin.get(f"dungeon{tileset_id}.dpl")
    dpla: DplaProtocol = dungeon_bin.get(f"dungeon{tileset_id}.dpla")
    dpci: DpciProtocol = dungeon_bin.get(f"dungeon{tileset_id}.dpci")
    dpc: DpcProtocol = dungeon_bin.get(f"dungeon{tileset_id}.dpc")

    fixedf = None
    if level.mapty_enum == Pmd2ScriptLevelMapType.FIXED_ROOM:
        fixedf = fixed.fixed_floors[layout.fixed_floor_id]

    return dma, dpc, dpci, dpl, dpla, fixedf
