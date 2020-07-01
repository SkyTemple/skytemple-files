AT4PN File Format
=================

The AT4PN container is a format used to contain image data.

Putting them into the ``compression_container`` package actually isn't very
acurate, because as it turns out, the image data isn't compressed at all..

Usage
-----
Use the class ``At4pnHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------

+---------+--------+-----------+---------------------+------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00    | 5      | string    | Magic Number        | ASCII "AT4PN"                                               |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x05    | 2      | uint16le  | Data Length         | The length of ``Data``.                                     |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x07    | Varies |           | Data                | The raw image data as 4bpp, usually tiled 8x8.              |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+

Credits
-------
I didn't do much of the work figuring out the file format. Without the following people, this implementation
wouldn't have been possible:

- psy_commando_ (C++ implementation, documentation and most of the research work!)

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- `psy_commando Dropbox`_


.. Links:

.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0

.. _psy_commando:                   https://github.com/PsyCommando/
