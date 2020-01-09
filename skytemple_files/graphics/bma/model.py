import math
from typing import Tuple, List

from PIL import Image, ImageDraw
from bitstring import BitStream

from skytemple_files.common.util import read_bytes, lcm
from skytemple_files.graphics.bpa.model import Bpa
from skytemple_files.graphics.bpc.model import Bpc, BPC_TILE_DIM

# Mask palette used for image composition
MASK_PAL = [
    0x00, 0x00, 0x00,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
    0xff, 0xff, 0xff,
]
MASK_PAL *= 16


class Bma:
    def __init__(self, data: BitStream):
        from skytemple_files.common.types.file_types import FileType

        self.map_width_camera = read_bytes(data, 0).uint
        self.map_height_camera = read_bytes(data, 1).uint
        # ALL game maps have the same values here. Changing them does nothing,
        # so the game seems to be hardcoded to 3x3.
        self.tiling_width = read_bytes(data, 2).uint
        self.tiling_height = read_bytes(data, 3).uint
        # Map width & height in meta tiles, so map.map_width_camera / map.tiling_width
        # The only maps this is not true for are G01P08A. S01P01B, S15P05A, S15P05B, it seems they
        # are missing one tile in width (32x instead of 33x)
        # The game doesn't seem to care if this value is off by less than 3 (tiling_w/h).
        self.map_width_meta = read_bytes(data, 4).uint
        self.map_height_meta = read_bytes(data, 5).uint
        # Through tests against the BPC, it was determined that unk5 is the number of layers:
        # It seems to be ignored by the game, however
        self.number_of_layers = read_bytes(data, 6, 2).uintle
        # Some kind of boolean flag? Seems to control if there is a third data block between
        # layer data and collision
        self.unk6 = read_bytes(data, 8, 2).uintle
        # has collision....? - boolean? but can also be 0x0002, so ehhhhh?
        self.unk7 = read_bytes(data, 0xA, 2).uintle

        # in p01p01a: 0xc - 0x27: Layer 1 header? 0xc messes everthing up. after that each row? 27 rows...?
        #             0xc -> 0xc8 = 200
        #             Same again? 0x28 is 0xc8 again. 0x29 - 0x43 are 27 rows for layer 1 again... Seems to repeat, with some odd ones in between
        #             Sometimes 0xC6 instead: Only 21 entries?
        #             -> UNTIL 0x214. At 0x215 Layer 2 starts.
        #             SEEMS TO BE NRL ENCODING:
        #                   2x12 bits of information stored in 3 bytes. C8 ->
        #                       Copy next and repeat 8 types (=9). 3x9=27!
        #               Decompressed length = (map_width_meta*map_height_meta*12)/8
        #                   = 513
        #               27 / 1,5 = 18! So the first set contains each tile for each row.
        #
        #               This seems to be the solution, it's the same for RRT
        #               [It also explains why changing a tile changes all tiles below!!]:
        #               "Each row has a series of Pair-24 NRL compressed values,
        #               one for each chunk column (rounded up to the nearest even number).
        #               These values are xor'ed with the respective indices of the previous
        #               row to get the actual indices of the chunks in the current row.
        #               The first row assumes all previous indices were 0."
        #               Chunk = Meta Tile, source:
        #               https://projectpokemon.org/docs/mystery-dungeon-nds/rrt-background-format-r113/
        #
        number_of_bytes_per_layer = math.ceil(self.map_width_meta * self.map_height_meta * 1.5)
        # Read first layer
        self.layer0, compressed_layer0_size = self._read_layer(FileType.BMA_LAYER_NRL.decompress(
            data[0xC * 8:],
            stop_when_size=number_of_bytes_per_layer
        ))
        self.layer1 = None
        compressed_layer1_size = 0
        collision_size = 0
        if self.number_of_layers > 1:
            # Read second layer
            self.layer1, compressed_layer1_size = self._read_layer(FileType.BMA_LAYER_NRL.decompress(
                data[(0xC + compressed_layer0_size) * 8:],
                stop_when_size=number_of_bytes_per_layer
            ))
        if self.unk6:
            # TODO IF SET THERE SEEMS TO BE ANOTHER UNKNOWN DATA BLOCK HERE.
            raise NotImplementedError()
        self.collision = None
        if self.unk7 > 0:
            # Read level collision
            # The collision is stored like this:
            # RLE:
            # Each byte codes one byte, that can have the values 0 or 1.
            # The highest bit determines whether to output 0 or 1 bytes. All the other
            # bits form an unsigned integer. This int determines the number of bytes to output. 1 extra
            # byte is always output. (So 0x03 means output 4 0 bytes and 0x83 means output 4 1 bytes).
            # The maximum value of repeats is the map with in 8x8 tiles. So for a 54 tile map, the max values
            # are 0x53 and 0xC3.
            #
            # To get the actual collision value, all bytes are XORed with the value of the tile in the previous row,
            # this is the same principle as for the layer tile indices.
            # False (0) = Walktru; True (1) = Solid
            #
            number_of_bytes_for_col = self.map_width_meta * self.map_height_meta * self.tiling_width * self.tiling_height
            self.collision, collision_size = self._read_collision(FileType.BMA_COLLISION_RLE.decompress(
                data[(0xC + compressed_layer0_size + compressed_layer1_size) * 8:],
                stop_when_size=number_of_bytes_for_col
            ))
            pass
        print(f"Number bytes not read: {int(len(data) / 8) - (0xC + compressed_layer0_size + compressed_layer1_size + collision_size)}")

    def __str__(self):
        return f"M: {self.map_width_camera}x{self.map_height_camera}, " \
               f"T: {self.tiling_width}x{self.tiling_height} - " \
               f"MM: {self.map_width_meta}x{self.map_height_meta} - " \
               f"L: {self.number_of_layers} -   " \
               f"unk6: 0x{self.unk6:04x}, " \
               f"unk7: 0x{self.unk7:04x}"

    def _read_layer(self, data: Tuple[BitStream, int]):
        # To get the actual index of a chunk, the value is XORed with the tile value right above!
        previous_row_values = [0 for _ in range(0, self.map_width_meta)]
        layer = []
        max_tiles = self.map_width_meta * self.map_height_meta
        i = 0
        skipped_on_prev = True
        for chunk in data[0].cut(12):
            if i >= max_tiles:
                # this happens if there is a leftover 12bit word.
                break
            index_in_row = i % self.map_width_meta
            # If the map width is odd, there is one extra chunk at the end of every row,
            # we remove this chunk.
            # TODO: DO NOT FORGET TO ADD THEM BACK DURING SERIALIZATION
            if not skipped_on_prev and index_in_row == 0 and self.map_width_meta % 2 != 0:
                skipped_on_prev = True
                continue
            skipped_on_prev = False
            cv = chunk.uint ^ previous_row_values[index_in_row]
            previous_row_values[index_in_row] = cv
            layer.append(cv)
            i += 1
        return layer, data[1]

    def _read_collision(self, data: Tuple[BitStream, int]):
        # To get the actual index of a chunk, the value is XORed with the tile value right above!
        previous_row_values = [False for _ in range(0, self.map_width_meta * self.tiling_width)]
        col = []
        for i, chunk in enumerate(data[0].cut(8)):
            index_in_row = i % (self.map_width_meta * self.tiling_width)
            cv = bool(chunk.uint ^ int(previous_row_values[index_in_row]))
            previous_row_values[index_in_row] = cv
            col.append(cv)
        return col, data[1]

    def to_pil(self, bpc: Bpc, palettes: List[List[int]], bpas: List[Bpa], include_collision=True) -> List[Image.Image]:
        """
        Converts the entire map into an image, as shown in the game. Each PIL image in the list returned is one
        frame. The palettes argument can be retrieved from the map's BPL (bpl.palettes).

        The method does not care about frame speeds. Each step of animation is simply returned as a new image,
        so if BPAs use different frame speeds, this is ignored; they effectively run at the same speed.
        If BPAs are using a different amount of frames per tile, the length of returned list of images will be the lowest
        common denominator of the different frame lengths.

        Does not include palette animations. You can apply them by switching out the palettes of the PIL
        using the information provided by the BPL.

        TODO: The speed can be increased SIGNIFICANTLY if we only re-render the changed
              animated tiles instead!

        TODO: This is soooo awfully slow right now. Good place to start profiling. (hint: it's mostly BitSreams fault...)
        """

        meta_tile_width = BPC_TILE_DIM * self.tiling_width
        meta_tile_height = BPC_TILE_DIM * self.tiling_height

        width_map = self.map_width_meta * meta_tile_width
        height_map = self.map_height_meta * meta_tile_height

        final_images = []
        lower_layer = 0 if bpc.number_of_layers == 1 else 1
        meta_tiles_lower = bpc.meta_tiles_animated_to_pil(lower_layer, palettes, bpas, 1)
        for img in meta_tiles_lower:
            fimg = Image.new('P', (width_map, height_map))
            fimg.putpalette(img.getpalette())

            # yes. self.layer0 is always the LOWER layer! It's the opposite from BPC
            for i, mt_idx in enumerate(self.layer0):
                x = i % self.map_width_meta
                y = math.floor(i / self.map_width_meta)
                fimg.paste(
                    img.crop((0, mt_idx * meta_tile_width, meta_tile_width, mt_idx * meta_tile_width + meta_tile_height)),
                    (x * meta_tile_width, y * meta_tile_height)
                )

            final_images.append(fimg)

        if bpc.number_of_layers > 1:
            # Overlay higher layer tiles
            meta_tiles_higher = bpc.meta_tiles_animated_to_pil(0, palettes, bpas, 1)
            len_lower = len(meta_tiles_lower)
            len_higher = len(meta_tiles_higher)
            if len_higher != len_lower:
                # oh fun! We are missing animations for one of the layers, let's stretch to the lowest common multiple
                lm = lcm(len_higher, len_lower)
                for i in range(len_lower, lm):
                    final_images.append(final_images[i % len_lower].copy())
                for i in range(len_higher, lm):
                    meta_tiles_higher.append(meta_tiles_higher[i % len_higher].copy())

            for j, img in enumerate(meta_tiles_higher):
                fimg = final_images[j]
                for i, mt_idx in enumerate(self.layer1):
                    x = i % self.map_width_meta
                    y = math.floor(i / self.map_width_meta)

                    cropped_img = img.crop((0, mt_idx * meta_tile_width, meta_tile_width, mt_idx * meta_tile_width + meta_tile_height))
                    cropped_img_mask = cropped_img.copy()
                    cropped_img_mask.putpalette(MASK_PAL)
                    fimg.paste(
                        cropped_img,
                        (x * meta_tile_width, y * meta_tile_height),
                        mask=cropped_img_mask.convert('1')
                    )

        if include_collision and self.unk7 > 0:
            # time for some RGB action!
            for i, img in enumerate(final_images):
                final_images[i] = img.convert('RGB')
                img = final_images[i]
                draw = ImageDraw.Draw(img, 'RGBA')
                for j, col in enumerate(self.collision):
                    x = j % (self.tiling_width * self.map_width_meta)
                    y = math.floor(j / (self.tiling_width * self.map_width_meta))
                    if col:
                        draw.rectangle((
                            (x * BPC_TILE_DIM, y * BPC_TILE_DIM),
                            ((x+1) * BPC_TILE_DIM, (y+1) * BPC_TILE_DIM)
                        ), fill=(0xff, 0x00, 0x00, 0x40))

        return final_images
