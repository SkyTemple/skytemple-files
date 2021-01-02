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
import itertools
from random import choice
from typing import List, Optional

from PIL import Image

from skytemple_files.graphics.bma.model import Bma
from skytemple_files.graphics.dma.model import Dma, DmaType
from skytemple_files.graphics.dpc.model import Dpc, DPC_TILING_DIM
from skytemple_files.graphics.dpci.model import Dpci, DPCI_TILE_DIM
from skytemple_files.graphics.dpl.model import Dpl
from skytemple_files.graphics.dpla.model import Dpla


class DmaDrawer:
    """Class to render DMAs as PIL images (or to just get the BPC tile indices for rules)."""
    def __init__(self, dma: Dma):
        self.dma = dma

    def rules_from_bma(self, bma: Bma) -> List[List[DmaType]]:
        rules = []
        active_row = None
        for i, chunk in enumerate(bma.layer0):
            if i % bma.map_width_chunks == 0:
                if active_row is not None:
                    rules.append(active_row)
                active_row = []
            rule = DmaType.WALL
            # I know this is a convoluted way of doing this but my brain doesn't want to work right now.
            if (chunk + 1) / 3 % 1 == 0 and (chunk + 1) / 3 > 0:
                rule = DmaType.WATER
            elif (chunk + 1) / 2 % 1 == 0 and (chunk + 1) / 2 > 0:
                rule = DmaType.FLOOR
            active_row.append(rule)
        rules.append(active_row)
        return rules

    def get_mappings_for_rules(self, rules: List[List[DmaType]], variation_index=None,
                               treat_outside_as_wall=False) -> List[List[int]]:
        """
        Return the DPC mappings for this DMA configuration and the given rules. If variation_index is given,
        this image variation is used for all tiles, otherwise one of the three variation is chosen at random.
        """
        mappings: List[List[int]] = []
        wall_matrix: List[List[bool]] = []
        water_matrix: List[List[bool]] = []
        for ry, rule_row in enumerate(rules):
            active_wall = []
            active_water = []
            wall_matrix.append(active_wall)
            water_matrix.append(active_water)
            for rx, rule_cell in enumerate(rule_row):
                if rule_cell == DmaType.WALL:
                    active_wall.append(True)
                    active_water.append(False)
                elif rule_cell == DmaType.WATER:
                    active_wall.append(False)
                    active_water.append(True)
                else:
                    active_wall.append(False)
                    active_water.append(False)

        for ry, rule_row in enumerate(rules):
            active_row = []
            mappings.append(active_row)
            for rx, rule_cell in enumerate(rule_row):
                solid_neighbors = self.dma.get_tile_neighbors(
                    water_matrix if rule_cell == DmaType.WATER else wall_matrix, rx, ry,
                    rule_cell != DmaType.FLOOR, treat_outside_as_wall
                )
                variations = self.dma.get(rule_cell, solid_neighbors)
                if variation_index is not None:
                    variation = variations[variation_index]
                else:
                    variation = choice(variations)
                active_row.append(variation)
        return mappings

    def draw(self, mappings: List[List[int]], dpci: Dpci, dpc: Dpc, dpl: Dpl, dpla: Optional[Dpla]) -> List[Image.Image]:
        chunks = dpc.chunks_to_pil(dpci, dpl.palettes, 1)

        chunk_dim = DPCI_TILE_DIM * DPC_TILING_DIM

        fimg = Image.new('P', (len(mappings[0]) * chunk_dim, len(mappings) * chunk_dim))
        fimg.putpalette(chunks.getpalette())

        def paste(chunk_index, x, y):
            fimg.paste(
                chunks.crop((0, chunk_index * chunk_dim, chunk_dim, chunk_index * chunk_dim + chunk_dim)),
                (x * chunk_dim, y * chunk_dim)
            )

        for y, row in enumerate(mappings):
            for x, cell in enumerate(row):
                paste(cell, x, y)

        images = []
        images.append(fimg)

        # Pal ani
        if dpla:
            number_frames = int(len(dpla.colors[0]) / 3)
            has_a_second_palette = len(dpla.colors) > 16 and len(dpla.colors[16]) > 0

            for fidx in range(0, number_frames):
                pal_copy = dpl.palettes.copy()
                img_copy = fimg.copy()
                # Put palette 11
                pal_copy[10] = dpla.get_palette_for_frame(0, fidx)
                if has_a_second_palette:
                    # Put palette 12
                    pal_copy[11] = dpla.get_palette_for_frame(1, fidx)
                img_copy.putpalette(itertools.chain.from_iterable(pal_copy))
                images.append(img_copy)

        return images
