ppmdu configuration files
=========================

These XML files are using the common XML configuration syntax of ppmdu. They are directly
copied from the `ppmdu repository by psy_commando`_ (except for ``skytemple.xml``).

Entrypoint is the pmd2data.xml. It may contain references to other ExternalFiles.

The skytemple.xml must be loaded last and merged with the pmd2data.xml. The module for converting the
XML files into the internal configuration object is ``skytemple_files.common.ppmdu_config.xml_reader``.
Some unused fields of the XML may not be imported.

Additional documentation can be found in the readme of the package ``skytemple_files.common.ppmdu_config``.

.. _ppmdu repository by psy_commando: https://github.com/PsyCommando/ppmdu/tree/master/resources
