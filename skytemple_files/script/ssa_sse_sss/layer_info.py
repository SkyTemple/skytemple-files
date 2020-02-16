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

from skytemple_files.script.ssa_sse_sss import ACTOR_ENTRY_LEN, OBJECT_ENTRY_LEN, PERFORMERS_ENTRY_LEN, \
    EVENTS_ENTRY_LEN, UNK10_ENTRY_LEN
from skytemple_files.script.ssa_sse_sss.header import SsaHeader


class SsaLayerInfo:
    """
    Information about the layers.
    """
    def __init__(self,
                 header: SsaHeader,
                 actors_count, actors_pointer,
                 objects_count, objects_pointer,
                 performers_count, performers_pointer,
                 events_count, events_pointer,
                 unk10_block_count, unk10_block_pointer):

        # If a value is (start offset of data block - 2), then it's count is 0.
        self.actors_count = actors_count
        self.objects_count = objects_count
        self.performers_count = performers_count
        self.events_count = events_count
        self.unk10_block_count = unk10_block_count

        self.actors_first_offset = None
        self.objects_first_offset = None
        self.performers_first_offset = None
        self.events_first_offset = None
        self.unk10_block_first_offset = None

        # It's also possible everything is just 0.
        if actors_pointer == 0 and objects_pointer == 0 and performers_pointer == 0 and events_pointer == 0 and unk10_block_pointer == 0:
            return

        if self.actors_count > 0:
            self.actors_first_offset = int((actors_pointer - header.actor_pointer) / ACTOR_ENTRY_LEN)
        elif header.actor_pointer is not None:
            assert header.actor_pointer - 2 == actors_pointer

        if self.objects_count > 0:
            self.objects_first_offset = int((objects_pointer - header.object_pointer) / OBJECT_ENTRY_LEN)
        elif header.object_pointer is not None:
            assert header.object_pointer - 2 == objects_pointer

        if self.performers_count > 0:
            self.performers_first_offset = int((performers_pointer - header.performer_pointer) / PERFORMERS_ENTRY_LEN)
        elif header.performer_pointer is not None:
            assert header.performer_pointer - 2 == performers_pointer

        if self.events_count > 0:
            self.events_first_offset = int((events_pointer - header.events_pointer) / EVENTS_ENTRY_LEN)
        elif header.events_pointer is not None:
            assert header.events_pointer - 2 == events_pointer

        if self.unk10_block_count > 0:
            self.unk10_block_first_offset = int((unk10_block_pointer - header.unk10_pointer) / UNK10_ENTRY_LEN)
        elif header.unk10_pointer is not None:
            assert header.unk10_pointer - 2 == unk10_block_pointer

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return f"SsaLayerInfo<{str({k:v for k,v in self.__dict__.items() if v is not None})}>"