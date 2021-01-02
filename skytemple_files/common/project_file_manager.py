"""A project file manager for storing non-ROM related files for SkyTemple projects."""
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
import json
import os
from typing import Optional, Tuple, List

from appdirs import user_config_dir

from explorerscript import EXPLORERSCRIPT_EXT
from explorerscript.source_map import SourceMap
from skytemple_files.common.util import open_utf8

DIRECTORY_NAME_SUFFIX = '.skytemple'
SCRIPT_DIR = 'SCRIPT'
EXPLORERSCRIPT_SOURCE_MAP_SUFFIX = '.sm'
EXPLORERSCRIPT_INCLUSION_MAP_SUFFIX = '.im'


class ProjectFileManager:
    """A project file manager for storing non-ROM related files for SkyTemple projects."""
    def __init__(self, rom_file_name: str):
        self.directory_name = rom_file_name + DIRECTORY_NAME_SUFFIX
        os.makedirs(self.directory_name, exist_ok=True)

    @classmethod
    def shared_config_dir(cls):
        """Returns the shared configuration directory for all SkyTemple projects."""
        return user_config_dir('skytemple', False)

    def dir(self, subdir=None):
        if subdir:
            subdir_path = os.path.join(self.directory_name, subdir)
            os.makedirs(subdir_path, exist_ok=True)
            return subdir_path
        return self.directory_name

    # ExplorerScript source code file managing:
    # The filename for all of the methods can either be the direct file name
    # (relative to project dir, must start with SCRIPT)
    # or the name of the ssb file in ROM, see _explorerscript_resolve_filename/explorerscript_get_path_for_ssb.

    def explorerscript_exists(self, filename):
        filename = self._explorerscript_resolve_filename(filename, EXPLORERSCRIPT_EXT)
        return os.path.exists(filename)

    def explorerscript_hash_up_to_date(self, filename, hash_compare):
        filename = self._explorerscript_resolve_filename(filename, '.ssb.sha256')
        if not os.path.exists(filename):
            return False
        with open_utf8(filename, 'r') as f:
            hash_file = f.read()
        return hash_file == hash_compare

    def explorerscript_load(self, filename, sourcemap=True) -> Tuple[str, SourceMap]:
        """Load the ExplorerScript file and it's source map if it exists, otherwise an empty map"""
        filename = self._explorerscript_resolve_filename(filename, EXPLORERSCRIPT_EXT)
        with open_utf8(filename, 'r') as f:
            source_code = f.read()
        sourcemap = self.explorerscript_load_sourcemap(filename) if sourcemap else SourceMap.create_empty()
        return source_code, sourcemap

    def explorerscript_load_sourcemap(self, filename) -> SourceMap:
        filename = self._explorerscript_resolve_filename(filename, EXPLORERSCRIPT_EXT + EXPLORERSCRIPT_SOURCE_MAP_SUFFIX)
        if os.path.exists(filename):
            with open_utf8(filename, 'r') as f:
                source_map_code = f.read()
            source_map = SourceMap.deserialize(source_map_code)
        else:
            source_map = SourceMap.create_empty()
        return source_map

    def explorerscript_save(self, filename, code, source_map: Optional[SourceMap] = None):
        """Save the ExplorerScript file and it's source map if given"""
        filename = self._explorerscript_resolve_filename(filename, EXPLORERSCRIPT_EXT)
        with open_utf8(filename, 'w') as f:
            f.write(code)
        if source_map:
            with open_utf8(filename + EXPLORERSCRIPT_SOURCE_MAP_SUFFIX, 'w') as f:
                f.write(source_map.serialize())

    def explorerscript_save_hash(self, filename, new_hash):
        filename = self._explorerscript_resolve_filename(filename, '.ssb.sha256')
        with open_utf8(filename, 'w') as f:
            f.write(new_hash)

    def explorerscript_include_usage_remove(self, filename, ssb_filename_that_is_included):
        """Removes an entry from the inclusion map for filename (can be SSB filename or inclusion map filename)."""
        filename = self._explorerscript_resolve_filename(filename, EXPLORERSCRIPT_EXT + EXPLORERSCRIPT_INCLUSION_MAP_SUFFIX)
        entries: List[str] = self._explorerscript_get_inclusion_map(filename)
        if ssb_filename_that_is_included in entries:
            entries.remove(ssb_filename_that_is_included)
        self._explorerscript_save_inclusion_map(filename, entries)

    def explorerscript_include_usage_add(self, filename, ssb_filename_that_is_included):
        """Adds an entry to the inclusion map for filename (can be SSB filename or inclusion map filename)."""
        filename = self._explorerscript_resolve_filename(filename, EXPLORERSCRIPT_EXT + EXPLORERSCRIPT_INCLUSION_MAP_SUFFIX)
        entries: List[str] = self._explorerscript_get_inclusion_map(filename)
        if ssb_filename_that_is_included not in entries:
            entries.append(ssb_filename_that_is_included)
        self._explorerscript_save_inclusion_map(filename, entries)

    def explorerscript_get_path_for_ssb(self, ssb_filename):
        """
        Returns a relative path (relative to project dir) to an exps file for a given ssb file.
        """
        return self._explorerscript_resolve_filename__relative(ssb_filename, EXPLORERSCRIPT_EXT)

    def _explorerscript_resolve_filename__relative(self, filename: str, desired_extension: str) -> str:
        """
        Removes the file extension and adds the desired extension.
        Returns the path relative to the project dir.
        """
        return '.'.join(filename.split('.')[:-1]).replace('/', os.path.sep) + desired_extension

    def _explorerscript_resolve_filename(self, filename: str, desired_extension: str) -> str:
        """
        Like the __relative version, but returns the full path and makes sure, that the directory exists.
        """
        filename = os.path.join(self.directory_name, self._explorerscript_resolve_filename__relative(
            filename, desired_extension
        ))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        return filename

    def _explorerscript_get_inclusion_map(self, filename):
        if not os.path.exists(filename):
            return []
        with open_utf8(filename, 'r') as f:
            return json.load(f)

    def _explorerscript_save_inclusion_map(self, filename, entries):
        with open_utf8(filename, 'w') as f:
            json.dump(entries, f, indent=0)
