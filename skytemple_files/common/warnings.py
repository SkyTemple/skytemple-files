#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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

from typing import Tuple


class DeprecatedToBeRemovedWarning(DeprecationWarning):
    """
    A special DeprecationWarning that includes a version in which the deprecated functionality is no longer
    expected to work.
    """

    expected_removal: Tuple[int, int, int]
    message: str

    def __init__(self, message: str, expected_removal: Tuple[int, int, int]):
        self.message = message
        self.expected_removal = expected_removal

    def __str__(self) -> str:
        """__str__ just returns the message. The version needs to be processed separately."""
        return self.message

    def __repr__(self) -> str:
        return (
            f"DeprecatedToBeRemovedWarning("
            f"message={repr(self.message)}, "
            f"expected_removal={repr(self.expected_removal)}"
            f")"
        )
