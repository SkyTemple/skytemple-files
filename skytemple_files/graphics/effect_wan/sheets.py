#  Copyright 2020-2024 Capypara and the SkyTemple Contributors
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
# mypy: ignore-errors

from __future__ import annotations

import glob
import math
import os
import xml.etree.ElementTree as ET

from PIL import Image

from skytemple_files.common.xml_util import prettify
from skytemple_files.graphics.effect_wan.model import (
    DEBUG_PRINT,
    DIM_TABLE,
    TEX_SIZE,
    ImageData,
    MetaFrame,
    SequenceFrame,
    WanFile,
)
from skytemple_files.user_error import UserValueError


def ExportSheets(outDir, wan):
    if not os.path.isdir(outDir):
        os.makedirs(outDir)

    for passNum in range(1, 4):
        ExportEffectStep(outDir, wan, passNum)

def ExportEffectStep(outDir, effectData, passNum):
    pass