; For use with ARMIPS
; 2021/06/07
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Use filestreams to load animation specs
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm
.definelabel FGetSize, 0x02008244

.definelabel IsLoadedFile, 0x020A6674
.definelabel AnimFileStream, IsLoadedFile+0x4

.definelabel AnimationFunctions, 0x022C07E0
.definelabel AnimationSector, 0x022C83A8

