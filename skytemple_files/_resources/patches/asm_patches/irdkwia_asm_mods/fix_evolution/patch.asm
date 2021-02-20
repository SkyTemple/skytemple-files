; For use with ARMIPS
; 2021/02/06
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Fix the evolution glitch
; ------------------------------------------------------------------------------


.org 0x0238CC70
.area 0x8
	b 0x0238CE34
	str r0,[r3, #+0x3c]
.endarea

.org 0x0238CC88
.area 0x4
	bl 0x0202511C
.endarea

.org 0x0238CE44
.area 0xC
	mov  r2,#0xA
	ldr r3,[r1, #+0x0]
	b 0x0238CC74
.endarea
