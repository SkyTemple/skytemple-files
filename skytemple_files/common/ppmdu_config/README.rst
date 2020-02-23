ppmdu configuration files
=========================

The ``data`` module contains a model of the static configuration used for ROMs of the games (things like offsets,
debug names, etc.).

The data may be loaded from ppmdu-format XML files, see directory ``skytemple_files._resources.ppmdu_config``.

The ``xml_reader`` reads the base configuration from XML files and the configuration that matches the specified
game codes (eg. "EoS_EU"). What files needs to be specified is explained in the other README.

The data may also be modified for a single ROM, to change debug names or adjust offsets.
