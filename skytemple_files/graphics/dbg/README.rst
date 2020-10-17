DBG File Format
===============
Contains background image chunk mappings for boss fights in dungeons, the secret bazar and
other purposes.

This file format is pretty much exactly structured like the layer data of `BMA`_ files,
but without any compression or headers.

This file format references chunks in the `DPC`_, `DPCI`_, `DPL`_ and `DPLA`_ files that come
right before these files in the dungeon.bin.

The name is not official.

The file can only be found SIR0 wrapped and PKDPX compressed in the dungeon.bin file.

Usage
-----
Use the class ``DbgHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

To read/write the SIR0 wrapped and PKDPX compressed versions of this file instead,
you can use the file handler in ``skytemple_files.container.dungeon_bin.sub.sir0_pkdpx_dbg``.

File Format
-----------
A stream of 16-bit unsigned integers. Each integer represents one chunk to place on a 32x32 chunks grid.

.. _DPL:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpl
.. _DPC:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpc
.. _DPCI:                           https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpci
.. _DPLA:                           https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpla
.. _BMA:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bma
