; For use with ARMIPS
; 2021/06/07
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Use filestreams to load animation specs
; ------------------------------------------------------------------------------


; TODO

.relativeinclude on
.nds
.arm

.definelabel FillWithZeros4BytesArray, 0x02003288
.definelabel FGetSize, 0x02008244

.definelabel CopyMoveTo, 0x02014A4C
.definelabel CopyMoveFrom, 0x02014A84

.definelabel CopyNBitsTo, 0x020509C0
.definelabel CopyNBitsFrom, 0x02050A40

.definelabel HookInitData, 0x02052C60

.definelabel OrgEndInit, 0x20560B8
.definelabel DebugFunc, 0x020509BC

.definelabel HookWriteTo, 0x0205920C
.definelabel HookReadFrom, 0x02059318

.definelabel MoveLevelPtr, 0x020A5D84
.definelabel InitData, MoveLevelPtr-0x30
.definelabel CopyMoveLevelTo, InitData-0x44
.definelabel CopyMoveLevelFrom, CopyMoveLevelTo-0x44
.definelabel IsLoadedFile, MoveLevelPtr+0x4
.definelabel MGrowFileStream, IsLoadedFile+0x4
