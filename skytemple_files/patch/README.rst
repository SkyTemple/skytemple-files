Patches
=======
Utilities for applying ROM patches.

To apply a patch or check it's status, use the ``patches.Patcher`` class. By default
the ``Patcher`` class can work with core patches defined in the XML of SkyTemple that
have handlers in the ``handler`` package. To apply Patch Packages
(see also ``docs/patch_packages`` directory) ``patches.Patcher.add_pkg`` may be used.

The ``patches`` module also contains ``PatchType``, via which handlers for core patches
can be retrieved.

The ``arm_patcher`` module contains a module for applying ARMIPS patches.
ARMIPS must be installed and in the ``PATH``.

The ``list_extractor`` module extracts binary lists from the game into separate files, wrapped in SIR0.
It implements the ``LooseBinFiles`` logic of the ppmdu configuration. Handlers may use it.

The data for applying the core patches in part of the ppmdu configuration (``pmd2data.xml``),
it is available via Pmd2Config (see package ``common.ppmdu_config``).

The ASM files for the core patches are stored in the ``_resources/ppmdu_patches`` directory.

List of patches
---------------

Actor list patch (ActorLoader)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The actor list patch changes the loading logic for the actor list so, that instead
of loading this information directly from the arm9 binary, it is loaded from an extra
file called ``BALANCE/actor_list.bin`` (name may be specified via ppmdu config, see
documentation of handler). The handler also uses the ``extractor`` to copy the existing
list to that file, before applying the patch

This list can be read with the filetype handler for ``ACTOR_LIST_BIN``
(``skytemple_files.list.actor.handler``).
