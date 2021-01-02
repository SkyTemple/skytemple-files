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

# Operations are encoded in command bytes (CMD):
# PHASE 1
CMD_1_ZERO_OUT      = 0x80  # All values below
CMD_1_FILL_OUT      = 0x80  # All values equal/above until next
CMD_1_COPY_BYTES    = 0xC0  # All values equal/above
# PHASE 2
CMD_2_SEEK_OFFSET   = 0x80  # All values below
CMD_2_FILL_LOW      = 0x80  # All values equal/above until next
CMD_2_COPY_LOW      = 0xC0  # All values equal/above
