#  Copyright 2020-2025 SkyTemple Contributors
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

from skytemple_files.user_error import USER_ERROR_MARK


class PatchPackageError(RuntimeError):
    pass


class PatchDependencyError(RuntimeError):
    pass


class PatchNotConfiguredError(RuntimeError):
    def __init__(self, message: str, config_parameter: str, error: str):
        super().__init__(message)
        self.config_parameter = config_parameter
        self.error = error
        setattr(self, USER_ERROR_MARK, True)
