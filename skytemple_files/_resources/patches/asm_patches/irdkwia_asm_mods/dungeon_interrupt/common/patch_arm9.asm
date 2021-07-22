; For use with ARMIPS
; 2021/06/09
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------

;.org 0x020587D8
;.area 0x4
;	nop
;.endarea

;.org 0x020587F8
;.area 0x4
;	nop
;.endarea

.org HookHPDisplay1
.area 0x4
	ldrsh r0,[r8,#+0x10]
.endarea
.org HookHPDisplay2
.area 0x10
	ldr r1,[r9,#+0x28]
	cmp r1,r0
	movgt r1,r0
	nop
.endarea
