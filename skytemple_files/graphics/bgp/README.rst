BGP File Format
===============

The BGP file format is used to store full-screen background images, most notably the various images that appear in the
background of the main menu. Please note, that many background seen in the game are actually stored as level map
backgrounds, see BMA_.

The entire file is stored using AT4PX_ compression!

Usage
-----
Use the class ``BgpHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x000   | 20     |           | Header_             | See Header_.                                                |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x020   | 1024   |           | Palettes_           | Stores 16 16 color palettes for use by the tiles.           |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x420   | 620    |           | `Tile Mapping`_     | For each 8x8 region of the screen, identifies which tile,   |
|         |        |           |                     | palette, and transform to use. List of uint16le.            |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0xC40   | Varies |           | Tiles_              | Consecutive 8x8 4bbp tiles for use in the tile mapping.     |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+

Header
~~~~~~

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00    | 4      | uint32le  | Palette Begin       | Pointer to Palettes_. Always 0x20.                          |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x04    | 4      | uint32le  | Palette Length      | Length of Palettes_. Always 1024.                           |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x08    | 4      | uint32le  | Tiles Begin         | Pointer to Tiles_. Always 0xC40.                            |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x0C    | 4      | uint32le  | Palette Length      | Length of Tiles_.                                           |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x10    | 4      | uint32le  | Tilemap Data Begin  | Pointer to `Tile Mapping`_.                                 |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x14    | 4      | uint32le  | Tilemap Data Length | Length of `Tile Mapping`_. Always 620.                      |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x18    | 4      | uint32le  | unk3                | Unknown. Usually 0x1.                                       |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x1C    | 4      | uint32le  | unk4                | Unknown. Usually 0x0.                                       |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+


Palettes
~~~~~~~~
A list of 16 palettes with 16 colors each, Each color has 4 bytes: Red, Green, Blue, and a 4th
unknown byte which is always set to 0x80.

Tile Mapping
~~~~~~~~~~~~
This is the same format as used by BPC_ Tile Mappings!

The Nintendo DS screen is 256x192 pixels. Because each tile is 8x8, this leaves a grid of 32x24, leaving 768 possible
tiles. At two bytes per tile mapping, this region is 1536 (0x600) bytes long.

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
    The index in the Palette table of the 16 color palette to use for the
    tile specified in the tile data index!


For each spot on the screen that needs a tile, the 4bpp 8x8 tile given by the Tile Data Index is used, transformed on
either axis if applicable, and its palette is 16 consecutive colors from the Palette above, after skipping 16 times the
Palette Index colors.

Tiles
~~~~~
Tiles are simple. They are simply 4bpp tiles of 8x8 pixels referenced by the Tile Mapping.

Credits
-------
I didn't do much of the work figuring out the file format. Without the following people, this implementation
wouldn't have been possible:

- evandixon_ (Figured out most of this format!)
- psy_commando_ (C++ implementation, documentation and most of the research work!)

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- `Project Pokémon documentation`_ (Documentation mostly adapted from there!)
- `psy_commando Dropbox`_


.. Links:

.. _Project Pokémon documentation:  https://projectpokemon.org/docs/mystery-dungeon-nds/pmd2-bgp-r41/
.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0

.. _psy_commando:                   https://github.com/PsyCommando/
.. _evandixon:                      https://projectpokemon.org/home/profile/183-evandixon/

.. _BPC:                            https://github.com/SkyTemple/skytemple_files/blob/master/skytemple_files/graphics/bpc
.. _BMA:                            https://github.com/SkyTemple/skytemple_files/blob/master/skytemple_files/graphics/bma
.. _AT4PX:                          https://github.com/SkyTemple/skytemple_files/blob/master/skytemple_files/compression_container/at4px