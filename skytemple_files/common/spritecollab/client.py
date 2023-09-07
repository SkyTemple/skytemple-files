"""
This module requires the ``spritecollab`` extra.

Utilities to interact with an instance of a spritecollab-rs GraphQL
server to retrieve metadata, portraits and sprites & tools to import
them into a ROM.

For details about the schema and queries, please read the schema
documentation at the server.

Use `SpriteCollabClient` to get started.
"""
from __future__ import annotations

#  Copyright 2020-2023 Capypara and the SkyTemple Contributors
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
import asyncio
import logging
import os.path
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from io import BytesIO
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
    Sequence,
)
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from zipfile import ZipFile

import PIL
from gql import Client
from gql.client import AsyncClientSession
from gql.dsl import DSLField, DSLFragment, DSLQuery, DSLSchema, dsl_gql
from gql.transport import AsyncTransport
from PIL import Image

from skytemple_files.common.ppmdu_config.data import Pmd2Index, Pmd2Sprite
from skytemple_files.common.ppmdu_config.script_data import Pmd2ScriptFaceName
from skytemple_files.common.spritecollab.requests import (
    AioRequestAdapter,
    AioRequestAdapterImpl,
    CachedRequestAdapter,
)
from skytemple_files.common.spritecollab.schema import (
    Config,
    CopyOf,
    Credit,
    Monster_Metadata,
    MonsterForm,
    Phase,
    Query,
    Sprite,
)
from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.xml_util import prettify
from skytemple_files.graphics.chara_wan.handler import CharaWanHandler
from skytemple_files.graphics.chara_wan.model import WanFile
from skytemple_files.graphics.chara_wan.sheets import MAX_ANIMS
from skytemple_files.graphics.kao.protocol import KaoImageProtocol
from skytemple_files.graphics.kao.sprite_bot_sheet import SpriteBotSheet

# This is the default "canonical" SpriteCollab server.
DEFAULT_SERVER = "https://spriteserver.pmdcollab.org/graphql"
EMOTION_NORMAL = "Normal"


logger = logging.getLogger(__name__)


T = TypeVar("T")


@dataclass
class MonsterFormInfo:
    _request_adapter: AioRequestAdapter = field(compare=False)
    monster_id: int
    form_path: str  # Does not include the monster ID.
    monster_name: str
    full_form_name: str  # This includes the monster name.
    shiny: bool
    female: bool
    canon: bool
    portraits_phase: Phase
    sprites_phase: Phase
    portraits_modified_date: Optional[datetime]  # This is None on errors.
    sprites_modified_date: Optional[datetime]  # This is None on errors.


@dataclass
class MonsterFormInfoWithPortrait(MonsterFormInfo):
    preview_portrait: Optional[str]

    async def fetch_preview_portrait(self) -> Optional[Image.Image]:
        if self.preview_portrait is not None:
            return await self._request_adapter.fetch_image(self.preview_portrait)
        return None


@dataclass
class SpriteUrls:
    anim: str
    offsets: str
    shadows: str


@dataclass
class MonsterFormDetails(MonsterFormInfo):
    portraits: Dict[str, str]
    portrait_sheet: str
    sprites: Dict[str, SpriteUrls]
    sprite_zip: Optional[str]
    sprites_copy_of: Dict[str, str]
    portrait_credits: List[Credit]
    sprite_credits: List[Credit]

    async def fetch_portrait(self, emotion_name: str) -> Optional[Image.Image]:
        if emotion_name in self.portraits:
            return await self._request_adapter.fetch_image(self.portraits[emotion_name])
        return None

    async def fetch_portrait_via_face_name(
        self, face_name: Pmd2ScriptFaceName
    ) -> Optional[Image.Image]:
        emotion_name = self._map_face_name(face_name)
        if emotion_name is not None and emotion_name in self.portraits:
            return await self._request_adapter.fetch_image(self.portraits[emotion_name])
        return None

    async def fetch_sprite_anim(self, action_name: str) -> Optional[Image.Image]:
        if action_name in self.sprites:
            return await self._request_adapter.fetch_image(
                self.sprites[action_name].anim
            )
        return None

    async def fetch_sprite_shadows(self, action_name: str) -> Optional[Image.Image]:
        if action_name in self.sprites:
            return await self._request_adapter.fetch_image(
                self.sprites[action_name].shadows
            )
        return None

    async def fetch_sprite_offsets(self, action_name: str) -> Optional[Image.Image]:
        if action_name in self.sprites:
            return await self._request_adapter.fetch_image(
                self.sprites[action_name].offsets
            )
        return None

    async def fetch_portrait_sheet(self) -> Image.Image:
        return await self._request_adapter.fetch_image(self.portrait_sheet)

    async def fetch_sprite_zip(self) -> Optional[bytes]:
        if self.sprite_zip is not None:
            return await self._request_adapter.fetch_bin(self.sprite_zip)
        return None

    @staticmethod
    def _map_face_name(face_name: Pmd2ScriptFaceName) -> Optional[str]:
        # This may seem a bit silly,
        # but for historic reasons, we can not
        # assume the server uses the same names
        # as the game. So we better be prepared
        # and have a function that can deal with
        # that.
        if face_name.name.lower() == "teary-eyed":
            return "Teary-Eyed"
        return face_name.name.lower().capitalize()


class SpriteCollabSession:
    """
    An active session on a SpriteCollab server.

    Don't construct this manually, use ``async with`` on an instance of `SpriteCollabClient`.
    Do not use instances of this outside said ``async with`` blocks.
    """

    _request_adapter: AioRequestAdapter
    _session: AsyncClientSession
    ds: DSLSchema

    def __init__(
        self,
        session: AsyncClientSession,
        ds: DSLSchema,
        request_adapter: AioRequestAdapter,
    ):
        self._request_adapter = request_adapter
        self._session = session
        self.ds = ds

    async def fetch_config(self) -> Config:
        """Query the server SpriteCollab configuration."""
        return (
            await self.execute_query(
                DSLQuery(
                    self.ds.Query.config.select(
                        self.ds.Config.portraitSize,
                        self.ds.Config.portraitTileX,
                        self.ds.Config.portraitTileY,
                        self.ds.Config.emotions,
                        self.ds.Config.actions,
                        self.ds.Config.completionEmotions,
                        self.ds.Config.completionActions,
                        self.ds.Config.actionMap.select(
                            self.ds.ActionId.id,
                            self.ds.ActionId.name,
                        ),
                    )
                )
            )
        )["config"]

    @overload
    async def list_monster_forms(
        self, with_preview_portrait: Literal[True]
    ) -> List[MonsterFormInfoWithPortrait]:
        ...

    @overload
    async def list_monster_forms(
        self, with_preview_portrait: Literal[False]
    ) -> List[MonsterFormInfo]:
        ...

    async def list_monster_forms(self, with_preview_portrait: bool):
        """
        Fetches some basic metadata about all monster forms. Each entry in the returned list is one
        form, the list is sorted by index.
        If `with_preview_portrait` the "Normal" emotion portrait is also returned.
        """
        portrait_extra_args = []
        if with_preview_portrait:
            portrait_extra_args.append(
                self.ds.MonsterFormPortraits.previewEmotion.select(self.ds.Portrait.url)
            )

        result = await self.execute_query(
            DSLQuery(
                self.ds.Query.monster.select(
                    self.ds.Monster.id,
                    self.ds.Monster.name,
                    self.ds.Monster.forms.select(
                        self.ds.MonsterForm.path,
                        self.ds.MonsterForm.fullName,
                        self.ds.MonsterForm.isShiny,
                        self.ds.MonsterForm.isFemale,
                        self.ds.MonsterForm.canon,
                        self.ds.MonsterForm.portraits.select(
                            self.ds.MonsterFormPortraits.phase,
                            self.ds.MonsterFormPortraits.modifiedDate,
                            *portrait_extra_args,
                        ),
                        self.ds.MonsterForm.sprites.select(
                            self.ds.MonsterFormSprites.phase,
                            self.ds.MonsterFormSprites.modifiedDate,
                        ),
                    ),
                )
            )
        )

        monsters: List[Union[MonsterFormInfo, MonsterFormInfoWithPortrait]] = []

        for monster in result["monster"]:
            for form in monster["forms"]:
                portraits_modified = None
                try:
                    portraits_modified = datetime.fromisoformat(
                        form["portraits"]["modifiedDate"]
                    )
                except (ValueError, TypeError):
                    pass
                sprites_modified = None
                try:
                    sprites_modified = datetime.fromisoformat(
                        form["sprites"]["modifiedDate"]
                    )
                except (ValueError, TypeError):
                    pass
                base_params = {
                    "monster_id": monster["id"],
                    "form_path": form["path"],
                    "monster_name": monster["name"],
                    "full_form_name": f'{monster["name"]} {form["fullName"]}'.rstrip(),
                    "shiny": form["isShiny"],
                    "female": form["isFemale"],
                    "canon": form["canon"],
                    "portraits_phase": form["portraits"]["phase"],
                    "sprites_phase": form["sprites"]["phase"],
                    "portraits_modified_date": portraits_modified,
                    "sprites_modified_date": sprites_modified,
                }

                if with_preview_portrait:
                    emotion = None
                    if form["portraits"]["previewEmotion"] is not None:
                        emotion = form["portraits"]["previewEmotion"]["url"]
                    monsters.append(
                        MonsterFormInfoWithPortrait(
                            _request_adapter=self._request_adapter,
                            **base_params,  # type: ignore
                            preview_portrait=emotion,
                        )
                    )
                else:
                    monsters.append(
                        MonsterFormInfo(
                            _request_adapter=self._request_adapter,
                            **base_params,  # type: ignore
                        )
                    )

        return monsters

    async def monster_form_details(
        self, monsters_and_forms: List[Tuple[int, str]]
    ) -> List[MonsterFormDetails]:
        """
        Returns details about monster forms for a monster, including credits and all portraits and sprites ready to be
        fetched. `monsters_and_forms` is a list of tuples, where the first entry is the
        monster ID and the second the form path.

        The returned list contains details for monsters in the same order as `monsters_and_forms`.

        Raises an error if any path could not be resolved to a valid form.
        """

        async def process_form(
            _idx: int, monster: Monster_Metadata, form: MonsterForm
        ) -> MonsterFormDetails:
            portraits_modified = None
            try:
                portraits_modified = datetime.fromisoformat(
                    form["portraits"]["modifiedDate"]
                )
            except (ValueError, TypeError):
                pass
            sprites_modified = None
            try:
                sprites_modified = datetime.fromisoformat(
                    form["sprites"]["modifiedDate"]
                )
            except (ValueError, TypeError):
                pass

            portraits = {}
            sprites = {}
            sprites_copy_of = {}
            for emotion in form["portraits"]["emotions"]:
                portraits[emotion["emotion"]] = emotion["url"]
            for emotion in form["portraits"]["emotionsFlipped"]:
                portraits[emotion["emotion"]] = emotion["url"]
            for action in form["sprites"]["actions"]:
                if "copyOf" in action:
                    action = cast(CopyOf, action)
                    sprites_copy_of[action["action"]] = action["copyOf"]
                else:
                    action = cast(Sprite, action)
                    sprites[action["action"]] = SpriteUrls(
                        anim=action["animUrl"],
                        offsets=action["offsetsUrl"],
                        shadows=action["shadowsUrl"],
                    )
            portrait_credits = []
            sprite_credits = []
            if form["portraits"]["creditPrimary"] is not None:
                portrait_credits.append(form["portraits"]["creditPrimary"])
            portrait_credits.extend(form["portraits"]["creditSecondary"])
            if form["sprites"]["creditPrimary"] is not None:
                sprite_credits.append(form["sprites"]["creditPrimary"])
            sprite_credits.extend(form["sprites"]["creditSecondary"])

            return MonsterFormDetails(
                _request_adapter=self._request_adapter,
                monster_id=monster["id"],
                form_path=form["path"],
                monster_name=monster["name"],
                full_form_name=f'{monster["name"]} {form["fullName"]}'.rstrip(),
                shiny=form["isShiny"],
                female=form["isFemale"],
                canon=form["canon"],
                portraits_phase=form["portraits"]["phase"],
                sprites_phase=form["sprites"]["phase"],
                portraits_modified_date=portraits_modified,
                sprites_modified_date=sprites_modified,
                portraits=portraits,
                portrait_sheet=form["portraits"]["sheetUrl"],
                sprites=sprites,
                sprite_zip=form["sprites"]["zipUrl"],
                sprites_copy_of=sprites_copy_of,
                portrait_credits=portrait_credits,
                sprite_credits=sprite_credits,
            )

        return await self._fetch_details(
            monsters_and_forms,
            lambda credit, sprite, copy_of: (
                self.ds.MonsterForm.path,
                self.ds.MonsterForm.fullName,
                self.ds.MonsterForm.isShiny,
                self.ds.MonsterForm.isFemale,
                self.ds.MonsterForm.canon,
                self.ds.MonsterForm.portraits.select(
                    self.ds.MonsterFormPortraits.phase,
                    self.ds.MonsterFormPortraits.modifiedDate,
                    self.ds.MonsterFormPortraits.emotions.select(
                        self.ds.Portrait.emotion, self.ds.Portrait.url
                    ),
                    self.ds.MonsterFormPortraits.emotionsFlipped.select(
                        self.ds.Portrait.emotion, self.ds.Portrait.url
                    ),
                    self.ds.MonsterFormPortraits.sheetUrl,
                    self.ds.MonsterFormPortraits.creditPrimary.select(credit),
                    self.ds.MonsterFormPortraits.creditSecondary.select(credit),
                ),
                self.ds.MonsterForm.sprites.select(
                    self.ds.MonsterFormSprites.phase,
                    self.ds.MonsterFormSprites.modifiedDate,
                    self.ds.MonsterFormSprites.actions.select(sprite, copy_of),
                    self.ds.MonsterFormSprites.zipUrl,
                    self.ds.MonsterFormSprites.creditPrimary.select(credit),
                    self.ds.MonsterFormSprites.creditSecondary.select(credit),
                ),
            ),
            process_form,
        )

    async def fetch_portraits(
        self, monsters_and_forms: Sequence[Tuple[int, str]]
    ) -> List[List[Optional[KaoImageProtocol]]]:
        """
        Fetch portraits for the given forms. `monsters_and_forms` is a list of tuples, where the first entry is the
        monster ID and the second the form path.

        The portraits are converted into a list of KaoImages, where None entries are slots that are either not available
        or were blacklisted or not whitelisted. The returned list contains portraits for monsters in the same order
        as `monsters_and_forms`.

        Raises an error if any path could not be resolved to a valid form.
        """

        async def process_form(
            idx: int, _monster: Monster_Metadata, form: MonsterForm
        ) -> List[Optional[KaoImageProtocol]]:
            kao = FileType.KAO.new(1)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                portrait_sheet = await self._request_adapter.fetch_bin(
                    form["portraits"]["sheetUrl"]
                )
                tmp.write(portrait_sheet)
                tmp.flush()
                tmp.close()

                this_sheet: List[Optional[KaoImageProtocol]] = [None] * 40
                try:
                    for subindex, image in SpriteBotSheet.load(
                        tmp.name, lambda *args: ""
                    ):
                        kao.set_from_img(0, subindex, image)
                        this_sheet[subindex] = kao.get(0, subindex)
                except PIL.UnidentifiedImageError as ex:
                    with open(tmp.name, "rb") as f:
                        logger.error(
                            f"Error trying to read downloaded sprite sheet for "
                            f"{monsters_and_forms[idx]} (could not be identified). "
                            f"Content of file: {f.read()!r}"
                        )
                    raise ex
                finally:
                    try:
                        os.unlink(tmp.name)
                    except Exception as ex:
                        logger.warning(
                            f"Failed to remove temporary file {tmp}: {type(ex)}: {ex}"
                        )

                return this_sheet

        return await self._fetch_details(
            monsters_and_forms,
            lambda _credit, _sprite, copy_of: (
                self.ds.MonsterForm.portraits.select(
                    self.ds.MonsterFormPortraits.sheetUrl
                ),
            ),
            process_form,
            include_sprite_fragments=False,
            include_credit_fragments=False,
        )

    async def fetch_sprites(
        self,
        monsters_and_forms: Sequence[Tuple[int, str]],
        actions: List[Optional[List[str]]],
        copy_to_event_sleep_if_missing: bool = False,
    ) -> List[Optional[Tuple[WanFile, Pmd2Sprite, int]]]:
        """
        Fetch sprites for the given forms. `monsters_and_forms` is a list of tuples, where the first entry is the
        monster ID and the second the form path.

        The sprites are converted into a merged WanFile. The returned list contains sprites for monsters in the same
        order as `monsters_and_forms`. The tuples in the list contain the wan file, a single Pmd2Sprite with the action
        mappings, and the shadow size.

        `actions` must be a list with one entry for each entry in `monsters_and_forms`. Each entry is a list of
        actions that should be imported (if they don't exist on SpriteCollab, they are ignored). Alternatively
        an entry can be None, in which case all available actions will be imported.

        If `copy_to_event_sleep_if_missing` is True and `EventSleep` and/or `Laying` and/or `Waking` are requested for
        a form but not available, all of those that were requested are set as a copy of `Sleep` instead.
        This only happens if the `Sleep` action is requested for a form.

        Raises an error if any path could not be resolved to a valid form.
        """
        if len(monsters_and_forms) != len(actions):
            raise ValueError(
                "The actions and monsters_and_forms parameters must have the same length."
            )

        async def process_form(
            idx: int, monster: Monster_Metadata, form: MonsterForm
        ) -> Optional[Tuple[WanFile, Pmd2Sprite, int]]:
            actions_for_this_form = actions[idx]
            if actions_for_this_form is not None:
                actions_for_this_form = [x.lower() for x in actions_for_this_form]
            if form["sprites"]["zipUrl"] is None:
                return None

            zipped_bytes = await self._request_adapter.fetch_bin(
                form["sprites"]["zipUrl"]
            )

            with tempfile.TemporaryDirectory() as tmp_dir:
                with ZipFile(BytesIO(zipped_bytes), "r") as zipObj:
                    zipObj.extractall(tmp_dir)
                xml_path = os.path.join(tmp_dir, "AnimData.xml")
                if not os.path.exists(xml_path):
                    raise RuntimeError(
                        f"AnimData.xml for sprite for form of monster {monster['id']} missing."
                    )
                try:
                    root = ElementTree.parse(xml_path).getroot()
                    shadow_size = int(root.find("ShadowSize").text)  # type: ignore
                    anims: List[Element] = root.find("Anims")  # type: ignore
                    sleep_found = None
                    event_sleep_found = None
                    wake_found = None
                    laying_found = None
                    event_sleep_requested = (
                        actions_for_this_form is None
                        or "eventsleep" in actions_for_this_form
                    )
                    wake_requested = (
                        actions_for_this_form is None or "wake" in actions_for_this_form
                    )
                    laying_requested = (
                        actions_for_this_form is None
                        or "laying" in actions_for_this_form
                    )
                    new_actions = []
                    action_indices = {}
                    for action in anims:
                        name = action.find("Name").text.lower()  # type: ignore
                        name_normal: str = action.find("Name").text  # type: ignore
                        if (
                            actions_for_this_form is None
                            or name in actions_for_this_form
                        ):
                            sleep_found = sleep_found or name == "sleep"
                            event_sleep_found = (
                                event_sleep_found or name == "eventsleep"
                            )
                            wake_requested = wake_requested or name == "wake"
                            laying_requested = laying_requested or name == "laying"
                            new_actions.append(action)
                            if action.find("Index") is not None:
                                idx = int(action.find("Index").text)  # type: ignore
                                action_indices[idx] = Pmd2Index(idx, [name_normal])
                        else:
                            fname = os.path.join(tmp_dir, f"{name_normal}-Anim.png")
                            if os.path.exists(fname):
                                os.remove(fname)
                            fname = os.path.join(tmp_dir, f"{name_normal}-Offsets.png")
                            if os.path.exists(fname):
                                os.remove(fname)
                            fname = os.path.join(tmp_dir, f"{name_normal}-Shadow.png")
                            if os.path.exists(fname):
                                os.remove(fname)
                    if copy_to_event_sleep_if_missing and sleep_found:
                        names = []
                        if event_sleep_requested and not event_sleep_found:
                            names.append(("EventSleep", 13))
                        if wake_requested and not wake_found:
                            names.append(("Wake", 14))
                        if laying_requested and not laying_found:
                            names.append(("Laying", 27))

                        for name, index in names:
                            while index in action_indices.keys():
                                index += 1
                            if index >= MAX_ANIMS:
                                # If we reached the max already, there isn't much we can do.
                                break
                            new_action = Element("Anim")
                            e = Element("Name")
                            e.text = name
                            new_action.append(e)
                            e = Element("Index")
                            e.text = str(index)
                            new_action.append(e)
                            e = Element("CopyOf")
                            e.text = "Sleep"
                            new_action.append(e)
                            new_actions.append(new_action)
                            action_indices[index] = Pmd2Index(index, [name])
                    anims.clear()
                    for action in new_actions:
                        anims.append(action)
                    with open(xml_path, "w") as f:
                        f.write(prettify(root))
                except Exception as ex:
                    raise RuntimeError(
                        f"Error processing AnimData.xml for sprite for form of monster {monster['id']}."
                    ) from ex

                return (
                    CharaWanHandler.import_sheets(tmp_dir),
                    Pmd2Sprite(-1, action_indices),
                    shadow_size,
                )

        return await self._fetch_details(
            monsters_and_forms,
            lambda _credit, _sprite, copy_of: (
                self.ds.MonsterForm.sprites.select(self.ds.MonsterFormSprites.zipUrl),
            ),
            process_form,
            include_sprite_fragments=False,
            include_credit_fragments=False,
        )

    async def execute_query(
        self, query: DSLQuery, *, fragments: Optional[Iterable[DSLFragment]] = None
    ) -> Query:
        """Note that you should upcast the returned type to match your actual query subtype."""
        if fragments is not None:
            return cast(Query, await self._session.execute(dsl_gql(*fragments, query)))
        return cast(Query, await self._session.execute(dsl_gql(query)))

    async def _fetch_details(
        self,
        monsters_and_forms: Sequence[Tuple[int, str]],
        selector_fn: Callable[
            [DSLFragment, DSLFragment, DSLFragment], Iterable[DSLField]
        ],
        form_cb: Callable[[int, Monster_Metadata, MonsterForm], Coroutine[Any, Any, T]],
        *,
        include_sprite_fragments: bool = True,
        include_credit_fragments: bool = True,
    ) -> List[T]:
        sprite = DSLFragment("SpriteUnionAsSprite")
        sprite.on(self.ds.Sprite)
        sprite.select(
            self.ds.Sprite.action,
            self.ds.Sprite.animUrl,
            self.ds.Sprite.offsetsUrl,
            self.ds.Sprite.shadowsUrl,
        )
        copy_of = DSLFragment("SpriteUnionAsCopyOf")
        copy_of.on(self.ds.CopyOf)
        copy_of.select(
            self.ds.CopyOf.action,
            self.ds.CopyOf.copyOf,
        )

        credit = DSLFragment("CreditFields")
        credit.on(self.ds.Credit)
        credit.select(
            self.ds.Credit.id,
            self.ds.Credit.name,
            self.ds.Credit.contact,
            self.ds.Credit.discordHandle,
        )

        fragments = []
        if include_sprite_fragments:
            fragments.append(sprite)
            fragments.append(copy_of)
        if include_credit_fragments:
            fragments.append(credit)

        # Count the number of unique monsters in the request
        monster_set = set(monster for monster, _ in monsters_and_forms)
        monster_count = len(monster_set)
        if monster_count < 2:
            coros = await self._fetch_details_single_mon(
                next(iter(monster_set)),
                [p for _, p in monsters_and_forms],
                fragments,
                sprite,
                copy_of,
                credit,
                selector_fn,
                form_cb,
            )
        else:
            coros = await self._fetch_details_multi_mons(
                monster_set,
                monsters_and_forms,
                fragments,
                sprite,
                copy_of,
                credit,
                selector_fn,
                form_cb,
            )

        return list(await asyncio.gather(*coros, return_exceptions=False))

    async def _fetch_details_single_mon(
        self,
        monster_id: int,
        paths: List[str],
        fragments: Iterable[DSLFragment],
        sprite: DSLFragment,
        copy_of: DSLFragment,
        credit: DSLFragment,
        selector_fn: Callable[
            [DSLFragment, DSLFragment, DSLFragment], Iterable[DSLField]
        ],
        form_cb: Callable[[int, Monster_Metadata, MonsterForm], Coroutine[Any, Any, T]],
    ) -> List[Coroutine[Any, Any, T]]:
        monster_forms = {}
        path_mapping = {}
        i = 0
        for path in paths:
            key = f"f_{i}"
            monster_forms[key] = self.ds.Monster.manual(path=path).select(
                *selector_fn(credit, sprite, copy_of)
            )
            path_mapping[path] = key
            i += 1

        result = await self.execute_query(
            DSLQuery(
                self.ds.Query.monster(filter=[monster_id]).select(
                    self.ds.Monster.id, self.ds.Monster.name, **monster_forms
                )
            ),
            fragments=fragments,
        )

        if len(result["monster"]) > 1:
            raise ValueError(
                f"Invalid server response error while trying to get forms for monster {monster_id}"
            )
        if len(result["monster"]) < 1:
            raise ValueError(f"Monster {monster_id} not found.")

        monster = result["monster"][0]
        coros = []
        i = 0
        for key, form in monster.items():
            if not key.startswith("f_"):
                continue
            if form is None:
                raise ValueError(
                    f"Form {path_mapping[key]} for monster {monster_id} not found"
                )

            coros.append(form_cb(i, monster, cast(MonsterForm, form)))
            i = i + 1
        return coros

    async def _fetch_details_multi_mons(
        self,
        monster_ids: Iterable[int],
        monsters_and_forms: Sequence[Tuple[int, str]],
        fragments: Iterable[DSLFragment],
        sprite: DSLFragment,
        copy_of: DSLFragment,
        credit: DSLFragment,
        selector_fn: Callable[
            [DSLFragment, DSLFragment, DSLFragment], Iterable[DSLField]
        ],
        form_cb: Callable[[int, Monster_Metadata, MonsterForm], Coroutine[Any, Any, T]],
    ) -> List[Coroutine[Any, Any, T]]:
        result = await self.execute_query(
            DSLQuery(
                self.ds.Query.monster(filter=monster_ids).select(
                    self.ds.Monster.id,
                    self.ds.Monster.name,
                    self.ds.Monster.forms().select(
                        *selector_fn(credit, sprite, copy_of)
                    ),
                )
            ),
            fragments=fragments,
        )

        collected_monsters_and_forms: List[Tuple[int, str]] = []
        collected_form_data: List[Tuple[Monster_Metadata, MonsterForm]] = []

        # We pre-process all the results, because we don't want
        # to call the callback, unless we really have everything we need.
        for monster in result["monster"]:
            for form in monster["forms"]:
                if (monster["id"], form["path"]) in monsters_and_forms:
                    collected_monsters_and_forms.append((monster["id"], form["path"]))
                    collected_form_data.append((monster, form))

        if len(collected_monsters_and_forms) < len(monsters_and_forms):
            raise ValueError(f"Some monsters or forms were not found.")

        coros = []
        for i, (monster_m, form_m) in enumerate(collected_form_data):
            coros.append(form_cb(i, monster_m, form_m))
        return coros


class SpriteCollabClient:
    """
    Client to connect to a SpriteCollab server. Use ``async with`` to get
    a tuple containing a session (`SpriteCollabSession`) and the DSL for the schema.
    """

    _request_adapter: AioRequestAdapter
    _client: Client
    _session: Optional[SpriteCollabSession]

    def __init__(
        self,
        *,
        server_url: str = DEFAULT_SERVER,
        cache_size: int = 5000,
        request_adapter: Optional[AioRequestAdapter] = None,
        use_ssl=True,
        use_certifi_ssl=False,
    ):
        """
        Create a new client instance.
        The last `cache_size` requests are cached (including fetched assets).
        To disable the cache, set ``cache_size`` to 0.
        If `use_ssl` is set to `False`, requests are always made via HTTP (SSL is disabled). "https://" at the start of
        the provided `server_url` is replaced with "http://" then. HTTP traffic may still be redirected to SSL.
        If `use_certifi_ssl` is used, then the certificate of the `certifi` package are used.
        The caller must make sure that package is installed.

        If you specify a custom request adapter, the `cache_size`, `use_ssl` and `use_certifi_ssl` parameters
        are ignored.
        """
        if not use_ssl:
            server_url = server_url.replace("https://", "http://")
        if request_adapter is None:
            if cache_size > 0:
                self._request_adapter = CachedRequestAdapter(
                    cache_size, use_certifi_ssl=use_certifi_ssl
                )
            else:
                self._request_adapter = AioRequestAdapterImpl(
                    use_certifi_ssl=use_certifi_ssl
                )
        else:
            self._request_adapter = request_adapter

        transport_or_schema = self._request_adapter.graphql_transport(url=server_url)

        if isinstance(transport_or_schema, AsyncTransport):
            self._client = Client(
                transport=transport_or_schema,
                fetch_schema_from_transport=True,
                execute_timeout=120,
            )
        else:
            # Execute against local schema
            self._client = Client(schema=transport_or_schema)

        self._session = None

    def flush_cache(self):
        """Clears the cache. This is also always done when creating a new session with ``async with``."""
        if isinstance(self._request_adapter, CachedRequestAdapter):
            self._request_adapter.flush_cache()

    async def __aenter__(self) -> SpriteCollabSession:
        session = await self._client.connect_async(True)
        if self._client.schema:
            ds = DSLSchema(self._client.schema)
            # self.flush_cache()
            self._session = SpriteCollabSession(session, ds, self._request_adapter)
            return self._session
        else:
            raise RuntimeError(
                "Failed to fetch GraphQL schema from SpriteCollab GraphQL server."
            )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        r = await self._client.close_async()
        self._session = None
        return r
