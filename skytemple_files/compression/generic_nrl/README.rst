Generic NRL compression
=======================
NRL is a variation of Run-Length Encoding.

This is the most common variation of it, that works with single byte units as input- and output size.

Usage
-----
Use the class ``GenericNrlHandler`` of the ``handler`` module, to compress and decompress binary data.

Command bytes
-------------
The compressed data contains command bytes that determine what to do. Between the command
bytes may be arguments, depending on the command.

There are three different types of operations:

+---------------+-----------------------------+-------------------------------------------------------------+
| CMD           | Name                        | Description                                                 |
+===============+=============================+=============================================================+
| 0x00 - 0x7F   | Write NULLs                 | Write CMD+1 bytes of NULL.                                  |
+---------------+-----------------------------+-------------------------------------------------------------+
| 0x80 - 0x8F   | Copy next byte x times      | Copy the value stored in the next byte CMD-0x80+1 times.    |
+---------------+-----------------------------+-------------------------------------------------------------+
| 0xC0 - 0xFF   | Copy next x bytes           | Copy the next CMD-0xC0+1 bytes as they are.                 |
+---------------+-----------------------------+-------------------------------------------------------------+

Decompression
-------------
To decompress, simply read the compressed data start to finish  and follow the instructions of the command bytes.

The decompression algorithm needs to know the size of decompressed data. If stops when it has written that amount
of bytes.

Compression
-----------
To compress, you have to options on what you want to check:

- check how many repeating characters there are starting at the current position. If they exceed a certain
  threshold, you either do "Write NULLs" or "Copy next byte x times". Otherwise you copy until a long enough
  repeating pattern is found ("Copy next x bytes").
- check how long until a threshold of repeating characters is found. If the sequence is longer than a defined
  threshold, you want to copy it using "Copy next x bytes",
  otherwise deal with "Write NULLs" or "Copy next byte x times" at the current pos.

(In hindsight the first option is definitely the better, but I went with the second for some NRL compressors...)

Based on this you decide which of the three options you want to do. Then you encode the command byte with it's
arguments if needed and write the arguments. Repeat this until the end of the uncompressed data is read.

Keep in mind, that for all of the operations, there is a limit to how many bytes can be copied (for Write NULLs you
can only write 0x7F nulls using one byte for example).

Credits
-------
Without the following people, this implementation wouldn't have been possible:

- MegaMinerd_ (Figured out Pair24, NRL compression and the format of maps for the RT games, which are very similar!)

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- `Project Pokémon documentation`_


.. Links:

.. _Project Pokémon documentation:  https://projectpokemon.org/docs/mystery-dungeon-nds/nrl-compression-r112/

.. _MegaMinerd:                     https://projectpokemon.org/home/profile/73557-megaminerd/
