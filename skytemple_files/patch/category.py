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
from enum import Enum, auto
from skytemple_files.common.i18n_util import _


class PatchCategory(Enum):
    IMPROVEMENT_TWEAK = auto(), _("Improvements and Tweaks")  # TRANSLATORS: Name for the category of ASM patch
    NEW_MECHANIC = auto(), _("New Mechanics")  # TRANSLATORS: Name for the category of ASM patch
    BUGFIXES = auto(), _("Bugfixes")  # TRANSLATORS: Name for the category of ASM patch
    UTILITY = auto(), _("Utility")  # TRANSLATORS: Name for the category of ASM patch
    OTHER = auto(), _("Others")

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: str, name_localized: str
    ):
        self.name_localized = name_localized

    def __str__(self):
        return f'PatchCategory.{self.name}'

    def __repr__(self):
        return str(self)

    @property
    def print_name(self):
        return self.name_localized
