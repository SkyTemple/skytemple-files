; For use with ARMIPS
; 2021/04/10
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Change the evo system
; ------------------------------------------------------------------------------

.org GenerateMissionEggPkmn
.area GMEPSize
	stmdb  r13!,{r3,r4,r5,r6,r14}
	sub  r13,r13,#0xC
	mov r4,r0
	ldrb r0,[r0, #+0x16]
	cmp r0,#0x5
	bne no_egg
	bl GetRandomSpawnPkmnID
	mov  r6,r0
	bl FStreamAlloc
	bl CheckOpen
	mov r1,r6,lsl #0x5
	add r1,r1,#0x16
	ldr r0,=filestream
	mov r2, #0
	bl FStreamSeek
	ldr r0,=filestream
	mov r1,r13
	mov r2,#0x2
	bl FStreamRead
	ldrh r5,[r13]
	ldr r0,=filestream
	mov r1,r13
	mov r2,#0xC
	bl FStreamRead
	bl FStreamDealloc
	cmp r5,#0
	beq str_egg
	cmp r5,#1
	ldreqsh r6,[r13]
	beq str_egg
	mov r0,r5
	bl RandMax
	mov r0,r0,lsl #0x1
	ldrsh r6,[r13,r0]
str_egg:
	strh r6,[r4, #+0x18]
no_egg:
	add  r13,r13,#0xC
	ldmia  r13!,{r3,r4,r5,r6,r15}
	.pool
	.fill (GenerateMissionEggPkmn+GMEPSize-.), 0xCC
.endarea
