; For use with ARMIPS
; 2021/02/06
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Use filestreams instead of hardcoded lists 
; ------------------------------------------------------------------------------

.definelabel BufferRead, 0x020A1188
.definelabel RanksFName, 0x020A118C
.definelabel RanksFStream, 0x020A11A0
.definelabel LoadRank, 0x020A1058
;LoadRank(r0: floor_id, r1: group_id)
.definelabel FRankHook1, 0x0204FB28
.definelabel FRankHook2, 0x0204FB94

.org FRankHook1
.area 0x24
	ldrb r0,[r13, #+0x1]
	mov r1,r2
	bl LoadRank
	nop
	nop
	nop
	add  r13,r13,#0x4
	ldmia  r13!,{r3,r4,r15}
	nop
.endarea

.org FRankHook2
.area 0x30
	ldrb r0,[r13, #+0x1]
	cmp r0,#0x1
	mov r1,r2
	movle  r0,#0x2
	bl LoadRank
	nop
	nop
	nop
	nop
	add  r13,r13,#0x4
	ldmia  r13!,{r3,r4,r15}
	nop
.endarea

.org LoadRank
.area 0x130
	stmdb  r13!,{r5,r6,r7,r8,r14}
	mov r5,r0
	mov r6,r1
	ldr r7,=RanksFStream
	ldr r8,=BufferRead
	bl FStreamAlloc
	mov r0,r7
	bl FStreamCtor
	mov r0,r7
	ldr r1,=RanksFName
	bl FStreamFOpen
	
	; Get the offset in file
	mov r0,r7
	mov r1,r6,lsl #0x2
	mov r2,#0x0
	bl FStreamSeek
	mov r0,r7
	mov r1,r8
	mov r2,#0x4
	bl FStreamRead
	
	; Get the mission floor byte
	mov r0,r7
	ldr r1,[r8, #+0x0]
	add r1,r1,r5
	mov r2,#0x0
	bl FStreamSeek
	mov r0,r7
	mov r1,r8
	mov r2,#0x1
	bl FStreamRead
	
	; Close the stream
	mov r0,r7
	bl FStreamClose
	bl FStreamDealloc
	ldrb r0,[r8, #+0x0]
	ldmia  r13!,{r5,r6,r7,r8,r15}
	.pool
	.fill (BufferRead - .), 0xCC;
.endarea

.org BufferRead
.area 0x4
	.fill 0x4, 0;
.endarea

.org RanksFName
.area 0x14
	.ascii "BALANCE/f_ranks.bin"
	dcb 0
.endarea

.org RanksFStream
.area 0x48
	.fill 0x48, 0;
.endarea
