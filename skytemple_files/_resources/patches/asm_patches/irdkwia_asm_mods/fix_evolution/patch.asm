; For use with ARMIPS
; 2021/02/20
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Fixes the evolution glitch
; ------------------------------------------------------------------------------


.org 0x0238CC70
.area 0x28
	ldr r1,[r15, #+0x2c]
	ldr r3,[r1, #+0x0]
	str r0,[r3, #+0x3c]
	ldr r0,[r1, #+0x0]
	ldr r1,[r0, #+0x3c]
	add  r0,r0,#0xB1
	add  r1,r1,#0x3A
	mov  r2,#0xA
	bl 0x0202511C
	ldmia  r13!,{r3,r15}
.endarea

.org 0x0238CE44
.area 0xC
	; Revert the changes from the previous patch
	.fill 0xC, 0
.endarea
