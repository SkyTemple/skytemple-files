BPC Tilemap NRL compression
===========================
Variation on `Generic NRL`_ compression, that also works with single bytes,
but reads and writes low and high bytes of a two-byte pair separately.

This means that first byte 0,2,4... are encoded using `Generic NRL`_ and after this bytes 1,3,5... .

Usage
-----
Use the class ``BpcTilemapHandler`` of the ``handler`` module, to compress and decompress binary data.

Command bytes
-------------
See `Generic NRL`_.

Decompression
-------------
See `Generic NRL`_, but keep in mind that you always dealing with every other byte.
After reaching the end of the expected length in the output buffer, return to the byte at
index 1 and repeat.

Compression
-----------
Also like `Generic NRL`_, but write data for every other byte.

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

.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0
.. _Project Pokémon documentation:  https://projectpokemon.org/docs/mystery-dungeon-nds/nrl-compression-r112/

.. _psy_commando:                   https://github.com/PsyCommando/
.. _MegaMinerd:                     https://projectpokemon.org/home/profile/73557-megaminerd/

.. _Generic NRL:                    https://github.com/Parakoopa/skytemple_files/blob/master/skytemple_files/compression/generic_nrl
