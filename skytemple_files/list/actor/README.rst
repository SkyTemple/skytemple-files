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

To save it, use ``common.util.save_ppmdu_config_changes``.

2. Use it directly
~~~~~~~~~~~~~~~~~~

Use the class ``ActorListBinHandler`` of the ``handler`` module, to open
and save models from binary data. The model that the handler returns is in the
module ``model``.

File Format
-----------
WIP.
