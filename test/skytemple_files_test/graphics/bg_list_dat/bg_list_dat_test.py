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
from __future__ import annotations

import os.path
from typing import Dict, List, Optional, Sequence, Union, no_type_check

from skytemple_files.common.util import mutate_sequence
from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler
from skytemple_files.graphics.bg_list_dat.protocol import (
    BgListEntryProtocol,
    BgListProtocol,
)
from skytemple_files.graphics.bma.protocol import BmaProtocol
from skytemple_files.graphics.bpa.protocol import BpaProtocol
from skytemple_files.graphics.bpc.protocol import BpcProtocol
from skytemple_files.graphics.bpl.protocol import BplProtocol
from skytemple_files_test.graphics.stubs.rom_file_provider import RomFileProviderStub
from skytemple_files_test.case import SkyTempleFilesTestCase, fixpath, romtest

FIXTURE_REPR = [
    {
        "bpl_name": "S00P01A",
        "bpc_name": "S00P01A",
        "bma_name": "S00P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "T00P01",
        "bpc_name": "T00P01",
        "bma_name": "T00P01",
        "bpa_names": ["T00P011", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "T00P02",
        "bpc_name": "T00P02",
        "bma_name": "T00P02",
        "bpa_names": [None, None, None, None, "T00P025", None, None, None],
    },
    {
        "bpl_name": "T00P03",
        "bpc_name": "T00P03",
        "bma_name": "T00P03",
        "bpa_names": [None, None, None, None, "T00P035", None, None, None],
    },
    {
        "bpl_name": "T00P04A",
        "bpc_name": "T00P04A",
        "bma_name": "T00P04A",
        "bpa_names": ["T00P04A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "T00P04A2",
        "bpc_name": "T00P04A",
        "bma_name": "T00P04A2",
        "bpa_names": ["T00P04A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D00P01",
        "bpc_name": "D00P01",
        "bma_name": "D00P01",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D00P02",
        "bpc_name": "D00P02",
        "bma_name": "D00P02",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V00P01",
        "bpc_name": "V00P01",
        "bma_name": "V00P01",
        "bpa_names": ["V00P011", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V00P02",
        "bpc_name": "V00P02",
        "bma_name": "V00P02",
        "bpa_names": ["V00P021", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V00P03",
        "bpc_name": "V00P03",
        "bma_name": "V00P03",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D01P11A",
        "bpc_name": "D01P11A",
        "bma_name": "D01P11A",
        "bpa_names": [None, None, None, None, "D01P11A5", None, None, None],
    },
    {
        "bpl_name": "D01P11B",
        "bpc_name": "D01P11B",
        "bma_name": "D01P11B",
        "bpa_names": [None, None, None, None, "D01P11B5", None, None, None],
    },
    {
        "bpl_name": "D01P41A",
        "bpc_name": "D01P41A",
        "bma_name": "D01P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D02P11A",
        "bpc_name": "D02P11A",
        "bma_name": "D02P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D02P31A",
        "bpc_name": "D02P31A",
        "bma_name": "D02P31A",
        "bpa_names": [None, None, None, None, "D02P31A5", None, None, None],
    },
    {
        "bpl_name": "D03P11A",
        "bpc_name": "D03P11A",
        "bma_name": "D03P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D03P41A",
        "bpc_name": "D03P41A",
        "bma_name": "D03P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D04P11A",
        "bpc_name": "D04P11A",
        "bma_name": "D04P11A",
        "bpa_names": [None, None, None, None, "D04P11A5", None, None, None],
    },
    {
        "bpl_name": "D04P12A",
        "bpc_name": "D04P12A",
        "bma_name": "D04P12A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D04P31A",
        "bpc_name": "D04P31A",
        "bma_name": "D04P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D05P11A",
        "bpc_name": "D05P11A",
        "bma_name": "D05P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D05P31A",
        "bpc_name": "D05P31A",
        "bma_name": "D05P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D06P11A",
        "bpc_name": "D06P11A",
        "bma_name": "D06P11A",
        "bpa_names": [None, None, None, None, "D06P11A5", None, None, None],
    },
    {
        "bpl_name": "D07P11A",
        "bpc_name": "D07P11A",
        "bma_name": "D07P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D08P11A",
        "bpc_name": "D08P11A",
        "bma_name": "D08P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D09P11A",
        "bpc_name": "D09P11A",
        "bma_name": "D09P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D10P21A",
        "bpc_name": "D10P21A",
        "bma_name": "D10P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D10P41A",
        "bpc_name": "D10P41A",
        "bma_name": "D10P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D11P11A",
        "bpc_name": "D11P11A",
        "bma_name": "D11P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D12P21A",
        "bpc_name": "D12P21A",
        "bma_name": "D12P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D12P41A",
        "bpc_name": "D12P41A",
        "bma_name": "D12P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D13P11A",
        "bpc_name": "D13P11A",
        "bma_name": "D13P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D14P11A",
        "bpc_name": "D14P11A",
        "bma_name": "D14P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D14P12A",
        "bpc_name": "D14P12A",
        "bma_name": "D14P12A",
        "bpa_names": ["D14P12A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D15P21A",
        "bpc_name": "D15P21A",
        "bma_name": "D15P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D15P41A",
        "bpc_name": "D15P41A",
        "bma_name": "D15P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D16P11A",
        "bpc_name": "D16P11A",
        "bma_name": "D16P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D16P31A",
        "bpc_name": "D16P31A",
        "bma_name": "D16P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D17P11A",
        "bpc_name": "D17P11A",
        "bma_name": "D17P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D17P31A",
        "bpc_name": "D17P31A",
        "bma_name": "D17P31A",
        "bpa_names": ["D17P31A1", None, None, None, "D17P31A5", None, None, None],
    },
    {
        "bpl_name": "D17P32A",
        "bpc_name": "D17P32A",
        "bma_name": "D17P32A",
        "bpa_names": ["D17P32A1", None, None, None, "D17P32A5", None, None, None],
    },
    {
        "bpl_name": "D17P33A",
        "bpc_name": "D17P33A",
        "bma_name": "D17P33A",
        "bpa_names": ["D17P33A1", None, None, None, "D17P33A5", None, None, None],
    },
    {
        "bpl_name": "D17P34A",
        "bpc_name": "D17P34A",
        "bma_name": "D17P34A",
        "bpa_names": ["D17P34A1", None, None, None, "D17P34A5", None, None, None],
    },
    {
        "bpl_name": "D17P45A",
        "bpc_name": "D17P45A",
        "bma_name": "D17P45A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D18P11A",
        "bpc_name": "D18P11A",
        "bma_name": "D18P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D19P11A",
        "bpc_name": "D19P11A",
        "bma_name": "D19P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D20P11A",
        "bpc_name": "D20P11A",
        "bma_name": "D20P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D21P21A",
        "bpc_name": "D21P21A",
        "bma_name": "D21P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D21P41A",
        "bpc_name": "D21P41A",
        "bma_name": "D21P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D22P11A",
        "bpc_name": "D22P11A",
        "bma_name": "D22P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D23P11A",
        "bpc_name": "D23P11A",
        "bma_name": "D23P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D24P11A",
        "bpc_name": "D24P11A",
        "bma_name": "D24P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D24P31A",
        "bpc_name": "D24P31A",
        "bma_name": "D24P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D24P31B",
        "bpc_name": "D24P31B",
        "bma_name": "D24P31B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D25P11A",
        "bpc_name": "D25P11A",
        "bma_name": "D25P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D26P21A",
        "bpc_name": "D26P21A",
        "bma_name": "D26P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D26P31A",
        "bpc_name": "D26P31A",
        "bma_name": "D26P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D26P43A",
        "bpc_name": "D26P43A",
        "bma_name": "D26P43A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D27P11A",
        "bpc_name": "D27P11A",
        "bma_name": "D27P11A",
        "bpa_names": ["D27P11A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D28P21A",
        "bpc_name": "D28P21A",
        "bma_name": "D28P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D28P31A",
        "bpc_name": "D28P31A",
        "bma_name": "D28P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D28P32A",
        "bpc_name": "D28P32A",
        "bma_name": "D28P32A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D28P33A",
        "bpc_name": "D28P33A",
        "bma_name": "D28P33A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D28P33C",
        "bpc_name": "D28P33C",
        "bma_name": "D28P33C",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D28P34A",
        "bpc_name": "D28P34A",
        "bma_name": "D28P34A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D28P44A",
        "bpc_name": "D28P44A",
        "bma_name": "D28P44A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D29P11A",
        "bpc_name": "D29P11A",
        "bma_name": "D29P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D30P21A",
        "bpc_name": "D30P21A",
        "bma_name": "D30P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D30P32A",
        "bpc_name": "D30P32A",
        "bma_name": "D30P32A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D30P33A",
        "bpc_name": "D30P33A",
        "bma_name": "D30P33A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D30P34A",
        "bpc_name": "D30P34A",
        "bma_name": "D30P34A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D30P41A",
        "bpc_name": "D30P41A",
        "bma_name": "D30P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D30P42A",
        "bpc_name": "D30P42A",
        "bma_name": "D30P42A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D31P11A",
        "bpc_name": "D31P11A",
        "bma_name": "D31P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D31P31A",
        "bpc_name": "D31P31A",
        "bma_name": "D31P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D31P41A",
        "bpc_name": "D31P41A",
        "bma_name": "D31P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D32P11A",
        "bpc_name": "D32P11A",
        "bma_name": "D32P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D32P12A",
        "bpc_name": "D32P12A",
        "bma_name": "D32P12A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D32P13A",
        "bpc_name": "D32P13A",
        "bma_name": "D32P13A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D32P14A",
        "bpc_name": "D32P14A",
        "bma_name": "D32P14A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D32P31A",
        "bpc_name": "D32P31A",
        "bma_name": "D32P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D32P32A",
        "bpc_name": "D32P32A",
        "bma_name": "D32P32A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D32P33A",
        "bpc_name": "D32P33A",
        "bma_name": "D32P33A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D32P41A",
        "bpc_name": "D32P41A",
        "bma_name": "D32P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D32P42A",
        "bpc_name": "D32P42A",
        "bma_name": "D32P42A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D32P43A",
        "bpc_name": "D32P43A",
        "bma_name": "D32P43A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D32P44A",
        "bpc_name": "D32P44A",
        "bma_name": "D32P44A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D33P41A",
        "bpc_name": "D33P41A",
        "bma_name": "D33P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D34P41A",
        "bpc_name": "D34P41A",
        "bma_name": "D34P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D35P21A",
        "bpc_name": "D35P21A",
        "bma_name": "D35P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D35P41A",
        "bpc_name": "D35P41A",
        "bma_name": "D35P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D36P11A",
        "bpc_name": "D36P11A",
        "bma_name": "D36P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D36P41A",
        "bpc_name": "D36P41A",
        "bma_name": "D36P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D37P11A",
        "bpc_name": "D37P11A",
        "bma_name": "D37P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D37P41A",
        "bpc_name": "D37P41A",
        "bma_name": "D37P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D38P11A",
        "bpc_name": "D38P11A",
        "bma_name": "D38P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D38P12A",
        "bpc_name": "D38P12A",
        "bma_name": "D38P12A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D39P21A",
        "bpc_name": "D39P21A",
        "bma_name": "D39P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D39P32A",
        "bpc_name": "D39P32A",
        "bma_name": "D39P32A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D39P41A",
        "bpc_name": "D39P41A",
        "bma_name": "D39P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D40P11A",
        "bpc_name": "D40P11A",
        "bma_name": "D40P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D41P21A",
        "bpc_name": "D41P21A",
        "bma_name": "D41P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D41P41A",
        "bpc_name": "D41P41A",
        "bma_name": "D41P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D42P21A",
        "bpc_name": "D42P21A",
        "bma_name": "D42P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D42P31A",
        "bpc_name": "D42P31A",
        "bma_name": "D42P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D42P41A",
        "bpc_name": "D42P41A",
        "bma_name": "D42P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D42P42A",
        "bpc_name": "D42P42A",
        "bma_name": "D42P42A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D43P31A",
        "bpc_name": "D43P31A",
        "bma_name": "D43P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D44P31A",
        "bpc_name": "D44P31A",
        "bma_name": "D44P31A",
        "bpa_names": ["D44P31A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D45P21A",
        "bpc_name": "D45P21A",
        "bma_name": "D45P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D45P31A",
        "bpc_name": "D45P31A",
        "bma_name": "D45P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D45P42A",
        "bpc_name": "D45P42A",
        "bma_name": "D45P42A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D46P11A",
        "bpc_name": "D46P11A",
        "bma_name": "D46P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D46P21A",
        "bpc_name": "D46P21A",
        "bma_name": "D46P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D46P31A",
        "bpc_name": "D46P31A",
        "bma_name": "D46P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D46P41A",
        "bpc_name": "D46P41A",
        "bma_name": "D46P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D47P11A",
        "bpc_name": "D47P11A",
        "bma_name": "D47P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D48P11A",
        "bpc_name": "D48P11A",
        "bma_name": "D48P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D48P21A",
        "bpc_name": "D48P21A",
        "bma_name": "D48P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D49P41A",
        "bpc_name": "D49P41A",
        "bma_name": "D49P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D50P11A",
        "bpc_name": "D50P11A",
        "bma_name": "D50P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D51P11A",
        "bpc_name": "D51P11A",
        "bma_name": "D51P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D51P21A",
        "bpc_name": "D51P21A",
        "bma_name": "D51P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D51P41A",
        "bpc_name": "D51P41A",
        "bma_name": "D51P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D52P11A",
        "bpc_name": "D52P11A",
        "bma_name": "D52P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D52P11C",
        "bpc_name": "D52P11C",
        "bma_name": "D52P11C",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D52P31A",
        "bpc_name": "D52P31A",
        "bma_name": "D52P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D52P32A",
        "bpc_name": "D52P32A",
        "bma_name": "D52P32A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D53P11A",
        "bpc_name": "D53P11A",
        "bma_name": "D53P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D53P11B",
        "bpc_name": "D53P11B",
        "bma_name": "D53P11B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D53P21A",
        "bpc_name": "D53P21A",
        "bma_name": "D53P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D53P41A",
        "bpc_name": "D53P41A",
        "bma_name": "D53P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D53P41B",
        "bpc_name": "D53P41B",
        "bma_name": "D53P41B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D53P41C",
        "bpc_name": "D53P41C",
        "bma_name": "D53P41C",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D54P11A",
        "bpc_name": "D54P11A",
        "bma_name": "D54P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D54P31A",
        "bpc_name": "D54P31A",
        "bma_name": "D54P31A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D54P32A",
        "bpc_name": "D54P32A",
        "bma_name": "D54P32A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D55P11A",
        "bpc_name": "D55P11A",
        "bma_name": "D55P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D55P21A",
        "bpc_name": "D55P21A",
        "bma_name": "D55P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D55P41A",
        "bpc_name": "D55P41A",
        "bma_name": "D55P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D56P11A",
        "bpc_name": "D56P11A",
        "bma_name": "D56P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D56P12A",
        "bpc_name": "D56P12A",
        "bma_name": "D56P12A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D56P21A",
        "bpc_name": "D56P21A",
        "bma_name": "D56P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D56P41A",
        "bpc_name": "D56P41A",
        "bma_name": "D56P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D57P21A",
        "bpc_name": "D57P21A",
        "bma_name": "D57P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D57P41A",
        "bpc_name": "D57P41A",
        "bma_name": "D57P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D57P42A",
        "bpc_name": "D57P42A",
        "bma_name": "D57P42A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D57P43A",
        "bpc_name": "D57P43A",
        "bma_name": "D57P43A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D57P44A",
        "bpc_name": "D57P44A",
        "bma_name": "D57P44A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D58P41A",
        "bpc_name": "D58P41A",
        "bma_name": "D58P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D59P41A",
        "bpc_name": "D59P41A",
        "bma_name": "D59P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D60P41A",
        "bpc_name": "D60P41A",
        "bma_name": "D60P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D61P41A",
        "bpc_name": "D61P41A",
        "bma_name": "D61P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D62P41A",
        "bpc_name": "D62P41A",
        "bma_name": "D62P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D63P41A",
        "bpc_name": "D63P41A",
        "bma_name": "D63P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D73P11A",
        "bpc_name": "D73P11A",
        "bma_name": "D73P11A",
        "bpa_names": ["D73P11A1", None, None, None, "D73P11A5", None, None, None],
    },
    {
        "bpl_name": "D73P21A",
        "bpc_name": "D73P21A",
        "bma_name": "D73P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D73P22A",
        "bpc_name": "D73P22A",
        "bma_name": "D73P22A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D73P23A",
        "bpc_name": "D73P23A",
        "bma_name": "D73P23A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D73P24A",
        "bpc_name": "D73P24A",
        "bma_name": "D73P24A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D73P25A",
        "bpc_name": "D73P25A",
        "bma_name": "D73P25A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D73P26A",
        "bpc_name": "D73P26A",
        "bma_name": "D73P26A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D73P27A",
        "bpc_name": "D73P27A",
        "bma_name": "D73P27A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D73P28A",
        "bpc_name": "D73P28A",
        "bma_name": "D73P28A",
        "bpa_names": ["D73P28A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D73P29A",
        "bpc_name": "D73P29A",
        "bma_name": "D73P29A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D73P31A",
        "bpc_name": "D73P31A",
        "bma_name": "D73P31A",
        "bpa_names": ["D73P31A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D73P41A",
        "bpc_name": "D73P41A",
        "bma_name": "D73P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D65P41A",
        "bpc_name": "D65P41A",
        "bma_name": "D65P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D66P41A",
        "bpc_name": "D66P41A",
        "bma_name": "D66P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D67P41A",
        "bpc_name": "D67P41A",
        "bma_name": "D67P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D68P41A",
        "bpc_name": "D68P41A",
        "bma_name": "D68P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D69P41A",
        "bpc_name": "D69P41A",
        "bma_name": "D69P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D70P41A",
        "bpc_name": "D70P41A",
        "bma_name": "D70P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D71P41A",
        "bpc_name": "D71P41A",
        "bma_name": "D71P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D72P41A",
        "bpc_name": "D72P41A",
        "bma_name": "D72P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D79P11A",
        "bpc_name": "D79P11A",
        "bma_name": "D79P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D79P21A",
        "bpc_name": "D79P21A",
        "bma_name": "D79P21A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D79P41A",
        "bpc_name": "D79P41A",
        "bma_name": "D79P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D80P41A",
        "bpc_name": "D80P41A",
        "bma_name": "D80P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D81P41A",
        "bpc_name": "D81P41A",
        "bma_name": "D81P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D82P41A",
        "bpc_name": "D82P41A",
        "bma_name": "D82P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D83P41A",
        "bpc_name": "D83P41A",
        "bma_name": "D83P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D84P41A",
        "bpc_name": "D84P41A",
        "bma_name": "D84P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D85P41A",
        "bpc_name": "D85P41A",
        "bma_name": "D85P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D86P41A",
        "bpc_name": "D86P41A",
        "bma_name": "D86P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D87P41A",
        "bpc_name": "D87P41A",
        "bma_name": "D87P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D88P41A",
        "bpc_name": "D88P41A",
        "bma_name": "D88P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D89P41A",
        "bpc_name": "D89P41A",
        "bma_name": "D89P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D90P41A",
        "bpc_name": "D90P41A",
        "bma_name": "D90P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D91P41A",
        "bpc_name": "D91P41A",
        "bma_name": "D91P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D92P41A",
        "bpc_name": "D92P41A",
        "bma_name": "D92P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D93P41A",
        "bpc_name": "D93P41A",
        "bma_name": "D93P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D94P41A",
        "bpc_name": "D94P41A",
        "bma_name": "D94P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "D95P41A",
        "bpc_name": "D95P41A",
        "bma_name": "D95P41A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P01A",
        "bpc_name": "G01P01A",
        "bma_name": "G01P01A",
        "bpa_names": ["G01P01A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P01A2",
        "bpc_name": "G01P01A",
        "bma_name": "G01P01A2",
        "bpa_names": ["G01P01A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P01B",
        "bpc_name": "G01P01B",
        "bma_name": "G01P01B",
        "bpa_names": ["G01P01B1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P01B2",
        "bpc_name": "G01P01B",
        "bma_name": "G01P01B2",
        "bpa_names": ["G01P01B1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P01C",
        "bpc_name": "G01P01C",
        "bma_name": "G01P01C",
        "bpa_names": ["G01P01C1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P01C2",
        "bpc_name": "G01P01C",
        "bma_name": "G01P01C2",
        "bpa_names": ["G01P01C1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P02A",
        "bpc_name": "G01P02A",
        "bma_name": "G01P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P03A",
        "bpc_name": "G01P03A",
        "bma_name": "G01P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P04A",
        "bpc_name": "G01P04A",
        "bma_name": "G01P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P04A2",
        "bpc_name": "G01P04A",
        "bma_name": "G01P04A2",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P04C",
        "bpc_name": "G01P04C",
        "bma_name": "G01P04C",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P04C2",
        "bpc_name": "G01P04C",
        "bma_name": "G01P04C2",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P05A",
        "bpc_name": "G01P05A",
        "bma_name": "G01P05A",
        "bpa_names": ["G01P05A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P05C",
        "bpc_name": "G01P05C",
        "bma_name": "G01P05C",
        "bpa_names": ["G01P05C1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P06A",
        "bpc_name": "G01P06A",
        "bma_name": "G01P06A",
        "bpa_names": ["G01P06A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P06B",
        "bpc_name": "G01P06B",
        "bma_name": "G01P06B",
        "bpa_names": ["G01P06B1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P07A",
        "bpc_name": "G01P07A",
        "bma_name": "G01P07A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P07C",
        "bpc_name": "G01P07C",
        "bma_name": "G01P07C",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P08A",
        "bpc_name": "G01P08A",
        "bma_name": "G01P08A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P09A",
        "bpc_name": "G01P09A",
        "bma_name": "G01P09A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P09C",
        "bpc_name": "G01P09C",
        "bma_name": "G01P09C",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P10A",
        "bpc_name": "G01P10A",
        "bma_name": "G01P10A",
        "bpa_names": ["G01P10A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "G01P10C",
        "bpc_name": "G01P10C",
        "bma_name": "G01P10C",
        "bpa_names": ["G01P10C1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "H01P99A",
        "bpc_name": "H01P99A",
        "bma_name": "H01P99A",
        "bpa_names": ["H01P99A1", None, None, None, "H01P99A5", None, None, None],
    },
    {
        "bpl_name": "H01P99C",
        "bpc_name": "H01P99C",
        "bma_name": "H01P99C",
        "bpa_names": ["H01P99C1", None, None, None, "H01P99C5", None, None, None],
    },
    {
        "bpl_name": "H01P99D",
        "bpc_name": "H01P99D",
        "bma_name": "H01P99D",
        "bpa_names": ["H01P99D1", None, None, None, "H01P99D5", None, None, None],
    },
    {
        "bpl_name": "H01P99E",
        "bpc_name": "H01P99E",
        "bma_name": "H01P99E",
        "bpa_names": ["H01P99E1", None, None, None, "H01P99E5", None, None, None],
    },
    {
        "bpl_name": "H02P99A",
        "bpc_name": "H02P99A",
        "bma_name": "H02P99A",
        "bpa_names": ["H02P99A1", None, None, None, "H02P99A5", None, None, None],
    },
    {
        "bpl_name": "H02P99C",
        "bpc_name": "H02P99C",
        "bma_name": "H02P99C",
        "bpa_names": ["H02P99C1", None, None, None, "H02P99C5", None, None, None],
    },
    {
        "bpl_name": "P01P01A",
        "bpc_name": "P01P01A",
        "bma_name": "P01P01A",
        "bpa_names": ["P01P01A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P01P02A",
        "bpc_name": "P01P02A",
        "bma_name": "P01P02A",
        "bpa_names": ["P01P02A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P01P03A",
        "bpc_name": "P01P03A",
        "bma_name": "P01P03A",
        "bpa_names": ["P01P03A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P01P04A",
        "bpc_name": "P01P04A",
        "bma_name": "P01P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P02P01A",
        "bpc_name": "P02P01A",
        "bma_name": "P02P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P03P01A",
        "bpc_name": "P03P01A",
        "bma_name": "P03P01A",
        "bpa_names": ["P03P01A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P03P02A",
        "bpc_name": "P03P02A",
        "bma_name": "P03P02A",
        "bpa_names": ["P03P02A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P04P01C",
        "bpc_name": "P04P01C",
        "bma_name": "P04P01C",
        "bpa_names": [None, None, None, None, "P04P01C5", None, None, None],
    },
    {
        "bpl_name": "P05P01A",
        "bpc_name": "P05P01A",
        "bma_name": "P05P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P05P02A",
        "bpc_name": "P05P02A",
        "bma_name": "P05P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P05P02A2",
        "bpc_name": "P05P02A",
        "bma_name": "P05P02A2",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P05P03A",
        "bpc_name": "P05P03A",
        "bma_name": "P05P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P05P04A",
        "bpc_name": "P05P04A",
        "bma_name": "P05P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P06P01A",
        "bpc_name": "P06P01A",
        "bma_name": "P06P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P07P01A",
        "bpc_name": "P07P01A",
        "bma_name": "P07P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P08P01A",
        "bpc_name": "P08P01A",
        "bma_name": "P08P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P09P01A",
        "bpc_name": "P09P01A",
        "bma_name": "P09P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P10P01A",
        "bpc_name": "P10P01A",
        "bma_name": "P10P01A",
        "bpa_names": [None, None, None, None, "P10P01A5", None, None, None],
    },
    {
        "bpl_name": "P11P01A",
        "bpc_name": "P11P01A",
        "bma_name": "P11P01A",
        "bpa_names": [None, None, None, None, "P11P01A5", None, None, None],
    },
    {
        "bpl_name": "P12P01A",
        "bpc_name": "P12P01A",
        "bma_name": "P12P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P12P02A",
        "bpc_name": "P12P02A",
        "bma_name": "P12P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P13P01A",
        "bpc_name": "P13P01A",
        "bma_name": "P13P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P14P01A",
        "bpc_name": "P14P01A",
        "bma_name": "P14P01A",
        "bpa_names": ["P14P01A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P14P01A2",
        "bpc_name": "P14P01A",
        "bma_name": "P14P01A2",
        "bpa_names": ["P14P01A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P15P01A",
        "bpc_name": "P15P01A",
        "bma_name": "P15P01A",
        "bpa_names": [None, None, None, None, "P15P01A5", None, None, None],
    },
    {
        "bpl_name": "P16P01A",
        "bpc_name": "P16P01A",
        "bma_name": "P16P01A",
        "bpa_names": [None, None, None, None, "P16P01A5", None, None, None],
    },
    {
        "bpl_name": "P17P01A",
        "bpc_name": "P17P01A",
        "bma_name": "P17P01A",
        "bpa_names": [None, None, None, None, "P17P01A5", None, None, None],
    },
    {
        "bpl_name": "P17P02A",
        "bpc_name": "P17P02A",
        "bma_name": "P17P02A",
        "bpa_names": ["P17P02A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P17P02C",
        "bpc_name": "P17P02C",
        "bma_name": "P17P02C",
        "bpa_names": ["P17P02C1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P18P01A",
        "bpc_name": "P18P01A",
        "bma_name": "P18P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P19P01A",
        "bpc_name": "P19P01A",
        "bma_name": "P19P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P19P02A",
        "bpc_name": "P19P02A",
        "bma_name": "P19P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P20P01A",
        "bpc_name": "P20P01A",
        "bma_name": "P20P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P20P02A",
        "bpc_name": "P20P02A",
        "bma_name": "P20P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P20P03A",
        "bpc_name": "P20P03A",
        "bma_name": "P20P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P21P02A",
        "bpc_name": "P21P02A",
        "bma_name": "P21P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P22P01A",
        "bpc_name": "P22P01A",
        "bma_name": "P22P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P23P01A",
        "bpc_name": "P23P01A",
        "bma_name": "P23P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P23P02A",
        "bpc_name": "P23P02A",
        "bma_name": "P23P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P24P01A",
        "bpc_name": "P24P01A",
        "bma_name": "P24P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P25P01A",
        "bpc_name": "P25P01A",
        "bma_name": "P25P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P26P01A",
        "bpc_name": "P26P01A",
        "bma_name": "P26P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P27P01A",
        "bpc_name": "P27P01A",
        "bma_name": "P27P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "P28P01A",
        "bpc_name": "P28P01A",
        "bma_name": "P28P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S01P01A",
        "bpc_name": "S01P01A",
        "bma_name": "S01P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S01P01B",
        "bpc_name": "S01P01B",
        "bma_name": "S01P01B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S01P02A",
        "bpc_name": "S01P02A",
        "bma_name": "S01P02A",
        "bpa_names": ["S01P02A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S01P03A",
        "bpc_name": "S01P02A",
        "bma_name": "S01P02A",
        "bpa_names": ["S01P02A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S01P04A",
        "bpc_name": "S01P04A",
        "bma_name": "S01P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S02P01A",
        "bpc_name": "S02P01A",
        "bma_name": "S02P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S03P01A",
        "bpc_name": "S03P01A",
        "bma_name": "S03P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S03P02A",
        "bpc_name": "S03P02A",
        "bma_name": "S03P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S04P01A",
        "bpc_name": "S04P01A",
        "bma_name": "S04P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S05P01A",
        "bpc_name": "S05P01A",
        "bma_name": "S05P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S05P02C",
        "bpc_name": "S05P02C",
        "bma_name": "S05P02C",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S05P03A",
        "bpc_name": "S05P03A",
        "bma_name": "S05P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S05P04A",
        "bpc_name": "S05P04A",
        "bma_name": "S05P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S06P01A",
        "bpc_name": "S06P01A",
        "bma_name": "S06P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S07P01A",
        "bpc_name": "S07P01A",
        "bma_name": "S07P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S07P02A",
        "bpc_name": "S07P02A",
        "bma_name": "S07P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S08P01A",
        "bpc_name": "S08P01A",
        "bma_name": "S08P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S11P01A",
        "bpc_name": "S11P01A",
        "bma_name": "S11P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S11P02C",
        "bpc_name": "S11P02C",
        "bma_name": "S11P02C",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S13P01A",
        "bpc_name": "S13P01A",
        "bma_name": "S13P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S13P01B",
        "bpc_name": "S13P01A",
        "bma_name": "S13P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S13P02A",
        "bpc_name": "S13P02A",
        "bma_name": "S13P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S13P03A",
        "bpc_name": "S13P03A",
        "bma_name": "S13P03A",
        "bpa_names": [None, None, None, None, "S13P03A5", None, None, None],
    },
    {
        "bpl_name": "S13P04A",
        "bpc_name": "S13P04A",
        "bma_name": "S13P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S13P04B",
        "bpc_name": "S13P04B",
        "bma_name": "S13P04B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S13P05A",
        "bpc_name": "S13P05A",
        "bma_name": "S13P05A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S13P06A",
        "bpc_name": "S13P06A",
        "bma_name": "S13P06A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S13P07A",
        "bpc_name": "S13P07A",
        "bma_name": "S13P07A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S13P08A",
        "bpc_name": "S13P08A",
        "bma_name": "S13P08A",
        "bpa_names": ["S13P08A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S13P09A",
        "bpc_name": "S13P09A",
        "bma_name": "S13P09A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S14P01A",
        "bpc_name": "S14P01A",
        "bma_name": "S14P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S15P01A",
        "bpc_name": "S15P01A",
        "bma_name": "S15P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S15P02A",
        "bpc_name": "S15P02A",
        "bma_name": "S15P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S15P03A",
        "bpc_name": "S15P03A",
        "bma_name": "S15P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S15P04A",
        "bpc_name": "S15P04A",
        "bma_name": "S15P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S15P05A",
        "bpc_name": "S15P05A",
        "bma_name": "S15P05A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S15P05B",
        "bpc_name": "S15P05B",
        "bma_name": "S15P05B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S17P01A",
        "bpc_name": "S17P01A",
        "bma_name": "S17P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S17P02A",
        "bpc_name": "S17P02A",
        "bma_name": "S17P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S20P01A",
        "bpc_name": "S20P01A",
        "bma_name": "S20P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S21P01A",
        "bpc_name": "S21P01A",
        "bma_name": "S21P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S99P01A",
        "bpc_name": "S99P01A",
        "bma_name": "S99P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S99P02A",
        "bpc_name": "S99P02A",
        "bma_name": "S99P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "S99P03A",
        "bpc_name": "S99P03A",
        "bma_name": "S99P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "T01P01A",
        "bpc_name": "T01P01A",
        "bma_name": "T01P01A",
        "bpa_names": [None, None, None, None, "T01P01A5", None, None, None],
    },
    {
        "bpl_name": "T01P02A",
        "bpc_name": "T01P02A",
        "bma_name": "T01P02A",
        "bpa_names": [None, None, None, None, "T01P02A5", None, None, None],
    },
    {
        "bpl_name": "T01P03A",
        "bpc_name": "T01P03A",
        "bma_name": "T01P03A",
        "bpa_names": ["T01P03A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "T01P03A2",
        "bpc_name": "T01P03A",
        "bma_name": "T01P03A2",
        "bpa_names": ["T01P03A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "T01P04A",
        "bpc_name": "T01P04A",
        "bma_name": "T01P04A",
        "bpa_names": ["T01P04A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V01P01A",
        "bpc_name": "V01P01A",
        "bma_name": "V01P01A",
        "bpa_names": ["V01P01A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V01P02A",
        "bpc_name": "V01P02A",
        "bma_name": "V01P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V01P03A",
        "bpc_name": "V01P03A",
        "bma_name": "V01P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V01P03B",
        "bpc_name": "V01P03B",
        "bma_name": "V01P03B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V01P03C",
        "bpc_name": "V01P03C",
        "bma_name": "V01P03C",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V01P04B",
        "bpc_name": "V01P04B",
        "bma_name": "V01P04B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V01P05B",
        "bpc_name": "V01P05B",
        "bma_name": "V01P05B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V01P06B",
        "bpc_name": "V01P06B",
        "bma_name": "V01P06B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V01P07B",
        "bpc_name": "V01P07B",
        "bma_name": "V01P07B",
        "bpa_names": ["V01P07B1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V01P08B",
        "bpc_name": "V01P08B",
        "bma_name": "V01P08B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V02P01A",
        "bpc_name": "V02P01A",
        "bma_name": "V02P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V02P02A",
        "bpc_name": "V02P02A",
        "bma_name": "V02P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V02P03A",
        "bpc_name": "V02P03A",
        "bma_name": "V02P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V02P06A",
        "bpc_name": "V02P06A",
        "bma_name": "V02P06A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V02P07A",
        "bpc_name": "V02P07A",
        "bma_name": "V02P07A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V02P08A",
        "bpc_name": "V02P08A",
        "bma_name": "V02P08A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P01A",
        "bpc_name": "V03P01A",
        "bma_name": "V03P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P02A",
        "bpc_name": "V03P02A",
        "bma_name": "V03P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P03A",
        "bpc_name": "V03P03A",
        "bma_name": "V03P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P04A",
        "bpc_name": "V03P04A",
        "bma_name": "V03P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P05C",
        "bpc_name": "V03P05C",
        "bma_name": "V03P05C",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P06A",
        "bpc_name": "V03P06A",
        "bma_name": "V03P06A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P06B",
        "bpc_name": "V03P06B",
        "bma_name": "V03P06B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P07A",
        "bpc_name": "V03P07A",
        "bma_name": "V03P07A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P08A",
        "bpc_name": "V03P08A",
        "bma_name": "V03P08A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P09A",
        "bpc_name": "V03P09A",
        "bma_name": "V03P09A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P11A",
        "bpc_name": "V03P11A",
        "bma_name": "V03P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P12A",
        "bpc_name": "V03P12A",
        "bma_name": "V03P12A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V03P13A",
        "bpc_name": "V03P13A",
        "bma_name": "V03P13A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V04P01A",
        "bpc_name": "V04P01A",
        "bma_name": "V04P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V04P02A",
        "bpc_name": "V04P02A",
        "bma_name": "V04P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V04P03A",
        "bpc_name": "V04P03A",
        "bma_name": "V04P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V05P01A",
        "bpc_name": "V05P01A",
        "bma_name": "V05P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V05P02A",
        "bpc_name": "V05P02A",
        "bma_name": "V05P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V05P03A",
        "bpc_name": "V05P03A",
        "bma_name": "V05P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V05P05A",
        "bpc_name": "V05P05A",
        "bma_name": "V05P05A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V09P01A",
        "bpc_name": "V09P01A",
        "bma_name": "V09P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V09P04A",
        "bpc_name": "V09P04A",
        "bma_name": "V09P04A",
        "bpa_names": ["V09P04A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V10P01C",
        "bpc_name": "V10P01C",
        "bma_name": "V10P01C",
        "bpa_names": ["V10P01C1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V10P03C",
        "bpc_name": "V10P03C",
        "bma_name": "V10P03C",
        "bpa_names": ["V10P03C1", None, None, None, "V10P03C5", None, None, None],
    },
    {
        "bpl_name": "V12P01A",
        "bpc_name": "V12P01A",
        "bma_name": "V12P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V13P01A",
        "bpc_name": "V13P01A",
        "bma_name": "V13P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V14P01A",
        "bpc_name": "V14P01A",
        "bma_name": "V14P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V14P03A",
        "bpc_name": "V14P03A",
        "bma_name": "V14P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V14P04A",
        "bpc_name": "V14P04A",
        "bma_name": "V14P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V15P01A",
        "bpc_name": "V15P01A",
        "bma_name": "V15P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V15P02A",
        "bpc_name": "V15P02A",
        "bma_name": "V15P02A",
        "bpa_names": [None, None, None, None, "V15P02A5", None, None, None],
    },
    {
        "bpl_name": "V15P03A",
        "bpc_name": "V15P03A",
        "bma_name": "V15P03A",
        "bpa_names": [None, None, None, None, "V15P03A5", None, None, None],
    },
    {
        "bpl_name": "V16P02A",
        "bpc_name": "V16P02A",
        "bma_name": "V16P02A",
        "bpa_names": ["V16P02A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V17P01A",
        "bpc_name": "V17P01A",
        "bma_name": "V17P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V17P02A",
        "bpc_name": "V17P02A",
        "bma_name": "V17P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V17P03A",
        "bpc_name": "V17P03A",
        "bma_name": "V17P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V19P01A",
        "bpc_name": "V19P01A",
        "bma_name": "V19P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V19P02A",
        "bpc_name": "V19P02A",
        "bma_name": "V19P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V19P03A",
        "bpc_name": "V19P03A",
        "bma_name": "V19P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V19P04A",
        "bpc_name": "V19P04A",
        "bma_name": "V19P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V19P05A",
        "bpc_name": "V19P05A",
        "bma_name": "V19P05A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V19P06A",
        "bpc_name": "V19P06A",
        "bma_name": "V19P06A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V21P01A",
        "bpc_name": "V21P01A",
        "bma_name": "V21P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V21P02A",
        "bpc_name": "V21P02A",
        "bma_name": "V21P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V21P02B",
        "bpc_name": "V21P02B",
        "bma_name": "V21P02B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V22P01A",
        "bpc_name": "V22P01A",
        "bma_name": "V22P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V22P02A",
        "bpc_name": "V22P02A",
        "bma_name": "V22P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V22P03A",
        "bpc_name": "V22P03A",
        "bma_name": "V22P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V23P01A",
        "bpc_name": "V23P01A",
        "bma_name": "V23P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V23P04A",
        "bpc_name": "V23P04A",
        "bma_name": "V23P04A",
        "bpa_names": [None, None, None, None, "V23P04A5", None, None, None],
    },
    {
        "bpl_name": "V23P05A",
        "bpc_name": "V23P05A",
        "bma_name": "V23P05A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V24P01A",
        "bpc_name": "V24P01A",
        "bma_name": "V24P01A",
        "bpa_names": [None, None, None, None, "V24P01A5", None, None, None],
    },
    {
        "bpl_name": "V24P02A",
        "bpc_name": "V24P02A",
        "bma_name": "V24P02A",
        "bpa_names": [None, None, None, None, "V24P02A5", None, None, None],
    },
    {
        "bpl_name": "V24P03A",
        "bpc_name": "V24P03A",
        "bma_name": "V24P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V24P04A",
        "bpc_name": "V24P04A",
        "bma_name": "V24P04A",
        "bpa_names": ["V24P04A1", None, None, None, "V24P04A5", None, None, None],
    },
    {
        "bpl_name": "V24P05A",
        "bpc_name": "V24P05A",
        "bma_name": "V24P05A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V24P06A",
        "bpc_name": "V24P06A",
        "bma_name": "V24P06A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V24P07A",
        "bpc_name": "V24P07A",
        "bma_name": "V24P07A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V24P08A",
        "bpc_name": "V24P08A",
        "bma_name": "V24P08A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V24P09A",
        "bpc_name": "V24P09A",
        "bma_name": "V24P09A",
        "bpa_names": ["V24P09A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V25P01A",
        "bpc_name": "V25P01A",
        "bma_name": "V25P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V25P02A",
        "bpc_name": "V25P02A",
        "bma_name": "V25P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V25P03A",
        "bpc_name": "V25P03A",
        "bma_name": "V25P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V25P04A",
        "bpc_name": "V25P04A",
        "bma_name": "V25P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V26P01A",
        "bpc_name": "V26P01A",
        "bma_name": "V26P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V26P02A",
        "bpc_name": "V26P02A",
        "bma_name": "V26P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V26P03A",
        "bpc_name": "V26P03A",
        "bma_name": "V26P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V26P04A",
        "bpc_name": "V26P04A",
        "bma_name": "V26P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V26P05A",
        "bpc_name": "V26P05A",
        "bma_name": "V26P05A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V26P06A",
        "bpc_name": "V26P06A",
        "bma_name": "V26P06A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V26P07A",
        "bpc_name": "V26P07A",
        "bma_name": "V26P07A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V26P09A",
        "bpc_name": "V26P09A",
        "bma_name": "V26P09A",
        "bpa_names": ["V26P09A1", None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V26P10A",
        "bpc_name": "V26P10A",
        "bma_name": "V26P10A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V26P11A",
        "bpc_name": "V26P11A",
        "bma_name": "V26P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V28P01A",
        "bpc_name": "V28P01A",
        "bma_name": "V28P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V31P01A",
        "bpc_name": "V31P01A",
        "bma_name": "V31P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V31P02A",
        "bpc_name": "V31P02A",
        "bma_name": "V31P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V32P01A",
        "bpc_name": "V32P01A",
        "bma_name": "V32P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V33P01A",
        "bpc_name": "V33P01A",
        "bma_name": "V33P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V34P01A",
        "bpc_name": "V34P01A",
        "bma_name": "V34P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V37P01A",
        "bpc_name": "V37P01A",
        "bma_name": "V37P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V37P02A",
        "bpc_name": "V37P02A",
        "bma_name": "V37P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V37P03A",
        "bpc_name": "V37P03A",
        "bma_name": "V37P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P01A",
        "bpc_name": "V38P01A",
        "bma_name": "V38P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P02A",
        "bpc_name": "V38P02A",
        "bma_name": "V38P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P03A",
        "bpc_name": "V38P03A",
        "bma_name": "V38P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P04A",
        "bpc_name": "V38P04A",
        "bma_name": "V38P04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P05A",
        "bpc_name": "V38P05A",
        "bma_name": "V38P05A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P06A",
        "bpc_name": "V38P06A",
        "bma_name": "V38P06A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P06C",
        "bpc_name": "V38P06C",
        "bma_name": "V38P06C",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P06D",
        "bpc_name": "V38P06D",
        "bma_name": "V38P06D",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P07A",
        "bpc_name": "V38P07A",
        "bma_name": "V38P07A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P08A",
        "bpc_name": "V38P08A",
        "bma_name": "V38P08A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P09A",
        "bpc_name": "V38P09A",
        "bma_name": "V38P09A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P10A",
        "bpc_name": "V38P10A",
        "bma_name": "V38P10A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V38P11A",
        "bpc_name": "V38P11A",
        "bma_name": "V38P11A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V39P01A",
        "bpc_name": "V39P01A",
        "bma_name": "V39P01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V39P02A",
        "bpc_name": "V39P02A",
        "bma_name": "V39P02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "V39P03A",
        "bpc_name": "V39P03A",
        "bma_name": "V39P03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "W00",
        "bpc_name": "W00",
        "bma_name": "W00",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "W01A",
        "bpc_name": "W01A",
        "bma_name": "W01A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "W01B",
        "bpc_name": "W01B",
        "bma_name": "W01B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "W02A",
        "bpc_name": "W02A",
        "bma_name": "W02A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "W02B",
        "bpc_name": "W02B",
        "bma_name": "W02B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "W03A",
        "bpc_name": "W03A",
        "bma_name": "W03A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "W03B",
        "bpc_name": "W03B",
        "bma_name": "W03B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "W04A",
        "bpc_name": "W04A",
        "bma_name": "W04A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "W04B",
        "bpc_name": "W04B",
        "bma_name": "W04B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "W05A",
        "bpc_name": "W05A",
        "bma_name": "W05A",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "W05B",
        "bpc_name": "W05B",
        "bma_name": "W05B",
        "bpa_names": [None, None, None, None, None, None, None, None],
    },
    {
        "bpl_name": "COCO",
        "bpc_name": "COCO",
        "bma_name": "COCO",
        "bpa_names": [None, "COCO2", None, None, None, None, None, None],
    },
]


class BgListDatTestCase(SkyTempleFilesTestCase[BgListDatHandler, BgListProtocol[BgListEntryProtocol]]):
    handler = BgListDatHandler

    def setUp(self) -> None:
        self.bg_list = self._load_main_fixture(self._fix_path_bg_list())
        self.assertIsNotNone(self.bg_list)

    def test_read(self) -> None:
        self.assertEqual(FIXTURE_REPR, self.format_list(self.bg_list))

    def test_write(self) -> None:
        expected = FIXTURE_REPR[:]
        # Add one new entry C2
        mdl = self.handler.get_entry_model_cls()(
            "C2_BPL",
            "C2_BPC",
            "C2_BMA",
            [
                "C2_BPA1",
                "C2_BPA2",
                "C2_BPA3",
                "C2_BPA4",
                None,
                "C2_BPA6",
                "C2_BPA7",
                "C2_BPA8",
            ],
        )
        with mutate_sequence(self.bg_list, "level") as entry:
            entry.append(mdl)
        expected.append(self.format_entry(mdl))  # type: ignore
        # Remove first entry
        with mutate_sequence(self.bg_list, "level") as entry:
            entry.pop(0)
        expected.pop(0)
        # Change third entry
        self.bg_list.level[2].bma_name = "THRD_BMA"
        with mutate_sequence(self.bg_list.level[2], "bpa_names") as entry:
            entry[1] = "12345678"
        expected[2]["bma_name"] = "THRD_BMA"  # type: ignore
        expected[2]["bpa_names"][1] = "12345678"  # type: ignore
        self.assertEqual(expected, self.format_list(self.bg_list))
        new_bg_list = self._save_and_reload_main_fixture(self.bg_list)
        self.assertEqual(expected, self.format_list(new_bg_list))

    def test_write_too_long_bpc(self) -> None:
        self.bg_list.level[0].bpc_name = "Way too long"
        with self.assertRaises(ValueError):
            self._save_and_reload_main_fixture(self.bg_list)

    def test_write_too_long_bpl(self) -> None:
        self.bg_list.level[0].bpl_name = "123456789"
        with self.assertRaises(ValueError):
            self._save_and_reload_main_fixture(self.bg_list)

    def test_write_too_long_bma(self) -> None:
        self.bg_list.level[0].bma_name = "Way too long"
        with self.assertRaises(ValueError):
            self._save_and_reload_main_fixture(self.bg_list)

    def test_write_too_long_bpa(self) -> None:
        with mutate_sequence(self.bg_list.level[0], "bpa_names") as entry:
            entry[0] = "Way too long"
        with self.assertRaises(ValueError):
            self._save_and_reload_main_fixture(self.bg_list)

    def test_get_bpl(self) -> None:
        self.assertIsInstance(self.bg_list.level[-1].get_bpl(self._fix_path_common()), BplProtocol)

    def test_get_bpl_rom_file_provider(self) -> None:
        self.assertIsInstance(self.bg_list.level[-1].get_bpl(RomFileProviderStub()), BplProtocol)

    def test_get_bpc(self) -> None:
        self.assertIsInstance(self.bg_list.level[-1].get_bpc(self._fix_path_common()), BpcProtocol)

    def test_get_bpc_rom_file_provider(self) -> None:
        self.assertIsInstance(self.bg_list.level[-1].get_bpc(RomFileProviderStub()), BpcProtocol)

    def test_get_bma(self) -> None:
        self.assertIsInstance(self.bg_list.level[-1].get_bma(self._fix_path_common()), BmaProtocol)

    def test_get_bma_rom_file_provider(self) -> None:
        self.assertIsInstance(self.bg_list.level[-1].get_bma(RomFileProviderStub()), BmaProtocol)

    def test_get_bpas(self) -> None:
        result = self.bg_list.level[-1].get_bpas(self._fix_path_common())
        self.assertIsInstance(result, list)
        self.assertEqual(8, len(result))
        self.assertIsNone(result[0])
        self.assertIsInstance(result[1], BpaProtocol)
        self.assertIsNone(result[2])
        self.assertIsNone(result[3])
        self.assertIsNone(result[4])
        self.assertIsNone(result[5])
        self.assertIsNone(result[6])
        self.assertIsNone(result[7])

    def test_get_bpas_rom_file_provider(self) -> None:
        result = self.bg_list.level[-1].get_bpas(RomFileProviderStub())
        self.assertIsInstance(result, list)
        self.assertEqual(8, len(result))
        self.assertIsNone(result[0])
        self.assertIsInstance(result[1], BpaProtocol)
        self.assertIsNone(result[2])
        self.assertIsNone(result[3])
        self.assertIsNone(result[4])
        self.assertIsNone(result[5])
        self.assertIsNone(result[6])
        self.assertIsNone(result[7])

    def test_find_bma(self) -> None:
        mdl = self.handler.get_entry_model_cls()(
            "C2_BPL",
            "C2_BPC",
            "COCO",
            [
                "C2_BPA1",
                "C2_BPA2",
                "C2_BPA3",
                "C2_BPA4",
                None,
                "C2_BPA6",
                "C2_BPA7",
                "C2_BPA8",
            ],
        )
        with mutate_sequence(self.bg_list, "level") as entry:
            entry.append(mdl)
        self.assertEqual(1, self.bg_list.find_bma("G01P01A"))
        self.assertEqual(0, self.bg_list.find_bma("nope"))
        self.assertEqual(2, self.bg_list.find_bma("COCO"))

    def test_find_bpl(self) -> None:
        mdl = self.handler.get_entry_model_cls()(
            "COCO",
            "C2_BPC",
            "C2_BMA",
            [
                "C2_BPA1",
                "C2_BPA2",
                "C2_BPA3",
                "C2_BPA4",
                None,
                "C2_BPA6",
                "C2_BPA7",
                "C2_BPA8",
            ],
        )
        with mutate_sequence(self.bg_list, "level") as entry:
            entry.append(mdl)
        self.assertEqual(1, self.bg_list.find_bpl("G01P01A"))
        self.assertEqual(0, self.bg_list.find_bpl("nope"))
        self.assertEqual(2, self.bg_list.find_bpl("COCO"))

    def test_find_bpc(self) -> None:
        self.assertEqual(1, self.bg_list.find_bpc("COCO"))
        self.assertEqual(0, self.bg_list.find_bpc("nope"))
        self.assertEqual(2, self.bg_list.find_bpc("G01P01A"))

    def test_find_bpa(self) -> None:
        self.assertEqual(2, self.bg_list.find_bpa("G01P01A1"))
        self.assertEqual(0, self.bg_list.find_bpa("nope"))
        self.assertEqual(1, self.bg_list.find_bpa("COCO2"))

    @romtest(file_ext="dat", path="MAP_BG/")
    def test_using_rom(self, _, file):
        bg_list_dat_before = self.handler.deserialize(file)
        bg_list_dat_after = self._save_and_reload_main_fixture(bg_list_dat_before)

        for idx, (entry_before, entry_after) in enumerate(zip(bg_list_dat_before.level, bg_list_dat_after.level)):
            self.assertEqual(entry_before.bma_name, entry_after.bma_name)
            self.assertEqual(entry_before.bpa_names, entry_after.bpa_names)
            self.assertEqual(entry_before.bpl_name, entry_after.bpl_name)
            self.assertEqual(entry_before.bpc_name, entry_after.bpc_name)

    @no_type_check
    @classmethod
    @fixpath
    def _fix_path_bg_list(cls) -> str:
        return "fixtures", "bg_list.dat"

    @staticmethod
    def _fix_path_common() -> str:
        return os.path.join(os.path.dirname(__file__), "..", "fixtures")

    @classmethod
    def format_list(cls, ldat: BgListProtocol) -> List[Dict[str, Union[str, Sequence[Optional[str]]]]]:
        return [cls.format_entry(x) for x in ldat.level]

    @staticmethod
    def format_entry(
        entry: BgListEntryProtocol,
    ) -> Dict[str, Union[str, Sequence[Optional[str]]]]:
        return {
            "bpl_name": entry.bpl_name,
            "bpc_name": entry.bpc_name,
            "bma_name": entry.bma_name,
            "bpa_names": entry.bpa_names,
        }
