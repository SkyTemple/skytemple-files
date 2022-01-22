; For use with ARMIPS
; 2021/04/25
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Adds Exp. Share
; ------------------------------------------------------------------------------

.org ExpGainAll
.area 0x4
	b ExpShare
.endarea


.org ReadjustExp
.area 0x4
	b ReadjustExpFunc
.endarea

.org HookLvlUp
.area 0xCC
	; Slightly modified original code
	ldrb r0,[r9, #+0x7]
	cmp r0,#0x0
	ldrneb r1,[r9, #+0xa]
	addne  r0,r13,#0x54
	blne GetTacticsLearned
	ldrsh r2,[r9, #+0x12]
	ldrsh r0,[r9, #+0x16]
	ldrb r7,[r9, #+0x1a]
	ldr r1,[ValueMaxHP]
	add  r0,r2,r0
	ldrb r3,[r9, #+0x1b]
	ldrb r2,[r9, #+0x1c]
	str r0,[r13, #+0x4]
	cmp r0,r1
	strgt r1,[r13, #+0x4]
	ldrb r1,[r9, #+0x1d]
	str r7,[r13, #+0x24]
	str r3,[r13, #+0x28]
	str r2,[r13, #+0x1c]
	str r1,[r13, #+0x20]
	ldr r0,[r13, #+0x8]
	bl IsExpEnabledInDungeon
	cmp r0,#0x0
	ldrneb r0,[r9, #+0xa]
	cmpne r0,MaxLvl
	ldrneb r0,[r9, #+0x6]
	cmpne r0,#0x1
	beq end_hook
	ldr r0,[r9, #+0x20]
	mov  r1,r11
	add  r2,r0,r11
	mov  r0,#0x0
	str r2,[r9, #+0x20]
	bl StoreExp
	bl HookLvlUpJump5
	mov  r1,#0x0
	str r1,[r13, #+0x0]
	mov  r2,r9
	mov  r3,r1
	bl HookLvlUpJump6
	cmp r11,#0x0
	beq no_display
	mov  r0,r10
	ldr r1,[ValueText]
	bl HookLvlUpJump7
no_display:
	mov  r0,r10
	mov  r1,r5
	mov  r2,#0x1
	mov  r3,r2
	bl HookLvlUpJump8
	orr  r6,r6,r0
end_hook:
.endarea
