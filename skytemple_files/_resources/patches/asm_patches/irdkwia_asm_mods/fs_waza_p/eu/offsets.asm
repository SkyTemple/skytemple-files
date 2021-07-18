; For use with ARMIPS
; 2021/04/07
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Use filestreams to access waza_p/waza_p2 instead of loading it entirely
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel FillWithZeros8Bytes, 0x02003228
.definelabel FillWithConstant1ByteArray, 0x020032A4

.definelabel FGetSize, 0x02008244

.definelabel PrintF, 0x0200C284

.definelabel LoadWazaP, 0x0201346C
.definelabel LoadWazaP2, 0x02013494
.definelabel UnloadCurrentWazaP, 0x020134BC

.definelabel GetMoveFlags, 0x020138E8
.definelabel GetMoveType, 0x0201390C
.definelabel GetMovesetLevelUpPtr, 0x0201392C
.definelabel IsInvalidMoveset, 0x02013974
.definelabel GetMovesetHMTMPtr, 0x0201399C
.definelabel GetMovesetEggPtr, 0x020139E8
.definelabel GetMoveUnk09, 0x02013A34
.definelabel GetMoveNbHits, 0x02013A54
.definelabel GetMoveBasePower, 0x02013A74
.definelabel GetMoveBasePowerOverworld, 0x02013A94
.definelabel GetMoveAccuracy, 0x02013AB4
.definelabel GetMoveBasePP, 0x02013AD8
.definelabel GetMovePPWithBonus, 0x02013AF8
.definelabel GetMoveMaxGinsengBoost, 0x02013B78
.definelabel GetMoveMaxGinsengBoostOverworld, 0x02013B98
.definelabel GetMoveCriticalRate, 0x02013BB8
.definelabel IsIceBreaker, 0x02013BD8
.definelabel IsAffectedByTaunt, 0x02013BF8
.definelabel GetMoveRangeID, 0x02013C18
.definelabel GetMoveActualAccuracy, 0x02013C38
.definelabel GetMoveBasePowerWithID, 0x02013C90
.definelabel IsMoveRangeID13, 0x02013CAC
.definelabel GetMoveMessageID, 0x02013CD8

.definelabel IsAffectedByMagicCoat, 0x02013DB0
.definelabel IsSnatchable, 0x02013DCC
.definelabel IsMouthMove, 0x02013DE8

.definelabel ConvertOverwoldToDungeonMoveset, 0x0201478C

.definelabel GetMoveCategory, 0x02015270

.definelabel OpenWaza, 0x0201533C
.definelabel SelectWaza, 0x020153A4

.definelabel UnkGetString, 0x02025B90

.definelabel EuclidianDivision, 0x0209023C

.definelabel NullMoveset, 0x020991A8

.definelabel IQSkillPPUp, 0x020A1E24
.definelabel ExclusiveItemPPUp2, 0x020A1E4C
.definelabel ExclusiveItemPPUp4, 0x020A1DF8

.definelabel LSSize, 0x800
.definelabel TrueUnloadCurrentWazaP, 0x020A6EC0 - LSSize
.definelabel ReadMoveValue, TrueUnloadCurrentWazaP+0x120
.definelabel ReadMoveBuffer, ReadMoveValue+0xD4
.definelabel ReadMoveset, ReadMoveBuffer+0x8
.definelabel ReadMovesetBuffer, ReadMoveset+0xA0
; r0: result = ReadMoveValue(r0: move_id, r1: value_offset, r2: value_size)

.definelabel CurrentWazaInfo, 0x020AFFA8 ;{0x4: MovesetTableAddr, 0x4: WazaID, 0x4: MoveInfoTableAddr}
.definelabel WazaFileNamesPtr, 0x020AFFB4 ;{0x4: WazaP, 0x4: WazaP2}
.definelabel MovesetTableAddr, 0x020AFFBC ;{0x4: WazaP, 0x4: WazaP2}
.definelabel MoveInfoTableAddr, 0x020AFFC4 ;{0x4: WazaP, 0x4: WazaP2}
.definelabel WazaFileInfo, 0x020AFFCC ;{0x8: WazaP, 0x8: WazaP2}
