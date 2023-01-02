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

import json
from typing import Dict, List

from ndspy.rom import NintendoDSRom

from skytemple_files.common.ppmdu_config.data import Pmd2Sprite
from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.common.util import OptionalKwargs, create_file_in_rom

SPRCONF_FILENAME = "MONSTER/sprconf.json"
SprconfType = Dict[int, Dict[int, List[str]]]


class SprconfHandler(DataHandler[SprconfType]):
    """Overrides for the sprite animation names configuration (pmd2spritedata.xml) in JSON."""

    @classmethod
    def deserialize(cls, data: bytes, **kwargs: OptionalKwargs) -> SprconfType:
        sprconf: SprconfType = {}
        for k, v in json.loads(str(data, "utf-8")).items():
            sprconf[int(k)] = {}
            for kk, vv in v.items():
                sprconf[int(k)][int(kk)] = vv
        return sprconf

    @classmethod
    def serialize(cls, data: SprconfType, **kwargs: OptionalKwargs) -> bytes:
        return bytes(json.dumps(data), "utf-8")

    @classmethod
    def load(cls, rom: NintendoDSRom, create=True) -> SprconfType:
        if rom.filenames.idOf(SPRCONF_FILENAME) is None:
            if create:
                create_file_in_rom(rom, SPRCONF_FILENAME, bytes("{}", "utf-8"))
                # don't return, fall down to below
            else:
                return dict()
        return cls.deserialize(rom.getFileByName(SPRCONF_FILENAME))

    @classmethod
    def update(cls, sprconf: SprconfType, sprite_data: Pmd2Sprite):
        sprconf[sprite_data.id] = {
            index.id: index.names for index in sprite_data.indices.values()
        }
