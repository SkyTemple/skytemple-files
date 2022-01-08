#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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
from dataclasses import dataclass
from typing import Sequence, List

from PIL import Image

from skytemple_files.graphics.bpa.protocol import BpaProtocol, BpaFrameInfoProtocol


thisdir = os.path.dirname(__file__)


# Testing mock class
class BpaFrameInfoMock(BpaFrameInfoProtocol):
    def __init__(self, duration_per_frame: int, unk2: int):
        self._duration_per_frame = duration_per_frame
        self._unk2 = unk2

    # Properties; because the mock only supports reading!
    @property
    def duration_per_frame(self) -> int:  # type: ignore
        return self._duration_per_frame

    @property
    def unk2(self) -> int:  # type: ignore
        return self._unk2


# Testing mock class
@dataclass
class BpaMock(BpaProtocol[BpaFrameInfoMock]):
    def __init__(self, data: bytes):
        self.stub_init_data = data
        self._number_of_tiles: int = 12
        self._number_of_frames: int = 6
        self._tiles: List[bytes] = [bytes(b'\xaa\xbb\xba\xaa*\xaa\xaa\xab\xba\xba\xba:\xba\xab\xab\xba\xaa\xbb\xaa;*\xba\xaa\xbb\xa2\xa3\xb3\xb3\xa3\xaa\xab:'), bytes(b'\xa3\xaa\xaa\xba;\xaa\xbb\xbb\xbb\xab\xbb3\xbb3\xba\xa3;\xbb\xa3\xab\xbb3;237#\xa23;#\xac'), bytes(b'wwwwwwwwwwwwwwwwwwwwwwwwswwwswww'), bytes(b'\xba\xaa\xa3:\xaa\xab\xba\xa3\xaa*\xaa\xba\xbb\xaa\xaa\xba\xab+\xaa\xba\xab\xba\xaa\xa2\xbb\xab\xab\xaa3\xbb\xaa\xaa'), bytes(b'\xb3s#,;7\'\xcc;w\'\xcc37\xa3\xcc3\xb3+\xc2\xba\xbb\xab\xcc\xbb3*\xc2\xba\xb3"\xcc'), bytes(b'wwwwwww7uw\xb77sw73{w\xb3\xbbsw\xaa\xbbu7\xbb\xbb5s\xa3\xba'), bytes(b'3\xbb\xab\xaaw:\xab\xaa;\xbb\xa3\xaaw\xba\xbb[s333z7;\xbawS\xaass\xa3\xaa\xbb'), bytes(b'\xa2*\xc2\xcc\xa2""\xcc"\xa2\xcc\xccRR\xc5\\"\xc2\xcc\xcc*\xc2\xcc\xcc\xa7\xc2\xcc\xcc\'\xc5\xcc\xcc'), bytes(b'2\xb7\xaa\xaa\xb2\xbb\xaa\xaa\xa2\xab+\xaa"\xaa\xaa\xaa"\xa2"\xaa,"\xaa\xa2\xac"\xa2""*\xaa\xa2'), bytes(b'3\xba7:;w;\xb3{w7733ws;3s\xba\xaa\xaa\xba\xa5\xa5\xaa\xa5\xaaUUZ\xaa'), bytes(b'w\xc5\xcc%w\xcc\\"\xaaR,"*""""""""""""\xa2","""\xc2'), bytes(b'**\xa2\xaa\xa2\xa2\xaa*""""*""""\xc2""\xc2\xcc""",,"""""'), bytes(b'\xaa\xbb\xba\xaa*\xaa\xaa\xab\xba\xba\xba:\xba\xab\xab\xba\xaa\xbb\xaa;*\xba\xaa\xbb\xa2\xa3\xb3\xb3\xa3\xaa\xab:'), bytes(b'\xa3\xaa\xaa\xba;\xaa\xbb\xbb\xbb\xab\xbb3\xbb3\xba\xa3;\xbb\xb3;\xbb\xb3\xb3{3\xb7\xb3{3;Z\xb2'), bytes(b'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'), bytes(b'\xba\xaa\xa3:\xaa\xab\xba\xa3\xaa*\xaa\xba\xbb\xaa\xaa\xba\xab+\xaa\xba\xab\xba\xaa\xa2\xbb\xab\xab\xaa3\xbb\xaa\xaa'), bytes(b"\xb3\xb3\xc5\xb2;\xb7\xc5\xb2;w\'\xcc37S\xc53\xb3[\xcc\xba\xbbU\xcc\xbb3\xcc\xcc\xba\xb3\xcc\xcc"), bytes(b'wwwwwww7uw\xb77sw73{w\xb3\xbb|w\xaa\xbb|7\xbb\xbb<s\xa3\xba'), bytes(b'3\xbb\xab\xaaw:\xab\xaa;\xbb\xa3\xaaw\xba\xbb[s333z7;\xbawS\xaass\xa3\xaa\xbb'), bytes(b'\xa2*\xcc\xcc\xa2"\xcc\xcc"\xc2\xcc\xccR\xc2\xcc\xcc"\xc2\xcc\xcc*\xc2\xcc\xcc\xa7\xc2\xcc\xcc\'\xc5\xcc\xcc'), bytes(b'<\xb7\xaa\xaa\xbc\xbb\xaa\xaa\xac\xab+\xaa,\xaa\xaa\xaa,\xa2"\xaa,"\xaa\xa2\xac"\xa2""*\xaa\xa2'), bytes(b'3\xba7:;w;\xb3{w7733ws;3s\xba\xaa\xaa\xba\xa5\xa5\xaa\xa5\xaaUUZ\xaa'), bytes(b'w\xc5\xcc,w\xcc\xcc"\xaaR,"*""""""""""""\xa2","""\xc2'), bytes(b'**\xa2\xaa\xa2\xa2\xaa*""""*""""\xc2""\xc2\xcc""",,"""""'), bytes(b'\xaa\xbb\xba\xaa*\xaa\xaa\xab\xba\xba\xba:\xba\xab\xab\xba\xaa\xbb\xaa;*\xba\xaa\xbb\xa2\xa3\xb3\xb3\xa3\xaa\xab:'), bytes(b'\xa3\xaa\xaa\xba;\xaa\xbb\xbb\xbb\xab\xbb3\xbb3\xba\xa3;\xbb\xb3;\xbb3;;373\xbb3;#\xac'), bytes(b'wwwwwwwwwwwwwwwwwwwwwwwwwwwwswww'), bytes(b'\xba\xaa\xa3:\xaa\xab\xba\xa3\xaa*\xaa\xba\xbb\xaa\xaa\xba\xab+\xaa\xba\xab\xba\xaa\xa2\xbb\xab\xab\xaa3\xbb\xaa\xaa'), bytes(b'\xb3s\xa3%;7[,;w\xcc\\3\xb7U\xc53\xb3R\xcc\xba+U\xcc\xbbR\xcc\xcc\xaa"\xcc\xcc'), bytes(b'{www{ww7zw\xb77\xa5w73,w\xb3\xbb\xccw\xaa\xbb\xcc3\xbb\xbb\xccz\xa3\xba'), bytes(b'3\xbb\xab\xaaw:\xab\xaa;\xbb\xa3\xaaw\xba\xbb+s33#z7;\xbawS\xaass\xa3\xaa\xbb'), bytes(b'"U\xcc\xcc\xa2\xcc\xcc\xcc"\xc5\xcc\xcc\xc2\xcc\xcc\xcc"\xcc\xcc\xcc*\xcc\xcc\xcc+\xc5\xcc\xcc+\xc5\xcc\xcc'), bytes(b'\xcc\xb2\xaa\xaa\xcc\xb2\xaa\xaa\xcc\xa2+\xaa\xcc\xa5\xaa\xaa\xcc""\xaa\\"\xaa\xa2\\"\xa2""*\xaa\xa2'), bytes(b'3\xba7:;w;\xb3{w7733ws;3s\xba\xaa\xaa\xba\xa5\xa5\xaa\xa5\xaaUUZ\xaa'), bytes(b'\xa7\xc5\xcc\xccw\xc2\xcc"\xaa"%"*""""""""""""\xa2","""\xc2'), bytes(b'**\xa2\xaa\xa2\xa2\xaa*""""*""""\xc2""\xc2\xcc""",,"""""'), bytes(b'\xaa\xbb\xba\xaa*\xaa\xaa\xab\xba\xba\xba:\xba\xab\xab\xba\xaa\xbb\xaa;*\xba\xaa\xbb\xa2\xa3\xb3\xb3\xa3\xaa\xab:'), bytes(b'\xa3\xaa\xaa\xba;\xaa\xbb\xbb\xbb\xab\xbb3\xbb3\xba\xa3;\xbb\xb3;\xbb3;;373\xbb3;#\xac'), bytes(b'wwwwwwwwwwwwwwwwwwwwwwwwwwwwswww'), bytes(b'\xba\xaa\xa3:\xaa\xab\xba\xa3\xaa*\xaa\xba\xbb\xaa\xaa\xba\xab+\xaa\xba\xab\xba\xaa\xa2\xbb\xab\xab\xaa3\xbb\xaa\xaa'), bytes(b'\xb3s\xa3%;7[,;w\xcc\\3\xb7U\xc53\xb3R\xcc\xba+U\xcc\xbbR\xcc\xcc\xaa"\xcc\xcc'), bytes(b'{www{ww7zw\xb77\xa5w73,w\xb3\xbb\xccw\xaa\xbb\xcc3\xbb\xbb\xccz\xa3\xba'), bytes(b'3\xbb\xab\xaaw:\xab\xaa;\xbb\xa3\xaaw\xba\xbb+s33#z7;\xbawS\xaass\xa3\xaa\xbb'), bytes(b'"U\xcc\xcc\xa2\xcc\xcc\xcc"\xc5\xcc\xcc\xc2\xcc\xcc\xcc"\xcc\xcc\xcc*\xcc\xcc\xcc+\xc5\xcc\xcc+\xc5\xcc\xcc'), bytes(b'\xcc\xb2\xaa\xaa\xcc\xb2\xaa\xaa\xcc\xa2+\xaa\xcc\xa5\xaa\xaa\xcc""\xaa\\"\xaa\xa2\\"\xa2""*\xaa\xa2'), bytes(b'3\xba7:;w;\xb3{w7733ws;3s\xba\xaa\xaa\xba\xa5\xa5\xaa\xa5\xaaUUZ\xaa'), bytes(b'\xa7\xc5\xcc\xccw\xc2\xcc"\xaa"%"*""""""""""""\xa2","""\xc2'), bytes(b'**\xa2\xaa\xa2\xa2\xaa*""""*""""\xc2""\xc2\xcc""",,"""""'), bytes(b'\xaa\xbb\xba\xaa*\xaa\xaa\xab\xba\xba\xba:\xba\xab\xab\xba\xaa\xbb\xaa;*\xba\xaa\xbb\xa2\xa3\xb3\xb3\xa3\xaa\xab:'), bytes(b'\xa3\xaa\xaa\xba;\xaa\xbb\xbb\xbb\xab\xbb3\xbb3\xba\xa3;\xbb\xb3;\xbb\xb3\xb3{3\xb7\xb3{3;Z\xb2'), bytes(b'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'), bytes(b'\xba\xaa\xa3:\xaa\xab\xba\xa3\xaa*\xaa\xba\xbb\xaa\xaa\xba\xab+\xaa\xba\xab\xba\xaa\xa2\xbb\xab\xab\xaa3\xbb\xaa\xaa'), bytes(b"\xb3\xb3\xc5\xb2;\xb7\xc5\xb2;w\'\xcc37S\xc53\xb3[\xcc\xba\xbbU\xcc\xbb3\xcc\xcc\xba\xb3\xcc\xcc"), bytes(b'wwwwwww7uw\xb77sw73{w\xb3\xbb|w\xaa\xbb|7\xbb\xbb<s\xa3\xba'), bytes(b'3\xbb\xab\xaaw:\xab\xaa;\xbb\xa3\xaaw\xba\xbb[s333z7;\xbawS\xaass\xa3\xaa\xbb'), bytes(b'\xa2*\xcc\xcc\xa2"\xcc\xcc"\xc2\xcc\xccR\xc2\xcc\xcc"\xc2\xcc\xcc*\xc2\xcc\xcc\xa7\xc2\xcc\xcc\'\xc5\xcc\xcc'), bytes(b'<\xb7\xaa\xaa\xbc\xbb\xaa\xaa\xac\xab+\xaa,\xaa\xaa\xaa,\xa2"\xaa,"\xaa\xa2\xac"\xa2""*\xaa\xa2'), bytes(b'3\xba7:;w;\xb3{w7733ws;3s\xba\xaa\xaa\xba\xa5\xa5\xaa\xa5\xaaUUZ\xaa'), bytes(b'w\xc5\xcc,w\xcc\xcc"\xaaR,"*""""""""""""\xa2","""\xc2'), bytes(b'**\xa2\xaa\xa2\xa2\xaa*""""*""""\xc2""\xc2\xcc""",,"""""'), bytes(b'\xaa\xbb\xba\xaa*\xaa\xaa\xab\xba\xba\xba:\xba\xab\xab\xba\xaa\xbb\xaa;*\xba\xaa\xbb\xa2\xa3\xb3\xb3\xa3\xaa\xab:'), bytes(b'\xa3\xaa\xaa\xba;\xaa\xbb\xbb\xbb\xab\xbb3\xbb3\xba\xa3;\xbb\xa3\xab\xbb3;237#\xa23;#\xac'), bytes(b'wwwwwwwwwwwwwwwwwwwwwwwwswwwswww'), bytes(b'\xba\xaa\xa3:\xaa\xab\xba\xa3\xaa*\xaa\xba\xbb\xaa\xaa\xba\xab+\xaa\xba\xab\xba\xaa\xa2\xbb\xab\xab\xaa3\xbb\xaa\xaa'), bytes(b'\xb3s#,;7\'\xcc;w\'\xcc37\xa3\xcc3\xb3+\xc2\xba\xbb\xab\xcc\xbb3*\xc2\xba\xb3"\xcc'), bytes(b'wwwwwww7uw\xb77sw73{w\xb3\xbbsw\xaa\xbbu7\xbb\xbb5s\xa3\xba'), bytes(b'3\xbb\xab\xaaw:\xab\xaa;\xbb\xa3\xaaw\xba\xbb[s333z7;\xbawS\xaass\xa3\xaa\xbb'), bytes(b'\xa2*\xc2\xcc\xa2""\xcc"\xa2\xcc\xccRR\xc5\\"\xc2\xcc\xcc*\xc2\xcc\xcc\xa7\xc2\xcc\xcc\'\xc5\xcc\xcc'), bytes(b'2\xb7\xaa\xaa\xb2\xbb\xaa\xaa\xa2\xab+\xaa"\xaa\xaa\xaa"\xa2"\xaa,"\xaa\xa2\xac"\xa2""*\xaa\xa2'), bytes(b'3\xba7:;w;\xb3{w7733ws;3s\xba\xaa\xaa\xba\xa5\xa5\xaa\xa5\xaaUUZ\xaa'), bytes(b'w\xc5\xcc%w\xcc\\"\xaaR,"*""""""""""""\xa2","""\xc2'), bytes(b'**\xa2\xaa\xa2\xa2\xaa*""""*""""\xc2""\xc2\xcc""",,"""""')]
        self._frame_info: List[BpaFrameInfoMock] = [
            BpaFrameInfoMock(5, 0),
            BpaFrameInfoMock(5, 0),
            BpaFrameInfoMock(10, 0),
            BpaFrameInfoMock(10, 0),
            BpaFrameInfoMock(5, 0),
            BpaFrameInfoMock(5, 0)
        ]

    # Properties; because the mock only supports reading!
    @property
    def number_of_tiles(self) -> int:  # type: ignore
        return self._number_of_tiles

    def mock__set_number_of_tiles(self, val: int):
        self._number_of_tiles = val

    @property
    def number_of_frames(self) -> int:  # type: ignore
        return self._number_of_frames

    @property
    def tiles(self) -> List[bytearray]:  # type: ignore
        return self._tiles  # type: ignore

    @property
    def frame_info(self) -> List[BpaFrameInfoMock]:  # type: ignore
        return self._frame_info

    def get_tile(self, tile_idx: int, frame_idx: int) -> bytes:
        raise NotImplementedError("Not implemented on mock.")

    def tiles_to_pil_separate(self, palette: List[int], width_in_tiles: int = 20) -> List[Image.Image]:
        from skytemple_files.graphics.test.mocks.bpl_mock import BplMock
        bpl_palettes = BplMock(bytes()).palettes
        for pal_id, bpl_palette in bpl_palettes:
            if palette == bpl_palette and width_in_tiles == 1:
                return [
                    Image.open(os.path.join(thisdir, 'data', 'bpa', f'tiles_to_pil_separate_pal_{pal_id}_wim_1_0.png')),
                    Image.open(os.path.join(thisdir, 'data', 'bpa', f'tiles_to_pil_separate_pal_{pal_id}_wim_1_1.png')),
                    Image.open(os.path.join(thisdir, 'data', 'bpa', f'tiles_to_pil_separate_pal_{pal_id}_wim_1_2.png')),
                    Image.open(os.path.join(thisdir, 'data', 'bpa', f'tiles_to_pil_separate_pal_{pal_id}_wim_1_3.png')),
                    Image.open(os.path.join(thisdir, 'data', 'bpa', f'tiles_to_pil_separate_pal_{pal_id}_wim_1_4.png')),
                    Image.open(os.path.join(thisdir, 'data', 'bpa', f'tiles_to_pil_separate_pal_{pal_id}_wim_1_5.png')),
                ]
        raise NotImplementedError("Invalid / unknown configuration for mock.")

    def pil_to_tiles(self, image: Image.Image) -> None:
        raise NotImplementedError("Not implemented on mock.")

    def pil_to_tiles_separate(self, images: List[Image.Image]) -> None:
        raise NotImplementedError("Not implemented on mock.")

    def tiles_for_frame(self, frame: int) -> Sequence[bytearray]:
        return self.tiles[frame * self.number_of_tiles:]


def _generate_mock_data():
    """Generate mock data using the assumed working implementation."""
    from skytemple_files.common.types.file_types import FileType
    from skytemple_files.graphics.test.mocks.bpl_mock import BplMock
    with open('../fixtures/MAP_BG/coco2.bpa', 'rb') as f:
        bpa = FileType.BPA.deserialize(f.read())

    for animation_spec in bpa.frame_info:
        print(f"BpaFrameInfoMock({animation_spec.duration_per_frame}, {animation_spec.unk2})")

    print(f"self._number_of_tiles: int = {bpa.number_of_tiles}")
    print(f"self._number_of_frames: int = {bpa.number_of_frames}")
    print(f"self._tiles: List[bytearray = {bpa.tiles}")

    for pal_id, pal in enumerate(BplMock(bytes()).palettes):
        for i, img in enumerate(bpa.tiles_to_pil_separate(pal, 1)):
            img.save(f'data/bpa/tiles_to_pil_separate_pal_{pal_id}_wim_1_{i}.png')


if __name__ == '__main__':
    _generate_mock_data()
