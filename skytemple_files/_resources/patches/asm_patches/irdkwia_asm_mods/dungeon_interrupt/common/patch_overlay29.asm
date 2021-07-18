; For use with ARMIPS
; 2021/07/18
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------

.org 0x022E00A8
.area 0x4
	blt CheckDungeonInterrupt
EndExecution:
.endarea

.org 0x022E02CC
.area 0x4
	nop
.endarea

.org 0x022FD668
.area 0x4
	mov r1,#0
.endarea

