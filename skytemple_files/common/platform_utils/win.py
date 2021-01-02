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

if not sys.platform.lower().startswith('win'):
    raise OSError("This module is only available under Windows.")


import winreg

WIN_THEME_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
WIN_THEME_REG_KEY = 'AppsUseLightTheme'


def win_use_light_theme():
    """Function to check if the current Windows theme is the light theme or the dark theme"""
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, WIN_THEME_REG_PATH, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, WIN_THEME_REG_KEY)
        winreg.CloseKey(registry_key)
        return value != 0
    except WindowsError:
        return None


def win_set_error_mode():
    """
    This tells Windows not to show error dialogs for 'No Disk'.
    See: https://github.com/SkyTemple/skytemple/issues/12
    """
    import msvcrt
    old_mode = msvcrt.SetErrorMode(0)
    msvcrt.SetErrorMode(old_mode & msvcrt.SEM_FAILCRITICALERRORS)
