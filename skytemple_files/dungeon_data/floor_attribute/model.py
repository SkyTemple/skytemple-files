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


from skytemple_files.common.util import read_u32


class FloorAttribute:
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)
        self.attrs = []
        last_ptr = read_u32(data, 0)
        nbgroups = last_ptr // 4
        for g in range(nbgroups):
            start = read_u32(data, g * 4)
            if g == nbgroups - 1:
                end = len(data)
            else:
                end = read_u32(data, g * 4 + 4)
            g_list = list(data[start:end])
            self.attrs.append(g_list)

    def extend_nb_floors(
        self, group_id: int, start_floor: int, nb_floors: int, rank: int = 0
    ):
        if nb_floors > 0:
            self.attrs[group_id] = (
                self.attrs[group_id][:start_floor]
                + ([rank] * nb_floors)
                + self.attrs[group_id][start_floor:]
            )
        elif nb_floors < 0:
            self.attrs[group_id] = (
                self.attrs[group_id][: start_floor + nb_floors]
                + self.attrs[group_id][start_floor:]
            )

    def reorder_floors(
        self, reorder_list: list[list[tuple[int, int | None, int | None]]]
    ):
        new_attrs = []
        for new_groups in reorder_list:
            new_attrs.append([0])
            for t_switch in new_groups:
                group_id = t_switch[0]
                start = t_switch[1]
                end = t_switch[2]
                if start == None:
                    start = 0
                start += 1  # type: ignore
                if end == None:
                    end = len(self.attrs[group_id])
                end += 1  # type: ignore
                new_attrs[-1].extend(self.attrs[group_id][start:end])
        self.attrs = new_attrs

    def adjust_nb_floors(self, group_id: int, nb_floors: int):
        while group_id >= len(self.attrs):
            self.attrs.append([0])
        if len(self.attrs[group_id]) > nb_floors:
            self.attrs[group_id] = self.attrs[group_id][:nb_floors]
        else:
            self.attrs[group_id].extend([0] * (nb_floors - len(self.attrs[group_id])))

    def set_floor_attr(self, group_id: int, floor_id: int, attr: int):
        self.attrs[group_id][floor_id] = attr

    def get_floor_attr(self, group_id: int, floor_id: int):
        return self.attrs[group_id][floor_id]
