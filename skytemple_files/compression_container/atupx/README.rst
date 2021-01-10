ATUPX File Format
=================

The ATUPX container is a custom format.

Its content is compressed using a custom compression format dubbed `Custom999`_ Compression.
This compression format is a modified version of the AT6P container compression format used in 999.
Changes made to the original algorithm are documented in the code.
This isn't natively supported by the game, but can be added via asm patching.

Usage
-----
Use the class ``AtupxHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00    | 5      | string    | Magic Number        | ASCII "ATUPX"                                               |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x05    | 2      | uint16le  | Container Length    | The length from the beginning of the header(!) to the end   |
|         |        |           |                     | of the compressed data.                                     |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x07    | 4      | uint16le  | Decompressed data   | The length of the dcompressed data.                         |
|         |        |           | Length              |                                                             |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x0b    | Varies | Custom999_| Custom999_                                                                        |
|         |        |           | Compressed Data                                                                   |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+

Credits
-------
I didn't do much of the work figuring out the file format. Without the following people, this implementation
wouldn't have been possible:

- pleoNeX and CUE (for the decompression algorithm of the original format).

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- The `AT6P Decompressor Class`_ (Documentation mostly adapted from there!)


.. Links:

.. _AT6P Decompressor Class:  https://github.com/pleonex/tinke/blob/master/Plugins/999HRPERDOOR/999HRPERDOOR/AT6P.cs
