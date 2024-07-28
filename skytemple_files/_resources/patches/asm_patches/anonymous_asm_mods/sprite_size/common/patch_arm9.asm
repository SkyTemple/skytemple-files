; Sprite Size in monster.md (0x2C)
.org HookMdAccess7
.area 0x38
	ldr r2,=MonsterFilePtr
	mov  r1,#0x44
	ldr r2,[r2, #+0x0]
	smlabb r0,r0,r1,r2
	ldrb r0,[r0, #+0x2C]
	cmp r0,#0x0
	ldmeqia  r13!,{r3,r15}
	cmp r0,#0x6
	movls  r0,#0x6
	ldmia  r13!,{r3,r15}
	.pool
.endarea

; Sprite File Size in monster.md (0x2D)
.org HookMdAccess8
.area 0x20
	ldr r2,=MonsterFilePtr
	mov  r1,#0x44
	ldr r2,[r2, #+0x0]
	smlabb r0,r0,r1,r2
	ldrb r0,[r0, #+0x2D]
	mov  r0,r0,lsl #0x9
	bx r14
	.pool
.endarea