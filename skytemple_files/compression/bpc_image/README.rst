BPC Image compression
=====================
Variation on Run-Length encoding that works with command bytes and a pattern memory.

Usage
-----
Use the class ``BpcImageHandler`` of the ``handler`` module, to compress and decompress binary data.

Memory
------
Both the compressor and decompressor must keep track of two 1-byte memory variables:

- ``pattern``: The current pattern memory
- ``patternbuffer``: The previous pattern memory.

Both start with the value 0.

The commands change the values of these variables, see below.

Command bytes
-------------
The compressed data contains command bytes that determine what to do. Between the command
bytes may be arguments, depending on the command.

There are four different types of operations:

+---------------+----------------------------------------+----------------------------------------------------------+-------------------------------------------------------------+
| CMD           | Constant                               | Name                                                     | Description                                                 |
+===============+========================================+==========================================================+=============================================================+
| 0x00 - 0x7D   | CMD_CP_FROM_POS                        | Copy next x bytes                                        | Copy the next CMD+1 bytes as they are.                      |
+---------------+----------------------------------------+----------------------------------------------------------+--------------------------+----------------------------------+
| 0x80 - 0xBE   | CMD_LOAD_BYTE_AS_PATTERN_AND_CP        | Load a pattern and write it x times                      | Load the next byte into ``pattern``.                        |
|               |                                        |                                                          | Write the new ``pattern`` value CMD+1-0x80 times,           |
+---------------+----------------------------------------+----------------------------------------------------------+--------------------------+----------------------------------+
| 0xC0 - 0xDE   | CMD_USE_LAST_PATTERN_AND_CP            | Write the current pattern x times                        | Write ``pattern`` value CMD+1-0xC0 times,                   |
+---------------+----------------------------------------+----------------------------------------------------------+--------------------------+----------------------------------+
| 0xE0 - 0xFE   | CMD_CYCLE_PATTERN_AND_CP               | Cycle the current pattern and write it x times           | Switch the values of ``pattern`` and ``patternbuffer``.     |
|               |                                        |                                                          | Write the new ``pattern`` value CMD+1-0xE0 times,           |
+---------------+----------------------------------------+----------------------------------------------------------+--------------------------+----------------------------------+

Additionally there are special variations of the commands above:

+---------------+----------------------------------------+----------------------------------------------------------+-------------------------------------------------------------+
| CMD           | Variation on                           | Type of variation                                        | Description                                                 |
+===============+========================================+==========================================================+=============================================================+
| 0x7E          | CMD_CP_FROM_POS                        | Read number of bytes to copy from next byte              | Instead of using CMD for the value, write (next byte val)+1 |
|               |                                        |                                                          | times.                                                      |
+---------------+----------------------------------------+----------------------------------------------------------+--------------------------+----------------------------------+
| 0x7F          | CMD_LOAD_BYTE_AS_PATTERN_AND_CP        | Read number of bytes to copy from next two bytes         | Instead of using CMD for the value, write (next two bytes   |
|               |                                        | (uintle16).                                              | as int)+1 times.                                            |
+---------------+----------------------------------------+----------------------------------------------------------+--------------------------+----------------------------------+
| 0xBF          | CMD_LOAD_BYTE_AS_PATTERN_AND_CP        | Read number of bytes to write from next byte             | Instead of using CMD for the value, write (next byte val)+1 |
|               |                                        |                                                          | times.                                                      |
+---------------+----------------------------------------+----------------------------------------------------------+--------------------------+----------------------------------+
| 0xDF          | CMD_USE_LAST_PATTERN_AND_CP            | Read number of bytes to write from next byte             | Instead of using CMD for the value, write (next byte val)+1 |
|               |                                        |                                                          | times.                                                      |
+---------------+----------------------------------------+----------------------------------------------------------+--------------------------+----------------------------------+
| 0xFF          | CMD_CYCLE_PATTERN_AND_CP__NEXT         | Read number of bytes to write from next byte             | Instead of using CMD for the value, write (next byte val)+1 |
|               |                                        |                                                          | times.                                                      |
+---------------+----------------------------------------+----------------------------------------------------------+--------------------------+----------------------------------+

Decompression
-------------
To decompress, simply read the compressed data start to finish  and follow the instructions of the command bytes.

The decompression algorithm needs to know the size of decompressed data. If stops when it has written that amount
of bytes.

The decompressor in this repository works using an optimized version of the algorithm
by psy_commando, that always reads and writes 16bits and deals with "leftover" bytes
separately. For the specific implementation details for this, see
`psy_commando's documentation on this algorithm`_.

.. _psy_commando's documentation on this algorithm: https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0&preview=BMA-BPL-BPC-BPA.txt

Compression
-----------
TODO for this documentation. But the general notes from `Generic NRL`_ basically apply, just with the different CMDs.
Keep in mind, you can store more bytes to copy using the special CMDs, and remember to keep track of the two pattern buffers you have!

Credits
-------
Without the following people, this implementation wouldn't have been possible:


- psy_commando_ (C++ implementation, documentation and most of the research work!)

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- `Project Pokémon documentation`_


.. Links:

.. _Project Pokémon documentation:  https://projectpokemon.org/docs/mystery-dungeon-nds/nrl-compression-r112/

.. _psy_commando:                   https://github.com/PsyCommando/

.. _Generic NRL:                    https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression/generic_nrl
