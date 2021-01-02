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

# Length of the default lookback buffer. The "sliding window" so to speak!
# Used to determine how far back the compressor looks for matching sequences!
PX_LOOKBACK_BUFFER_SIZE = 4096
# The longest sequence of similar bytes we can use!
PX_MAX_MATCH_SEQLEN = 18
# The shortest sequence of similar bytes we can use!
PX_MIN_MATCH_SEQLEN = 3
# The nb of unique lengths we can use when copying a sequence.
# This is due to ctrl flags taking over a part of the value range between 0x0 and 0xF
# The amount of possible lengths a sequence to lookup can have, considering
# there are 9 ctrl flags, and only 0 to 15 as range to contain all that info!
# 9 + 7 = 16
PX_NB_POSSIBLE_SEQUENCES_LEN = PX_NB_POSSIBLE_SEQ_LEN = 7
# bytes:
PX_MINIMUM_COMPRESSED_SIZE = 9
