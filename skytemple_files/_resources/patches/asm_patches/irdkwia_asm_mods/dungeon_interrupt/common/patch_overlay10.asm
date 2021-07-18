; For use with ARMIPS
; 2021/07/18
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------
.definelabel Ov10PatchZone, 0x022DBFB0-0x1000
.definelabel ContinueExecution, 0x022E00C8

.org Ov10PatchZone
.area 0x800
CheckDungeonInterrupt:
	stmdb r13!, {r4,r5,r6,r7}
	mov r4,r1
	ldr r0,=0x02353538
	ldr r0,[r0]
	ldrb r5,[r0,#+0x748]
	
	; Open
	bl FStreamAlloc
	ldr r0,=filestream
	bl FStreamCtor
	ldr r0,=filestream
	ldr r1,=filename
	bl FStreamFOpen
	
	ldr r0,=filestream
	ldr r1,=info
	mov r2,#4
	bl FStreamRead
	
	ldr r0,=filestream
	mov r1,r5,lsl #0x1
	mov r2,#1
	bl FStreamSeek
	
	ldr r0,=filestream
	ldr r1,=info+4
	mov r2,#4
	bl FStreamRead
	
	ldr r0,=info
	ldr r3,[r0]
	ldrh r6,[r0, #+0x4]
	ldrh r7,[r0, #+0x6]
	
	ldr r0,=filestream
	mov r2,#6
	mla r1,r6,r2,r3
	mov r2,#0
	bl FStreamSeek
	b check_loop
loop:
	ldr r0,=filestream
	ldr r1,=info
	mov r2,#6
	bl FStreamRead
	
	ldr r0,=info
	ldrb r1,[r0]
	cmp r4,r1
	moveq r6,#1
	beq end_loop
	add r6,r6,#1
check_loop:
	cmp r6,r7
	blt loop
	mov r6,#0
end_loop:
	; Close
	ldr r0,=filestream
	bl FStreamClose
	bl FStreamDealloc
	
	cmp r6,#0
	beq continue_exec
	
	ldr r7,=info
	ldrb r0,[r7,#+0x1]
	cmp r0,#2
	addls r15,r15,r0,lsl #0x2
	b end_switch
	b end_switch
	b case_1
case_1:
	mov r0,#0
	ldrh r1,[r7,#+0x2]
	ldrb r2,[r7,#+0x4]
	bl 0x0204B678
	ldrb r1,[r7,#+0x5]
	cmp r0,r1
	movne r6,#0
end_switch:
	cmp r6,#0
	beq continue_exec
	ldmia r13!, {r4,r5,r6,r7}
	b EndExecution
continue_exec:
	ldmia r13!, {r4,r5,r6,r7}
	b ContinueExecution
	.pool
info:
	.word 0x00000000
	.word 0x00000000
filestream:
	.fill 0x48, 0x0
filename:
	.ascii "BALANCE/inter_d.bin",0
.endarea
