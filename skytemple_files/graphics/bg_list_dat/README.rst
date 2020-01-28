bg_list.dat File Format
=======================

``/MAP_BG/bg_list.dat``:
Part of the map backgrounds building process.
Contains a mapping of level ids to BPC_, BMA_, BPA_ and BPL_ files.

Usage
-----
Use the class ``BgListDatHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

The model can be used to load the BPC_, BMA_, BPA_ and BPL_ files.

File Format
-----------

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x000   |        |           | Array of            | A list of level entries, the index is the level id.         |
|         |        |           | `Level Entry`_      |                                                             |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+

Level Entry
~~~~~~~~~~~
A single entry is 88 bytes in size.
All Strings have a fixed length of 8 characters and are also null terminated, if shorter.

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00    | 8      | string    | BPL_ name           | Never null.                                                 |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x08    | 8      | string    | BPC_ name           | Never null.                                                 |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x10    | 8      | string    | BMA_ name           | Never null.                                                 |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x18    | 8      | string    | BPA_ 1 name         | First BPC layer assigned BPA - Number 1. Can be null.       |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x20    | 8      | string    | BPA_ 2 name         | First BPC layer assigned BPA - Number 2. Can be null.       |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x28    | 8      | string    | BPA_ 3 name         | First BPC layer assigned BPA - Number 3. Can be null.       |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x30    | 8      | string    | BPA_ 4 name         | First BPC layer assigned BPA - Number 4. Can be null.       |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x38    | 8      | string    | BPA_ 5 name         | Second BPC layer assigned BPA - Number 1. Can be null.      |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x40    | 8      | string    | BPA_ 6 name         | Second BPC layer assigned BPA - Number 2. Can be null.      |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x48    | 8      | string    | BPA_ 7 name         | Second BPC layer assigned BPA - Number 3. Can be null.      |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x50    | 8      | string    | BPA_ 8 name         | Second BPC layer assigned BPA - Number 4. Can be null.      |
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

.. _BPC:                            https://github.com/SkyTemple/skytemple_files/blob/master/skytemple_files/graphics/bpc
.. _BMA:                            https://github.com/SkyTemple/skytemple_files/blob/master/skytemple_files/graphics/bma
.. _BPA:                            https://github.com/SkyTemple/skytemple_files/blob/master/skytemple_files/graphics/bpa
.. _BPL:                            https://github.com/SkyTemple/skytemple_files/blob/master/skytemple_files/graphics/bpl