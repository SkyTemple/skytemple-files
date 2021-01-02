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
import sys

if not sys.platform.lower().startswith('darwin'):
    raise OSError("This module is only available under macOS.")

from Foundation import NSUserDefaults


def macos_use_light_theme():
    """Function to check if the current macOS theme is the light theme or the dark theme"""
    return NSUserDefaults.standardUserDefaults().stringForKey_('AppleInterfaceStyle') != 'Dark'
