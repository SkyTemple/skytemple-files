Rom Data Loader
===============

This package contains a loader (``loader.RomDataLoader``) to patch
``Pmd2Data`` with real data from the ROM. The following data is supported:

- Pmd2Data.script_data.level_entities (Actor list):

  Loaded from ``BALANCE/actor_list.bin`` when this file exists. The
  file exists, when the ``ActorAndLevelLoader`` patch is applied.
