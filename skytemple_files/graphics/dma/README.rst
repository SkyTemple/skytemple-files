DMA File Format
===============
A list of 1 byte unsigned numbers that refer to chunks as specfied in `DPC`_.
Each entry in this list is the chunk to use to render a type of dungeon tile. Each type has three variants and a few
other properties (is it a ground/wall/water tile, which directions next to me are solid, etc).
See `Index Mapping`_ for more details.

The list contains 0x930 entries.

This file format is in it's purpose roughly the equivalent of `BMA`_ files but for dungeons.

The name is not official.

The file can only be found SIR0 wrapped and AT4PX compressed in the dungeon.bin file.

Usage
-----
Use the class ``DmaHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

To read/write the SIR0 wrapped & AT4PX compressed versions of this file instead, you can
use the file handler in ``skytemple_files.container.dungeon_bin.sub.at4px_dpc``.

The model further clusters the chunk types as specified below.

Index mapping
~~~~~~~~~~~~~
First of, please note that all mappings stored in this file have three variations. To get the actual
index we are working with here, you need to do divide by three (``i = floor(i /3)``). If you multiply
this by 3 again you will get the three variations for this index.

The index is a 10-bit bitfield.

The highest two bits
####################
The highest two bits define the type of the tile:

+---------+---------------------------------------+
| Value   | Type                                  |
+=========+=======================================+
| 0b00    | Wall tile                             |
+---------+---------------------------------------+
| 0b01    | Water / lava / chasm tile             |
+---------+---------------------------------------+
| 0b10    | Ground / floor tile                   |
+---------+---------------------------------------+
| 0b11    | Extra / special tile (see below)      |
+---------+---------------------------------------+

The lowest eight bits (if not "extra")
######################################
If a bit is set, it means there is a wall on that neighboring tile,
otherwise it means there is none there.

+---------+---------------------------------------+
| Bit     | Direction                             |
+=========+=======================================+
| 0       | South                                 |
+---------+---------------------------------------+
| 1       | South East                            |
+---------+---------------------------------------+
| 2       | East                                  |
+---------+---------------------------------------+
| 3       | North East                            |
+---------+---------------------------------------+
| 4       | North                                 |
+---------+---------------------------------------+
| 5       | North West                            |
+---------+---------------------------------------+
| 6       | West                                  |
+---------+---------------------------------------+
| 7       | South West                            |
+---------+---------------------------------------+

Extra tiles
###########
In the set of extra tiles, every third tile build a group. There are three groups. We don't know much about these
work yet.

+---------+---------------------------------------+
| Group   | Description                           |
+=========+=======================================+
| 0       | Another ground tile variation?        |
+---------+---------------------------------------+
| 1       | The first is the void tile, the       |
|         | others are another wall variation?    |
+---------+---------------------------------------+
| 2       | Another ground tile variation?        |
+---------+---------------------------------------+

Credits
-------
Without the following people, this implementation wouldn't have been possible:

- MegaMinerd_ (Without him I would still be sitting here figuring out how the indexing works!)

Much of the reverse-engineering work is based on the MapBG file formats. See those file handlers
for more credits!

(There are probably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

.. Links:

.. _MegaMinerd:                     https://projectpokemon.org/home/profile/73557-megaminerd/

.. _DPCI:                           https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpci
.. _DPL:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpl
.. _DPLA:                           https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpla
.. _BPC:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpc
.. _BGP:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bgp

.. _BMA:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bma
.. _DPC:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpc