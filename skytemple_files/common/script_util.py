"""Utility functions for dealing with the script engine"""
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
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
import re
from collections import OrderedDict
from typing import List, Union, Tuple, Dict

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

from ndspy.fnt import Folder

from skytemple_files.common.types.file_types import FileType

SCRIPT_DIR = 'SCRIPT'
COMMON_DIR = 'COMMON'
SSE_EXT = '.sse'
SSB_EXT = '.ssb'
SSA_EXT = '.ssa'
SSS_EXT = '.sss'
LSD_EXT = '.lsd'
ENTER_SSE = 'enter' + SSE_EXT
UNIONALL_SSB = 'unionall' + SSB_EXT
ENTER_SSB_PATTERN = re.compile("^enter\\d{1,2}\\.ssb$")


class MapEntry(TypedDict):
    name: str
    enter_sse: Union[str, None]
    enter_ssbs: List[str]
    # Dict of sss files and their ssb files:
    subscripts: Dict[str, List[str]]
    # LSD file name
    lsd: Union[str, None]
    # SSA and SSB file tuples (not loaded from LSD but read from dir directly!)
    ssas: List[Tuple[str, str]]


class ScriptFiles(TypedDict):
    common: List[str]
    maps: Dict[str, MapEntry]


def load_script_files(script_folder: Folder) -> ScriptFiles:
    """Returns information about the files used by the script engine in an 'introspectable' way."""
    script_files = ScriptFiles(common=[], maps=OrderedDict())
    for map_or_common_name, folder in script_folder.folders:
        if map_or_common_name == COMMON_DIR:
            # Common script directory
            for filename in folder.files:
                script_files['common'].append(filename)
        else:
            # Map directory
            map = MapEntry(name=map_or_common_name, enter_sse=None, enter_ssbs=[], subscripts=OrderedDict(), lsd=None, ssas=[])
            ssa_stems = []
            ssbs = []
            script_files['maps'][map_or_common_name] = map
            for filename in folder.files:
                if filename == ENTER_SSE:
                    # Enter SSE
                    map['enter_sse'] = filename
                elif ENTER_SSB_PATTERN.match(filename):
                    # Enter SSB
                    map['enter_ssbs'].append(filename)
                elif filename == map_or_common_name.lower() + LSD_EXT:
                    # LSD file
                    map['lsd'] = filename
                elif filename.endswith(SSS_EXT):
                    # Subscript SSS
                    map['subscripts'][filename] = []
                elif filename.endswith(SSA_EXT):
                    # Acting SSA file
                    ssa_stems.append(filename[:-(len(SSA_EXT))])
                elif filename.endswith(SSB_EXT):
                    # Acting or Subscript SSB:
                    ssbs.append(filename)
            # Process ssbs
            for ssb in ssbs:
                ssb_stem = ssb[:-(len(SSB_EXT))]
                if ssb_stem in ssa_stems:
                    # SSB is for SSA file:
                    map['ssas'].append((ssb_stem + SSA_EXT, ssb))
                for subscript_name, list_of_ssbs_for_subscript in map['subscripts'].items():
                    # SSB is for subscript
                    if ssb_stem.startswith(subscript_name[:-len(SSS_EXT)]):
                        list_of_ssbs_for_subscript.append(ssb)
                        break

    return script_files
