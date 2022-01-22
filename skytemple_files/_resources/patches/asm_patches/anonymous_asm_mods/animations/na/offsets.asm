; For use with ARMIPS
; 2021/06/07
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Use filestreams to load animation specs
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm
.definelabel FGetSize, 0x02008244

.definelabel IsLoadedFile, 0x020A5DD4
.definelabel AnimFileStream, IsLoadedFile+0x4

.definelabel AnimationFunctions, 0x022BFEA0
.definelabel AnimationSector, 0x022C7A50

