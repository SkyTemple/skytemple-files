wan File Format for Pokemon overworld sprites
===============

The file ``/MONSTER/monster.bin``, ``/MONSTER/m_ground.bin``, and ``/MONSTER/m_attack.bin`` contains overworld sprites.

The file contains 1,154 slots for portraits. These are directly mapped to the entries in the ``monster.md``,
which means an entry for all of the first gender of all Pokémon (0-600) and an optional entry for the
second genders (601-1,154). If the second gender entry is not defined, the game falls back to using the portrait
of the first gender.

Each slot contains exactly 40 sub-slots. Each of these is assigned an
emotion. See the `Project Pokémon documentation`_ for more details.

Usage
-----
Use the class ``CharaWanHandler`` of the ``handler`` module, to open and save
models from binary data. The model that the handler returns is in the
module ``model``.

To import or export a WanFile to sheets, use ``ImportSheets`` and ``ExportSheets`` in the ``sheets`` module.
``ExportSheets`` requires a sdwImg object and an anim_names_map.
sdwImg is typically a reference to the shadow.png image that is read in by Pillow.
anim_names_map is a list that maps animation index to name.  The game itself does not have full consistency to what animation index contains what animation.  Thus, an arbitrary name mapping created BY THE USER must be passed in.  An example for Bulbasaur would be:
anim_name_map = ["Walk", "Attack", "Strike", "Shoot", "Shake/Dance", "Sleep", "Hurt", "Idle", "Swing", "Double", "Hop", "Charge", "Rotate", "EventSleep", "Wake", "Eat", "Tumble", "Pose", "Pull", "Pain", "Float", "DeepBreath", "Nod", "Sit", "LookUp", "Sink", "Trip", "Laying", "LeapForth", "Head", "Cringe", "LostBalance", "TumbleBack", "Faint", "HitGround"]

A convenient community-created mapping for every sprite in the base game can be found here:
https://docs.google.com/spreadsheets/d/16bnauXeTendm1xQSrk6pbobCFFeeHXghpFfyo4jWLYo/edit#gid=0


It's often convenient to combine the WanFiles of ``/MONSTER/monster.bin``, ``/MONSTER/m_ground.bin``, and ``/MONSTER/m_attack.bin`` together when extracting files from the game into sheets, or splitting them apart when doing the inverse.
``SplitWan`` and ``MergeWan`` fulfill this role.
The ``anim_map`` parameter in ``SplitWan`` is needed to determine which splitted ``WanFile`` gets which animation.  It is passed in as a list of list of booleans.
For example:

anim_presence_map = [[True, True],
					 [True, False, True],
					 [False, False, True, True, True]]
This will split a WanFile with 5 or more animations into 3 WanFiles.
The first WanFile will get animations 0 and 1.
The second WanFile will get animations 0 and 2.
The third WanFile will get animations 2, 3, and 4.
The array can be jagged.


For reference, wan files in monster.bin almost always have animations 0, 5, 6, 7, and 11.
wan files in m_ground.bin almost always have animations 0, 7, and 8.  However, some (often cutscene important ones) can have animations from any index.
wan files in m_attack.bin almost always get animations 1, 2, 3, 4, 8, 9, 10, 11, 12.  Failure to include any of these essentials risks their attack animations to fail. The few sprites without these animations are those that exist purely in the cutscenes.


File Format
-----------

See `Project Pokémon documentation`_.

Credits
-------
I didn't do much of the work figuring out the file format. Without the following people, this implementation
wouldn't have been possible:

- psy_commando_ (C++ implementation, documentation and most of the research work!)
Based on following documentations:

- `Project Pokémon documentation`_ (Documentation mostly adapted from there!)
- `psy_commando Dropbox`_


.. Links:

.. _Project Pokémon documentation:  https://projectpokemon.org/home/docs/mystery-dungeon-nds/wanwat-file-format-r50/
.. _psy_commando Dropbox:           https://www.dropbox.com/sh/8on92uax2mf79gv/AADCmlKOD9oC_NhHnRXVdmMSa?dl=0