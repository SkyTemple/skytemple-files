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
import collections.abc
from typing import Sequence

from skytemple_files.common.protocol import TilemapEntryProtocol


def assert_tilemap_lists_equal(expected: Sequence[TilemapEntryProtocol], actual: Sequence[TilemapEntryProtocol]):
    assert isinstance(expected, collections.abc.Sequence)
    assert isinstance(actual, collections.abc.Sequence)
    assert len(expected) == len(actual)
    for e, a in zip(expected, actual):
        assert e.to_int() == a.to_int()
