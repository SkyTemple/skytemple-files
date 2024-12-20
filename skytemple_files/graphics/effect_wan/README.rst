wan File Format for VFX
===============

The file ``/EFFECT/effect.bin`` contains vfx used for dungeon battle, weather effects, and some ground mode vfx.

The file contains 293 effect entries.  They contain the following data:

* effect0000: Only contains animation data.  Relies on the Image data of 00292 and loaded at the start.
* effect0001: Generic effects loaded at the start.
* effect0002-0259: VFX for attacks and certain ground mode cutscenes.
* effect0260-00267: VFX for ground mode cutscenes.
* effect0268-00289: Not WAN.  Used for screen effects in moves and cutscenes.
* effect0290-00291: Not Sir0
* effect0292: Only contains image data.  The palette is loaded at the start and sticks around to be used by various other effects in the list.

This parser deals with only the WAN files.

Each slot contains one or more animations. See the `Project Pokémon documentation`_ for more details.

Usage
-----
Use the class ``EffectWanHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

To export a WanFile to sheets, use ``ExportSheets`` in the ``sheets`` module.
``ExportSheets`` requires a base effect model.  In unmodded EoS, this is effect292.

Import is currently not supported.


File Format
-----------

See `Project Pokémon documentation`_.

Credits
-------
Without the following people, this implementation wouldn't have been possible:

- psy_commando_ (C++ implementation, documentation and most of the research work!)
Based on following documentations:

- `Project Pokémon documentation`_ (Documentation mostly adapted from there!)
- `psy_commando Dropbox`_


.. Links:

.. _Project Pokémon documentation:  https://projectpokemon.org/home/docs/mystery-dungeon-nds/wan-format-for-effectbin-r156/
.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0