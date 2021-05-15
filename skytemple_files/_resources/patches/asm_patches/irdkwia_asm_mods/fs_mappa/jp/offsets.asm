; For use with ARMIPS
; 2021/04/14
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Use filestreams to partially load mappa files instead of loading entirely
; ------------------------------------------------------------------------------

; WARNING! Not Tested!

.relativeinclude on
.nds
.arm

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
