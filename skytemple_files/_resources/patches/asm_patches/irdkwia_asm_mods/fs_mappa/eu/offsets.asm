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

.definelabel GetSecondFormIfValid, 0x02054F20

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
