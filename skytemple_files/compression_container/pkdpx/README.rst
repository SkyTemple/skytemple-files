PKDPX File Format
=================

The PKDPX format is used as a compressed container for generic data.
Unlike its specialized equivalent the AT4PX format, the PKDPX format can contain any
kind of data.

Just like the AT4PX format, its not unusual to find PKDPX files wrapped inside a
SIR0 container! Its content is compressed using a custom compression format dubbed
PX Compression for the lack of a better name.

Usage
-----
Use the class ``PkdpxHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------

Please see `Project Pokémon`_ for the file type documentation.

.. _Project Pokémon: https://projectpokemon.org/docs/mystery-dungeon-nds/pkdpx-file-format-r44/

