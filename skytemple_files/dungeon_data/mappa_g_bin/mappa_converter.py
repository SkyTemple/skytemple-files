""""Module to convert mappa_*.bin to mappa_g*.bin."""
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
from skytemple_files.dungeon_data.mappa_bin.model import MappaBin
from skytemple_files.dungeon_data.mappa_g_bin.model import MappaGBin, MappaGFloor, MappaGFloorLayout


def convert_mappa_to_mappag(mappa: MappaBin) -> MappaGBin:
    mappag_floor_lists = []
    for floor_list in mappa.floor_lists:
        gfloor_list = []
        mappag_floor_lists.append(gfloor_list)
        for floor in floor_list:
            gfloor_list.append(MappaGFloor(MappaGFloorLayout(
                floor.layout.tileset_id, floor.layout.fixed_floor_id
            )))

    return MappaGBin(mappag_floor_lists)
