; For use with ARMIPS
; 2023/03/11
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Expand Portrait Structure Size to accept compressed portraits up to 808 bytes
; ------------------------------------------------------------------------------
;
.relativeinclude on
.nds
.arm

.org PatchSize
.area 0x4
	mov  r0,#0x388
.endarea

