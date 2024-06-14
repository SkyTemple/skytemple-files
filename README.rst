|logo|

SkyTemple Files
===============

|build| |pypi-version| |pypi-downloads| |pypi-license| |pypi-pyversions| |discord|

.. |logo| image:: https://raw.githubusercontent.com/SkyTemple/skytemple/master/skytemple/data/icons/hicolor/256x256/apps/skytemple.png

.. |build| image:: https://img.shields.io/github/actions/workflow/status/SkyTemple/skytemple-files/build-test-publish.yml
    :target: https://pypi.org/project/skytemple-files/
    :alt: Build Status

.. |pypi-version| image:: https://img.shields.io/pypi/v/skytemple-files
    :target: https://pypi.org/project/skytemple-files/
    :alt: Version

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/skytemple-files
    :target: https://pypi.org/project/skytemple-files/
    :alt: Downloads

.. |pypi-license| image:: https://img.shields.io/pypi/l/skytemple-files
    :alt: License (GPLv3)

.. |pypi-pyversions| image:: https://img.shields.io/pypi/pyversions/skytemple-files
    :alt: Supported Python versions

.. |discord| image:: https://img.shields.io/discord/710190644152369162?label=Discord
    :target: https://discord.gg/skytemple
    :alt: Discord

.. |kofi| image:: https://www.ko-fi.com/img/githubbutton_sm.svg
    :target: https://ko-fi.com/I2I81E5KH
    :alt: Ko-Fi

Python library to work with the files inside the ROM of Pokémon Mystery Dungeon Explorers of Sky.

In addition to the dependencies in the ``requirements.txt`` and ``pyproject.toml``, ARMIPS must
be installed and in the system's ``PATH`` to be able to apply ROM patches.

File API v2
~~~~~~~~~~~
The module ``skytemple_files.common.file_api_v2`` contains the main API to work with files and (supported) hardcoded
data from the game, as well as patches.

This API provides two types of data access:

- Assets: Machine- and human-readable versions of the files stored in the game. These are always used primarily if
  they exist. They are specified as part of PMDCollab eos-asset-spec_ for support for best other ROM hacking tools.
- ROM: The actual ROM file where all of the binary serialized files are stored.

If the contents of assets does not match the contents of the file in the ROM, this can be handled in different ways.
Saving data will always always write changes to both the Assets and the ROM.

Information about patches applied via this API are also stored in asset files, to apply the changes again. Same goes
for supported hardcoded data in ARM9/ARM7 or overlays. Note that most patches do not support un-applying, but it should
always be possible to apply assets to an unmodified ROM again.

The main advantage of primarily working via asset files is the ability to share changes with other tools and
collaborators on a project, as well as being able to use the assets in the decomp_. This also allows for some degree
of reproducibility. In theory it should be possible to turn an unmodified ROM into a ROM hack just from its asset files.

Note however that SkyTemple Files can only apply assets which it implements. Some other tools may support editing
other file formats in the ROM, these need to apply their changes on their own.

.. _decomp: https://github.com/pret/pmd-sky.

CLI APIs
~~~~~~~~
SkyTemple Files exposes CLI commands if the extra ``cli`` is enabled (see below). Add the ``--help`` parameter to these
for more information. The implementations are stored in ``skytemple_files.common.cli``.

- ``assets``: Manage unpacking and packing ROMs using the "File API v2".

These APIs are not exposed via a command, they must be run via the Python interpreter directly, eg.
``python -m skytemple_files.common.cli assets``. The SkyTemple GUI app will eventually expose these APIs via it's own ``skytemple`` command.

Classic APIs
~~~~~~~~~~~~
SkyTemple Files provides the following additional APIs which are also relatively stable. Most of these are the underlying
APIs that the "File API v2" uses:

- File Types: ``skytemple_files.common.types.file_types.FileType`` exposes all the file type handlers for all supported
  file formats. These handlers can read/write binary data from the ROM as well as assets.
- Patches: Patches can be loaded and applied via the API in the ``skytemple_files.patch.patches`` directory.
- Pmd2Data: Each ROM has a static configuration model which describes a lot of its properties. Some are replaced with
  dynamic information from the ROM on load, the rest is loaded from PPMDU configuration files. The API is defined
  in ``skytemple_files.common.ppmdu_config.data``, a function to load it given any ROM can be found in
  ``skytemple_files.common.util``. The PPMDU XML files can be found under ``skytemple_files/_resources/ppmdu_config``.
- pmdsky-debug: pmdsky-debug_ information is exposed for each ROM via the Pmd2Data structures. The information is
  available as Python objects via pmdsky-debug-py_.
- Hardcoded data: Functions to read and write hardcoded data from binaries in the ROM (ARM9/ARM7, overlays) can be found
  in ``skytemple_files.hardcoded``.
- SpriteCollab: Sprites and Portraits can be loaded from SpriteCollab using this API. See the "Extras" section below
  for more information.

.. _pmdsky-debug: https://github.com/UsernameFodder/pmdsky-debug
.. _pmdsky-debug-py: https://github.com/SkyTemple/pmdsky-debug-py

Example
~~~~~~~
Directly in the package (``skytemple_files`` directory) you can find an example script that help with understanding
how to use this library. After installing the package you will have is as a cli command: ``skytemple_export_maps``.

The example script does not use the new File API, it uses the classic APIs.

Implementations and Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can find the handlers inside the packages of this Python package, with ``README.rst`` files explaining the
file formats for a lot, but not all of them.
Additional documentation for misc. things can be found in the ``/docs`` directory.

The assets generated by the "File API v2" are defined as part of PMDCollab eos-asset-spec_. The documentation for those
can be found there.

Some file types are implemented both in Python and Rust. The Rust implementations can be found in skytemple-rust_.

.. _skytemple-rust: https://github.com/SkyTemple/skytemple-rust
.. _eos-asset-spec: https://eos-asset-spec.pmdcollab.org

Extras
~~~~~~

spritecollab
------------
With the ``spritecollab`` extra, the package ``skytemple_files.common.spritecollab.client`` is available to
interact with the SpriteCollab GraphQL server for retrieving portrait and sprite assets by the community.

More information:

- https://sprites.pmdcollab.org
- https://spriteserver.pmdcollab.org
- https://github.com/PMDCollab/SpriteCollab
- https://github.com/PMDCollab/spritecollab-srv

cli
---
This extra is required for the CLI APIs to function.

|kofi|
