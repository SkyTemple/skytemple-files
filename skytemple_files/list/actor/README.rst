Actor list
==========

List of actors as a binary file. This file does not exist by default.
The patch ``ActorLoader`` must be applied
(``skytemple_files.patch.patches.PatchType.ACTOR_LOADER``).

Usage
-----

1. Load it via ppmdu ROM configuration (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use ``common.util.get_ppmdu_config_for_rom`` to load the ``Pmd2Data``
object for the ROM. It's ``script_data`` contains a field ``level_entities``.
This field contains this list (if the patch is applied!)

2. Use it directly
~~~~~~~~~~~~~~~~~~
This is useful when you want to modify the data.

Use the class ``ActorListBinHandler`` of the ``handler`` module, to open
and save models from binary data. The model that the handler returns is in the
module ``model``.

The data is Sir0 wrapped, so you probably want to use ``Sir0Handler.wrap_object``
and ``Sir0Handler.unwrap`` instead.

File Format
-----------
WIP.
