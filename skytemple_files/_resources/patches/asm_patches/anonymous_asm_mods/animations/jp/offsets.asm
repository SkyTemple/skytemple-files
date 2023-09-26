; For use with ARMIPS
; 2021/06/07 - Updated 2023/09/20
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Use filestreams to load animation specs
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm
.definelabel FGetSize, 0x02008244

.definelabel IsLoadedFile, 0x020A721C
.definelabel AnimFileStream, IsLoadedFile+0x4

.definelabel AnimationFunctions, 0x022C1644
.definelabel AnimationSector, 0x022C9138

