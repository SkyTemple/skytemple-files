BPC File Format
===============
Contains a tileset for up to two layers of tiles for a map background.

The tiles are built and assigned palettes using tile mappings, and each 3x3 block of this tile mapping builds a
chunk, that is used by the BMA_ files to assemble the map background.

The palettes are stored in the BPL_.

The BPC_ files are directly linked with BPA_ files via the `bg_list.dat`_, and BPA_ tiles are referenced in tile
mappings. See `BPA tiles`_ for more information.

Must be used together with it's BPC_, BPL_ and BMA_ files. See `bg_list.dat`_.

Usage
-----
Use the class ``BpcHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------

The compressed size of compressed data blocks is unknown until decompressed. However the decompressed
size is known and must be passed as the stopping size to the decompression algorithms. See the sections for more info.

+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
| Offset  | Length | Type                  | Name                  | Description                                                 |
+=========+========+=======================+=======================+=============================================================+
| 0x0000  | 2      | uint16le              | Upper Layer Pointer   | Pointer to "Upper Layer Tiles".                                 |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
| 0x0002  | 2      | uint16le              | Lower Layer Pointer   | Pointer to "Lower Layer Tiles". May be 0, in this case the  |
|         |        |                       |                       | map only has a lower layer and 0x00 actually points to that |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
| 0x0004  | Varies | Array                 | 1-2 `Layer Specs`_    | Settings for each layer.                                    |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | Varies | `BPC Image Comp`_     | Upper `Layer Data`_   | Only if upper layer exists. Layer image data.               |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | 0-1    |                       | (Padding)             | Align next entry on 2 bytes.                                |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | Varies | `BPC Image Comp`_     | Lower `Layer Data`_   | Layer image data.                                           |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | 0-1    |                       | (Padding)             | Align next entry on 2 bytes.                                |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | Varies | `BPC Tilemap NRL`_    | Up. `Tile Mappings`_  | Only if upper layer exists. Layer tile Mappings.            |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | 0-1    |                       | (Padding)             | Align next entry on 2 bytes.                                |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | Varies | `BPC Tilemap NRL`_    | Lw. `Tile Mappings`_  | Layer tile Mappings.                                        |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | 0-1    |                       | (Padding)             | Align next entry on 2 bytes.                                |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+


Layer Specs
~~~~~~~~~~~

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00    | 2      | uint16le  | Number of Tiles     | The number of tiles stored in the data + 1. The +1 is the   |
|         |        |           |                     | null tile at the beginning of tiles, that is not stored.    |
|         |        |           |                     | See `Layer Data`_.                                          |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x02    | 2      | uint16le  | BPA slot 1          | The number of tiles in the BPA on this slot. The BPA used   |
|         |        |           |                     | for this slot is defined in the `bg_list.dat`_. 0 if no BPA |
|         |        |           |                     | is assigned. See `BPA tiles`_ for more information.         |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x04    | 2      | uint16le  | BPA slot 2          | See above.                                                  |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x06    | 2      | uint16le  | BPA slot 3          | See above.                                                  |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x08    | 2      | uint16le  | BPA slot 4          | See above.                                                  |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x0A    | 2      | uint16le  | Number of Chunks    | Number of chunks in the tilemap + 1. The +1 is the null     |
|         |        |           |                     | chunk at the beginning of tile mappings, that is not stored.|
|         |        |           |                     | See `Tile Mappings`_. Since a chunk is made of 3x3 tile     |
|         |        |           |                     | mappings, the number of entries in the tile mappings        |
|         |        |           |                     | is (this-1)x9 or (this)x9, first is stored size, second is  |
|         |        |           |                     | size including the 9 tile mapping entries for null chunk.   |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+

Layer Data
~~~~~~~~~~
`BPC Image Comp`_ compressed.

**Decompressed size:** (LayerSpecs.NumberOfTiles-1) * 32

Contains all pixel data for the layer. They are simple 8x8 4bpp images, that are referenced in the
`Tile Mappings`_.

After reading this data block, a null tile must be inserted to index 0. This null tile is not stored!


Tile Mappings
~~~~~~~~~~~~~
`BPC Tilemap NRL`_ compressed.

**Decompressed size:** (LayerSpecs.NumberOfChunks - 1) * 9 * 2

When decompressed, this is the same format as used by BGP_ Tile Mappings!

A list of tile mapping entries. Each block of 9 tile mapping entries forms one chunk used by the BMA_. A chunk
has to be drawn as a 3x3 grid of tiles on the screen.

The tile entry is a uint16le made up of 4 parts.

.. code::

    0000 0011 1111 1111
           \__________/
    The tile data index.
    The index of the image tile to place.


    0000 0100 0000 0000
          |
    The X axis flip byte
    Whether the tile is flipped on the X axis or not. (1 = yes, 0 = no)


    0000 1000 0000 0000
         |
    The Y axis flip byte
    Whether the tile is flipped on the Y axis or not. (1 = yes, 0 = no)


    1111 0000 0000 0000
    \__/
    The palette index.
    The index in the BPL palette table to use for the
    tile specified in the tile data index!


For each spot on the screen that needs a tile, the 4bpp 8x8 tile given by the Tile Data Index is used, transformed on
either axis if applicable, and its palette is 16 consecutive colors from the Palette above, after skipping 16 times the
Palette Index colors.

Tile Mappings may reference tiles, that do not exist in the `Layer Data`_. See `BPA tiles`_.

After reading this data block, 9 null tile mappings must be inserted to index 0-8. This null chunk is not stored!

BPA tiles
~~~~~~~~~
Tile Mappings can reference tiles, that are not part of the BPC layer's `Layer Data`_. These tiles are BPA_ tiles.
To draw the tile mappings insert all of the layer's BPA_ tiles at the end of the BPC tiles.

Example: BPC has 20 tiles. BPA1 has 4 tiles. BPC tiles go from 0-19. BPA1 tiles go from 20-23.

Credits
-------
Without the following people, this implementation wouldn't have been possible:

- psy_commando_ (C++ implementation, documentation and most of the research work!)

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- `psy_commando Dropbox`_


.. Links:

.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0

.. _psy_commando:                   https://github.com/PsyCommando/

.. _BPC:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpc
.. _BMA:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bma
.. _BPA:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpa
.. _BPL:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpl
.. _bg_list.dat:                    https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bg_list_dat
.. _BPC Image Comp:                 https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression/bpc_image
.. _BPC Tilemap NRL:                https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression/bpc_tilemap
.. _BGP:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bgp
