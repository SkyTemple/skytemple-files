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

# Creates BitStreams from KAO models.
# file is 16-bytes aligned!
from sys import maxsize

from skytemple_files.common.util import *
from skytemple_files.graphics.kao.model import Kao, SUBENTRIES, SUBENTRY_LEN, KAO_FILE_BYTE_ALIGNMENT, \
    KAO_IMG_PAL_B_SIZE

DEBUG = False


class KaoWriter:
    def __init__(self, kao: Kao):
        self.kao = kao
        self.new_data = None
        pass

    def write(self, force_rebuild_all=False, update_kao=True) -> bytes:
        """
        Builds a new kao file as a BitStream.
        The entire Kao starting from the first modified image needs
        to be rebuilt, because the game expects the images in order and seems to use
        the TOC pointers to indicate the size of image chunks, so there can be
        no empty spaces.

        This also updates the data representation of the original kao, unless
        update_kao is False.
        """
        from skytemple_files.common.types.file_types import FileType

        # At worst all images are 848 bytes long - However assuming this would allocate over 300MB...
        # Let's just use 10MB. We will enlarge if necessary.
        self.new_data = bytearray(80000000)

        # To increase overall performance, first find the index of the first modified image, we will start from
        # there and just copy the rest
        if not force_rebuild_all:
            start_index = maxsize
            start_subindex = maxsize
            for i, si, k in self.kao.loaded_kaos_flat:
                if k.modified:
                    if update_kao:
                        k.modified = False
                    if i < start_index:
                        start_index = i
                    if si < start_subindex:
                        start_subindex = si

            if start_index == maxsize:
                if DEBUG:
                    print(f"KaoWriter: Nothing changed, returning original")
                # Nothing was changed
                return self.kao.original_data
            else:
                # Copy image data from beginning to that point - this will also copy the old TOC but we will write over that
                current_toc_offset = self.kao.first_toc + (start_index * SUBENTRIES * SUBENTRY_LEN) + start_subindex * SUBENTRY_LEN
                pnt = read_sintle(self.kao.original_data, current_toc_offset, SUBENTRY_LEN)
                if pnt < 0:
                    current_image_offset = -pnt
                else:
                    current_image_offset = pnt
                self.new_data[0:current_image_offset] = self.kao.original_data[0:current_image_offset]
                if DEBUG:
                    print(f"KaoWriter: First modified image: {start_index}, {start_subindex} "
                          f"- will start at TOC {current_toc_offset} and img {current_image_offset}.")
        else:
            start_index = start_subindex = 0
            size_toc = (self.kao.toc_len * SUBENTRIES * SUBENTRY_LEN)
            current_toc_offset = self.kao.first_toc
            current_image_offset = current_toc_offset + size_toc
        
        current_null_pointer = -current_image_offset  # Always start at that null pointer!
        #Otherwise, stuff will break since a 0 pointer is considered as valid in the model!

        # Rebuild KAO
        for i in range(start_index, self.kao.toc_len):
            for si in range(start_subindex, SUBENTRIES):
                if self.kao.has_loaded(i, si):
                    # Image is loaded, use image data for new pointer
                    kao_image = self.kao.get(i, si)
                    if kao_image.empty is True:
                        self._update_toc_entry(current_toc_offset, current_null_pointer.to_bytes(SUBENTRY_LEN, 'little', signed=True))
                        current_toc_offset += SUBENTRY_LEN
                        continue
                    image_data_bs = kao_image.get_internal()
                    image_data_start = 0
                    image_data_end = len(image_data_bs)
                else:
                    # Image is not loaded, get image data directly, is faster than building KaoImage first
                    pnt = read_sintle(self.kao.original_data, current_toc_offset, SUBENTRY_LEN)
                    if pnt < 0:
                        # Null pointer, write new null pointer
                        if DEBUG:
                            print(f"KaoWriter: Null pointer for {i},{si} at TOC {current_toc_offset}: "
                                  f"Written NULL: {current_null_pointer}")
                        # Write NULL pointer
                        self._update_toc_entry(current_toc_offset, current_null_pointer.to_bytes(SUBENTRY_LEN, 'little', signed=True))
                        current_toc_offset += SUBENTRY_LEN
                        continue
                    image_data_bs = self.kao.original_data
                    image_data_start = pnt
                    image_data_end = image_data_start + KAO_IMG_PAL_B_SIZE + FileType.COMMON_AT.cont_size(
                        image_data_bs, image_data_start + KAO_IMG_PAL_B_SIZE
                    )
                # Update the TOC entry to point to the current image offset
                self._update_toc_entry(current_toc_offset, current_image_offset.to_bytes(SUBENTRY_LEN, 'little', signed=True))
                #assert len(self.new_data) / 8 == current_size  # Size must not have changed
                current_image_end = current_image_offset + (image_data_end - image_data_start)
                # Write image data starting at current offset
                self.new_data[current_image_offset:current_image_end] = image_data_bs[image_data_start:image_data_end]
                #assert len(self.new_data) / 8 == current_size  # Size must not have changed
                # Update NULL pointer
                current_null_pointer = -current_image_end
                if DEBUG:
                    print(f"KaoWriter:    Writing image {i},{si} at TOC {current_toc_offset}: "
                          f"Image at {current_image_offset}, size {current_image_offset}. "
                          f"Resulting end: {current_image_end}. "
                          f"Resulting NULL pointer: {current_null_pointer}")
                current_image_offset = current_image_end
                current_toc_offset += SUBENTRY_LEN

            start_subindex = 0  # For all next passes always start with the first image of course!

        # Cut off image buffer, but make sure it keeps being 16 byte aligned.
        remainder = current_image_offset % KAO_FILE_BYTE_ALIGNMENT
        if remainder > 0:
            current_image_offset += KAO_FILE_BYTE_ALIGNMENT - remainder
        current_size = len(self.new_data)
        if current_image_offset > current_size:
            self.new_data += bytearray(current_image_offset - current_size)
        else:
            self.new_data = self.new_data[:current_image_offset]

        if update_kao:
            self.kao.original_data = self.new_data

        return self.new_data

    def _update_toc_entry(self, offs, bs: bytes):
        self.new_data[offs:offs+SUBENTRY_LEN] = bs
