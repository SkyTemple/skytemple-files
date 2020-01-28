PX Compression
==============

The PX compression format, for a lack of better name, is a custom compression format.
Most of the files using this compression method are contained within either PKDPX_ or AT4PX_ containers.

Usage
-----
Use the class ``PxHandler`` of the ``handler`` module, to compress and decompress PX binary data.

Overview of the Format
----------------------
The format itself is nothing wildly complex. It revolve around using what we'll call a command byte.

The command byte is what will tell the decompressor what to do with the data that comes after it.
The command byte can hold information for up to 8 "operations" to do on the data that follows.
Each operation is represented as a bit.
And each operation may use one or more byte(s) of data after the command byte.

If the highest bit is 1, we copy the first following byte as-is.
If its 0, we compare the value of the high nybble of the following byte to the list of control flags.
And depending on which flag match, or if none match, we'll know what to do next.

Note that, those control flags are always "0n" where "n" is an hexadecimal value from 0 to F.
Also, note that, these flags are computed on a file by file basis!
They're "tailor-made" for each individual file.

Decompression and Compression
-----------------------------
Please see the `Project Pokémon documentation`_.

Credits
-------
I didn't do much of the work figuring out the file format. Without the following people, this implementation
wouldn't have been possible:

- psy_commando_ (C++ implementation, documentation and most of the research work! The compressor and decompressor
  in this package are directly based on their C++ implementation!)
- Zhorken_ (Figured out PX compression and header)

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- `Project Pokémon documentation`_ (Documentation mostly adapted from there!)
- `psy_commando Dropbox`_


.. Links:

.. _Project Pokémon documentation:  https://projectpokemon.org/docs/mystery-dungeon-nds/pmd2-px-compression-r45/
.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0

.. _psy_commando:                   https://github.com/PsyCommando/
.. _Zhorken:                        https://github.com/Zhorken

.. _AT4PX:                          https://github.com/SkyTemple/skytemple_files/blob/master/skytemple_files/compression_container/at4px
.. _PKDPX:                          https://github.com/SkyTemple/skytemple_files/blob/master/skytemple_files/compression_container/pkdpx
