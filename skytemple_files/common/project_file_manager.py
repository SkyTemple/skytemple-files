"""A project file manager for storing non-ROM related files for SkyTemple projects."""
#  Copyright 2020 Parakoopa
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
import os
from typing import Optional, Tuple

from explorerscript import EXPLORERSCRIPT_EXT
from explorerscript.source_map import SourceMap
from skytemple_files.common.script_util import SSB_EXT

DIRECTORY_NAME_SUFFIX = '.skytemple'
SCRIPT_DIR = 'SCRIPT'
EXPLORERSCRIPT_SOURCE_MAP_SUFFIX = '.sm'


class ProjectFileManager:
    """A project file manager for storing non-ROM related files for SkyTemple projects."""
    def __init__(self, rom_file_name: str):
        self.directory_name = rom_file_name + DIRECTORY_NAME_SUFFIX
        os.makedirs(self.directory_name, exist_ok=True)

    def dir(self, subdir=None):
        if subdir:
            subdir_path = os.path.join(self.directory_name, subdir)
            os.makedirs(subdir_path, exist_ok=True)
            return subdir_path
        return self.directory_name

    # ExplorerScript source code file managing:
    # The filename for all of the methods can either be the direct file name
    # (relative to project dir, must start with SCRIPT)
    # or the name of the ssb file in ROM, see _explorerscript_resolve_filename

    def explorerscript_exists(self, filename):
        filename = self._explorerscript_resolve_filename(filename, EXPLORERSCRIPT_EXT)
        return os.path.exists(filename)

    def explorerscript_hash_up_to_date(self, filename, hash_compare):
        filename = self._explorerscript_resolve_filename(filename, '.ssb.sha256')
        if not os.path.exists(filename):
            return False
        with open(filename, 'r') as f:
            hash_file = f.read()
        return hash_file == hash_compare

    def explorerscript_load(self, filename) -> Tuple[str, SourceMap]:
        """Load the ExplorerScript file and it's source map if it exists, otherwise an empty map"""
        filename = self._explorerscript_resolve_filename(filename, EXPLORERSCRIPT_EXT)
        with open(filename, 'r') as f:
            source_code = f.read()
        if os.path.exists(filename + EXPLORERSCRIPT_SOURCE_MAP_SUFFIX):
            with open(filename + EXPLORERSCRIPT_SOURCE_MAP_SUFFIX, 'r') as f:
                source_map_code = f.read()
            source_map = SourceMap.deserialize(source_map_code)
        else:
            source_map = SourceMap({}, [])
        return source_code, source_map

    def explorerscript_save(self, filename, code, source_map: Optional[SourceMap] = None):
        """Save the ExplorerScript file and it's source map if given"""
        filename = self._explorerscript_resolve_filename(filename, EXPLORERSCRIPT_EXT)
        with open(filename, 'w') as f:
            f.write(code)
        if source_map:
            with open(filename + EXPLORERSCRIPT_SOURCE_MAP_SUFFIX, 'w') as f:
                f.write(source_map.serialize())

    def explorerscript_save_hash(self, filename, new_hash):
        filename = self._explorerscript_resolve_filename(filename, '.ssb.sha256')
        with open(filename, 'w') as f:
            f.write(new_hash)

    def _explorerscript_resolve_filename(self, filename: str, desired_extension: str) -> str:
        """
        First makes sure, that the filename starts with SCRIPT.
        Then checks, if the file extension is ssb. If so, removes the ssb suffix and attaches
        the desired extension.
        Also makes sure, that the directories on the way exist.
        Returns the resulting full path, including the project dir.
        """
        if not filename.startswith(SCRIPT_DIR):
            raise ValueError(f"The filename for the ExplorerScript related file must be "
                             f"stored relative to the {SCRIPT_DIR} directory.")
        if filename[-4:] == SSB_EXT:
            filename = filename[:-4] + desired_extension
        filename = os.path.join(self.directory_name, filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        return filename
