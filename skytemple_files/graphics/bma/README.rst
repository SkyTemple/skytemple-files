BMA File Format
===============
Contains the chunk mappings, collisions, and a data layer that seems to contain NPC talking spot data, for map magrounds.
Also contains information on the map's dimensions. These files contain the "building constructions" for the actual map.

Must be used together with it's BPC_, BPL_ and BPA_ files. See `bg_list.dat`_.

Usage
-----
Use the class ``BmaHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------
All data blocks come right after another. Please note that some blocks may not exist (see description).
The compressed size of NRL and RLE compressed data blocks is unknown until decompressed. However the decompressed
size is known and must be passed as the stopping size to the decompression algorithms. See the sections for more info.

All layers contain data that when read build the map from top-left to bottom-right.

+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
| Offset  | Length | Type                  | Name                  | Description                                                 |
+=========+========+=======================+=======================+=============================================================+
| 0x0000  | 12     |                       | Header_               | See Header_.                                                |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
| 0x0012  | Varies | `BMA Layer NRL`_      | `Chunk Mappings`_     | Chunk Mappings for the lower layer.                         |
|         |        |                       | for lower layer       |                                                             |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | Varies | `BMA Layer NRL`_      | `Chunk Mappings`_     | ONLY IF Header_.NumberOfLayers > 1:                         |
|         |        |                       | for upper layer       | Chunk Mappings for the upper layer.                         |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | Varies | `Generic NRL`_        | `Unknown Data Layer`_ | ONLY IF Header_.HasDataLayer: `Unknown Data Layer`_.        |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | Varies | `BMA Collision RLE`_  | `Collision`_ Layer 1  | ONLY IF Header_.HasCollision > 0: Collision data used by    |
|         |        |                       |                       | game.                                                       |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | Varies | `BMA Collision RLE`_  | `Collision`_ Layer 2  | ONLY IF Header_.HasCollision > 1: More collision data?      |
|         |        |                       |                       | Seems to be only used by 5 maps, where it is redundant and  |
|         |        |                       |                       | it seems the game completely ignores this data.             |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+

Header
~~~~~~

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00    | 1      | uint8     | Map Width Camera    | Map width that the camera in game will travel in tiles.     |
|         |        |           |                     | Also the width of the collision and unknown data layers!    |
|         |        |           |                     | For most maps (Map Width Chunks) * (Tiling Width)           |
|         |        |           |                     | = (Map Width Camera).                                       |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x01    | 1      | uint8     | Map Height Camera   | Map height that the camera in game will travel in tiles.    |
|         |        |           |                     | Also the height of the collision and unknown data layers!   |
|         |        |           |                     | For most maps (Map Height Chunks) * (Tiling Height)         |
|         |        |           |                     | = (Map Height Camera).                                      |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x02    | 1      | uint8     | Tiling Width        | Width of chunks in tiles. Always 3! The game is hardcoded   |
|         |        |           |                     | to only support 3x3 tiled chunks! This value is ignored!    |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x03    | 1      | uint8     | Tiling Height       | Height of chunks in tiles. Always 3! The game is hardcoded  |
|         |        |           |                     | to only support 3x3 tiled chunks! This value is ignored!    |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x04    | 1      | uint8     | Map Width Camera    | Map width in chunks. Also the width of the chunk mappings.  |
|         |        |           |                     | WARNING: If this value is odd, the actual number of chunk   |
|         |        |           |                     | mappings per row is this value + 1. The last entry in each  |
|         |        |           |                     | row is 0 then. See `Chunk Mappings`_ for more details!      |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x05    | 1      | uint8     | Map Height Camera   | Map height in chunks. Also the height of the chunk mappings.|
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x06    | 2      | uint16le  | NumberOfLayers      | Number of layers in this map. Must match BPC_ layer size.   |
|         |        |           |                     | Allowed values are only 1 or 2.                             |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x08    | 2      | uint16le  | unk6 (HasDataLayer) | Seems to be a boolean flag (0 or 1). If >0, the             |
|         |        |           |                     | `Unknown Data Layer`_ exists.                               |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x0A    | 2      | uint16le  | HasCollision        | Number of `Collision`_ layers. 0, 1 or 2.                   |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+

Chunk Mappings
~~~~~~~~~~~~~~
`BMA Layer NRL`_ compressed (Pair24 integers).

**Decompressed size:** (Map Width Chunks [+1 of odd number]) * (Map Height Chunks) * size(uint12)

Contains a list of 12-bit integers, which code which chunk of the BPC_ to place at the position on the map.

After decompression, you need to XOR the values with the values from the previous row, to get
the actual value for a chunk. For the first row the values to XOR against are all 0.

If the map width is odd, each row contains an additional null tile, which is not displayed in-game.

Implementation note: The `BMA Layer NRL`_ decompressor of SkyTemple uses 16-bit LE integers, for easier reading.

Note for compression: The game reads each row separately. All need to be separately compressed.

Unknown Data Layer
~~~~~~~~~~~~~~~~~~
`Generic NRL`_ compressed.

**Decompressed size:** (Map Width Camera) * (Map Height Camera)

Contains a value for each tile. The actual meaning of the values is unknown, but it seems that it's used
to mark NPC talking spots on the map. If the player stays on a numbered tile, tiles with the same number in the
area are also checked for NPCs to talk to, as if the player were also standing on those tiles...? Might also
be used for other data?

Note for compression: The game reads each row separately. All need to be separately compressed.

Collision
~~~~~~~~~
`BMA Collision RLE`_ compressed.

**Decompressed size:** (Map Width Camera) * (Map Height Camera)

Contains a boolean value for each tile. 1 means solid (the player can't pass through the tile), 0 means free to
walk through.

After decompression, you need to XOR the values with the values from the previous row, to get
the actual value for a tile. For the first row the values to XOR against are all 0.

Note for compression: The game reads each row separately. All need to be separately compressed.

Credits
-------
Without the following people, this implementation wouldn't have been possible:

- psy_commando_ (C++ implementation, documentation and most of the research work!)
- MegaMinerd_ (Figured out Pair24, NRL compression and the format of maps for the RT games, which are very similar!)

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- `Project Pokémon documentation`_
- `psy_commando Dropbox`_


.. Links:

.. _Project Pokémon documentation:  https://projectpokemon.org/docs/mystery-dungeon-nds/rrt-background-format-r113/
.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0

.. _psy_commando:                   https://github.com/PsyCommando/
.. _MegaMinerd:                     https://projectpokemon.org/home/profile/73557-megaminerd/

.. _BPC:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpc
.. _BMA:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bma
.. _BPA:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpa
.. _BPL:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpl
.. _bg_list.dat:                    https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bg_list_dat
.. _BMA Layer NRL:                  https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression/bma_layer_nrl
.. _Generic NRL:                    https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression/generic_nrl
.. _BMA Collision RLE:              https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression/bma_collision_rle