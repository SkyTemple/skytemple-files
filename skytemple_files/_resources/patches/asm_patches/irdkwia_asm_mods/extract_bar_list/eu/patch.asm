; For use with ARMIPS
; 2021/03/11
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Use filestreams to load bar item list
; ------------------------------------------------------------------------------

.definelabel FullLoad1, 0x0238ACEC
.definelabel CheckOnly1, 0x0238B1F8
.definelabel CheckOnly2, 0x0238D130
.definelabel FullLoad2, 0x0238DC60

.definelabel BarGetListFunc, 0x0238AC80
.definelabel BarListFunc, 0x0238E700
.definelabel BarFStream, BarListFunc+0x5AC - 0x48
.definelabel BarFName, BarFStream - 0x14
.definelabel BufferRead, BarFName - 0x16
.definelabel PageCache, BufferRead - 0x2
.definelabel PageData, PageCache - 0x400

.org BarGetListFunc
.area 0x40
	stmdb  r13!,{r14}
	bl BarListFunc
	ldmia  r13!,{r15}
check_only:
	stmdb  r13!,{r14}
	mov r1,#0
	bl BarGetListFunc
	ldmia  r13!,{r15}
full_load:
	stmdb  r13!,{r14}
	mov r1,#1
	bl BarGetListFunc
	ldmia  r13!,{r15}
	.fill BarGetListFunc + 0x40 - ., 0xCC
.endarea

.org FullLoad1
.area 0x4
	bl full_load
.endarea
.org CheckOnly1
.area 0x4
	bl check_only
.endarea
.org CheckOnly2
.area 0x4
	bl check_only
.endarea
.org FullLoad2
.area 0x4
	bl full_load
.endarea

.org BarListFunc
.area PageData-BarListFunc
	stmdb  r13!,{r5,r6,r7,r8,r9,r10,r14}
	mov r5,r1
	mov r6,r0
	mov r9, #0
	
	ldr r8,=PageCache
	mov r7, r6, lsr 0x9
	ldrh r8,[r8]
	subs r10,r8,r7
	cmpeq r5,#0
	beq no_read
	
	mov r9, #1
	ldr r7,=BarFStream
	ldr r8,=BufferRead
	bl FStreamAlloc
	mov r0,r7
	bl FStreamCtor
	mov r0,r7
	ldr r1,=BarFName
	bl FStreamFOpen
	
	movs r10,r10
	beq no_read
	
	mov r0,r7
	mov r1,r8
	mov r2,#0x4
	bl FStreamRead
	
	; Get the offset in file
	mov r0,r7
	mov r1, r6, lsr 0x9
	mov r1, r1, lsl #0x9
	mov r2,#0x1 ; Relative seek
	bl FStreamSeek
	mov r0,r7
	ldr r1,=PageData
	mov r2,#0x400
	bl FStreamRead
	
	ldr r1,=PageCache
	mov r0, r6, lsr 0x9
	strh r0,[r1]
no_read:
	ldr r1,=0x1FF
	and r0,r6,r1
	ldr r1,=PageData
	mov r0,r0,lsl 0x1
	ldrsh r1,[r1, r0]
	mvn r0, #0
	cmp r0,r1
	moveq r6,#0
	beq end
	cmp r5,#0
	moveq r6,#1
	beq end
	
	ldr r0,[r8, #+0x0]
	mov r2,#0x14
	mla r1,r1,r2,r0
	mov r0,r7
	mov r2,#0x0
	bl FStreamSeek
	mov r0,r7
	add r1,r8,#0x2
	mov r2,#0x14
	bl FStreamRead
	mov r6,r8
end:
	; Close the stream
	cmp r9,#0
	beq no_close
	mov r0,r7
	bl FStreamClose
	bl FStreamDealloc
no_close:
	mov r0,r6
	ldmia  r13!,{r5,r6,r7,r8,r9,r10,r15}
	.pool
	.fill PageData - ., 0xCC
.endarea

.org PageData
.area 0x400
	.fill 0x400, 0
.endarea
.org PageCache
.area 0x2
	.fill 0x2, 0xFF
.endarea

.org BufferRead
.area 0x16
	.fill 0x16, 0
.endarea

.org BarFName
.area 0x14
	.ascii "BALANCE/itembar.bin"
	dcb 0
.endarea

.org BarFStream
.area 0x48
	.fill 0x48, 0
.endarea
