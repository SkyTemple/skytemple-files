Creating Patch Packages
=======================

Patch packages contain ROM patches, the XML definitions
and the Python logic for applying them.

The SkyTemple core patches are instead directly contained in the core ppmdu XML
configuration and the ``skytemple_files.patch`` package.

However as an example for this mechanism, the ``ActorLoader`` patch is also contained
in the ``actor_loader.skypatch`` archive.

Applying Patch Packages
-----------------------
To apply a patch file, load it via the ``Patcher``:

.. code:: python

    from ndspy.rom import NintendoDSRom
    from skytemple_files.common.util import get_ppmdu_config_for_rom
    from skytemple_files.patch.patches import Patcher

    in_rom = NintendoDSRom.fromFile('my_rom.nds'))

    # Load PPMDU config
    config = get_ppmdu_config_for_rom(in_rom)

    patcher = Patcher(in_rom, config)
    patcher.add_pkg('my_patch.skypatch')
    patcher.apply('MyPatchName')

Creating Patch Packages
-----------------------
A patch package is a ZIP file with the file contents as described below. The
should have the file extension ``.skypatch``.

config.xml
~~~~~~~~~~
TODO: Documentation for this. For now see the skypatch file in this dir as an
example. If you would like to write this documentation, please open a Pull Request!

patch.py
~~~~~~~~
TODO: Documentation for this. For now see the skypatch file in this dir as an
example. If you would like to write this documentation, please open a Pull Request!

asm_patches/eos/{na,eu,jp}
~~~~~~~~~~~~~~~~~~~~~~~~~~
TODO: Documentation for this. For now see the skypatch file in this dir as an
example. If you would like to write this documentation, please open a Pull Request!
