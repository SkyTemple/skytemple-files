dungeon.bin file handler
========================

The ``dungeon.bin`` file is a `pack file`_.

It contains 1036 files. This file handler gives a convenient way to access them,
and provides "file names" to access them by (created by SkyTemple, not actually
from ROM).

You can find an index of all files below.

This file handler package also contains some file handlers for some formats stored exclusively
in this bin pack file (as far as we know right now), such as some handlers for images and
palettes.

Usage
-----
Use the class ``DungeonBinHandler`` of the ``handler`` module, to open and save
the binary ``dungeon.bin`` files. The model that the handler returns is in the
module ``model``.

You can access individual files by accessing them by index from the model (eg. ``model[0]``),
or by using a file name with ``model.get(file_name)``. See the model class for more information.

Iterating over the model yields the models of the contained files, in order.

File index
----------

File names and types
--------------------
A list of file names and file type handlers is stored as part of the static ppmdu XML configuration.

It can be found in the ``_resources/ppmdu_config/pmd2dungeondata.xml``.

Credits
-------
Without the following people, this implementation wouldn't have been possible:

- psy_commando_ (documentation and most of the research work!)

Based on following documentations:

- `psy_commando Dropbox`_


.. Links:

.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0

.. _psy_commando:                   https://github.com/PsyCommando/

.. _pack file:                      https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/container/bin_pack
