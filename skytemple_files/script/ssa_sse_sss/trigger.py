#  Copyright 2020 Parakoopa
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


class SsaTrigger:
    def __init__(self, coroutine_id, unk2, unk3, script_id):
        self.coroutine_id = coroutine_id
        self.unk2 = unk2
        self.unk3 = unk3
        self.script_id = script_id

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return f"SsaTrigger<{str({k: v for k, v in self.__dict__.items() if v is not None})}>"
