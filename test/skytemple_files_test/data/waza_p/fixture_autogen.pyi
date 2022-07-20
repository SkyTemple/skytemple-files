# because IDEs and editors won't be able to parse the big file...
# See notes in ./fixtures/make_fixture.sh
from typing import Tuple

from skytemple_files_test.data.waza_p.fixture import *

FIX_MOVES_BYTES: Tuple[bytes, ...]
FIX_MOVES: Tuple[WazaMoveStub, ...]
FIX_LEARNSETS: Tuple[WazaLearnsetStub, ...]
