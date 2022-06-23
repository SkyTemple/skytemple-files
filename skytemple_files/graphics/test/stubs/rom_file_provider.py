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

import os.path

from skytemple_files.common.protocol import RomFileProviderProtocol


class RomFileProviderStub(RomFileProviderProtocol):
    def getFileByName(self, filename: str) -> bytes:
        dirn = os.path.dirname(__file__)
        if filename == "MAP_BG/coco.bma":
            with open(
                os.path.join(dirn, "..", "fixtures", "MAP_BG", "coco.bma"), "rb"
            ) as f:
                return f.read()
        if filename == "MAP_BG/coco.bpc":
            with open(
                os.path.join(dirn, "..", "fixtures", "MAP_BG", "coco.bpc"), "rb"
            ) as f:
                return f.read()
        if filename == "MAP_BG/coco.bpl":
            with open(
                os.path.join(dirn, "..", "fixtures", "MAP_BG", "coco.bpl"), "rb"
            ) as f:
                return f.read()
        if filename == "MAP_BG/coco1.bpa":
            with open(
                os.path.join(dirn, "..", "fixtures", "MAP_BG", "coco1.bpa"), "rb"
            ) as f:
                return f.read()
        if filename == "MAP_BG/coco2.bpa":
            with open(
                os.path.join(dirn, "..", "fixtures", "MAP_BG", "coco2.bpa"), "rb"
            ) as f:
                return f.read()
        raise NotImplementedError(f"Invalid filename for stub: {filename}")
