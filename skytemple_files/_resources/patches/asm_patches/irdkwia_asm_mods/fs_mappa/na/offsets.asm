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

.definelabel GetSecondFormIfValid, 0x02054BA4

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
