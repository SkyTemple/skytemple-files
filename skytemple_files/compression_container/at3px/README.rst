AT3PX File Format
=================

The AT3PX container is a format very similar to AT4PX, the only difference is that the decompressed data field is omitted, 
which free 2 bytes as opposed to AT4PX.
This is natively supported by the game, but never used. This is likely because this format can't provide the decompressed
size, which is used sometimes by the game (but not always!)

Its content is compressed using a custom compression format dubbed `PX`_ Compression for the lack of a better name.

Usage
-----
Use the class ``At3pxHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00    | 5      | string    | Magic Number        | ASCII "AT3PX"                                               |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x05    | 2      | uint16le  | Container Length    | The length from the beginning of the header(!) to the end   |
|         |        |           |                     | of the compressed data.                                     |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x07    | 9      |           | Control Flags       | A list of flags to be used in decompressing the container's |
|         |        |           |                     | content.                                                    |
|         |        |           |                     | More detail about their purpose in the PX_ README.          |
|         |        |           |                     | Flags are stored in lower half of each byte.                |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x10    | Varies | PX_       | PX_ Compressed Data                                                               |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+

Credits
-------
I didn't do much of the work figuring out the file format. Without the following people, this implementation
wouldn't have been possible:

- psy_commando_ (C++ implementation, documentation and most of the research work!)
- Zhorken_ (Figured out PX compression and header)

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- `Project Pokémon documentation`_ (Documentation mostly adapted from there!)
- `psy_commando Dropbox`_


.. Links:

.. _Project Pokémon documentation:  https://projectpokemon.org/docs/mystery-dungeon-nds/at4px-file-format-r40/
.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0

.. _psy_commando:                   https://github.com/PsyCommando/
.. _Zhorken:                        https://github.com/Zhorken

.. _PKDPX:                          https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression_container/pkdpx
.. _SIR0:                           https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/container/sir0
.. _PX:                             https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression/px
