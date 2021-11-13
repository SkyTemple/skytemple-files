"""
pytest configuration.
Collects all packages called "test" within skytemple_files to run tests from.
"""
#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
from os.path import isdir
TEST_DIR_NAME = 'test'


def pytest_ignore_collect(path):
    if isdir(path.strpath):
        return False
    parts = path.strpath.split(path.sep)
    return not (len(parts) > 1 and parts[-2] == TEST_DIR_NAME and parts[-1].endswith('_test.py'))
