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
from typing import TypeVar, Protocol, Optional, Sequence


class SwdlPcmdProtocol(Protocol):
    chunk_data: bytes


class SampleFormatConsts:
    PCM_8BIT = 0x0000
    PCM_16BIT = 0x0100
    ADPCM_4BIT = 0x0200
    PSG = 0x0300  # possibly


PCMD = TypeVar('PCMD', bound=SwdlPcmdProtocol)


class SwdlPcmdReferenceProtocol(Protocol[PCMD]):
    pcmd: PCMD
    offset: int
    length: int


PCMDR = TypeVar('PCMDR', bound=SwdlPcmdReferenceProtocol)


class SwdlSampleInfoTblEntryProtocol(Protocol[PCMDR]):
    id: int
    ftune: int
    ctune: int
    rootkey: int  # seems unused by game!
    ktps: int
    volume: int  # (0-127)
    pan: int  # (0-64-127)
    unk5: int  # probably key_group, always 0
    unk58: int
    sample_format: int  # compare against SampleFormatConsts
    unk9: int
    loop: bool
    unk10: int
    unk11: int
    unk12: int
    unk13: int
    sample_rate: int
    sample: Optional[PCMDR]
    loop_begin_pos: int  # (For ADPCM samples, the 4 bytes preamble is counted in the loopbeg!)
    loop_length: int

    envelope: int
    envelope_multiplier: int
    unk19: int
    unk20: int
    unk21: int
    unk22: int
    attack_volume: int
    attack: int
    decay: int
    sustain: int
    hold: int
    decay2: int
    release: int
    unk57: int


TE = TypeVar('TE', bound=SwdlSampleInfoTblEntryProtocol)


class SwdlWaviProtocol(Protocol[TE]):
    sample_info_table: Sequence[Optional[TE]]


class SwdlLfoEntryProtocol(Protocol):
    unk34: int
    unk52: int
    dest: int
    wshape: int
    rate: int
    unk29: int
    depth: int
    delay: int
    unk32: int
    unk33: int


class SwdlSplitEntryProtocol(Protocol):
    id: int
    unk11: int
    unk25: int
    lowkey: int
    hikey: int
    lolevel: int
    hilevel: int
    unk16: int
    unk17: int
    sample_id: int
    ftune: int
    ctune: int
    rootkey: int
    ktps: int
    sample_volume: int
    sample_pan: int
    keygroup_id: int
    unk22: int
    unk23: int
    unk24: int

    envelope: int
    envelope_multiplier: int
    unk37: int
    unk38: int
    unk39: int
    unk40: int
    attack_volume: int
    attack: int
    decay: int
    sustain: int
    hold: int
    decay2: int
    release: int
    unk53: int
    

SS = TypeVar('SS', bound=SwdlSplitEntryProtocol)
SL = TypeVar('SL', bound=SwdlLfoEntryProtocol)


class SwdlProgramTableProtocol(Protocol[SS, SL]):
    id: int
    prg_volume: int
    prg_pan: int
    unk3: int
    that_f_byte: int
    unk4: int
    unk5: int
    unk7: int
    unk8: int
    unk9: int
    lfos: Sequence[SL]
    splits: Sequence[SS]


SPT = TypeVar('SPT', bound=SwdlProgramTableProtocol)


class SwdlPrgiProtocol(Protocol[SPT]):
    program_table: Sequence[Optional[SPT]] = []


class SwdlKeygroupProtocol(Protocol):
    id: int
    poly: int
    priority: int
    vclow: int
    vchigh: int
    unk50: int
    unk51: int


KG = TypeVar('KG', bound=SwdlKeygroupProtocol)


class SwdlKgrpProtocol(Protocol[KG]):
    keygroups: Sequence[KG]


class SwdlPcmdLenProtocol(Protocol):
    reference: Optional[int]
    external: bool


PL = TypeVar('PL', bound=SwdlPcmdLenProtocol)


class SwdlHeaderProtocol(Protocol[PL]):
    version: int
    unk1: int
    unk2: int
    modified_date: bytes
    file_name: bytes
    unk13: int
    pcmdlen: PL
    unk17: int


H = TypeVar('H', bound=SwdlHeaderProtocol)
W = TypeVar('W', bound=SwdlWaviProtocol)
C = TypeVar('C', bound=SwdlPcmdProtocol)
P = TypeVar('P', bound=SwdlPrgiProtocol)
K = TypeVar('K', bound=SwdlKgrpProtocol)


class SwdlProtocol(Protocol[H, W, C, P, K]):
    header: H
    wavi: W
    pcmd: Optional[C]
    prgi: Optional[P]
    kgrp: Optional[K]

    @abstractmethod
    def __init__(self, data: bytes): ...
