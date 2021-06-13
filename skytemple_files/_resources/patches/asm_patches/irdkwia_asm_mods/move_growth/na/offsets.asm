; For use with ARMIPS
; 2021/06/09
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Implements Move Growth
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel FillWithZeros4BytesArray, 0x02003288
.definelabel FGetSize, 0x02008244

.definelabel GetMoveBasePower, 0x020139CC
.definelabel GetMoveAccuracy, 0x02013A0C
.definelabel GetMovePPWithBonus, 0x02013A50

.definelabel CopyMoveTo, 0x02014A4C
.definelabel CopyMoveFrom, 0x02014A84

.definelabel CopyNBitsTo, 0x020509C0
.definelabel CopyNBitsFrom, 0x02050A40

.definelabel HookInitData, 0x02052C60
.definelabel HookClearData, 0x02052C78

.definelabel OrgEndInit, 0x20560B8
.definelabel DebugFunc, 0x020509BC

.definelabel HookWriteTo, 0x0205920C
.definelabel HookReadFrom, 0x02059318

.definelabel MoveLevelPtr, 0x020A5D84
.definelabel InitData, MoveLevelPtr-0x2C
.definelabel ClearData, InitData-0x20
.definelabel CopyMoveLevelTo, ClearData-0x44
.definelabel CopyMoveLevelFrom, CopyMoveLevelTo-0x44
.definelabel GetMoveLevelProxy, CopyMoveLevelFrom-0x2C
.definelabel GetMovePPProxy, GetMoveLevelProxy-0x2C
.definelabel ProxyExtendAccuracy, GetMovePPProxy-0x2C
.definelabel ProxyExtendPower, ProxyExtendAccuracy-0x2C
.definelabel IsLoadedFile, MoveLevelPtr+0x4
.definelabel MGrowFileStream, IsLoadedFile+0x4

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

.definelabel Ov10PatchZone, 0x022DBFB0-0x1000

.definelabel DungeonBaseStructurePtr, 0x02353538


.definelabel HookMenuPP1, 0x02388B80
