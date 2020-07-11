BMA Layer NRL compression
=========================
Variation on `Generic NRL`_ compression, that reads pairs of Pair24_-encoded 12-bit integers.

This implementation returns the uncompressed integers as 16bit ints (easier to work with).

Usage
-----
Use the class ``BmaLayerNrlHandler`` of the ``handler`` module, to compress and decompress binary data.

Command bytes
-------------
See `Generic NRL`_. We are not working with single bytes but instead with three bytes! So
one copy actually copies three bytes.

Decompression
-------------
See `Generic NRL`_, but write and read three bytes instead of one, and decode Pair24_.

Compression
-----------
Also like `Generic NRL`_, but write and read three bytes instead of one, and decode Pair24_.

Pair24
------
Pair24 is a way of packing two 12-bit values into 3 bytes.
In this form, null runs output two null values instead of a null byte while repeat and literal runs
read/output value pairs instead of bytes.

Packing is as follows:

.. code::

    1111 1111 2222 3333 4444 4444
    1- The lowest 8 bits of the first value
    2- The lowest 4 bits of the second value
    3- The highest 4 bits of the first value
    4- The highest 8 bits of the second value

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

.. _Generic NRL:                    https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression/generic_nrl
