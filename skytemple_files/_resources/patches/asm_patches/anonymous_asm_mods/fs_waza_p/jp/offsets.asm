; For use with ARMIPS
; 2021/04/07
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Use filestreams to access waza_p/waza_p2 instead of loading it entirely
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel FillWithZeros8Bytes, 0x02003228
.definelabel FillWithConstant1ByteArray, 0x020032A4

.definelabel FGetSize, 0x02008244

.definelabel PrintF, 0x0200C1FC

.definelabel LoadWazaP, 0x02013394
.definelabel LoadWazaP2, 0x020133BC
.definelabel UnloadCurrentWazaP, 0x020133E4

.definelabel GetMoveFlags, 0x02013810
.definelabel GetMoveType, 0x02013834
.definelabel GetMovesetLevelUpPtr, 0x02013854
.definelabel IsInvalidMoveset, 0x0201389C
.definelabel GetMovesetHMTMPtr, 0x020138C4
.definelabel GetMovesetEggPtr, 0x02013910
.definelabel GetMoveUnk09, 0x0201395C
.definelabel GetMoveNbHits, 0x0201397C
.definelabel GetMoveBasePower, 0x0201399C
.definelabel GetMoveBasePowerOverworld, 0x020139BC
.definelabel GetMoveAccuracy, 0x020139DC
.definelabel GetMoveBasePP, 0x02013A00
.definelabel GetMovePPWithBonus, 0x02013A20
.definelabel GetMoveMaxGinsengBoost, 0x02013AA0
.definelabel GetMoveMaxGinsengBoostOverworld, 0x02013AC0
.definelabel GetMoveCriticalRate, 0x02013AE0
.definelabel IsIceBreaker, 0x02013B00
.definelabel IsAffectedByTaunt, 0x02013B20
.definelabel GetMoveRangeID, 0x02013B40
.definelabel GetMoveActualAccuracy, 0x02013B60
.definelabel GetMoveBasePowerWithID, 0x02013BB8
.definelabel IsMoveRangeID13, 0x02013BD4
.definelabel GetMoveMessageID, 0x02013C00

.definelabel IsAffectedByMagicCoat, 0x02013CD8
.definelabel IsSnatchable, 0x02013CF4
.definelabel IsMouthMove, 0x02013D10

.definelabel ConvertOverwoldToDungeonMoveset, 0x020146B4

.definelabel GetMoveCategory, 0x02015198

.definelabel OpenWaza, 0x02015264
.definelabel SelectWaza, 0x020152CC

.definelabel UnkGetString, 0x020258A4

.definelabel EuclidianDivision, 0x0209018C

.definelabel NullMoveset, 0x02099058

.definelabel IQSkillPPUp, 0x020A2C74
.definelabel ExclusiveItemPPUp2, 0x020A2C9C
.definelabel ExclusiveItemPPUp4, 0x020A2C48

.definelabel LSSize, 0x800
.definelabel TrueUnloadCurrentWazaP, 0x020A7A68 - LSSize
.definelabel ReadMoveValue, TrueUnloadCurrentWazaP+0x120
.definelabel ReadMoveBuffer, ReadMoveValue+0xD4
.definelabel ReadMoveset, ReadMoveBuffer+0x8
.definelabel ReadMovesetBuffer, ReadMoveset+0xA0
; r0: result = ReadMoveValue(r0: move_id, r1: value_offset, r2: value_size)

.definelabel CurrentWazaInfo, 0x020B0B1C ;{0x4: MovesetTableAddr, 0x4: WazaID, 0x4: MoveInfoTableAddr}
.definelabel WazaFileNamesPtr, 0x020B0B28 ;{0x4: WazaP, 0x4: WazaP2}
.definelabel MovesetTableAddr, 0x020B0B30 ;{0x4: WazaP, 0x4: WazaP2}
.definelabel MoveInfoTableAddr, 0x020B0B38 ;{0x4: WazaP, 0x4: WazaP2}
.definelabel WazaFileInfo, 0x020B0B40 ;{0x8: WazaP, 0x8: WazaP2}
