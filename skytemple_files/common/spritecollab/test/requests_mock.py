#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
from __future__ import annotations

import os
import zipfile
from io import BytesIO
from typing import Optional

from graphql import GraphQLSchema

from skytemple_files.common.spritecollab.requests import AioRequestAdapter

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

# A list of tuples of URLs for this mock and files on disks containing the content, for testing.
FIX_TEST_FILES = [
    ("test-portrait-sheet:1", os.path.join(FIXTURES_DIR, "portrait", "sheet1.png")),
    ("test-portrait:Normal.png", os.path.join(FIXTURES_DIR, "portrait", "Normal.png")),
    (
        "test-sprite:1:Attack-Anim.png",
        os.path.join(FIXTURES_DIR, "sprite", "1", "Attack-Anim.png"),
    ),
]
# Like above, but contains one additional row of Nones.
FIX_TEST_FILES_WITH_NONE = FIX_TEST_FILES + [(None, None)]  # type: ignore


class AioRequestAdapterMock(AioRequestAdapter):
    async def fetch_bin(self, url: str) -> bytes:
        assert isinstance(url, str)

        def read(fpath: str) -> bytes:
            with open(fpath, "rb") as f:
                return f.read()

        def make_zip(dpath: str) -> bytes:
            data = BytesIO()
            with zipfile.ZipFile(data, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(dpath):
                    for file in files:
                        zipf.write(
                            os.path.join(root, file),
                            os.path.relpath(
                                os.path.join(root, file), os.path.join(dpath)
                            ),
                        )
            return data.getvalue()

        def do_fetch_bin() -> Optional[bytes]:
            parts = url.split(":", 1)
            if len(parts) != 2:
                return None
            typ, path = parts
            path = path.replace("..", "").replace("/", "")  # safety.
            if typ == "test-portrait-sheet":
                if path == "1":
                    return read(os.path.join(FIXTURES_DIR, "portrait", "sheet1.png"))
                if path == "2":
                    return read(os.path.join(FIXTURES_DIR, "portrait", "sheet2.png"))
            if typ == "test-sprite-zip":
                if path == "1":
                    return make_zip(os.path.join(FIXTURES_DIR, "sprite", "1"))
                if path == "2":
                    return make_zip(os.path.join(FIXTURES_DIR, "sprite", "2"))
            if typ == "test-portrait":
                full_path = os.path.join(FIXTURES_DIR, "portrait", path)
                if os.path.exists(full_path):
                    return read(full_path)
            if typ == "test-sprite":
                sub_parts = path.split(":", 1)
                if len(sub_parts) != 2:
                    return None
                sprite_id, path = sub_parts
                if sprite_id == "1":
                    full_path = os.path.join(FIXTURES_DIR, "sprite", "1", path)
                    if os.path.exists(full_path):
                        return read(full_path)
                if sprite_id == "2":
                    full_path = os.path.join(FIXTURES_DIR, "sprite", "2", path)
                    if os.path.exists(full_path):
                        return read(full_path)
            return None

        r = do_fetch_bin()
        if r is None:
            raise ValueError("Invalid / unknown url for mock: " + url)
        return r

    def graphql_transport(self, url: str) -> GraphQLSchema:
        from skytemple_files.common.spritecollab.test.schema_mock import (
            SprieCollabLocalSchema,
        )

        return SprieCollabLocalSchema
