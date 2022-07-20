# because IDEs and editors won't be able to parse the big file...
# See notes in ./fixtures/make_fixture.sh

from skytemple_files_test.dungeon_data.mappa_bin.fixture import *

FIX_FLOOR_LAYOUTS: Tuple[MappaFloorLayoutStub, ...]
FIX_TERRAIN_SETTINGS_LISTS: Tuple[MappaFloorTerrainSettingsStub, ...]
FIX_MONSTER_LISTS: Tuple[Tuple[MappaMonsterStub, ...], ...]
FIX_TRAP_LISTS: Tuple[MappaTrapListStub, ...]
FIX_ITEM_LISTS: Tuple[MappaItemListStub, ...]
FIX_FLOOR_LISTS: Tuple[Tuple[MappaFloorStub, ...], ...]
FIX_FLOORS: Tuple[MappaFloorStub, ...]
