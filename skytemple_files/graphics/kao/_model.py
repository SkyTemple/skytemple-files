#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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

import math
import warnings
from collections.abc import Iterator
from typing import Optional, Tuple, List, Union, Dict

from PIL import Image
from range_typed_integers import i32

from skytemple_files.common.i18n_util import _, f
from skytemple_files.common.util import (
    iter_bytes_4bit_le,
    read_i32,
    read_bytes,
    write_i32,
    simple_quant,
    read_u32,
)
from skytemple_files.compression_container.common_at.handler import (
    COMMON_AT_MUST_COMPRESS_3,
    CommonAtType,
)
from skytemple_files.graphics.kao import (
    KAO_IMG_IMG_DIM,
    KAO_IMG_METAPIXELS_DIM,
    KAO_IMG_PAL_B_SIZE,
    SUBENTRIES,
    SUBENTRY_LEN,
)
from skytemple_files.graphics.kao.protocol import KaoImageProtocol, KaoProtocol


class KaoImage(KaoImageProtocol):
    def __init__(self, whole_kao_data: bytes, start_pnt: int):
        if not isinstance(whole_kao_data, memoryview):
            whole_kao_data = memoryview(whole_kao_data)

        """Construct a KaoImage using a raw image buffer (16 color palette, followed by AT)"""
        from skytemple_files.common.types.file_types import FileType

        cont_len = FileType.COMMON_AT.cont_size(
            whole_kao_data, start_pnt + KAO_IMG_PAL_B_SIZE
        )
        # palette size + at container size
        self.original_size = KAO_IMG_PAL_B_SIZE + cont_len
        self.pal_data = read_bytes(whole_kao_data, start_pnt, KAO_IMG_PAL_B_SIZE)
        self.compressed_img_data = read_bytes(
            whole_kao_data, start_pnt + KAO_IMG_PAL_B_SIZE, cont_len
        )
        self.as_pil: Optional[Image.Image] = None  # lazy loading
        self.modified = False
        self.empty = False

    @classmethod
    def create_from_raw(cls, cimg: bytes, pal: bytes) -> "KaoImage":
        """Create from raw compressed image and palette data"""
        return cls(bytes(pal) + bytes(cimg), 0)

    def get(self) -> Image.Image:
        """Returns the portrait as a PIL image with a 16-bit color palette"""
        if not self.as_pil:
            self.as_pil = kao_to_pil(self)
        return self.as_pil

    def clone(self) -> "KaoImage":
        return KaoImage(self.get_internal(), 0)

    def size(self) -> int:
        return KAO_IMG_PAL_B_SIZE + len(self.compressed_img_data)

    def get_internal(self) -> bytes:
        """Returns the portrait as 16 color palette followed by AT compressed image data"""
        return bytes(self.pal_data) + bytes(self.compressed_img_data)

    def set(self, pil: Image.Image) -> "KaoImage":
        """Sets the portrait using a PIL image with 16-bit color palette as input"""
        new_pal, new_img = pil_to_kao(pil)
        self.pal_data = new_pal
        self.compressed_img_data = new_img
        self.modified = True
        self.as_pil = None
        self.empty = False
        return self

    @classmethod
    def new(cls, pil: Image.Image) -> "KaoImage":
        """Creates a new KaoImage from a PIL image with 16-bit color palette as input"""
        new_pal, new_img = pil_to_kao(pil)
        new = cls(new_pal + new_img, 0)
        new.modified = True
        return new

    def raw(self) -> Tuple[bytes, bytes]:
        """Returns raw image data and palettes"""
        return bytes(self.compressed_img_data), bytes(self.pal_data)


class Kao(KaoProtocol[KaoImage]):
    # noinspection PyMissingConstructor
    def __init__(self, data: bytes):
        if not isinstance(data, memoryview):
            data = memoryview(data)

        # First 160 bytes are padding
        first_toc = SUBENTRIES * SUBENTRY_LEN
        # The following line won't work; what if the first byte of the first pointer is 0?
        # first_toc = next(x for x, val in enumerate(data) if val != 0)
        assert (
            first_toc % SUBENTRIES * SUBENTRY_LEN == 0
        )  # Padding should be a whole TOC entry
        # first pointer = end of TOC
        first_pointer = read_u32(data, first_toc)
        toc_len = int((first_pointer - first_toc) / (SUBENTRIES * SUBENTRY_LEN))

        self.original_data: bytearray = data  # type: ignore
        self.first_toc = first_toc
        self.toc_len: int = toc_len
        self.reset(toc_len)

    @classmethod
    def create_new(cls, number_entries: int):
        """Creates a new empty KAO with the specified number of entries."""
        self = cls.__new__(cls)
        self.first_toc = SUBENTRIES * SUBENTRY_LEN
        self.original_data = bytearray(
            [255] * (self.first_toc + (SUBENTRIES * SUBENTRY_LEN) * number_entries)
        )
        self.toc_len = number_entries
        self.reset(self.toc_len)
        return self

    def n_entries(self) -> int:
        return self.toc_len

    def expand(self, new_size: int) -> None:
        if new_size < self.toc_len:
            raise ValueError(f"Can't reduce size from {self.toc_len} to {new_size}")
        from skytemple_files.graphics.kao._writer import KaoWriter

        # Write all changes
        self.original_data = bytearray(KaoWriter().write(self))

        # Prepare for expanding
        expand_len = new_size - self.toc_len
        expand_size = expand_len * (SUBENTRIES * SUBENTRY_LEN)
        limit = self.first_toc + (self.toc_len * SUBENTRIES * SUBENTRY_LEN)
        # Rewrite all pointers
        last_pnt = i32(0)
        for x in range(self.toc_len * SUBENTRIES):
            start = self.first_toc + x * SUBENTRY_LEN
            pnt = read_i32(self.original_data, start)
            if pnt < 0:
                pnt -= expand_size  # type: ignore
                last_pnt = pnt
            elif pnt > 0:
                last_pnt = -KaoImage(self.original_data, pnt).size() - expand_size  # type: ignore
                pnt += expand_size  # type: ignore
            write_i32(self.original_data, pnt, start)

        # Expand
        expand_pnt = bytearray(4)
        write_i32(expand_pnt, last_pnt, 0)
        self.original_data = (
            self.original_data[:limit]
            + (expand_pnt * (expand_len * SUBENTRIES))
            + self.original_data[limit:]
        )
        self.toc_len = new_size
        self.reset(new_size)

    def reset(self, toc_len: int) -> None:
        self.loaded_kaos: List[List[Optional[KaoImage]]] = [
            [None for __ in range(0, SUBENTRIES)] for _ in range(0, toc_len)
        ]
        self.loaded_kaos_flat: List[
            Tuple[int, int, KaoImage]
        ] = []  # cache for performance

    def get(self, index: int, subindex: int) -> Union[KaoImage, None]:
        """Get the KaoImage at the specified location or None if no image is specified"""
        if index >= self.toc_len or index < 0:
            raise ValueError(
                f"The index requested must be between 0 and {self.toc_len}"
            )
        if subindex >= SUBENTRIES or subindex < 0:
            raise ValueError(
                f"The subindex requested must be between 0 and {SUBENTRIES}"
            )
        if self.loaded_kaos[index][subindex] is None:
            start_toc_entry = (
                self.first_toc
                + (index * SUBENTRIES * SUBENTRY_LEN)
                + subindex * SUBENTRY_LEN
            )
            pnt = read_i32(self.original_data, start_toc_entry)
            if pnt < 0:
                # NULL pointer
                return None
            self.loaded_kaos[index][subindex] = KaoImage(self.original_data, pnt)
            self.loaded_kaos_flat.append((index, subindex, self.loaded_kaos[index][subindex]))  # type: ignore
        elif self.loaded_kaos[index][subindex].empty:  # type: ignore
            return None
        return self.loaded_kaos[index][subindex]

    def set(self, index: int, subindex: int, img: KaoImageProtocol) -> None:
        return self._set_impl(index, subindex, img)

    def set_from_img(self, index: int, subindex: int, img: Image.Image) -> None:
        return self._set_impl(index, subindex, img)

    def _set_impl(
        self, index: int, subindex: int, img: Union[KaoImageProtocol, Image.Image]
    ) -> None:
        """
        Set the KaoImage at the specified location. This fails,
        if there is already an image there. Use get instead.
        """
        if index > self.toc_len or index < 0:
            raise ValueError(
                f"The index requested must be between 0 and {self.toc_len}"
            )
        if subindex > SUBENTRIES or subindex < 0:
            raise ValueError(
                f"The subindex requested must be between 0 and {SUBENTRIES}"
            )
        k = self.get(index, subindex)
        if isinstance(img, KaoImage):
            if k is not None:
                self.loaded_kaos_flat = [
                    (i, s, x)
                    for i, s, x in self.loaded_kaos_flat
                    if i != index or s != subindex
                ]
            img.modified = True
            self.loaded_kaos[index][subindex] = img
            self.loaded_kaos_flat.append((index, subindex, img))
            return
        else:
            if k is not None:
                k.set(img)  # type: ignore
                return

            self.loaded_kaos[index][subindex] = KaoImage.new(img)  # type: ignore
            self.loaded_kaos_flat.append((index, subindex, self.loaded_kaos[index][subindex]))  # type: ignore

    def delete(self, index: int, subindex: int) -> None:
        try:
            kao = self.get(index, subindex)
        except ValueError:
            return
        if kao:
            kao.empty = True
            kao.modified = True

    def has_loaded(self, index: int, subindex: int) -> bool:
        """Returns whether or not a kao image at the specified index was loaded"""
        return self.loaded_kaos[index][subindex] is not None

    def __iter__(self) -> "KaoIterator":
        """
        Iterates over all KaoImages.
        """
        return KaoIterator(self, self.toc_len, SUBENTRIES)


class KaoIterator(Iterator):  # type: ignore
    def __init__(self, kao: Kao, indices: int, subindices: int):
        self.kao = kao
        self.current_index = 0
        self.current_subindex = 0
        self.max_index = indices
        self.max_subindex = subindices

    def __next__(self) -> Tuple[int, int, Union[KaoImage, None]]:
        """Tuple: index, subindex, KaoImage or None"""
        if self.current_index < self.max_index:
            old_index = self.current_index
            old_subindex = self.current_subindex
            ret = None
            try:
                ret = self.kao.get(self.current_index, self.current_subindex)
            except ValueError as ex:
                warnings.warn(
                    f(_("Could not load KAO at {old_index},{old_subindex}: {ex}"))
                )
            self.current_subindex += 1
            if self.current_subindex >= self.max_subindex:
                self.current_index += 1
                self.current_subindex = 0
            return old_index, old_subindex, ret
        else:
            raise StopIteration


def kao_to_pil(kao: KaoImage) -> Image.Image:
    """Converts the data in Kao image to a PIL image"""
    from skytemple_files.common.types.file_types import FileType

    # Generates an array where every three entries a new color begins (r, g, b, r, g, b...)
    uncompressed_image_data = FileType.COMMON_AT.deserialize(
        kao.compressed_img_data
    ).decompress()

    return uncompressed_kao_to_pil(kao.pal_data, uncompressed_image_data)


def uncompressed_kao_to_pil(
    pal_data: bytes, uncompressed_image_data: bytes
) -> Image.Image:
    # The images are made up of 25 8x8 tiles stored linearly in the data, but to be arranged
    # as 5x5 "meta-pixels".
    img_dim = KAO_IMG_METAPIXELS_DIM * KAO_IMG_IMG_DIM
    pil_img_data = bytearray(img_dim * img_dim)

    for idx, pix in enumerate(iter_bytes_4bit_le(uncompressed_image_data)):
        # yikes... the mappings below can probably be simplified a lot
        tile_id = math.floor(idx / (KAO_IMG_METAPIXELS_DIM * KAO_IMG_METAPIXELS_DIM))
        tile_x = tile_id % KAO_IMG_IMG_DIM
        tile_y = math.floor(tile_id / KAO_IMG_IMG_DIM)

        idx_in_tile = idx - (KAO_IMG_METAPIXELS_DIM * KAO_IMG_METAPIXELS_DIM) * tile_id
        in_tile_x = idx_in_tile % KAO_IMG_METAPIXELS_DIM
        in_tile_y = math.floor(idx_in_tile / KAO_IMG_METAPIXELS_DIM)

        result_x = tile_x * KAO_IMG_METAPIXELS_DIM + in_tile_x
        result_y = tile_y * KAO_IMG_METAPIXELS_DIM + in_tile_y
        nidx = result_y * img_dim + result_x
        # print(f"{tile_id} : {tile_x}x{tile_y} -- {idx_in_tile} : {in_tile_x}x{in_tile_y} -> {result_x}x{result_y}={nidx}")
        pil_img_data[nidx] = pix

    assert len(pil_img_data) == img_dim * img_dim
    im = Image.frombuffer("P", (img_dim, img_dim), pil_img_data, "raw", "P", 0, 1)

    im.putpalette(pal_data)

    return im


def pil_to_kao(
    pil: Image.Image, allowed_compressions: Optional[List[CommonAtType]] = None
) -> Tuple[bytes, bytes]:
    """Converts a PIL image (with a 16 bit palette) to a kao palette and at compressed image data"""
    from skytemple_files.common.types.file_types import FileType

    if allowed_compressions is None:
        allowed_compressions = COMMON_AT_MUST_COMPRESS_3

    img_dim = KAO_IMG_METAPIXELS_DIM * KAO_IMG_IMG_DIM
    if pil.width != img_dim or pil.height != img_dim:
        raise ValueError(
            f(
                _(
                    "Can not convert PIL image to Kao: Image dimensions must be {img_dim}x{img_dim}px."
                )
            )
        )
    if (
        pil.mode != "P"
        or pil.palette.mode != "RGB"
        or len(pil.palette.palette) != 16 * 3
    ):
        pil = simple_quant(pil, False)
    new_palette = bytearray(pil.palette.palette)

    # We have to cut the image back into this annoying tiling format :(
    new_img_size = int(img_dim * img_dim / 2)
    new_img = bytearray(new_img_size)
    raw_pil_image = pil.tobytes("raw", "P")
    the_two_px_to_write = [0, 0]
    for idx, pix in enumerate(raw_pil_image):
        # We store 2 bytes as one... in LE
        the_two_px_to_write[idx % 2] = pix
        if idx % 2 == 1:
            # -1 because we are always processing 2 px at the same time
            x = (idx - 1) % img_dim
            y = int((idx - 1) / img_dim)

            tile_x = math.floor(x / KAO_IMG_METAPIXELS_DIM) % KAO_IMG_METAPIXELS_DIM
            tile_y = math.floor(y / KAO_IMG_METAPIXELS_DIM) % KAO_IMG_METAPIXELS_DIM
            tile_id = tile_y * KAO_IMG_IMG_DIM + tile_x

            in_tile_x = x - KAO_IMG_METAPIXELS_DIM * tile_x
            in_tile_y = y - KAO_IMG_METAPIXELS_DIM * tile_y
            idx_in_tile = in_tile_y * KAO_IMG_METAPIXELS_DIM + in_tile_x

            nidx = int(
                (
                    tile_id * KAO_IMG_METAPIXELS_DIM * KAO_IMG_METAPIXELS_DIM
                    + idx_in_tile
                )
                / 2
            )
            # print(f"{idx}@{x}x{y}: {tile_id} : {tile_x}x{tile_y} -- {idx_in_tile} : {in_tile_x}x{in_tile_y} = {nidx}")
            # Little endian:
            new_img[nidx] = the_two_px_to_write[0] + (the_two_px_to_write[1] << 4)
    # Palette reordering algorithm
    # Tries to reorder the palette to have a more favorable data
    # configuration for the PX algorithm
    pairs: Dict[Tuple[int, int], int] = {}
    for x in range(len(new_img) - 1):
        l = [
            new_img[x] % 16,
            new_img[x] // 16,
            new_img[x + 1] % 16,
            new_img[x + 1] // 16,
        ]
        if l.count(l[0]) == 3 or (l.count(l[0]) == 1 and l.count(l[1]) == 3):
            a = l[0]
            for b in l:
                if b != a:
                    break
            if a >= b:
                c = b
                b = a
                a = c
            if (a, b) in pairs:
                pairs[(a, b)] += 1
            else:
                pairs[(a, b)] = 1
    new_order = [0]
    for k, v in sorted(pairs.items(), key=lambda x: -x[1]):
        k0_in_no = k[0] in new_order
        k1_in_no = k[1] in new_order
        if k0_in_no and k1_in_no:
            continue
        elif k0_in_no or k1_in_no:
            if k0_in_no:
                to_check = k[0]
                to_add = k[1]
            elif k1_in_no:
                to_check = k[1]
                to_add = k[0]
            i = new_order.index(to_check)
            if i > 0:
                if new_order[i - 1] == -1:
                    new_order.insert(i, to_add)
                if len(new_order) == i + 1 or new_order[i + 1] == -1:
                    new_order.insert(i + 1, to_add)
        else:
            new_order.append(-1)
            new_order.append(k[0])
            new_order.append(k[1])
    while -1 in new_order:
        new_order.remove(-1)
    for x in range(16):
        if not x in new_order:
            new_order.append(x)
    new_img_new = bytearray(800)
    for i, v in enumerate(new_img):
        new_v = (new_order.index(v % 16)) + (new_order.index(v // 16)) * 16
        new_img_new[i] = new_v
    new_palette_new = bytearray(KAO_IMG_PAL_B_SIZE)
    for i, v in enumerate(new_order):
        new_palette_new[i * 3] = new_palette[v * 3]
        new_palette_new[i * 3 + 1] = new_palette[v * 3 + 1]
        new_palette_new[i * 3 + 2] = new_palette[v * 3 + 2]
    new_img = new_img_new
    new_palette = new_palette_new
    # End of palette reordering

    # You can check if this works correctly, by checking if the reverse action returns the
    # correct image again:
    # >>> uncompressed_kao_to_pil(new_palette, new_img).show()

    new_img_compressed = FileType.COMMON_AT.serialize(
        FileType.COMMON_AT.compress(new_img, allowed_compressions)
    )
    if len(new_img_compressed) > 800:
        raise AttributeError(
            f(
                _(
                    "This portrait does not compress well, the result size is greater than 800 bytes ({len(new_img_compressed)} bytes total).\n"
                    "If you haven't done already, try applying the 'ProvideATUPXSupport' to install an optimized compression algorithm, "
                    "which might be able to better compress this image."
                )
            )
        )
    # You can check if compression works, by uncompressing and checking the image again:
    # >>> unc = FileType.COMMON_AT.unserialize(new_img_compressed).decompress()
    # >>> uncompressed_kao_to_pil(new_palette, unc).show()

    return new_palette[:KAO_IMG_PAL_B_SIZE], new_img_compressed
