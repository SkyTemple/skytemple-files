; For use with ARMIPS
; 2021/06/09
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Implements Move Growth
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel FillWithZeros4BytesArray, 0x02003288
.definelabel FGetSize, 0x02008244

.definelabel GetMoveBasePower, 0x02013A74
.definelabel GetMoveAccuracy, 0x02013AB4
.definelabel GetMovePPWithBonus, 0x02013AF8

.definelabel CopyMoveTo, 0x02014AF4
.definelabel CopyMoveFrom, 0x02014B2C

.definelabel CopyNBitsTo, 0x02050CF8
.definelabel CopyNBitsFrom, 0x02050D78

; TODO
.definelabel HookInitData, 0x02052C60

.definelabel OrgEndInit, 0x20560B8
.definelabel DebugFunc, 0x020509BC

.definelabel HookWriteTo, 0x0205920C
.definelabel HookReadFrom, 0x02059318
; END TODO

.definelabel MoveLevelPtr, 0x020A6624
.definelabel InitData, MoveLevelPtr-0x30
.definelabel CopyMoveLevelTo, InitData-0x44
.definelabel CopyMoveLevelFrom, CopyMoveLevelTo-0x44
.definelabel IsLoadedFile, MoveLevelPtr+0x4
.definelabel MGrowFileStream, IsLoadedFile+0x4

; TODO
.definelabel HookGetActualPower, 0x02302340
.definelabel HookGetActualAccuracy, 0x02323C5C
.definelabel HookPP1, 0x022FABD8
.definelabel HookPP2, 0x022FB8DC
.definelabel HookPP3, 0x02317C60
.definelabel HookPP4, 0x02317D94
.definelabel HookPP5, 0x02317EBC
.definelabel HookPP6, 0x0231E9F4
.definelabel HookPP6_1, 0x022E056C
.definelabel HookPP6_2, 0x022F9A78
.definelabel HookPP6_3, 0x022FAABC
.definelabel HookPP6_6, 0x0231E3FC
.definelabel HookPP7, 0x0232D574
.definelabel HookPP8_1, 0x02348100
.definelabel HookPP8_2, 0x02348128
.definelabel HookPP8_3, 0x02348138
.definelabel HookPP8, 0x023481F8
; END TODO

.definelabel Ov10PatchZone, 0x022DC908-0x1000

.definelabel DungeonBaseStructurePtr, 0x02354138
