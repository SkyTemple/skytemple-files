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
import urllib.request
from enum import Enum


RELEASE_WEB = "https://release.skytemple.org/"


class ReleaseType(Enum):
    SKYTEMPLE = "skytemple"
    SKYTEMPLE_RANDOMIZER = "randomizer"


def check_newest_release(rtype: ReleaseType) -> str:
    """
    Returns the newest release using release.skytemple.org.
    May fail if no connection can be established!
    """
    return urllib.request.urlopen(RELEASE_WEB + rtype.value).read().decode('utf-8').trim().strip()
