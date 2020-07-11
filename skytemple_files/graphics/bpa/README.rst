BPA File Format
===============
Contains 8x8 4bpp animated tiles, used for map backgrounds. The tiles are loaded by BPC_ and inserted
into the BPC tile list. See BPC_ for more details.

The tiles are stored uncompressed. For each frame all tiles are stored right next to each other, this
also means that all tiles in the BPA have the same number of frames.

The images are indexed, the palette for the images is stored in the BPL_ file, and which palette to use is
determined by the tile mappings of the BPC_.

Used together with it's BPC_, BPL_ and BMA_ files. See `bg_list.dat`_.

Usage
-----
Use the class ``BpaHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00    | 2      | uint16le  | Number of Tiles     | The number of individual tiles.                             |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x02    | 2      | uint16le  | Number of Frames    | The number of frames for each tile.                         |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x04    | Varies | Array     | `Frame Info`_       | Settings for each frame. One entry per frame.               |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
|         | 32     | 4bpp 8x8  | Tile 0 Frame 0      | First tile, first frame                                     |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| ... Rest of the tiles for frame 0 ...                                                                            |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
|         | 32     | 4bpp 8x8  | Tile X Frame 0      | Last tile (X = Number tiles -1), first frame                |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| ... Rest of the tiles for the rest of the frames ...                                                             |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
|         | 32     | 4bpp 8x8  | Tile 0 Frame Y      | First tile, last frame (Y = Number frames - 1)              |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| ... Rest of the tiles for frame Y ...                                                                            |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
|         | 32     | 4bpp 8x8  | Tile X Frame Y      | Last tile, last frame                                       |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+

Frame Info
~~~~~~~~~~

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00    | 2      | uint16le  | duration_per_frame  | Time in game frames to hold a single image frame for        |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x02    | 2      | uint16le  | unk2                | Always 0x00? above may also be a uint32le instead!          |
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
