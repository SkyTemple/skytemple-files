; For use with ARMIPS
; 2021/06/07
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Use filestreams to load animation specs
; ------------------------------------------------------------------------------

.org IsLoadedFile
.area 0x4
	.word 0x0
.endarea

.org AnimFileStream
.area 0x48
	.fill 0x48, 0x0
.endarea
