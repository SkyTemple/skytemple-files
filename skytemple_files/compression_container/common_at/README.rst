AT File Format
=================

The common file format for AT3PX, AT4PX, PKDPX and AT4PN files.
All those files formats can be swapped when the game needs one of those.

Its not unusual to find AT containers wrapped itself by a SIR0_ container.

Usage
-----
Use the class ``CommonAtHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------

+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| Offset  | Length | Type      | Name                | Description                                                 |
+=========+========+===========+=====================+=============================================================+
| 0x00    | 5      | string    | Magic Number        | Varies depending on the AT container                        |
+---------+--------+-----------+---------------------+-------------------------------------------------------------+
| 0x05    | 2      | uint16le  | Container Length    | For most the length of the whole container                  |
|         |        |           |                     | Only the length of the data for AT4PN files                 |
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
.. _AT3PX:                          https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression_container/at3px
.. _AT4PX:                          https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression_container/at4px
.. _AT4PN:                          https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/compression_container/at4pn
.. _SIR0:                           https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/container/sir0
