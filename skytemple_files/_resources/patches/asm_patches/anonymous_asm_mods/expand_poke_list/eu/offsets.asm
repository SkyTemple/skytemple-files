; For use with ARMIPS
; 2021/04/14
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Use filestreams to partially load mappa files instead of loading entirely
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel IsItemForSpecialSpawnInBag, 0x0200F0F8

.definelabel CanMonsterSpawn, 0x0204D698

.definelabel GetNbFloorsPlus1, 0x0204F8EC
.definelabel GetNbPreviousFloors, 0x0204F918
.definelabel TransformDungeonData, 0x0204F984

.definelabel IsDojoDungeon, 0x020517E8

.definelabel GetSpriteFileSize, 0x02052B54
.definelabel NeedItemToSpawn, 0x02052E98

.definelabel ModMonster, 0x020547FC
.definelabel StoreMonsterID, 0x0205481C
.definelabel GetSpawnLevel, 0x02054834
.definelabel GotoGetGender, 0x02054ADC

.definelabel GetNbRecruited, 0x020555F0

.definelabel IsBossFight, 0x022E11A4

.definelabel LoadMappaFileAttributes, 0x022E796C

.definelabel RandMax, 0x022EB448

.definelabel UnknownFunc1, 0x022EB5FC
.definelabel UnknownFunc3, 0x022EB614

.definelabel GetTotalSpriteFileSize, 0x022F7A20

.definelabel IsFemaleFloor, 0x022F7D6C

.definelabel IsSatisfyingScenarioConditionToSpawn, 0x022FBFF8

.definelabel IsInSpawnList, 0x0231BE5C

.definelabel IsFixedFloor, 0x02336DA4

.definelabel UnknownFunc6, 0x02344A04

.definelabel UnknownMissionFunc, 0x02349D4C
.definelabel UnknownFunc5, 0x02349E1C
.definelabel UnknownFunc2, 0x02349F4C
.definelabel UnknownGetSize, 0x02349F78
.definelabel UnknownFunc4, 0x0234A0A4

.definelabel DungeonAuxilaryStructurePtr, 0x02352190

.definelabel TimeFilename, 0x023521A5
.definelabel DarknessFilename, 0x023521C1
.definelabel SkyFilename, 0x023521DD

.definelabel DungeonBaseStructurePtr, 0x02354138

; //////////////////////////////////////////////////////
; patch arm9.bin

.definelabel HookMissionPkmnLimit1, 0x0205D484
.definelabel HookMissionPkmnLimit2, 0x0205D2B0
.definelabel IsPkmnIDNotInMFList, 0x02062D90
.definelabel IsPkmnIDNotStoryForbidden, 0x02062E60
.definelabel GetPerformanceFlagWithChecks, 0x0204CDCC
.definelabel GetPlayerPkmnStr, 0x02055AEC
.definelabel GetPartnerPkmnStr, 0x02055B14
.definelabel PkmnIDMissionForbiddenList, 0x020A43AC
.definelabel StoryForbiddenPkmnList, 0x020A4314
.definelabel HookMissionGeneratePossiblePokemonList1, 0x0205FAD8
.definelabel HookMissionGeneratePossiblePokemonList2, 0x0205FB10
.definelabel HookLimitSearchSpecialLog, 0x02050574
.definelabel HookPokedexMax, 0x02050578
.definelabel HookExclusiveItemCheck, 0x02011090
.definelabel HookAdventureLogSpecialCheck, 0x02050580
.definelabel HookReadSave, 0x0204D900
.definelabel HookWriteSave, 0x0204D710
.definelabel SetPkmnFlag1, 0x0204D484
.definelabel GetPkmnFlag1, 0x0204D4C0
.definelabel SetPkmnFlag2, 0x0204D4FC
.definelabel GetPkmnFlag2, 0x0204D540
.definelabel ProgressStructPtr, 0x020B0890
.definelabel IsValid, 0x02054AE8
.definelabel HookN2MSearch, 0x020B5128
.definelabel HookN2MSearchBase, 0x020B5198
.definelabel MonsterFilePtr, 0x020B12D0
.definelabel HookM2NSearch, 0x020B5200
.definelabel HookM2NSearchBase, 0x020B5270
.definelabel HookSortNb1, 0x0203B8B8
.definelabel HookSortNb2, 0x0203B8F0
.definelabel GetDexNb, 0x02052A78
.definelabel HookModMonster, 0x02054818
.definelabel IsInvalidMoveset, 0x02013974
.definelabel IsInvalidMovesetEgg, 0x02053ED8
.definelabel HookListForDungeon, 0x02055700
.definelabel GetSecondFormIfValid, 0x02054F20
.definelabel GetFirstFormIfValid, 0x02054F5C
.definelabel HookGetMovesetLevelUpPtr, 0x02013934
.definelabel HookGetMovesetHMTMPtr, 0x020139A4
.definelabel HookGetMovesetEggPtr, 0x020139F0
.definelabel HookPortrait1, 0x0204DC28
.definelabel HookPortrait2, 0x0204DC44
.definelabel HookPortrait3, 0x0204DD14
.definelabel HookPortrait4, 0x0204DD30
.definelabel HookStringsPkmn1, 0x020526E0
.definelabel HookStringsPkmn2, 0x02052720
.definelabel HookStringsPkmn3, 0x02052798
.definelabel HookStringsPkmn4, 0x020529C8
.definelabel HookStringsPkmn5, 0x02052A0C
.definelabel HookStringsCate1, 0x02052AB0
.definelabel HookMdAccess1, 0x020526D8
.definelabel HookMdAccess2, 0x02052714
.definelabel HookMdAccess3, 0x0205278C
.definelabel HookMdAccess4, 0x020529C0
.definelabel HookMdAccess5, 0x02052A04
.definelabel HookMdAccess6, 0x02052AA8
.definelabel HookMdAccess7, 0x02052B1C
.definelabel HookMdAccess8, 0x02052B54
.definelabel HookMdAccess9, 0x02053B2C
.definelabel HookMdAccess10, 0x02053B4C

; //////////////////////////////////////////////////////
; patch overlay_0010.bin

.definelabel HookAnim1, 0x022BF980
.definelabel HookAnim2, 0x022BF9EC
.definelabel HookAnim3, 0x022BFA58
.definelabel HookAnim4, 0x022C03A0

; //////////////////////////////////////////////////////
; patch overlay_0011.bin

.definelabel HookDisplay, 0x022DCBC4
.definelabel HookTblTalk1, 0x022E04DC

; //////////////////////////////////////////////////////
; patch overlay_0019.bin

.definelabel RecruitablePokemonsTable, 0x0238E628
.definelabel HookSpindaRecruitTable1, 0x0238ADB8
.definelabel HookSpindaRecruitTable2, 0x0238ADC4
.definelabel HookSpindaRecruitTable3, 0x0238AE60
.definelabel HookSpindaRecruitTable4, 0x0238AE6C
.definelabel GotoCheckValidPkmnIDForMissions, 0x02062DE4
.definelabel HookSpindaRecruitGender1, 0x0238AD70
.definelabel HookSpindaRecruitGender2, 0x0238AE14
.definelabel HookSpindaRecruitGender3, 0x0238AECC
.definelabel HookSpindaRecruit1, 0x0238AD08
.definelabel HookSpindaRecruit2, 0x0238AD54

; //////////////////////////////////////////////////////
; patch overlay_0029.bin

.definelabel StoreSpriteFileIndexBothGenders, 0x022F7DC4
.definelabel LoadSpriteForPkmn, 0x022F7E8C
.definelabel LoadPokemonSpriteFiles, 0x022F800C
.definelabel SetKecleonEntryForFloor, 0x022F7D6C
.definelabel GetKecleonEntryForFloor, 0x022F7DA4
.definelabel HookDungeonMonsterMod1, 0x022FCB48
.definelabel HookDungeonMonsterMod2, 0x022FCC44
.definelabel HookDungeonMonsterMod3, 0x0231AE44
.definelabel HookDungeonMonsterLimit1, 0x022F7CB4
.definelabel HookDungeonMonsterLimit2, 0x022F81E8
.definelabel HookDungeonMonsterLimit3, 0x02344C28
.definelabel HookDungeonMonsterLimit4C1, 0x02344E10
.definelabel HookDungeonMonsterLimit4C2, 0x02344E38
.definelabel HookDungeonMonsterLimit4, 0x02344E88
.definelabel HookDungeonStructSize1, 0x022DF3B8
.definelabel HookDungeonStructSize2, 0x022DF3EC
.definelabel HookDungeonSpriteFile1, 0x022F7AFC
.definelabel HookDungeonSpriteFile3, 0x022F7FA4
.definelabel HookDungeonSpriteFile4, 0x022F7D5C
.definelabel HookDungeonSpriteFile5, 0x022F7F80
.definelabel HookDungeonSpriteFile6, 0x022F81B0
.definelabel HookDungeonSpriteFile7, 0x022FC5E4
.definelabel HookDungeonRec1, 0x022FCAF0
.definelabel HookDungeonRec2, 0x022FCB64
.definelabel HookDungeonRec3, 0x022FCBB4
.definelabel HookDungeonRec4, 0x022FCBD8
.definelabel HookDungeonRec5, 0x022FCC00
.definelabel HookDungeonRec6, 0x0231AE58
.definelabel HookTblTalk2, 0x022F6770
.definelabel HookTblTalk3, 0x0234DC2C
.definelabel HookTblTalk4, 0x0234DC60
.definelabel HookTblTalk5, 0x0234DC6C
.definelabel HookTblTalk6, 0x0234DC8C
.definelabel HookTblTalk7, 0x0234DDE8
.definelabel HookTblTalk8, 0x0234DDF4
.definelabel HookTblTalk9, 0x0234DE08
.definelabel HookTblTalk10, 0x0234DE2C
.definelabel HookTblTalk11, 0x02354400

; //////////////////////////////////////////////////////
; patch overlay_0031.bin

.definelabel HookRecSearch1, 0x02389AB0
.definelabel HookRecSearch2, 0x02389D7C
.definelabel HookRecSearch3, 0x02389D94
