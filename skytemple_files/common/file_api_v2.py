"""
API to read/write files from ROMS and file storage.

Using this API files and hardcoded in a game ROM can be manipulated
while also storing machine and human-readable versions of those files
out-of-ROM (so-called "assets"; eg. as YAML or PNG).
Requesting to read a file from the ROM will first try to load it from assets,
and fall back to the ROM if no assets have been saved yet for that file.
Writing a model back to ROM will also write the model to the asset files.

The API implements mechanisms for dealing with conflicts between the state of
assets and actual files in ROM.

This API also supports handling patches and exposes the static ROM data (Pmd2Data).
"""
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
