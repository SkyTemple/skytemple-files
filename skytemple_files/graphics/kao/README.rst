kao File Format
===============

The file ``/FONT/kaomado.kao`` contains character portraits.

The file contains 1,154 slots for portraits. These are directly mapped to the entries in the ``monster.md``,
which means an entry for all of the first gender of all Pokémon (0-600) and an optional entry for the
second genders (601-1,154). If the second gender entry is not defined, the game falls back to using the portrait
of the first gender.

Each slot contains exactly 40 sub-slots. Each of these is assigned an
emotion. See the `Project Pokémon documentation`_ for more details.

Usage
-----
Use the class ``KaoHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00000 | 160    |           | Null Entry          | The first entry in the table of content is entirely filled  |
|         |        |           |                     | with zeros. It is not assigned an index.                    |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x000A0 | 184800 |           | `Table of Content`_ | The table of content goes from here, to the offset of the   |
|         |        |           |                     | first valid pointer in the ToC. More details below in the   |
|         |        |           |                     | `Table of Content`_ section.                                |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x2D1E0 | Varies |           | `Portrait Data`_    | This is where all the portrait data is stored one after the |
|         |        |           |                     | other. More details in the Portraits Data section below.    |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+

Table of Content
~~~~~~~~~~~~~~~~
Each block of 160 bytes represent all possible portrait slots for a single pokemon.
There are 40 potraits slots per pokemon, however not a single pokemon uses its 40 slots.
Each of these slots are 32 bits signed integers containing the offset of the portrait data it refers to.
Most of those slots are filled with a null value.

The null value is particular in that, its not just 0. Its actually calculated by taking the end offset of
the data pointed to by the last valid pointer we've encountered starting from offset 0, and then changing the
sign of the end offset to negative.

For example, if our last valid pointer's value is 0x030058, and the end offset of the data pointed to by
that pointer is 0x03034C. Then the value for any subsequent null entries, until the next non-null one would be:

    ``-( 0x0003034C ) => 0xFFFCFCB4``

All TOC entries have the following structure:

+---------+--------+----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type     | Name                | Description                                                 |
+=========+========+==========+=====================+=============================================================+
| 0x00    | 4      | sint32le | Portrait Pointer 00 | Pointer to the first portrait for this Pokémon              |
+---------+--------+----------+---------------------+-------------------------------------------------------------+
| ... Rest of the pointers ...                                                                                    |
+---------+--------+----------+---------------------+-------------------------------------------------------------+
| 0x9C    | 4      | sint32le | Portrait Pointer 39 | Pointer to the last portrait for this Pokémon               |
+---------+--------+----------+---------------------+-------------------------------------------------------------+

Portrait Data
~~~~~~~~~~~~~
Each portraits is made up of 2 things. A 16 color palette, followed immediately by a `AT`_ compressed container
containing the actual image data for the portrait.

The portraits do not carry any information about their formats. However, we do know that they're all 4 bits per
pixels indexed images, and have a resolution of 40 x 40 pixels. The images are also tiled, which means they're made
up of smaller "images" called tiles. Each tile is 8 x 8 pixels itself. Each tiles are filled linearly with the pixels
contained in the decompressed file. The portraits are made of 5 tiles on their width, and 5 on their height for a total
of 25 tiles.

Structure of one portrait:

+---------+--------+----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type     | Name                | Description                                                 |
+=========+========+==========+=====================+=============================================================+
| 0x00    | 48     |          | Color Palette       | 16 colors RGB color palette (3 bytes RGB). First color is   |
|         |        |          |                     | transparent.                                                |
+---------+--------+----------+---------------------+-------------------------------------------------------------+
| 0x30    | Varies | AT_      | Compressed Image    | This contains the actual image data for the portrait.       |
|         |        |          |                     | Its a compressed AT_ container that contains                |
|         |        |          |                     | the raw pixels of the image. The image itself, once         |
|         |        |          |                     | decompressed, is stored as an indexed 4 bits per            |
|         |        |          |                     | pixels, 40x40, tiled image. Once decompressed each images   |
|         |        |          |                     | has a length of 800 bytes.                                  |
+---------+--------+----------+---------------------+-------------------------------------------------------------+

More Details
------------
See `Project Pokémon documentation`_.

Credits
-------
I didn't do much of the work figuring out the file format. Without the following people, this implementation
wouldn't have been possible:

- psy_commando_ (C++ implementation, documentation and most of the research work!)
- Zhorken_ (Figured out PX compression and Pokémon and emotion names)

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- `Project Pokémon documentation`_ (Documentation mostly adapted from there!)
- `psy_commando Dropbox`_


.. Links:

.. _Project Pokémon documentation:  https://projectpokemon.org/docs/mystery-dungeon-nds/kaomadokao-file-format-r54/
.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0

.. _psy_commando:                   https://github.com/PsyCommando/
.. _Zhorken:                        https://github.com/Zhorken

.. _AT:                             https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression_container/common_at
