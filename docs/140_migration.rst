SkyTemple Files 1.4.0 Deprecation Migration Guide
=================================================
SkyTemple Files 1.4.0 deprecates and removes some APIs found in previous versions.

This document explains some common cases primarily found in patches and how to migrate to using the new
mechanisms while keeping backwards compatibility.

Deprecation of ``read_{s|u}int{be|le}`` and ``write_{s|u}int{be|le}``
---------------------------------------------------------------------
Functions like `read_uintle` and `write_sintle` in `skytemple_files.common.util` have been deprecated and replaced
with more specialized functions like `read_u8` or `write_u32`. If integers of dynamic sizes based on paremters need to
be read, `read_dynamic` can be used instead.

The deprecated functions will be removed in SkyTemple Files 1.6.0.

Example
~~~~~~~
Replace the following code...:

.. code:: python

    from skytemple_files.common.util import read_uintle

    def do_something(data: bytes):
        output = read_uintle(data, 0x12, 2)

...with:

.. code:: python

    from skytemple_files.common.util import read_u16

    def do_something(data: bytes):
        output = read_u16(data, 0x12)

PPMDU Binary deprecation
------------------------
SkyTemple 1.4.0 deprecates and partially removes the binary and symbol definitions
(ARM9, ARM7, Overlays) that were present in the ``pmd2data.xml``. They have been replaced with
`pmdsky-debug-py`, which provides symbol data via `pmdsky-debug`_.

The following things have been removed:

- Any information on symbols in objects previously found in `Pmd2Data.binaries`. All types revolving
  around this have also been removed (``Pmd2Binary*`` classes).
- The return value of `Pmd2Data.binaries` has been replaced with a mostly useless replacement object. It can
  still be accessed like a dict to retrieve binaries like before (eg. `data.binaries['arm9.bin`]`), but these items
  can only be used with the deprecated `get_binary_from_rom_ppmdu` and `set_binary_in_rom_ppmdu`, see below).
  It contains, as stated above, no useful information anymore and is not of instance `Pmd2Binary`.
- The ``Binaries`` section has been fully removed from the ``pmd2data.xml``.

The following functionality has been deprecated (will raise deprecation warnings and will be removed in
SkyTemple Files 1.6.0):
- Retrieving `Pmd2Data.binaries`.
- `get_binary_from_rom_ppmdu` and `set_binary_in_rom_ppmdu`. However right now they work just as before,
  taking in a value from an item of `Pmd2Data.binaries`.

Replacements:
- Use binary and symbol information of pmdsky-debug-py, provided via `Pmd2Data.bin_sections` and
  `Pmd2Data.extra_bin_sections` (for SkyTemple extensions, such as info on overlay 36).
- Use `get_binary_in_rom` and `set_binary_in_rom`. These use the before mentioned pmdsky-debug-py references.

Example
~~~~~~~
Replace the following code...:

.. code:: python

    from ndspy.rom import NintendoDSRom
    from skytemple_files.common.ppmdu_config.data import Pmd2Data

    from skytemple_files.common.util import get_binary_from_rom_ppmdu

    def do_something(rom: NintendoDSRom, config: Pmd2Data):
        binary_data = get_binary_from_rom_ppmdu(rom, config.binaries['overlay/overlay_0029.bin'])

...with:

.. code:: python

    from ndspy.rom import NintendoDSRom
    from skytemple_files.common.ppmdu_config.data import Pmd2Data

    from skytemple_files.common.util import get_binary_from_rom

    def do_something(rom: NintendoDSRom, config: Pmd2Data):
        binary_data = get_binary_from_rom(rom, config.bin_sections.overlay29)


.. _pmdsky-debug: https://github.com/UsernameFodder/pmdsky-debug


Backwards compatibility
-----------------------
To keep backwards compatibility, check the version of skytemple-files and use the old
or new functionality accordingly.

We recommend you phase out the backwards compatibility after the release of SkyTemple Files 1.6.0.

.. code:: python

    from importlib.metadata import version
    from packaging.version import parse as parse_version

    from ndspy.rom import NintendoDSRom
    from skytemple_files.common.ppmdu_config.data import Pmd2Data

    def do_something(data: bytes, rom: NintendoDSRom, config: Pmd2Data):
        skytemple_files_version = parse_version(version('skytemple-files'))

        if skytemple_files_version >= parse_version('1.4.0a0'):  # a0 is optional, but makes sure this also works for pre-releases.
            # SkyTemple Files 1.4
            # NOW import functions we know exist in 1.4:
            from skytemple_files.common.util import read_u16, get_binary_from_rom
            output = read_u16(data, 0x12)
            binary_data = get_binary_from_rom(rom, config.bin_sections.overlay29)

        else:
            # SkyTemple Files < 1.4
            # NOW import old functions.
            from skytemple_files.common.util import read_uintle, get_binary_from_rom_ppmdu
            output = read_uintle(data, 0x12, 2)
            binary_data = get_binary_from_rom_ppmdu(rom, config.binaries['overlay/overlay_0029.bin'])

.. note::

    This requires `packaging` to be installed. This is usually the case, since it's also a
    dependency of SkyTemple (the GUI app) and setuptools.
