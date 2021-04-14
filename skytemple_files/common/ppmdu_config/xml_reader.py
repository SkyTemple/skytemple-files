"""Module to read ppmdu "PMD2" XML files into the config data model"""
#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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
import os
import re
from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError

from skytemple_files.common.ppmdu_config.data import *
from skytemple_files.common.ppmdu_config.dungeon_data import Pmd2BinPackFile, Pmd2DungeonBinFiles, Pmd2DungeonItem, \
    Pmd2DungeonDungeon, Pmd2DungeonItemCategory
from skytemple_files.common.ppmdu_config.script_data import *
from skytemple_files.common.util import get_resources_dir
from skytemple_files.common.i18n_util import _


def id_matches_edition(e_game, edition):
    for key, value in e_game.attrib.items():
        if key.startswith('id') and value == edition:
            return True
    return False


class Pmd2XmlReader:
    def __init__(self, file_names: List[str], game_edition: str, translate_strings=True):
        """
        Create a parser.
        :param file_names: XML files. these will be merged.
        :param game_edition: Game edition, must be in the format XoX_RE (XoX is game version, RE is 2 letter region code).
        :raises ParseError: On XML parse errors
        :raises OSError: If the file wasn't found
        """
        # First merge the external XML files
        roots = []
        for f in file_names:
            this_file_root = ElementTree.parse(f).getroot()
            for elem in this_file_root:
                if elem.tag == 'External':
                    filepath = os.path.join(os.path.dirname(f), elem.attrib['filepath'])
                    this_file_root = XmlCombiner(
                        [this_file_root, ElementTree.parse(filepath).getroot()]
                    ).combine().getroot()
            roots.append(this_file_root)
        self._root = XmlCombiner(roots).combine().getroot()
        self._game_edition = game_edition
        self._game_version = game_edition.split('_')[0]
        self._translate_strings = translate_strings

    @classmethod
    def load_default(cls, for_version='EoS_EU', translate_strings=True) -> Pmd2Data:
        """
        Load the default pmd2data.xml, patched with the skytemple.xml and create a Pmd2Data object for the version
        passed.
        """
        res_dir = os.path.join(get_resources_dir(), 'ppmdu_config')
        return Pmd2XmlReader([
            os.path.join(res_dir, 'pmd2data.xml'),
            os.path.join(res_dir, 'skytemple.xml')
        ], for_version, translate_strings).parse()

    def parse(self) -> Pmd2Data:
        """
        Create a Pmd2Data object from the XML given.
        """
        game_editions = []
        game_constants = {}
        binaries = []
        string_index_data = None
        asm_patches_constants = None
        script_data = None
        dungeon_data = None
        string_encoding = None
        animation_names = {}
        for e in self._root:
            ###########################
            if e.tag == 'GameEditions':
                for e_edition in e:
                    game_editions.append(Pmd2GameEdition(
                        e_edition.attrib['id'],
                        e_edition.attrib['gamecode'],
                        e_edition.attrib['version'],
                        e_edition.attrib['region'],
                        self._xml_int(e_edition.attrib['arm9off14']),
                        e_edition.attrib['defaultlang'],
                        self._xml_bool(e_edition.attrib['issupported'])
                    ))
            ###########################
            elif e.tag == 'GameConstants':
                for e_game in e:
                    if ('version' in e_game.attrib and e_game.attrib['version'] == self._game_version) or \
                       ('version2' in e_game.attrib and e_game.attrib['version2'] == self._game_version) or \
                       ('version3' in e_game.attrib and e_game.attrib['version3'] == self._game_version):
                        for e_value in e_game:
                            game_constants[e_value.attrib['id']] = self._xml_int(e_value.attrib['value'])
            ###########################
            elif e.tag == 'Binaries':
                for e_game in e:
                    if id_matches_edition(e_game, self._game_edition):
                        for e_binary in e_game:
                            blocks = []
                            fns = []
                            pointers = []
                            for e_node in e_binary:
                                if e_node.tag == 'Block':
                                    blocks.append(Pmd2BinaryBlock(
                                        e_node.attrib['name'],
                                        self._xml_int(e_node.attrib['beg']),
                                        self._xml_int(e_node.attrib['end'])
                                    ))
                                elif e_node.tag == 'Fn':
                                    fns.append(Pmd2BinaryFunction(
                                        e_node.attrib['name'],
                                        self._xml_int(e_node.attrib['beg'])
                                    ))
                                elif e_node.tag == 'Pointer':
                                    pointers.append(Pmd2BinaryPointer(
                                        e_node.attrib['name'],
                                        self._xml_int(e_node.attrib['beg'])
                                    ))
                            bin = Pmd2Binary(
                                e_binary.attrib['filepath'],
                                self._xml_int(e_binary.attrib['loadaddress']),
                                blocks,
                                fns,
                                pointers
                            )
                            binaries.append(bin)
                            for x in blocks:
                                x.add_parent(bin)
                            for x in fns:
                                x.add_parent(bin)
                            for x in pointers:
                                x.add_parent(bin)
            ###########################
            elif e.tag == 'ASMPatchesConstants':
                asm_patches_constants = Pmd2AsmPatchesConstantsXmlReader(self._game_edition).read(e)
            ###########################
            elif e.tag == 'StringIndexData':
                for e_game in e:
                    if id_matches_edition(e_game, self._game_edition):
                        languages = []
                        string_blocks = []
                        for e_sub in e_game:
                            if e_sub.tag == 'Languages':
                                for e_language in e_sub:
                                    languages.append(Pmd2Language(
                                        e_language.attrib['filename'],
                                        e_language.attrib['name'],
                                        self._(e_language.attrib['name']),
                                        e_language.attrib['locale'],
                                    ))
                            if e_sub.tag == 'StringBlocks':
                                for e_string_block in e_sub:
                                    string_blocks.append(Pmd2StringBlock(
                                        e_string_block.attrib['name'],
                                        self._(e_string_block.attrib['name']),
                                        self._xml_int(e_string_block.attrib['beg']),
                                        self._xml_int(e_string_block.attrib['end'])
                                    ))
                        string_index_data = Pmd2StringIndexData(
                            languages, string_blocks
                        )
            ###########################
            elif e.tag == 'ScriptData':
                script_data = self._parse_script_data(e)
            ###########################
            elif e.tag == 'DungeonData':
                dungeon_data = self._parse_dungeon_data(e)
            ###########################
            elif e.tag == 'StringEncoding':
                for e_game in e:
                    if id_matches_edition(e_game, self._game_edition):
                        string_encoding = e_game.attrib['codec']
            ###########################
            elif e.tag == 'AnimationNames':
                for e_game in e:
                    if id_matches_edition(e_game, self._game_edition):
                        for e_sprite in e_game:
                            indices = {}
                            for e_index in e_sprite:
                                names = []
                                idx = self._xml_int(e_index.attrib['id'])
                                indices[idx] = Pmd2Index(idx, names)
                                for e_name in e_index:
                                    names.append(e_name.text)
                            idx = self._xml_int(e_sprite.attrib['id'])
                            animation_names[idx] = Pmd2Sprite(idx, indices)

        game_edition_for_this_rom = None
        for game_edition in game_editions:
            if game_edition.id == self._game_edition:
                game_edition_for_this_rom = game_edition
                break
        if game_edition_for_this_rom is None:
            raise ValueError(f"Game edition {self._game_edition} is not defined in the XML.")
        return Pmd2Data(
            game_edition_for_this_rom,
            game_editions,
            game_constants,
            binaries,
            string_index_data,
            asm_patches_constants,
            script_data,
            dungeon_data,
            string_encoding,
            animation_names
        )

    def _parse_script_data(self, script_root) -> Pmd2ScriptData:
        game_variables_table = []
        objects_list = []
        face_names = []
        face_position_modes = []
        directions = {}
        common_routine_info = []
        menu_ids = []
        process_specials = []
        sprite_effects = []
        bgms = []
        level_list = []
        lives_entities = []
        op_codes = []
        ground_state_structs = {}
        for e_game in script_root:
            if id_matches_edition(e_game, self._game_edition):
                for e in e_game:
                    ###########################
                    if e.tag == 'GameVariablesTable' or e.tag == 'GameVariablesTableExtended':
                        for i, e_var in enumerate(e):
                            game_variables_table.append(Pmd2ScriptGameVar(
                                i if e.tag == 'GameVariablesTable' else i + 0x400,
                                self._xml_int(e_var.attrib['type']),
                                self._xml_int(e_var.attrib['unk1']),
                                self._xml_int(e_var.attrib['memoffset']),
                                self._xml_int(e_var.attrib['bitshift']),
                                self._xml_int(e_var.attrib['nbvalues']),
                                self._xml_int(e_var.attrib['unk4']),
                                e_var.attrib['name'],
                                e.tag == 'GameVariablesTableExtended'
                            ))
                    ###########################
                    elif e.tag == 'ObjectsList':
                        for e_obj in e:
                            objects_list.append(Pmd2ScriptObject(
                                self._xml_int(e_obj.attrib['_id']),
                                self._xml_int(e_obj.attrib['unk1']),
                                self._xml_int(e_obj.attrib['unk2']),
                                self._xml_int(e_obj.attrib['unk3']),
                                e_obj.attrib['name']
                            ))
                    ###########################
                    elif e.tag == 'FaceNames':
                        for i, e_fn in enumerate(e):
                            face_names.append(Pmd2ScriptFaceName(i, e_fn.text))
                    ###########################
                    elif e.tag == 'FacePositionModes':
                        for i, e_mode in enumerate(e):
                            face_position_modes.append(Pmd2ScriptFacePositionMode(i, e_mode.text))
                    ###########################
                    elif e.tag == 'Directions':
                        for idx, e_dir in enumerate(e):
                            i = self._xml_int(e_dir.attrib['_id'])
                            directions[i] = Pmd2ScriptDirection(i, e_dir.text, idx)
                    ###########################
                    elif e.tag == 'CommonRoutineInfo':
                        for e_cri in e:
                            common_routine_info.append(Pmd2ScriptRoutine(
                                self._xml_int(e_cri.attrib['id']),
                                self._xml_int(e_cri.attrib['unk1']),
                                e_cri.attrib['name']
                            ))
                    ###########################
                    elif e.tag == 'MenuIds':
                        for e_menu in e:
                            menu_ids.append(Pmd2ScriptMenu(
                                self._xml_int(e_menu.attrib['id']),
                                e_menu.attrib['name']
                            ))
                    ###########################
                    elif e.tag == 'ProcessSpecialIDs':
                        for e_psid in e:
                            process_specials.append(Pmd2ScriptSpecial(
                                self._xml_int(e_psid.attrib['id']),
                                e_psid.attrib['name']
                            ))
                    ###########################
                    elif e.tag == 'SpriteEffectIDs':
                        for e_sei in e:
                            sprite_effects.append(Pmd2ScriptSpriteEffect(
                                self._xml_int(e_sei.attrib['id']),
                                e_sei.attrib['name']
                            ))
                    ###########################
                    elif e.tag == 'BackgroundMusicIDs':
                        for i, e_bgm in enumerate(e):
                            bgms.append(Pmd2ScriptBgm(
                                i, e_bgm.text,
                                self._xml_bool(e_bgm.attrib['loops']) if 'loops' in e_bgm.attrib else False
                            ))
                    ###########################
                    elif e.tag == 'LevelList':
                        for e_level in e:
                            level_list.append(Pmd2ScriptLevel(
                                self._xml_int(e_level.attrib['_id']),
                                self._xml_int(e_level.attrib['mapid']),
                                e_level.attrib['name'],
                                self._xml_int(e_level.attrib['mapty']) if 'mapty' in e_level.attrib else None,
                                self._xml_int(e_level.attrib['unk2']),
                                self._xml_int(e_level.attrib['unk4'])
                            ))
                    ###########################
                    elif e.tag == 'LivesEntityTable':
                        for e_ent in e:
                            lives_entities.append(Pmd2ScriptEntity(
                                self._xml_int(e_ent.attrib['_id']),
                                self._xml_int(e_ent.attrib['entid']),
                                e_ent.attrib['name'],
                                self._xml_int(e_ent.attrib['type']),
                                self._xml_int(e_ent.attrib['unk3']),
                                self._xml_int(e_ent.attrib['unk4'])
                            ))
                    ###########################
                    elif e.tag == 'OpCodes':
                        for e_code in e:
                            arguments = []
                            repeating_argument_group = None
                            for e_argument in e_code:
                                if e_argument.tag == 'Argument':
                                    arguments.append(Pmd2ScriptOpCodeArgument(
                                        self._xml_int(e_argument.attrib['id']),
                                        e_argument.attrib['type'],
                                        e_argument.attrib['name'],
                                    ))
                                elif e_argument.tag == 'RepeatingArgumentGroup':
                                    arg_group_args = []
                                    for e_arg_group_arg in e_argument:
                                        arg_group_args.append(Pmd2ScriptOpCodeArgument(
                                            # Arguments in repeating groups have no ids,
                                            # they are ordered and repeating instead.
                                            -1,
                                            e_arg_group_arg.attrib['type'],
                                            e_arg_group_arg.attrib['name'],
                                        ))
                                    repeating_argument_group = Pmd2ScriptOpCodeRepeatingArgumentGroup(
                                        self._xml_int(e_argument.attrib['id']),
                                        arg_group_args
                                    )
                            arguments = sorted(arguments, key=lambda a: a.id)
                            op_codes.append(Pmd2ScriptOpCode(
                                self._xml_int(e_code.attrib['id']),
                                e_code.attrib['name'],
                                self._xml_int(e_code.attrib['params']),
                                self._xml_int(e_code.attrib['stringidx']),
                                self._xml_int(e_code.attrib['unk2']),
                                self._xml_int(e_code.attrib['unk3']),
                                arguments,
                                repeating_argument_group
                            ))
                    elif e.tag == 'GroundStateStructs':
                        for e_code in e:
                            ground_state_structs[e_code.tag] = Pmd2ScriptGroundStateStruct(
                                self._xml_int(e_code.attrib['offset']),
                                self._xml_int(e_code.attrib['entrylength']),
                                self._xml_int(e_code.attrib['maxentries'])
                            )
        return Pmd2ScriptData(
            game_variables_table,
            objects_list,
            face_names,
            face_position_modes,
            directions,
            common_routine_info,
            menu_ids,
            process_specials,
            sprite_effects,
            bgms,
            level_list,
            lives_entities,
            op_codes,
            ground_state_structs
        )

    def _parse_dungeon_data(self, dungeon_root) -> Pmd2DungeonData:
        dungeon_bin_files = None
        items = []
        dungeons = []
        item_categories = {}
        for e_game in dungeon_root:
            if id_matches_edition(e_game, self._game_edition):
                for e in e_game:
                    ###########################
                    if e.tag == 'DungeonBinFiles':
                        files = []
                        for i, e_var in enumerate(e):
                            files.append(Pmd2BinPackFile(
                                self._xml_int(e_var.attrib['idxfirst']),
                                self._xml_int(e_var.attrib['idxlast']) if 'idxlast' in e_var.attrib else None,
                                e_var.attrib['type'],
                                e_var.attrib['name']
                            ))
                        dungeon_bin_files = Pmd2DungeonBinFiles(files)
                    ###########################
                    if e.tag == 'Items':
                        for i, e_item in enumerate(e):
                            items.append(Pmd2DungeonItem(i, e_item.text))
                    ###########################
                    if e.tag == 'Dungeons':
                        for i, e_dungeon in enumerate(e):
                            dungeons.append(Pmd2DungeonDungeon(i, e_dungeon.text))
                    ###########################
                    if e.tag == 'ItemCategories':
                        for e_game in e:
                            if id_matches_edition(e_game, self._game_edition):
                                for i, e_item_cat in enumerate(e_game):
                                    citems = []
                                    for e_item in e_item_cat:
                                        if e_item.tag != 'Item':
                                            raise ValueError("Excpeted Item as subtag for ItemCategory.")
                                        citems.append(self._xml_int(e_item.text))
                                    item_categories[self._xml_int(e_item_cat.attrib['id'])] = Pmd2DungeonItemCategory(
                                        self._xml_int(e_item_cat.attrib['id']),
                                        e_item_cat.attrib['name'],
                                        citems
                                    )
        return Pmd2DungeonData(
            dungeon_bin_files,
            items,
            dungeons,
            item_categories
        )

    @staticmethod
    def _xml_int(s: str):
        s = s.strip()
        if s.startswith('0x'):
            return int(s, 16)
        return int(s)

    @staticmethod
    def _xml_bool(s: str):
        if s == "false":
            return False
        if s == "true":
            return True
        raise ParseError(f"Invalid boolean '{s}'")

    def _(self, string):
        if self._translate_strings:
            return _(string)
        return string


class Pmd2AsmPatchesConstantsXmlReader:
    def __init__(self, game_edition):
        self._game_edition = game_edition

    def read(self, e) -> Pmd2AsmPatchesConstants:
        loose_bin_files = []
        patch_dir = None
        patches = []
        for sub_e in e:
            if sub_e.tag == 'LooseBinFiles':
                for e_game in sub_e:
                    if id_matches_edition(e_game, self._game_edition):
                        for e_node in e_game:
                            loose_bin_files.append(Pmd2LooseBinFile(
                                e_node.attrib['srcdata'],
                                e_node.attrib['filepath'],
                            ))
            elif sub_e.tag == 'PatchesDir':
                for e_game in sub_e:
                    if id_matches_edition(e_game, self._game_edition):
                        patch_dir = Pmd2PatchDir(e_game.attrib['filepath'], e_game.attrib['stubpath'])
            elif sub_e.tag == 'Patches':
                for e_game in sub_e:
                    if id_matches_edition(e_game, self._game_edition):
                        for e_node in e_game:
                            if e_node.tag == 'Patch':
                                patches.append(self._parse_patch(e_node))
                            if e_node.tag == 'SimplePatch':
                                patches.append(self._parse_simple_patch(e_node))
        return Pmd2AsmPatchesConstants(
            loose_bin_files,
            patch_dir,
            patches,
        )

    def _parse_patch(self, e_patch) -> Pmd2Patch:
        includes = []
        open_bins = []
        for e_sub in e_patch:
            if e_sub.tag == 'Include':
                includes.append(Pmd2PatchInclude(e_sub.attrib['filename']))
            if e_sub.tag == 'OpenBin':
                open_bin_includes = []
                for e_include in e_sub:
                    open_bin_includes.append(Pmd2PatchInclude(e_include.attrib['filename']))
                open_bins.append(Pmd2PatchOpenBin(e_sub.attrib['filepath'], open_bin_includes))
        return Pmd2Patch(
            e_patch.attrib['id'],
            includes,
            open_bins
        )

    def _parse_simple_patch(self, e_patch) -> Pmd2SimplePatch:
        includes = []
        string_replacements = []
        for e_sub in e_patch:
            if e_sub.tag == 'Include':
                includes.append(Pmd2PatchInclude(e_sub.attrib['filename']))
            if e_sub.tag == 'Replace':
                games = []
                for e_game in e_sub:
                    games.append(Pmd2PatchStringReplacementGame(
                        e_game.attrib['id'], e_game.attrib['replace']
                    ))
                string_replacements.append(Pmd2PatchStringReplacement(
                    e_sub.attrib['filename'], re.compile(e_sub.attrib['regexp']), games
                ))
        return Pmd2SimplePatch(
            e_patch.attrib['id'],
            includes,
            string_replacements
        )


class XmlCombinerMergeConfig:
    def __init__(self, strategy, key):
        self.strategy = strategy
        self.key = key


class XmlCombiner:
    def __init__(self, roots):
        # save all the roots, in order, to be processed later
        self.roots = roots

    def combine(self) -> ElementTree.ElementTree:
        for r in self.roots[1:]:
            # Build MergeConfig
            merge_config = self.read_merge_config(r) or None
            # combine each element with the first one, and update that
            self.combine_element(self.roots[0], r, merge_config)
        # return the string representation
        return ElementTree.ElementTree(self.roots[0])

    def combine_element(self, one, other, merge_config: Union[XmlCombinerMergeConfig, None]):
        """
        This function recursively updates either the text or the children
        of an element if another element is found in `one`, or adds it
        from `other` if not found.
        """
        # Default merge strategy simply works with tag mappings
        one_mapping = {el.tag: el for el in one}
        for el in other:
            if not merge_config:
                # Default merge strategy: Just append, don't change existing attributes.
                # Assume only one per tag exists and map via that.
                try:
                    matching_element_in_one = one_mapping[el.tag]
                except KeyError:
                    # Append
                    one_mapping[el.tag] = el
                    one.append(el)
                    continue
            elif merge_config.strategy == 'key':
                # Key based merge strategy: Map via a field and update all attributes. If no mapping found, append
                matching_element_in_one = self.ms_key__find(one, el, merge_config.key)
                if matching_element_in_one is None:
                    # Append
                    one_mapping[el.tag] = el
                    one.append(el)
                    continue
                else:
                    for key, value in el.attrib.items():
                        matching_element_in_one.attrib[key] = value
            if len(el) > 0:
                # Recursion
                new_merge_config = self.read_merge_config(el) or None
                self.combine_element(matching_element_in_one, el, new_merge_config)

    def read_merge_config(self, r):
        if 'merge_strategy' in r.attrib:
            merge_key = r.attrib['merge_key'] if 'merge_key' in r.attrib else None
            return XmlCombinerMergeConfig(r.attrib['merge_strategy'], merge_key)
        return None

    def ms_key__find(self, elem_to_search_in, elem_with_search_field, key):
        search_field = elem_with_search_field.attrib[key]
        for e in elem_to_search_in:
            if key in e.attrib and e.attrib[key] == search_field:
                return e
        return None


if __name__ == '__main__':
    print(Pmd2XmlReader.load_default())
