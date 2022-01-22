; For use with ARMIPS
; 2021/07/18
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------

.org Ov10PatchZone
.area 0x400
interrupted_floor:
	.word 0
SetInterrupt:
	ldr r1,=interrupted
	strb r0,[r1]
	bx r14
ClearInterruption:
	ldr r0,=interrupted_floor
	mov r2,#0
	str r2,[r0]
	ldr r1,=interrupted
	strb r2,[r1]
	ldr r3,=music_no_interrupt
	str r2,[r3]
	bx r14
FillIfNotInterrupted:
	mov r1,#0
	ldr r0,[r13,#+0x44]
	cmp r0,#0
	beq no_fill
	ldr r2,=interrupted
	ldrb r0,[r2]
	cmp r0,#1
	movne r1,#1
no_fill:
	bx r14
CheckConquest:
	stmdb r13!,{r14}
	ldr r3,=interrupted
	ldrb r2,[r3]
	cmp r2,#1
	mov r2,#0
	strb r2,[r3]
	blne SetConquest
	ldmia r13!,{r15}
CheckEndDungeon:
	stmdb r13!,{r14}
	ldr r1,=interrupted
	ldrb r0,[r1]
	cmp r0,#1
	.if InterruptOnly == 1
		blne RefillTeam
	.else
		nop
	.endif
	ldmia r13!,{r15}
	.pool
music_no_interrupt:
	.word 0
MusicFadeOut:
	ldr r0,[music_no_interrupt]
	cmp r0,#0
	bne EndMusicFadeOut
	mov  r0,#0x14
	bl FuncFadeOut1
	mov  r0,#0x14
	bl FuncFadeOut2
	b EndMusicFadeOut
MusicInterrupt:
	ldr r0,[music_no_interrupt]
	cmp r0,#0
	bne EndMusicInterrupt
	bl FuncStop1
	bl FuncStop2
	b EndMusicInterrupt
CheckDungeonInterrupt:
	ldr r0,=interrupted_floor
	str r1,[r0]
	stmdb r13!, {r4,r5,r6,r7,r8}
	mov r8,#0
	mov r4,r1
	ldr r0,=DungeonBaseStructurePtr
	ldr r0,[r0]
	ldrb r5,[r0,#+0x748]
	movge r8,#1
	
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
	and r1,r1,#0x7F
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
	cmp r0,#5
	addls r15,r15,r0,lsl #0x2
	b end_switch
	b end_switch
	b case_1
	b case_2
	b case_3
	b case_4
	b case_5
case_1:
	mov r4,#0
	b case_common_1_2
case_2:
	mov r4,#1
case_common_1_2:
	mov r0,#0
	ldrh r1,[r7,#+0x2]
	ldrh r2,[r7,#+0x4]
	bl GetGameVarPos
	cmp r0,r4
	movne r6,#0
	b end_switch
case_3:
	mov r4,#0
	b case_common_3_4_5
case_4:
	mov r4,#1
	b case_common_3_4_5
case_5:
	mov r4,#2
case_common_3_4_5:
	mov r0,#0
	ldrh r1,[r7,#+0x2]
	mov r2,#0
	bl GetGameVarPos
	ldrb r1,[r7,#+0x4]
	cmp r0,r1
	bne check_case_common_3_4_5
	mov r0,#0
	ldrh r1,[r7,#+0x2]
	mov r2,#1
	bl GetGameVarPos
	ldrb r1,[r7,#+0x5]
	cmp r0,r1
check_case_common_3_4_5:
	blt check_case_4
	bgt check_case_5
	b end_switch
check_case_4:
	cmp r4,#1
	movne r6,#0
	b end_switch
check_case_5:
	cmp r4,#2
	movne r6,#0
end_switch:
	cmp r6,#0
	beq continue_exec
	ldrb r0,[r7,#+0x0]
	tst r0,#0x80
	movne r1,#1
	ldrne r0,=music_no_interrupt
	strne r1,[r0]
	mov r0,#1
	bl SetInterrupt
	ldmia r13!, {r4,r5,r6,r7,r8}
	b EndExecution
continue_exec:
	cmp r8,#0
	ldr r0,=interrupted_floor
	mov r1,#0
	str r1,[r0]
	ldmia r13!, {r4,r5,r6,r7,r8}
	bne EndExecution
	b ContinueExecution
	.pool
info:
	.word 0x00000000
	.word 0x00000000
interrupted:
	.word 0x00000000
filestream:
	.fill 0x48, 0x0
filename:
	.ascii "BALANCE/inter_d.bin",0
.endarea
