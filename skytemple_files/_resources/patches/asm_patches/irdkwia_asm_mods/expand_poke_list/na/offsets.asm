; For use with ARMIPS
; 2021/04/14
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Use filestreams to partially load mappa files instead of loading entirely
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel IsItemForSpecialSpawnInBag, 0x0200F050

.definelabel CanMonsterSpawn, 0x0204D360

.definelabel TransformDungeonData, 0x0204F64C
.definelabel GetNbFloorsPlus1, 0x0204F5B4
.definelabel GetNbPreviousFloors, 0x0204F5E0

.definelabel IsDojoDungeon, 0x020514B0

.definelabel GetSpriteFileSize, 0x0205281C
.definelabel NeedItemToSpawn, 0x02052B60

.definelabel ModMonster, 0x02054480
.definelabel StoreMonsterID, 0x020544A0
.definelabel GetSpawnLevel, 0x020544B8
.definelabel GotoGetGender, 0x02054760

.definelabel GetNbRecruited, 0x02055274

.definelabel IsBossFight, 0x022E0864

.definelabel LoadMappaFileAttributes, 0x022E6FBC

.definelabel RandMax, 0x022EAA98

.definelabel UnknownFunc1, 0x022EAC4C
.definelabel UnknownFunc3, 0x022EAC64

.definelabel GetTotalSpriteFileSize, 0x022F7068

.definelabel IsFemaleFloor, 0x022F73B4

.definelabel IsSatisfyingScenarioConditionToSpawn, 0x022FB5EC

.definelabel IsInSpawnList, 0x0231B3FC

.definelabel IsFixedFloor, 0x023361D4

.definelabel UnknownFunc6, 0x02343E20

.definelabel UnknownMissionFunc, 0x0234914C
.definelabel UnknownFunc5, 0x0234921C
.definelabel UnknownFunc2, 0x0234934C
.definelabel UnknownGetSize, 0x02349378
.definelabel UnknownFunc4, 0x023494A4

.definelabel DungeonAuxilaryStructurePtr, 0x02351584

.definelabel TimeFilename, 0x02351599
.definelabel DarknessFilename, 0x023515B5
.definelabel SkyFilename, 0x023515D1

.definelabel DungeonBaseStructurePtr, 0x02353538

; //////////////////////////////////////////////////////
; patch arm9.bin

.definelabel HookMissionPkmnLimit1, 0x0205D108
.definelabel HookMissionPkmnLimit2, 0x0205CF34
.definelabel IsPkmnIDNotInMFList, 0x02062A14
.definelabel IsPkmnIDNotStoryForbidden, 0x02062AE4
.definelabel GetPerformanceFlagWithChecks, 0x0204CA94
.definelabel GetPlayerPkmnStr, 0x02055770
.definelabel GetPartnerPkmnStr, 0x02055798
.definelabel PkmnIDMissionForbiddenList, 0x020A3DAC
.definelabel StoryForbiddenPkmnList, 0x020A3D14
.definelabel HookMissionGeneratePossiblePokemonList1, 0x0205F75C
.definelabel HookMissionGeneratePossiblePokemonList2, 0x0205F794
.definelabel HookLimitSearchSpecialLog, 0x0205023C
.definelabel HookPokedexMax, 0x02050240
.definelabel HookExclusiveItemCheck, 0x02010FE8
.definelabel HookAdventureLogSpecialCheck, 0x02050248
.definelabel HookReadSave, 0x0204D5C8
.definelabel HookWriteSave, 0x0204D3D8
.definelabel SetPkmnFlag1, 0x0204D14C
.definelabel GetPkmnFlag1, 0x0204D188
.definelabel SetPkmnFlag2, 0x0204D1C4
.definelabel GetPkmnFlag2, 0x0204D208
.definelabel ProgressStructPtr, 0x020AFF74
.definelabel IsValid, 0x0205476C
.definelabel HookN2MSearch, 0x020B47E8
.definelabel HookN2MSearchBase, 0x020B4858
.definelabel MonsterFilePtr, 0x020B09B4
.definelabel HookM2NSearch, 0x020B48C0
.definelabel HookM2NSearchBase, 0x020B4930
.definelabel HookSortNb1, 0x0203B5BC
.definelabel HookSortNb2, 0x0203B5F4
.definelabel GetDexNb, 0x02052740
.definelabel HookModMonster, 0x0205449C
.definelabel IsInvalidMoveset, 0x020138CC
.definelabel IsInvalidMovesetEgg, 0x02053B5C
.definelabel HookListForDungeon, 0x02055384
.definelabel GetSecondFormIfValid, 0x02054BA4
.definelabel GetFirstFormIfValid, 0x02054BE0
.definelabel HookGetMovesetLevelUpPtr, 0x0201388C
.definelabel HookGetMovesetHMTMPtr, 0x020138FC
.definelabel HookGetMovesetEggPtr, 0x02013948
.definelabel HookPortrait1, 0x0204D8F0
.definelabel HookPortrait2, 0x0204D90C
.definelabel HookPortrait3, 0x0204D9DC
.definelabel HookPortrait4, 0x0204D9F8
.definelabel HookStringsPkmn1, 0x020523A8
.definelabel HookStringsPkmn2, 0x020523E8
.definelabel HookStringsPkmn3, 0x02052460
.definelabel HookStringsPkmn4, 0x02052690
.definelabel HookStringsPkmn5, 0x020526D4
.definelabel HookStringsCate1, 0x02052778
.definelabel HookMdAccess1, 0x020523A0
.definelabel HookMdAccess2, 0x020523DC
.definelabel HookMdAccess3, 0x02052454
.definelabel HookMdAccess4, 0x02052688
.definelabel HookMdAccess5, 0x020526CC
.definelabel HookMdAccess6, 0x02052770
.definelabel HookMdAccess7, 0x020527E4
.definelabel HookMdAccess8, 0x0205281C
.definelabel HookMdAccess9, 0x020537B0
.definelabel HookMdAccess10, 0x020537D0

; //////////////////////////////////////////////////////
; patch overlay_0010.bin

.definelabel HookAnim1, 0x022BF040
.definelabel HookAnim2, 0x022BF0AC
.definelabel HookAnim3, 0x022BF118
.definelabel HookAnim4, 0x022BFA60

; //////////////////////////////////////////////////////
; patch overlay_0011.bin

.definelabel HookDisplay, 0x022DC284
.definelabel HookTblTalk1, 0x022DFB9C

; //////////////////////////////////////////////////////
; patch overlay_0019.bin

.definelabel RecruitablePokemonsTable, 0x0238DAF4
.definelabel HookSpindaRecruitTable1, 0x0238A278
.definelabel HookSpindaRecruitTable2, 0x0238A284
.definelabel HookSpindaRecruitTable3, 0x0238A320
.definelabel HookSpindaRecruitTable4, 0x0238A32C
.definelabel GotoCheckValidPkmnIDForMissions, 0x02062A58
.definelabel HookSpindaRecruitGender1, 0x0238A230
.definelabel HookSpindaRecruitGender2, 0x0238A2D4
.definelabel HookSpindaRecruitGender3, 0x0238A38C
.definelabel HookSpindaRecruit1, 0x0238A1C8
.definelabel HookSpindaRecruit2, 0x0238A214

; //////////////////////////////////////////////////////
; patch overlay_0029.bin

.definelabel StoreSpriteFileIndexBothGenders, 0x022F740C
.definelabel LoadSpriteForPkmn, 0x022F74D4
.definelabel LoadPokemonSpriteFiles, 0x022F7654
.definelabel SetKecleonEntryForFloor, 0x022F73B4
.definelabel GetKecleonEntryForFloor, 0x022F73EC
.definelabel HookDungeonMonsterMod1, 0x022FC14C
.definelabel HookDungeonMonsterMod2, 0x022FC248
.definelabel HookDungeonMonsterMod3, 0x0231A3E4
.definelabel HookDungeonMonsterLimit1, 0x022F72FC
.definelabel HookDungeonMonsterLimit2, 0x022F7830
.definelabel HookDungeonMonsterLimit3, 0x02344044
.definelabel HookDungeonMonsterLimit4C1, 0x0234422C
.definelabel HookDungeonMonsterLimit4C2, 0x02344254
.definelabel HookDungeonMonsterLimit4, 0x023442A4
.definelabel HookDungeonStructSize1, 0x022DEA78
.definelabel HookDungeonStructSize2, 0x022DEAAC
.definelabel HookDungeonSpriteFile1, 0x022F7144
.definelabel HookDungeonSpriteFile3, 0x022F75EC
.definelabel HookDungeonSpriteFile4, 0x022F73A4
.definelabel HookDungeonSpriteFile5, 0x022F75C8
.definelabel HookDungeonSpriteFile6, 0x022F77F8
.definelabel HookDungeonSpriteFile7, 0x022FBBE8
.definelabel HookDungeonRec1, 0x022FC0F4
.definelabel HookDungeonRec2, 0x022FC168
.definelabel HookDungeonRec3, 0x022FC1B8
.definelabel HookDungeonRec4, 0x022FC1DC
.definelabel HookDungeonRec5, 0x022FC204
.definelabel HookDungeonRec6, 0x0231A3F8
.definelabel HookTblTalk2, 0x022F5DB4
.definelabel HookTblTalk3, 0x0234D02C
.definelabel HookTblTalk4, 0x0234D060
.definelabel HookTblTalk5, 0x0234D06C
.definelabel HookTblTalk6, 0x0234D08C
.definelabel HookTblTalk7, 0x0234D1E8
.definelabel HookTblTalk8, 0x0234D1F4
.definelabel HookTblTalk9, 0x0234D208
.definelabel HookTblTalk10, 0x0234D22C
.definelabel HookTblTalk11, 0x023537E8

; //////////////////////////////////////////////////////
; patch overlay_0031.bin

.definelabel HookRecSearch1, 0x02388E8C
.definelabel HookRecSearch2, 0x02389158
.definelabel HookRecSearch3, 0x02389170
