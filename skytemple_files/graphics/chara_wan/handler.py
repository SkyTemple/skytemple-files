#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.import math
import os
from typing import List

from PIL import Image

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.chara_wan.model import WanFile
from skytemple_files.graphics.chara_wan.sheets import ExportSheets, ImportSheets
from skytemple_files.graphics.chara_wan.split_merge import MergeWan, SplitWan

ANIM_NAME_MAP = "???????????????????"
ANIM_PRESENCE = []
# monster
ANIM_PRESENCE.append([True, False, False, False, False, True, True, True, False, False, False, True])
# ground
ANIM_PRESENCE.append([True, False, False, False, False, False, True, True, False, False, False, False, True])
# attack
ANIM_PRESENCE.append([False, True, True, True, True, False, False, False, True, True, True, True, True])


class CharaWanHandler(DataHandler[WanFile]):
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> 'WanFile':
        from skytemple_files.common.types.file_types import FileType
        return FileType.SIR0.unwrap_obj(FileType.SIR0.deserialize(data), WanFile)

    @classmethod
    def serialize(cls, data: 'WanFile', **kwargs) -> bytes:
        from skytemple_files.common.types.file_types import FileType
        return FileType.SIR0.serialize(FileType.SIR0.wrap_obj(data))

    @classmethod
    def export_sheets(cls, out_dir, wan):
        shadow_img = Image.open(os.path.join(os.path.dirname(__file__), 'Shadow.png'))
        return ExportSheets(out_dir, shadow_img, wan, ANIM_NAME_MAP)

    @classmethod
    def import_sheets(cls, in_dir, strict=False):
        return ImportSheets(in_dir, strict)

    @classmethod
    def merge_wan(cls, wan_monster: WanFile, wan_ground: WanFile, wan_attack: WanFile):
        return MergeWan([wan_monster, wan_ground, wan_attack])

    @classmethod
    def split_wan(cls, wan: WanFile) -> List[WanFile]:
        return SplitWan(wan, ANIM_PRESENCE)
