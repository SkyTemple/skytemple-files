|logo|

SkyTemple Files
===============

|build| |pypi-version| |pypi-downloads| |pypi-license| |pypi-pyversions| |discord|

.. |logo| image:: https://raw.githubusercontent.com/SkyTemple/skytemple/master/skytemple/data/icons/hicolor/256x256/apps/skytemple.png

.. |build| image:: https://img.shields.io/github/workflow/status/SkyTemple/skytemple-files/Build,%20test%20and%20publish
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

The main handlers for file types can be found in the members of the class ``skytemple_files.common.types.file_types.FileType``.

You can find the handlers inside the packages of this Python package, with ``README.rst`` files explaining the
file formats. Additional documentation for misc. things can be found in the ``/docs`` directory. For usage examples
see the ``dbg`` packages and the SkyTemple main application.

Directly in the package (``skytemple_files`` directory) you can find a few an example script that help with understanding
how to use this library. After installing the package you will have is as a cli command: ``skytemple_export_maps``.

In addition to the dependencies in the ``requirements.txt`` and ``setup.py``, ARMIPS must
be installed and in the system's ``PATH`` to be able to apply ROM patches.

|kofi|
