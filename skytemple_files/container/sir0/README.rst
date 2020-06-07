SIR0 Format
===========

The SIR0 format is a pretty common wrapper file format with as primary
function wrapping other file formats. It provides a pointer to the format's
"entry point", along with a list of file offsets to the pointers which need to
be translated to NDS memory when the file is loaded.

When a SIR0 file gets loaded into memory, its magic number turns from SIR0 to
SIRO, and all the pointers in the entire file are modified to be offset relative
to the NDS's memory. The second pointer in the SIR header is also set to null
when the file has been loaded and turned into a SIRO.


Usage
-----
Use the class ``Sir0Handler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

The ``wrap`` method can be used to wrap existing binary data. It expects the ``content``,
a list of offsets to pointers (``pointer_offsets`` keyword agument) and optionally a
pointer to the data ``data_pointer``.

Alternatively the method ``wrap_obj`` can also be set to wrap an instance of ``Sir0Serializable``.

File Format
-----------

Please see `Project Pokémon`_ for the file type documentation.

.. _Project Pokémon: https://projectpokemon.org/docs/mystery-dungeon-nds/sir0siro-format-r46/
