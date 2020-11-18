Dungeon Data Validator
======================

This package contains a validator to validate the dungeon definitions in
``skytemple_files.hardcoded.dungeons`` against the floor data in the mappa file.

The following things are validated:

- Dungeon entries do not re-use floors of previous dungeons.
- A floor list that is used by at least one dungeon has **all** of it's entries used.
- References to the mappa file are valid (floor list and floor actually exist).
- Total number of floors for a dungeon is valid.
