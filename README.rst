|logo|

SkyTemple Files
===============

|build| |pypi-version| |pypi-downloads| |pypi-license| |pypi-pyversions| |discord|

.. |logo| image:: https://raw.githubusercontent.com/SkyTemple/skytemple/master/skytemple/data/icons/hicolor/256x256/apps/skytemple.png

.. |build| image:: https://jenkins.riptide.parakoopa.de/buildStatus/icon?job=skytemple-files%2Fmaster
    :target: https://jenkins.riptide.parakoopa.de/blue/organizations/jenkins/skytemple-files/activity
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
    :target: https://discord.gg/4e3X36f
    :alt: Discord

.. |kofi| image:: https://www.ko-fi.com/img/githubbutton_sm.svg
    :target: https://ko-fi.com/I2I81E5KH
    :alt: Ko-Fi

Python library to work with the files inside the ROM of Pokémon Mystery Dungeon Explorers of Sky.

This is still very WIP, so I didn't feel like
putting a proper README here! But you'll find
README's containing the documentation for file types
in the directories for the file handlers.

Directly in the package (``skytemple_files`` directory) you can find a new example scripts that help with how
to use this library. After installing the package you will have them as cli commands ``skytemple_<name>``. So for
``dungeon_randomizer.py`` it's ``skytemple_dungeon_randomizer``::

  $ skytemple_dungeon_randomizer input.nds output.nds

In addition to the dependencies in the ``requirements.txt`` and ``setup.py``, ARMIPS must
be installed and in the system's ``PATH`` to be able to apply ROM patches.

|kofi|
