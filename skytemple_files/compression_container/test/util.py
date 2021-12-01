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
import os.path
from glob import glob
from typing import Generator, Tuple

from PIL import Image


def load_dataset() -> Generator[Tuple[str, bytes], None, None]:
    for file in _get_fixture_paths():
        img: Image.Image = Image.open(file)
        yield os.path.basename(file), img.tobytes()


def dataset_name_func(testcase_func, _, param):
    return f'{testcase_func.__name__}/{param.args[0]}'


def _get_fixture_paths() -> Generator[str, None, None]:
    for file in glob(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'fixtures', '*.png')):
        yield file
