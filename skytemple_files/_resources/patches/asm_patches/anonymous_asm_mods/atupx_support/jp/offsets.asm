; For use with ARMIPS
; 2021/06/13
; For Explorers of Sky Japan ONLY!
; Should not be used with any other version!
; ------------------------------------------------------------------------------
; Provides support for reading ATUPX data
; ------------------------------------------------------------------------------
;
.relativeinclude on
.nds
.arm

.definelabel EndNextPartATAlgo1, 0x0201FA60
.definelabel EndNextPartATAlgo2, 0x0201FF9C
.definelabel EndNextPartATAlgo3, 0x020204BC
.definelabel HookATAlgorithm1, 0x0201F704
.definelabel HookATAlgorithm2, 0x0201FB68
.definelabel HookATAlgorithm3, 0x020200B4
.definelabel WriteByteFromMemoryPointer, 0x020204C8
.definelabel HookCompare, 0x020205C0
.definelabel HookATGetSize, 0x020205CC
.definelabel UnknownFunction, 0x0207BF08
.definelabel NewAlgoStart, 0x020A5CDC
