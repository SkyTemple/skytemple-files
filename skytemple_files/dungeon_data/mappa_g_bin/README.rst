``mappa_g*.bin`` File Format
============================
XYZ

Usage
-----
Use the class ``MappaGBinHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

The ``mappa_g*.bin`` files are normally Sir0 wrapped, so the handler works with Sir0 wrapped models by default.
See the handler class for more details.

File Format
-----------
XYZ

Color entry
~~~~~~~~~~~
XYZ TBD - this table is only here for later.
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
| Offset  | Length | Type                  | Name                  | Description                                                 |
+=========+========+=======================+=======================+=============================================================+
| 0x00    | 2      | uint16                | NumberColors          | The amount of frames/colors that this color                 |
|         |        |                       |                       | entry cycles through.                                       |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
| 0x02    | 2      | uint16                | DurationPerFrame      | Time in game frames to hold a single palette frame for      |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
|         | Varies | List of `Color`_      | ColorFrames           | One color per NumberColors.                                 |
|         |        |                       |                       | If NumberColors == 0, this contains one NULL color          |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+

Credits
-------
Without the following people, this implementation wouldn't have been possible:

- End_ (documentation on the mappa.bin file format)
- psy_commando_ (research work)
- Aissurteivos_ (research work)
- OgreGunner_ (research work)

You can find more documentation here:

- `Dropbox by psy_commando`_
- `Google Doc by End`_
- `Randomizer by Aissurteivos`_
- `Gamefaqs Thread by OgreGunner`_

(There are probably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

.. Links:

.. _End:                            https://projectpokemon.org/home/profile/68315-end45/
.. _Aissurteivos:                   https://github.com/Aissurteivos/
.. _psy_commando:                   https://github.com/PsyCommando/
.. _OgreGunner:                     https://gamefaqs.gamespot.com/boards/938930-pokemon-mystery-dungeon-explorers-of-darkness/50597686

.. _Google Doc by End:              https://docs.google.com/document/d/1UfiFz4xAPtGd-1X2JNE0Jy2z-BLkze1PE4Fo9u-QeYo/edit
.. _Randomizer by Aissurteivos:     https://github.com/Aissurteivos/mdrngzer/blob/master/doc/rom.md
.. _Gamefaqs Thread by OgreGunner:  https://gamefaqs.gamespot.com/boards/938930-pokemon-mystery-dungeon-explorers-of-darkness/50597686
.. _Dropbox by psy_commando:        https://www.dropbox.com/sh/8on92uax2mf79gv/AAB2efAZ8qMTdxct15QQGJoLa/mappa_g_.txt?dl=0
