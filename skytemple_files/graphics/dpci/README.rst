DPCI File Format
================
Contains 8x8px 4bpp indexed images. Those images are the dungeon tiles used by the game.

This file format, used togehter with `DPC`_ is the equivalent of `BPC`_ files but for dungeons.

The name is not official.

The file can only be found AT4PX compressed in the dungeon.bin file.

Usage
-----
Use the class ``DpciHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

To read/write the AT4PX compressed versions of this file instead, you can
use the file handler in ``skytemple_files.container.dungeon_bin.sub.at4px_dpci``.

File Format
-----------
Contains a stream of 8x8px 4bpp indexed images (tiles). The tiles use only 16 colors for palettes.

.. Links:

.. _DPC:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpc
.. _BPC:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpc
