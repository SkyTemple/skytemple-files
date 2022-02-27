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
from enum import Enum
from typing import Protocol, Dict, Optional, Sequence, List, TypeVar, Tuple, Any

from explorerscript.source_map import SourceMap
from explorerscript.ssb_converting.ssb_data_types import SsbRoutineInfo, SsbOperation


class HasIdAndNameProtocol(Protocol):
    id: int
    name: str


class ScriptDirectionProtocol(Protocol):
    ssb_id: int
    name: str


class ScriptOpCodeArgumentProtocol(Protocol):
    id: int
    type: str
    name: str


class ScriptOpCodeRepeatingArgumentGroupProtocol(Protocol):
    id: int
    arguments: Sequence[ScriptOpCodeArgumentProtocol]


class ScriptOpCodeProtocol(HasIdAndNameProtocol):
    params: int
    stringidx: int
    unk2: int
    unk3: int
    arguments: Sequence[ScriptOpCodeArgumentProtocol]
    repeating_argument_group: Optional[ScriptOpCodeRepeatingArgumentGroupProtocol]


class ScriptDataProtocol(Protocol):
    @property
    @abstractmethod
    def game_variables__by_id(self) -> Dict[int, HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def game_variables__by_name(self) -> Dict[str, HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def objects__by_id(self) -> Dict[int, HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def face_names__by_id(self) -> Dict[int, HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def face_position_modes__by_id(self) -> List[HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def directions__by_ssb_id(self) -> Dict[int, ScriptDirectionProtocol]: ...

    @property
    @abstractmethod
    def common_routine_info__by_id(self) -> List[HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def menus__by_id(self) -> Dict[int, HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def process_specials__by_id(self) -> Dict[int, HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def sprite_effects__by_id(self) -> Dict[int, HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def bgms__by_id(self) -> Dict[int, HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def level_list__by_id(self) -> Dict[int, HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def level_entities__by_id(self) -> Dict[int, HasIdAndNameProtocol]: ...

    @property
    @abstractmethod
    def op_codes__by_id(self) -> Dict[int, ScriptOpCodeProtocol]: ...


class SourceMapV2Protocol(Protocol):
    # todo
    pass


class SsbRoutineType(Enum):
    GENERIC = 1
    ACTOR = 3
    OBJECT = 4
    PERFORMER = 5
    COROUTINE = 9
    INVALID = -1


class OperationProtocol(Protocol):
    offset: int
    op_code: HasIdAndNameProtocol
    params: List[Any]


class RoutineInfoProtocol(Protocol):
    type: SsbRoutineType
    linked_to: int
    linked_to_name: Optional[str] = None

    @property
    def linked_to_repr(self) -> Optional[str]: ...


S = TypeVar("S", bound=ScriptDataProtocol, contravariant=True)
R = TypeVar("R", bound=RoutineInfoProtocol)
O = TypeVar("O", bound=OperationProtocol)


class SsbProtocol(Protocol[S, R, O]):
    original_binary_data: bytes
    routine_info: List[Tuple[int, R]]
    routine_ops: List[List[O]]
    constants: List[str]
    strings: Dict[str, List[str]]

    @classmethod
    @abstractmethod
    def create_empty(cls, scriptdata: S, game_region: str) -> 'SsbProtocol': ...

    @abstractmethod
    def __init__(self, data: bytes, scriptdata: S, game_region: str, string_codec: str): ...

    def to_explorerscript(self) -> Tuple[str, SourceMap]: ...

    def to_explorerscript_v2(self) -> Tuple[str, SourceMapV2Protocol]: ...

    def to_ssb_script(self) -> Tuple[str, SourceMap]: ...
