Pack File Format
================

The pack file format is used to pack multiple files into one binary container.

Usage
-----
Use the class ``BinPackHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

The files can be indexed from the model. They are returned as bytes. You
can use another handler to read the data back in. To save the data back
to the pack, assign it at the same index at the model and use the ``handler``
module to serialize the pack.

File Format
-----------

Please see `Project Pokémon`_ for the file type documentation.

.. _Project Pokémon: https://projectpokemon.org/docs/mystery-dungeon-nds/pmd2-pack-file-format-r42/
