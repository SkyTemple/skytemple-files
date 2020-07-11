DPL File Format
===============
A raw list of RGBx colors, usually to be read into 16x16 color palettes.

This file format, used together with `DPLA`_ is the equivalent of `BPL`_ files but for dungeons.

The name is not official.

Usage
-----
Use the class ``DplHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

The file can be found stored raw in the dungeon.bin.

File Format
-----------
Contains a stream of 4 byte RGBx color, with the "x" always being 128.

Usually pairs of 16 colors build up one palette, the first palette will usually be rendered transpaent by the game.

.. Links:

.. _DPLA:                           https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/dpla
.. _BPL:                            https://github.com/SkyTemple/skytemple-files/blob/master/skytemple_files/graphics/bpl
