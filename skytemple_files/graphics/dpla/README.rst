DPLA File Format
================
DPLA contains animations for colors. The number of colors stored is usually a multiple of 16,
each of these 16-color pairs is considered a palette.

For each of the color entries an arbitrary amount of colors can be found. The color will cycle
through all of the colors in this list as part of a palette animation.

This is meant to replace the palettes 11 and 12 in `DPL`_ palettes. The first 16 colors replace
and animate palette 11 and the last 16 colors replace and animate palette 12 [this is yet to be
tested, as of writing!].

This file format, used togehter with `DPL`_ is the equivalent of `BPL`_ files but for dungeons.

The name is not official.

The file can only be found SIR0 wrapped in the dungeon.bin file. The pointers point to the start
of each color entry.

Usage
-----
Use the class ``DplaHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

To read/write the SIR0 wrapped versions of this file instead, you can
use the file handler in ``skytemple_files.container.dungeon_bin.sub.sir0_dpla``.

File Format
-----------
The file consists of two parts:
- a list of pointers (uint32) for each color entry
- the color entries

If wrapped in Sir0 the content data pointer points to the list of pointers.

Color entry
~~~~~~~~~~~
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
| Offset  | Length | Type                  | Name                  | Description                                                 |
+=========+========+=======================+=======================+=============================================================+
| 0x00    | 2      | uint16                | NumberColors          | The amount of frames/colors that this color                 |
|         |        |                       |                       | entry cycles through.                                       |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
| 0x02    | 2      | uin16                 | Unk2                  | Probably the speed / duration to hold a frame!              |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | Varies | List of `Color`_      | ColorFrames           | One color per NumberColors.                                 |
|         |        |                       |                       | If NumberColors == 0, this contains one NULL color          |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+

Color
~~~~~
4 byte RGBx color, with the "x" always being 128.

Credits
-------
Without the following people, this implementation wouldn't have been possible:

- psy_commando_ (documentation and most of the research work!)

Much of the reverse-engineering work is based on the MapBG file formats. See those file handlers
for more credits!

(There are probably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

.. Links:

.. _psy_commando:                   https://github.com/PsyCommando/

.. _DPL:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpl
.. _BPL:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpl
