.org 0x023A7080+0xA00
.area 0xA30-0xA00

FallenAndCantGetUp:
    
	; r0 = Dereferenced DungeonBaseStructPtr
	; r1 = 0x2
	push r0-r12,r14
	mov r4,r0
	strb r1,[r4,6h] ; Advance to the next floor
	ldrb r0,[r4,0x748] ; Dungeon ID
	bl DungeonGoesUp
	cmp r0,#0
	beq fall_ret ; Dungeon is descending
	ldrb r0,[r4,0x749] ; Floor ID
	subs r0,r0,#2
	movmi r0,#0 ; Avoiding underflow
	strb r0,[r4,0x749]
fall_ret:
	pop r0-r12,r15
    .pool
.endarea
