; For use with ARMIPS
; 2021/06/13
; For Explorers of Sky North American ONLY!
; Should not be used with any other version!
; ------------------------------------------------------------------------------
; Provides support for reading ATUPX data
; ------------------------------------------------------------------------------
;
.relativeinclude on
.nds
.arm

.definelabel EndNextPartATAlgo1, 0x0201FA08
.definelabel EndNextPartATAlgo2, 0x0201FF44
.definelabel EndNextPartATAlgo3, 0x02020464
.definelabel HookATAlgorithm1, 0x0201F6AC
.definelabel HookATAlgorithm2, 0x0201FB10
.definelabel HookATAlgorithm3, 0x0202005C
.definelabel WriteByteFromMemoryPointer, 0x02020470
.definelabel HookCompare, 0x02020568
.definelabel HookATGetSize, 0x02020574
.definelabel UnknownFunction, 0x0207BC20
.definelabel NewAlgoStart, 0x020A48F8
