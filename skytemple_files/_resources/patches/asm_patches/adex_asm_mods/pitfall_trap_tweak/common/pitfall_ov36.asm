.org 0x023A7080+0xA00
.area 0xA60-0xA00

FallenAndCantGetUp:
    
	; r0 = Dereferenced DungeonBaseStructPtr
	; r1 = 0x2
	push r0-r12,r14
	mov r4,r0
	strb r1,[r4,6h] ; Advance to the next floor
	ldrb r0,[r4,0x748] ; Dungeon ID
	bl DungeonGoesUp
	cmp r0,#0
	popeq r0-r12,r15 ; Dungeon is descending
	ldrb r0,[r4,0x749] ; Floor ID
	subs r0,r0,#2
	movmi r0,#0 ; Avoiding underflow
	strb r0,[r4,0x749]
	mov r0,#1
	str r0,[PITFALL_ACTIVE_FLAG]
	pop r0-r12,r15

ShouldDisplayUi:
	ldr r0,[PITFALL_ACTIVE_FLAG]
	cmp r0,#0
	popne r4-r11,r15
	sub r13,r13,#0x44 ; Original instruction
	b DisplayUiStart+4

ResetPitfallFlag:
	mov r0,#2 ; Original instruction
	mov r1,#0
	str r1,[PITFALL_ACTIVE_FLAG]
	bx r14
    .pool
PITFALL_ACTIVE_FLAG:
	.word 0x0
.endarea
