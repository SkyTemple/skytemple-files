; For use with ARMIPS
; 2021/04/14 - Updated 2023/09/24
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Use filestreams to partially load mappa files instead of loading entirely
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

; The JP dungeon struct differs from the NA/EU dungeon struct, at least presumably due to the monster struct having 4 less bytes.
; We have to account for the difference in offsets!

.definelabel DUNGEON_DIFF_A4, 0xA4

; General offsets

.definelabel IsItemForSpecialSpawnInBag, 0x0200F020

.definelabel CanMonsterSpawn, 0x0204D6C0

.definelabel GetNbFloorsPlus1, 0x0204F90C
.definelabel GetNbPreviousFloors, 0x0204F938
.definelabel TransformDungeonData, 0x0204F9A4

.definelabel IsDojoDungeon, 0x02051800

.definelabel GetSpriteFileSize, 0x02052B54
.definelabel NeedItemToSpawn, 0x02052E98

.definelabel ModMonster, 0x020547B8
.definelabel StoreMonsterID, 0x020547D8
.definelabel GetSpawnLevel, 0x020547F0
.definelabel GotoGetGender, 0x02054A98

.definelabel GetSecondFormIfValid, 0x02054EDC

.definelabel GetNbRecruited, 0x02055610

.definelabel IsBossFight, 0x022E1EF4

.definelabel LoadMappaFileAttributes, 0x022E862C

.definelabel RandMax, 0x022EC100

.definelabel UnknownFunc1, 0x022EC2B4
.definelabel UnknownFunc3, 0x022EC2CC

.definelabel GetTotalSpriteFileSize, 0x022F8634

.definelabel IsFemaleFloor, 0x022F897C

.definelabel IsSatisfyingScenarioConditionToSpawn, 0x022FCAC0

.definelabel IsInSpawnList, 0x0231C8C8

.definelabel IsFixedFloor, 0x023375A4

.definelabel UnknownFunc6, 0x023451E4

.definelabel UnknownMissionFunc, 0x0234A474
.definelabel UnknownFunc5, 0x0234A544
.definelabel UnknownFunc2, 0x0234A674
.definelabel UnknownGetSize, 0x0234A6A0
.definelabel UnknownFunc4, 0x0234A7CC

.definelabel DungeonAuxilaryStructurePtr, 0x02352804

.definelabel TimeFilename, 0x02352819
.definelabel DarknessFilename, 0x02352835
.definelabel SkyFilename, 0x02352851

.definelabel DungeonBaseStructurePtr, 0x023547b8

; //////////////////////////////////////////////////////
; patch arm9.bin

.definelabel HookMissionPkmnLimit1, 0x0205D408
.definelabel HookMissionPkmnLimit2, 0x0205D234
.definelabel IsPkmnIDNotInMFList, 0x02062CFC
.definelabel IsPkmnIDNotStoryForbidden, 0x02062DCC
.definelabel GetPerformanceFlagWithChecks, 0x0204CDF4
.definelabel GetPlayerPkmnStr, 0x02055B0C
.definelabel GetPartnerPkmnStr, 0x02055B34
.definelabel PkmnIDMissionForbiddenList, 0x020A5190
.definelabel StoryForbiddenPkmnList, 0x020A50F8
.definelabel HookMissionGeneratePossiblePokemonList1, 0x0205FA4C
.definelabel HookMissionGeneratePossiblePokemonList2, 0x0205FA84
.definelabel HookLimitSearchSpecialLog, 0x02050588
.definelabel HookPokedexMax, 0x0205058C
.definelabel HookExclusiveItemCheck, 0x02010FB8
.definelabel HookAdventureLogSpecialCheck, 0x02050594
.definelabel HookReadSave, 0x0204D928
.definelabel HookWriteSave, 0x0204D738
.definelabel SetPkmnFlag1, 0x0204D4AC
.definelabel GetPkmnFlag1, 0x0204D4E8
.definelabel SetPkmnFlag2, 0x0204D524
.definelabel GetPkmnFlag2, 0x0204D568
.definelabel ProgressStructPtr, 0x020B17E8
.definelabel IsValid, 0x02054AA4
.definelabel HookN2MSearch, 0x020B60B0
.definelabel HookN2MSearchBase, 0x020B6120
.definelabel MonsterFilePtr, 0x020B2228
.definelabel HookM2NSearch, 0x020B6188
.definelabel HookM2NSearchBase, 0x020B61F8
.definelabel HookSortNb1, 0x0203B99C
.definelabel HookSortNb2, 0x0203B9D4
.definelabel GetDexNb, 0x02052A7C
.definelabel HookModMonster, 0x020547D4
.definelabel IsInvalidMoveset, 0x0201389C
.definelabel IsInvalidMovesetEgg, 0x02053E94
.definelabel HookListForDungeon, 0x02055728
.definelabel GetSecondFormIfValid, 0x02054EDC
.definelabel GetFirstFormIfValid, 0x02054F18
.definelabel HookGetMovesetLevelUpPtr, 0x0201385C
.definelabel HookGetMovesetHMTMPtr, 0x020138CC
.definelabel HookGetMovesetEggPtr, 0x02013918
.definelabel HookPortrait1, 0x0204DC50
.definelabel HookPortrait2, 0x0204DC6C
.definelabel HookPortrait3, 0x0204DD3C
.definelabel HookPortrait4, 0x0204DD58
.definelabel HookStringsPkmn1, 0x020526F8
.definelabel HookStringsPkmn2, 0x02052738
.definelabel HookStringsPkmn3, 0x020527AC
.definelabel HookStringsPkmn4, 0x020529CC
.definelabel HookStringsPkmn5, 0x02052A10
.definelabel HookStringsCate1, 0x02052AB4 ; WARNING! IS ONLY 1 INSTRUCTION IN JP, BUT IS 2 IN NA/EU!
.definelabel HookMdAccess1, 0x020526F0
.definelabel HookMdAccess2, 0x0205272C
.definelabel HookMdAccess3, 0x020527A0
.definelabel HookMdAccess4, 0x020529C4
.definelabel HookMdAccess5, 0x02052A08
.definelabel HookMdAccess6, 0x02052AAC
.definelabel HookMdAccess7, 0x02052B1C
.definelabel HookMdAccess8, 0x02052B54
.definelabel HookMdAccess9, 0x02053Ae8
.definelabel HookMdAccess10, 0x02053B08

; //////////////////////////////////////////////////////
; patch overlay_0010.bin

.definelabel HookAnim1, 0x022C07E4
.definelabel HookAnim2, 0x022C0850
.definelabel HookAnim3, 0x022C08BC
.definelabel HookAnim4, 0x022C1204

; //////////////////////////////////////////////////////
; patch overlay_0011.bin

.definelabel HookDisplay, 0x022DD924
.definelabel HookTblTalk1, 0x022E1240

; //////////////////////////////////////////////////////
; patch overlay_0019.bin

.definelabel RecruitablePokemonsTable, 0x0238F04C
.definelabel HookSpindaRecruitTable1, 0x0238B7D8
.definelabel HookSpindaRecruitTable2, 0x0238B7E4
.definelabel HookSpindaRecruitTable3, 0x0238B880
.definelabel HookSpindaRecruitTable4, 0x0238B88C
.definelabel GotoCheckValidPkmnIDForMissions, 0x02062D40
.definelabel HookSpindaRecruitGender1, 0x0238B790
.definelabel HookSpindaRecruitGender2, 0x0238B834
.definelabel HookSpindaRecruitGender3, 0x0238B8EC
.definelabel HookSpindaRecruit1, 0x0238B728
.definelabel HookSpindaRecruit2, 0x0238B774

; //////////////////////////////////////////////////////
; patch overlay_0029.bin

.definelabel StoreSpriteFileIndexBothGenders, 0x022F89D4
.definelabel LoadSpriteForPkmn, 0x022F8A9C
.definelabel LoadPokemonSpriteFiles, 0x022F8C18
.definelabel SetKecleonEntryForFloor, 0x022F897C
.definelabel GetKecleonEntryForFloor, 0x022F89B4
.definelabel HookDungeonMonsterMod1, 0x022FD53C
.definelabel HookDungeonMonsterMod2, 0x022FD638
.definelabel HookDungeonMonsterMod3, 0x0231B8B4
.definelabel HookDungeonMonsterLimit1, 0x022F88C8
.definelabel HookDungeonMonsterLimit2, 0x022F8DF0
.definelabel HookDungeonMonsterLimit3, 0x02345408
.definelabel HookDungeonMonsterLimit4C1, 0x023455F0
.definelabel HookDungeonMonsterLimit4C2, 0x02345618
.definelabel HookDungeonMonsterLimit4, 0x02345668
.definelabel HookDungeonStructSize1, 0x022E0118
.definelabel HookDungeonStructSize2, 0x022E014C
.definelabel HookDungeonSpriteFile1, 0x022F8710
.definelabel HookDungeonSpriteFile3, 0x022F8BB0
.definelabel HookDungeonSpriteFile4, 0x022F8960 ; WARNING! Cannot use word! Change the immediate values!
.definelabel HookDungeonSpriteFile5, 0x022F8AB4 ; WARNING! Cannot use word! Change the immediate values!
.definelabel HookDungeonSpriteFile6_0, 0x022F8D40 ; WARNING! Cannot use word! Change the immediate values!
.definelabel HookDungeonSpriteFile6_1, 0x022F8D70 ; WARNING! Cannot use word! Change the immediate values! EXCLUSIVE TO JP!
.definelabel HookDungeonSpriteFile7, 0x022FD038 ; WARNING! Cannot use word! Change the immediate values!
.definelabel HookDungeonRec1, 0x022FD4E4
.definelabel HookDungeonRec2, 0x022FD558
.definelabel HookDungeonRec3, 0x022FD5A8
.definelabel HookDungeonRec4, 0x022FD5CC
.definelabel HookDungeonRec5, 0x022FD5F4
.definelabel HookDungeonRec6, 0x0231B8C8
.definelabel HookTblTalk2, 0x022F739C ; Uhh, there's a 0x1B difference...sure, why not?
.definelabel HookTblTalk3, 0x0234E290
.definelabel HookTblTalk4, 0x0234E2C4
.definelabel HookTblTalk5, 0x0234E2D0
.definelabel HookTblTalk6, 0x0234E2F0
.definelabel HookTblTalk7, 0x0234E470
.definelabel HookTblTalk8, 0x0234E47C
.definelabel HookTblTalk9, 0x0234E494
.definelabel HookTblTalk10, 0x0234E4B8
.definelabel HookTblTalk11, 0x02354A60

; //////////////////////////////////////////////////////
; patch overlay_0031.bin

.definelabel HookRecSearch1, 0x0238A104
.definelabel HookRecSearch2, 0x0238A418
.definelabel HookRecSearch3, 0x0238A430
