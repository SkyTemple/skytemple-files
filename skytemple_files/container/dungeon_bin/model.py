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
import logging
from typing import Dict, Optional

from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2DungeonBinFiles, Pmd2BinPackFile
from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.container.bin_pack.model import BinPack
logger = logging.getLogger(__name__)


class DungeonBinPack(BinPack):
    def __init__(self, data: bytes, files_def: Pmd2DungeonBinFiles):
        super().__init__(data)
        self.files_def = files_def
        self._loaded_models: Dict[int, any] = {}

    def get(self, filename):
        """Returns a file by name."""
        for i in range(0, len(self)):
            if filename == self.get_filename(i):
                return self[i]
        raise KeyError(f"File {filename} not found.")

    def set(self, filename, data):
        """Sets a file by name."""
        for i in range(0, len(self)):
            if filename == self.get_filename(i):
                self[i] = data
                return
        raise KeyError(f"File {filename} not found.")

    def get_filename(self, index):
        """Returns the filename for a file at a given index."""
        fdef = self.files_def.get(index)
        return fdef.name.replace('%d', str(index)).replace('%i', str(index - fdef.idxfirst))

    def get_files_with_ext(self, ext):
        files = []
        for idx in range(0, len(self)):
            fn = self.get_filename(idx)
            if fn.endswith('.' + ext):
                files.append(fn)
        return files

    def serialize_subfiles(self):
        """Serializes all loaded modules and updates self._files again."""
        for idx, model in self._loaded_models.items():
            handler = self._get_handler(self.files_def.get(idx).type)
            if handler is None:
                self._files[idx] = model
            else:
                self._files[idx] = handler.serialize(model)

    def __getitem__(self, index):
        return self._get_model(index)

    def __setitem__(self, index, value):
        self._set_model(index, value)

    def __delitem__(self, key):
        raise NotImplementedError("The dungeon.bin model does not support removing files.")

    def __iter__(self):
        for i in range(0, len(self)):
            yield self._get_model(i)

    def _get_model(self, index):
        if index not in self._loaded_models:
            self._loaded_models[index] = self._load_model(self._files[index], self.files_def.get(index))
        return self._loaded_models[index]

    def _set_model(self, index, value):
        self._loaded_models[index] = value

    def _load_model(self, file_bytes: bytes, file_def: Pmd2BinPackFile):
        handler = self._get_handler(file_def.type)
        if handler is None:
            # We don't have a handler... just return the bytes instead.
            logger.warning(f"No file handler for {file_def.type} found, falling back to bytes.")
            return file_bytes
        try:
            return handler.deserialize(file_bytes)
        except NotImplementedError:
            logger.warning(f"File handler for {file_def.type} not implemented, falling back to bytes.")
            return file_bytes

    def _get_handler(self, type_name: str) -> Optional[DataHandler]:
        from skytemple_files.common.types.file_types import FileType
        if hasattr(FileType, type_name):
            return getattr(FileType, type_name)
        return None
