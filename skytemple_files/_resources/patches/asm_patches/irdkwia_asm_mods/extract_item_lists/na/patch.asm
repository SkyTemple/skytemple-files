; For use with ARMIPS
; 2021/01/30
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Use filestreams instead of hardcoded lists 
; ------------------------------------------------------------------------------

.definelabel CacheHoldStruct, 0x0209F1C4
.definelabel CacheUpdateStruct, 0x0209F1CC
.definelabel CacheFunction, 0x0209F594
.definelabel CacheData, 0x0209F904
.definelabel CacheSize, 0x11D0
.definelabel CacheBlocks, 0x6
.definelabel CacheLast, 0x5
.definelabel ListSize, 0x2F8
.definelabel FileNamesTable, 0x020B0948
.definelabel FunctionHook1, 0x0200E054
.definelabel FunctionHook2, 0x0200E1D8
.definelabel FunctionHook3, 0x0200E1EC

.org CacheHoldStruct
.area CacheBlocks
	.fill CacheBlocks, 0x00
.endarea
.org CacheUpdateStruct
.area CacheBlocks
	.fill CacheBlocks, 0x00
.endarea

.org CacheData
.area CacheSize
	.fill CacheSize, 0x00
.endarea

.org CacheFunction
.area 0x180
	mov r8,#0x0
	mov r0,#0x0
	mov r7,#0x0
	mov r11,CacheBlocks
	ldr r2,=CacheHoldStruct
cache_find_loop:
	; Il faut que je cache des trucs
	ldrb r1, [r2, +r0]
	cmp r1,r6
	bne next_find_loop
	ldr r7,=CacheData
	mov r1,ListSize
	mla r7,r1,r0,r7
	mov r11,r0
	mov r8,#0x1
	b end_find_loop
next_find_loop:
	add r0,r0,#0x1
	cmp r0,CacheBlocks
	blt cache_find_loop
end_find_loop:

	mov r0,#0x0
	ldr r2,=CacheUpdateStruct
	cmp r8, #0x1
	ldreqb r10, [r2, +r11]
	movne r10, #0x0
	
cache_update_loop:
	ldrb r1, [r2, +r0]
	cmp r1,#0x0
	cmpeq r8,#0x0
	cmpeq r7,#0x0
	bne skip_choice
	ldr r7,=CacheHoldStruct
	strb r6, [r7, +r0]
	ldr r7,=CacheData
	mov r9,ListSize
	mla r7,r9,r0,r7
	mov r11,r0
skip_choice:
	cmp r1,r10
	subgt r1,r1,#0x1
	cmp r0,r11
	moveq r1,CacheLast
	strb r1, [r2, +r0]
	
next_update_loop:
	add r0,r0,#0x1
	cmp r0,CacheBlocks
	blt cache_update_loop
end_update_loop:
	cmp r8,#0x1
	beq no_need_alloc
	b need_alloc
	.pool
.endarea

.org FunctionHook1
.area 0xF4
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r14}
	mov  r6,r0
	mov  r5,r1
	mov  r4,r2
	cmp r6,#0x0
	moveq r6,#0x1
	b CacheFunction
	nop
	nop
	nop
need_alloc: 
	mov  r0,#0x48
	mov  r1,#0x0
	bl MemAlloc
	mov r8,r0
	ldr r0,=FileNamesTable
	sub  r1,r6,#0x1
	ldr r6,[r0,+r1, lsl #0x2]

	; Open File Stream

	bl FStreamAlloc
	mov r0,r8
	bl FStreamCtor
	mov r0,r8
	mov r1,r6
	bl FStreamFOpen

	; Loop
	ldr r10,=0xffff8ad0
	sub  r13,r13,#0x4
	mov  r11,#0x0
	rsb  r6,r10,#0x0
	b cond_main

main_loop:
	mov r0,r8 ; Read in buffer
	mov r1,r13
	mov r2,#0x2
	bl FStreamRead
	ldrh r14,[r13, +0x0]
	cmp r14,r6
	bcc nocopy
	add  r14,r14,r10
	b cond_copy
copy_loop:
	mov  r9,r11,lsl #0x1
	mov r0, #0x0
	strh r0,[r7, +r9]
	add  r11,r11,#0x1
	sub  r14,r14,#0x1
cond_copy:
	cmp r14,#0x0
	bne copy_loop
	b next_main
nocopy:
	mov  r9,r11,lsl #0x1
	strh r14,[r7, +r9]
	add  r11,r11,#0x1
next_main:
	add  r0,r0,#0x1
cond_main:
	mov r14, #0x2F8
	cmp r11, r14, asr 0x1
	blt main_loop

end_loop:
	add  r13,r13,#0x4

	mov r0,r8
	bl FStreamClose
	bl FStreamDealloc
	mov r0,r8
	bl MemFree

	;Free Space

	nop
	nop
	nop
no_need_alloc:
.endarea

; Remove the blocks allocation
.org FunctionHook2
.area 0x10
	nop
	nop
	nop
	nop
.endarea

.org FunctionHook3
.area 0xC
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
	.pool
.endarea
