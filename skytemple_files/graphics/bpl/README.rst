BPL File Format
===============
Contains up to 16 16-color palettes for map backgrounds. Also optionally contains an additional
palette used for palette animation, and settings for palette animations.

The first color of each palette is always transparent and is omitted in the data!

Used together with it's BPC_, BMA_ and BPA_ files. See `bg_list.dat`_.

Usage
-----
Use the class ``BplHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------

+---------+--------+-----------+-----------------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                        | Description                                                 |
+=========+========+===========+=============================+=============================================================+
| 0x00    | 2      | uint16le  | Number of Palettes          | How many palettes are stored in the file (1-16)             |
+---------+--------+-----------+-----------------------------+-------------------------------------------------------------+
| 0x02    | 2      | uint16le  | Has Palette                 | Boolean (0/1). Whether or not this palette contains the     |
|         |        |           | Animations                  | List of `Animation Specification`_ and Animation Palette    |
|         |        |           |                             | blocks.                                                     |
+---------+--------+-----------+-----------------------------+-------------------------------------------------------------+
| 0x04    | Varies | Array of  | Palettes                    | Up to 16 (see 0x00) 15 color palettes. Each color is stored |
|         |        | RGBx      |                             | as 4 bytes (RGBx), with the 4th byte always 0x00. 15 colors,|
|         |        |           |                             | because the color at index 0 is not stored (always 0,0,0,0).|
+---------+--------+-----------+-----------------------------+-------------------------------------------------------------+
|         | Varies | Array     | List of                     | Settings for the palette animation for each palette. Length |
|         |        |           | `Animation Specification`_  | of entries is stored in 0x00. Only exists if 0x02 > 0       |
+---------+--------+-----------+-----------------------------+-------------------------------------------------------------+
|         | Varies | Array of  | Animation Palette           | An unknown amount of animation colors. The colors end at the|
|         |        | RGBx      |                             | end of the file. RGBx again, 4th color byte is always 0x00. |
|         |        |           |                             | 15 colors make one "frame" of animation (no transparent)    |
+---------+--------+-----------+-----------------------------+-------------------------------------------------------------+

Animation Specification
~~~~~~~~~~~~~~~~~~~~~~~
Seems to control, how a single palette is affected by palette animation. It is unknown what the values mean,
but they probably control the speed and which color(s?) to change.

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00    | 2      | uint16le  | duration_per_frame  | Time in game frames to hold a single palette frame for      |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x02    | 2      | uint16le  | number_of_frames    | Number of frames. This is also usually the length of frames |
|         |        |           |                     | in animation palette, but it can also be less.              |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+

Credits
-------
Without the following people, this implementation wouldn't have been possible:

- psy_commando_ (C++ implementation, documentation and most of the research work!)

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- `psy_commando Dropbox`_


.. Links:

.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0

.. _psy_commando:                   https://github.com/PsyCommando/

.. _BPC:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpc
.. _BMA:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bma
.. _BPA:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpa
.. _BPL:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpl
.. _bg_list.dat:                    https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bg_list_dat
