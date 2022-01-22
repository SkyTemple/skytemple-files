; For use with ARMIPS
; 2021/04/07
; For Explorers of Sky NA Only
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

.definelabel LoadWazaP, 0x020133C4
.definelabel LoadWazaP2, 0x020133EC
.definelabel UnloadCurrentWazaP, 0x02013414

.definelabel GetMoveFlags, 0x02013840
.definelabel GetMoveType, 0x02013864
.definelabel GetMovesetLevelUpPtr, 0x02013884
.definelabel IsInvalidMoveset, 0x020138CC
.definelabel GetMovesetHMTMPtr, 0x020138F4
.definelabel GetMovesetEggPtr, 0x02013940
.definelabel GetMoveUnk09, 0x0201398C
.definelabel GetMoveNbHits, 0x020139AC
.definelabel GetMoveBasePower, 0x020139CC
.definelabel GetMoveBasePowerOverworld, 0x020139EC
.definelabel GetMoveAccuracy, 0x02013A0C
.definelabel GetMoveBasePP, 0x02013A30
.definelabel GetMovePPWithBonus, 0x02013A50
.definelabel GetMoveMaxGinsengBoost, 0x02013AD0
.definelabel GetMoveMaxGinsengBoostOverworld, 0x02013AF0
.definelabel GetMoveCriticalRate, 0x02013B10
.definelabel IsIceBreaker, 0x02013B30
.definelabel IsAffectedByTaunt, 0x02013B50
.definelabel GetMoveRangeID, 0x02013B70
.definelabel GetMoveActualAccuracy, 0x02013B90
.definelabel GetMoveBasePowerWithID, 0x02013BE8
.definelabel IsMoveRangeID13, 0x02013C04
.definelabel GetMoveMessageID, 0x02013C30

.definelabel IsAffectedByMagicCoat, 0x02013D08
.definelabel IsSnatchable, 0x02013D24
.definelabel IsMouthMove, 0x02013D40

.definelabel ConvertOverwoldToDungeonMoveset, 0x020146E4

.definelabel GetMoveCategory, 0x020151C8

.definelabel OpenWaza, 0x02015294
.definelabel SelectWaza, 0x020152FC

.definelabel UnkGetString, 0x020258C4

.definelabel EuclidianDivision, 0x0208FEA4

.definelabel NullMoveset, 0x02098D64

.definelabel IQSkillPPUp, 0x020A18A0
.definelabel ExclusiveItemPPUp2, 0x020A18C8
.definelabel ExclusiveItemPPUp4, 0x020A1874

.definelabel LSSize, 0x800
.definelabel TrueUnloadCurrentWazaP, 0x020A6620 - LSSize
.definelabel ReadMoveValue, TrueUnloadCurrentWazaP+0x120
.definelabel ReadMoveBuffer, ReadMoveValue+0xD4
.definelabel ReadMoveset, ReadMoveBuffer+0x8
.definelabel ReadMovesetBuffer, ReadMoveset+0xA0
; r0: result = ReadMoveValue(r0: move_id, r1: value_offset, r2: value_size)

.definelabel CurrentWazaInfo, 0x020AF6DC ;{0x4: MovesetTableAddr, 0x4: WazaID, 0x4: MoveInfoTableAddr}
.definelabel WazaFileNamesPtr, 0x020AF6E8 ;{0x4: WazaP, 0x4: WazaP2}
.definelabel MovesetTableAddr, 0x020AF6F0 ;{0x4: WazaP, 0x4: WazaP2}
.definelabel MoveInfoTableAddr, 0x020AF6F8 ;{0x4: WazaP, 0x4: WazaP2}
.definelabel WazaFileInfo, 0x020AF700 ;{0x8: WazaP, 0x8: WazaP2}
