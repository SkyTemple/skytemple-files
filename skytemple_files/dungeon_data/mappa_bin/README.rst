``mappa_*.bin`` File Format
===========================
The ``mappa_s.bin`` file in the  ``BALANCE`` directory contains data for dungeon floor generation.

Usage
-----
Use the class ``MappaBinHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

The ``mappa_*.bin`` files are normally Sir0 wrapped, so the handler works with Sir0 wrapped models by default.
See the handler class for more details.

File Format
-----------
For documentation, please see the `Dropbox by psy_commando`_ and the `Google Doc by End`_.

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

.. _Frostbyte:                      https://github.com/Frostbyte0x70/
.. _Aissurteivos:                   https://github.com/Aissurteivos/
.. _psy_commando:                   https://github.com/PsyCommando/
.. _OgreGunner:                     https://gamefaqs.gamespot.com/boards/938930-pokemon-mystery-dungeon-explorers-of-darkness/50597686

.. _Google Doc by End:              https://docs.google.com/document/d/1UfiFz4xAPtGd-1X2JNE0Jy2z-BLkze1PE4Fo9u-QeYo/edit
.. _Randomizer by Aissurteivos:     https://github.com/Aissurteivos/mdrngzer/blob/master/doc/rom.md
.. _Gamefaqs Thread by OgreGunner:  https://gamefaqs.gamespot.com/boards/938930-pokemon-mystery-dungeon-explorers-of-darkness/50597686
.. _Dropbox by psy_commando:        https://www.dropbox.com/sh/8on92uax2mf79gv/AACQ4alDuQl9jTCM_OYI6J-Oa/Mappa.txt?dl=0
