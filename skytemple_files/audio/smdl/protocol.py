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
from abc import abstractmethod
from typing import Protocol, Sequence, Union, TypeVar, Optional


class SmdlHeaderProtocol(Protocol):
    version: int
    unk1: int
    unk2: int
    modified_date: bytes
    file_name: bytes
    unk5: int
    unk6: int
    unk8: int
    unk9: int


class SmdlSongProtocol(Protocol):
    unk1: int
    unk2: int
    unk3: int
    unk4: int
    tpqn: int
    unk5: int
    nbchans: int
    unk6: int
    unk7: int
    unk8: int
    unk9: int
    unk10: int
    unk11: int
    unk12: int


class SmdlEocProtocol(Protocol):
    param1: int
    param2: int


class SmdlTrackHeaderProtocol(Protocol):
    param1: int
    param2: int


class SmdlTrackPreambleProtocol(Protocol):
    track_id: int
    channel_id: int
    unk1: int
    unk2: int


class SmdlEventPlayNoteProtocol(Protocol):
    velocity: int
    octave_mod: int
    note: int
    key_down_duration: Optional[int]


class SmdlEventPauseProtocol(Protocol):
    value: int


class SmdlEventSpecialProtocol(Protocol):
    op: int
    params: Sequence[int]


SmdlEventProtocol = Union[SmdlEventSpecialProtocol, SmdlEventPauseProtocol, SmdlEventPlayNoteProtocol]


TH = TypeVar('TH', bound=SmdlTrackHeaderProtocol)
TP = TypeVar('TP', bound=SmdlTrackPreambleProtocol)
E = TypeVar('E', bound=SmdlEventProtocol)


class SmdlTrackProtocol(Protocol[TH, TP, E]):
    header: TH
    preamble: TP
    events: Sequence[E]


H = TypeVar('H', bound=SmdlHeaderProtocol)
S = TypeVar('S', bound=SmdlSongProtocol)
O = TypeVar('O', bound=SmdlEocProtocol)
T = TypeVar('T', bound=SmdlTrackProtocol)


class SmdlProtocol(Protocol[H, S, T, O]):
    header: H
    song: S
    tracks: Sequence[T]
    eoc: O

    @abstractmethod
    def __init__(self, data: bytes): ...
