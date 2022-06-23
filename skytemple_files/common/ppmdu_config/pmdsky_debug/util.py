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
from __future__ import annotations

import re
from typing import Dict, Generic, TypeVar

V = TypeVar('V')
PASCAL_REGEX = re.compile(r'(?<!^)(?=[A-Z])')


class MultiCasingDict(Dict[str, V], Generic[V]):
    """
    A dictionary that treats entries using
    ThisCasing (pascal) and THIS_CASING (screaming snake) the same for getting items.

    As an implementation detail, camel case is also accepted and converted. For all other
    types of casings used for getting items the behaviour is undefined.

    NOTE: This behaviour is only implemented for this class itself NOT for its key set.
    """

    def __getitem__(self, k: str) -> V:
        try:
            return super().__getitem__(k)
        except KeyError as ex:
            try:
                return super().__getitem__(self._pascal_to_screaming_snake(k))
            except KeyError:
                try:
                    return super().__getitem__(self._screaming_snake_to_pascal(k))
                except KeyError:
                    # We re-raise the original exception to not confuse the caller.
                    raise ex

    def __contains__(self, o: object) -> bool:
        if not isinstance(o, str):
            return False
        if super().__contains__(o):
            return True
        if super().__contains__(self._pascal_to_screaming_snake(o)):
            return True
        return super().__contains__(self._screaming_snake_to_pascal(o))

    @staticmethod
    def _pascal_to_screaming_snake(string: str) -> str:
        return PASCAL_REGEX.sub('_', string).upper()


    @staticmethod
    def _screaming_snake_to_pascal(string) -> str:
        return ''.join(word.title() for word in string.split('_'))
