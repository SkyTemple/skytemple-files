DPC File Format
===============
Contains a tileset for dungeon tiles.

The tiles are built and assigned palettes using tile mappings, and each 3x3 block of this tile mapping builds a
chunk. Those chunks are the actual 24x24 chunks that make up each field in a dungeon.

The tile mappings contain palette indices that are references to the same dungeon's `DPL`_ + `DPLA`_ palette files.
The image data for the tiles must be read from the dungeon's `DPCI`_ file.

This file format, used togehter with `DPCI`_ is the equivalent of `BPC`_ files but for dungeons.

The name is not official.

The file can only be found AT4PX compressed in the dungeon.bin file.

Usage
-----
Use the class ``DpciHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

To read/write the AT4PX compressed versions of this file instead, you can
use the file handler in ``skytemple_files.container.dungeon_bin.sub.at4px_dpc``.

File Format
-----------
The file contains a stream of bytes, that is the same as `BGP`_ and `BPC`_ tile mappings. Every 18 bytes
make up one 3x3 chunk.

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
    The index in the DPL palette table to use for the
    tile specified in the tile data index!


For each spot on the screen that needs a tile, the 4bpp 8x8 tile given by the Tile Data Index is used, transformed on
either axis if applicable, and its palette is 16 consecutive colors from the DPL, after skipping 16 times the
Palette Index colors.


Credits
-------
Without the following people, this implementation wouldn't have been possible:

- psy_commando_ (Documentation and most of the research work!)

Much of the reverse-engineering work is based on the MapBG file formats. See those file handlers
for more credits!

(There are probably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

.. Links:

.. _psy_commando:                   https://github.com/PsyCommando/

.. _DPCI:                           https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpci
.. _DPL:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpl
.. _DPLA:                           https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpla
.. _BPC:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpc
.. _BGP:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bgp
