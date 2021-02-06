; For use with ARMIPS
; 2021/02/06
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Use filestreams instead of hardcoded lists 
; ------------------------------------------------------------------------------

.definelabel HookFunction1, 0x0200E094
.definelabel HookFunction2, 0x020637D8
.definelabel GetMaxReachedFloor, 0x0204D630
.definelabel LoadItemTable, 0x02095130
.definelabel BufferReadA, 0x020982B4
.definelabel AItemsFName, 0x020982D4
.definelabel AItemsFStream, 0x020982E8

.org HookFunction1
.area 0x48
outer_loop:
	mov r4, #0x0
inner_loop:
	add r0, r4, r3, lsl #0x5
	bl GetMaxReachedFloor
	cmp r0, #0x0
	beq inner_loop_add
	mov r0, #0x1
	orr r5, r5, r0, lsl r4
inner_loop_add:
	add r4, r4, #0x1
	cmp r4, 0x20
	blt inner_loop
end_inner_loop:
	mov r0, r3
	ldr r0, [r6, +r0]
	ands r5, r0, r5
	bne item_available
	add r3, r3, #0x1
	cmp r3, 0x8
	blt outer_loop
	b end_outer_loop
.endarea

.org HookFunction2
.area 0x4C
	stmdb  r13!,{r3,r4,r5,r6,r14}
	b LoadItemTable
end_load_item_table:
	mov r3, #0x0
	mov r5, #0x0
	b outer_loop
end_outer_loop: 
	mov r0, #0x0
	ldmia  r13!,{r3,r4,r5,r6,r15}
item_available: 
	mov r0, #0x1
	ldmia  r13!,{r3,r4,r5,r6,r15}
	.fill (HookFunction2 + 0x4C - .), 0xCC;
.endarea

.org LoadItemTable
.area 0x3184
	ldr r6,=BufferReadA
	mov r4,r0
	ldr r5,=AItemsFStream
	bl FStreamAlloc
	mov r0,r5
	bl FStreamCtor
	mov r0,r5
	ldr r1,=AItemsFName
	bl FStreamFOpen
	
	; Get the line in file
	mov r0,r5
	mov r1,r4,lsl #0x5
	mov r2,#0x0
	bl FStreamSeek
	mov r0,r5
	mov r1,r6
	mov r2,#0x20
	bl FStreamRead
	
	; Close the stream
	mov r0,r5
	bl FStreamClose
	bl FStreamDealloc
	
	b end_load_item_table
	
	.pool
	.fill (BufferReadA - .), 0xCC;
.endarea

.org BufferReadA
.area 0x20
	.fill 0x20, 0;
.endarea

.org AItemsFName
.area 0x14
	.ascii "BALANCE/a_items.bin"
	dcb 0
.endarea

.org AItemsFStream
.area 0x48
	.fill 0x48, 0;
.endarea
