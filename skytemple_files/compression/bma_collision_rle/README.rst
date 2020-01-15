BMA Collision RLE
=================
Very simple Run-Length Encoding compression, that compresses bytes with
the values 0 and 1.

Usage
-----
Use the class ``BmaCollisionRleHandler`` of the ``handler`` module, to compress and decompress binary data.

Command bytes
-------------
The compressed data contains command bytes that determine what to do. Between the command
bytes may be arguments, depending on the command.

There are three different types of operations:

+---------------+-----------------------------+-------------------------------------------------------------+
| CMD           | Name                        | Description                                                 |
+===============+=============================+=============================================================+
| 0x00 - 0x7F   | Write 0s                    | Write CMD+1 bytes of 0.                                     |
+---------------+-----------------------------+-------------------------------------------------------------+
| 0x80 - 0xFF   | Write 1s                    | Write CMD+1-0x80 bytes of 1.                                |
+---------------+-----------------------------+-------------------------------------------------------------+

Decompression
-------------
To decompress, simply read the compressed data start to finish  and follow the instructions of the command bytes.

The decompression algorithm needs to know the size of decompressed data. If stops when it has written that amount
of bytes.

Compression
-----------
Count the numbers of repeating 0s or 1s starting from the current position
and write the CMD for it.
