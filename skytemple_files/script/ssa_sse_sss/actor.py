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
from skytemple_files.script.ssa_sse_sss.position import SsaPosition


class SsaActor:
    def __init__(self, actor_id, pos: SsaPosition, script_id, unkE):
        self.actor_id = actor_id
        self.pos = pos
        self.script_id = script_id
        self.unkE = unkE

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return f"SsaActor<{str({k: v for k, v in self.__dict__.items() if v is not None})}>"
