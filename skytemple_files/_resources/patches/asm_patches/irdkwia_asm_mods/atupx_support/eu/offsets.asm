; For use with ARMIPS
; 2021/06/13
; For Explorers of Sky European ONLY!
; Should not be used with any other version!
; ------------------------------------------------------------------------------
; Provides support for reading ATUPX data
; ------------------------------------------------------------------------------
;
.relativeinclude on
.nds
.arm

.definelabel EndNextPartATAlgo1, 0x0201FAA4
.definelabel EndNextPartATAlgo2, 0x0201FFE0
.definelabel EndNextPartATAlgo3, 0x02020500
.definelabel HookATAlgorithm1, 0x0201F748
.definelabel HookATAlgorithm2, 0x0201FBAC
.definelabel HookATAlgorithm3, 0x020200F8
.definelabel WriteByteFromMemoryPointer, 0x0202050C
.definelabel HookCompare, 0x02020604
.definelabel HookATGetSize, 0x02020610
.definelabel UnknownFunction, 0x207BFB8
.definelabel NewAlgoStart, 0x020A4EF8
