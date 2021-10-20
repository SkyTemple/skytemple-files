; For use with ARMIPS
; 2021/06/09
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Implements Move Growth
; ------------------------------------------------------------------------------

.org HookMenuPP1
.area 0x68
	add  r5,r4,#0x124
label_hmpp1_2:
	ldrb r0,[r5,+r9, lsl #0x3]
	add  r8,r5,r9,lsl #0x3
	tst r0,#0x1
	beq label_hmpp1_1
	ldrh r1,[r8, #+0x2]
	bic  r1,r1,#0x100
	strh r1,[r8, #+0x2]
	mov  r0,r6
	mov  r1,r8
	bl GetPPWithLevelBonus
	ldrb r1,[r8, #+0x6]
	cmp r1,r0
	ble label_hmpp1_1
	mov  r0,r6
	mov  r1,r8
	bl GetPPWithLevelBonus
	strb r0,[r8, #+0x6]
label_hmpp1_1:
	add  r9,r9,#0x1
	cmp r9,#0x4
	blt label_hmpp1_2
	nop
	nop
	nop
.endarea
