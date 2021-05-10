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

import os
from tempfile import NamedTemporaryFile

from ndspy.rom import NintendoDSRom

from skytemple_files.audio.swdl.wavi import SampleFormatConsts
from skytemple_files.common.util import get_files_from_rom_with_extension
from skytemple_files.audio.swdl.handler import SwdlHandler

def run(cmd):
    print(f'> {cmd}')
    os.system(cmd)

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
output_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')
os.makedirs(output_dir, exist_ok=True)
rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

for filename in get_files_from_rom_with_extension(rom, 'swd'):
    print(filename)
    model = SwdlHandler.deserialize(rom.getFileByName(filename))
    #print(model)

    for i, smpl in enumerate(model.wavi.sample_info_table):
        if smpl is not None and smpl.sample is not None:
            with NamedTemporaryFile(mode='wb') as f:
                if smpl.sample_format == SampleFormatConsts.ADPCM_4BIT:
                    f.write(smpl.sample)
                else:
                    f.write(smpl.sample)
                f.flush()
                out_fname = os.path.join(output_dir, filename.replace('/', '_') + '_' + str(i) + '.wav')
                if smpl.sample_format == SampleFormatConsts.ADPCM_4BIT:
                    run(f'sox -t ima -r {smpl.sample_rate} -e ima-adpcm {f.name} -e signed-integer -b 16 {out_fname}')
                elif smpl.sample_format == SampleFormatConsts.PCM_8BIT:
                    pass#run(f'sox -t s8 -c 1 -r {smpl.sample_rate} -e signed-integer {f.name} -e signed-integer -b 16 {out_fname}')
                elif smpl.sample_format == SampleFormatConsts.PCM_16BIT:
                    pass#run(f'sox -t s16 -c 1 -r {smpl.sample_rate} -e signed-integer {f.name} -e signed-integer -b 16 {out_fname}')
                else:
                    print(f"Unknown format: 0x{smpl.sample_format:0x}")
