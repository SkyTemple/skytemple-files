LSD File Format
===============
LSD files contains a list of names that matches all SSA + SSB pairs in a level's directory.

SSE and SSS files are NOT matched against SSSBs using these files. They are matched
using a defined naming pattern (eg. ``enter.sse`` -> ``enterXX.ssb``)

Usage
-----
Use the class ``LsdHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

To get a meaningful list of all files used by the script engine,
use the function ``load_script_files`` of the module ``skytemple_files.common.script_util``.

The LSD file for a level is in the ``MapEntry.lsd`` field. Files that should be stored in the
LSD file are in the ``MapEntry.ssas`` field, but please note that the function doesn't collect
the SSA+SSB pairs using the LSD file but rather by collecting all files in the directory.

File Format
-----------

+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
| Offset  | Length | Type                  | Name                  | Description                                                 |
+=========+========+=======================+=======================+=============================================================+
| 0x0000  | 2      | unit16le              | Number of entries     | Number of SSA+SSB pairs                                     |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+
| 0x0002  | Varies | Array of 8 byte       | Entry                 | Name of the SSA and SSB files without file extension.       |
|         |        | strings               |                       |                                                             |
+---------+--------+-----------------------+-----------------------+-------------------------------------------------------------+

Strings are always 8 bytes long, unusued bytes are 0.

Credits
-------
Without the following people, this implementation wouldn't have been possible:

- psy_commando_ (Documentation and research work)
- `Nerketur Kamashi`_ (Documentation, research work and reference implementation (PMDSE))
- Aissurteivos

(There are propably more people that worked on this! I collected the names from existing documentation I found.
If I missed you, please open an Issue!)

Based on following documentations:

- `Project Pokémon documentation`_
- `psy_commando Dropbox`_


.. Links:

.. _Project Pokémon documentation:  https://projectpokemon.org/docs/mystery-dungeon-nds/
.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0

.. _psy_commando:                   https://github.com/PsyCommando/
.. _Nerketur Kamashi:              https://projectpokemon.org/home/profile/49243-nerketur/
