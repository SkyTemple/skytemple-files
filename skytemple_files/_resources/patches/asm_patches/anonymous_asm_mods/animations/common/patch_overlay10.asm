; For use with ARMIPS
; 2021/06/07
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Use filestreams to load animation specs
; ------------------------------------------------------------------------------

.org AnimationFunctions
.area 0x90
	stmdb r13!, {r14}
	bl LoadIfNot
	bl ReadGlobalAnimation
	ldmia r13!, {r15}
	nop
	stmdb r13!, {r14}
	bl LoadIfNot
	bl ReadMoveAnimation
	ldmia r13!, {r15}
	nop
	stmdb r13!, {r14}
	bl LoadIfNot
	bl ReadSpecialMoveAnimation
	ldmia r13!, {r15}
	nop
	stmdb r13!, {r14}
	bl LoadIfNot
	bl ReadTrapAnimation
	ldmia r13!, {r15}
	nop
	stmdb r13!, {r14}
	bl LoadIfNot
	mov r1, #0
	bl ReadItemAnimation
	ldmia r13!, {r15}
	stmdb r13!, {r14}
	bl LoadIfNot
	mov r1, #1
	bl ReadItemAnimation
	ldmia r13!, {r15}
	stmdb r13!, {r14}
	bl LoadIfNot
	bl ReadMoveAnimation
	ldr r0, [r0, #+0xC]
	ldmia r13!, {r15}
	nop
.endarea

.org AnimationSector
.area 0x14560
LoadIfNot:
	stmdb r13!, {r0,r1,r2,r3,r14}
	ldr r0,=IsLoadedFile
	ldr r1,[r0]
	cmp r1,#0
	bne no_load
	mov r1,#1
	str r1,[r0]
	bl FStreamAlloc
	ldr r0,=AnimFileStream
	bl FStreamCtor
	ldr r0,=AnimFileStream
	ldr r1,=AnimFileName
	bl FStreamFOpen
	bl FStreamDealloc
no_load:
	ldmia r13!, {r0,r1,r2,r3,r15}
	.pool
ReadPartFile: ;(r0: main_id, r1: sec_id, r2: buffer, r3: size, [r13]: elts)
	stmdb r13!, {r4,r5,r6,r7,r8,r14}
	;.word 0x773e3b33 ; To test file usage
	mov r4,r0
	mov r5,r1
	mov r6,r2
	mov r7,r3
	ldr r8,[r13,#+0x18]
	bl FStreamAlloc
	ldr r0,=AnimFileStream
	mov r1,r4,lsl #0x2
	mov r2, #0
	bl FStreamSeek
	ldr r0,=AnimFileStream
	ldr r1,=BufferFilePtr
	mov r2,#0x4
	bl FStreamRead
	ldr r1,=BufferFilePtr
	ldr r1,[r1]
	mla r4,r7,r5,r1
	mov r1,r4
	ldr r0,=AnimFileStream
	mov r2, #0
	bl FStreamSeek
	ldr r0,=AnimFileStream
	bl FGetSize
	mla r2,r7,r8,r4
	cmp r2,r0
	movge r2,r0
	sub r2,r2,r4
	ldr r0,=AnimFileStream
	mov r1,r6
	bl FStreamRead
	bl FStreamDealloc
	ldmia r13!, {r4,r5,r6,r7,r8,r15}
	.pool
ReadGlobalAnimation: ; (r0: anim_id)
	stmdb r13!, {r14}
	ldr r1,=CurrentGlobalAnim
	ldrsh r2, [r1]
	cmp r2,r0
	beq no_global_read
	strh r0, [r1]
	sub r13,r13,#0x4
	mov r1,r0
	mov r0, #1
	str r0, [r13]
	mov r0, #3
	ldr r2,=BufferGlobalAnim
	mov r3, #0x1C
	bl ReadPartFile
	add r13,r13,#0x4
no_global_read:
	ldr r0,=BufferGlobalAnim
	ldmia r13!, {r15}
	.pool
ReadMoveAnimation: ; (r0: move_id)
	stmdb r13!, {r14}
	ldr r1,=CurrentMoveAnim
	ldrsh r2, [r1]
	cmp r2,r0
	beq no_move_read
	strh r0, [r1]
	sub r13,r13,#0x4
	mov r1,r0
	mov r0, #1
	str r0, [r13]
	mov r0, #2
	ldr r2,=BufferMoveAnim
	mov r3, #0x18
	bl ReadPartFile
	add r13,r13,#0x4
no_move_read:
	ldr r0,=BufferMoveAnim
	ldmia r13!, {r15}
	.pool
ReadSpecialMoveAnimation: ; (r0: ent_id)
	stmdb r13!, {r14}
	ldr r1,=CurrentSpecialMoveAnim
	ldr r2, [r1]
	cmp r2,r0
	beq no_spe_move_read
	;.word 0x773e3b34
	str r0, [r1]
	sub r13,r13,#0x4
	mov r1,r0
	mov r0, #0x800
	str r0, [r13]
	mov r0, #4
	ldr r2,=BufferSpecialMoveAnim
	mov r3, #0x6
	bl ReadPartFile
	add r13,r13,#0x4
no_spe_move_read:
	ldr r0,=BufferSpecialMoveAnim
	ldmia r13!, {r15}
	.pool
ReadItemAnimation: ; (r0: item_id, r1: pos)
	stmdb r13!, {r4,r14}
	mov r4,r1,lsl #0x1
	ldr r1,=CurrentItemAnim
	ldrsh r2, [r1]
	cmp r2,r0
	beq no_item_read
	strh r0, [r1]
	sub r13,r13,#0x4
	mov r1,r0
	mov r0, #1
	str r0, [r13]
	mov r0, #1
	ldr r2,=BufferItemAnim
	mov r3, #0x4
	bl ReadPartFile
	add r13,r13,#0x4
no_item_read:
	ldr r0,=BufferItemAnim
	ldrsh r0,[r0,r4]
	ldmia r13!, {r4,r15}
	.pool
ReadTrapAnimation: ; (r0: trap_id)
	stmdb r13!, {r14}
	ldr r1,=CurrentTrapAnim
	ldrsh r2, [r1]
	cmp r2,r0
	beq no_trap_read
	strh r0, [r1]
	sub r13,r13,#0x4
	mov r1,r0
	mov r0, #1
	str r0, [r13]
	mov r0, #0
	ldr r2,=BufferTrapAnim
	mov r3, #0x2
	bl ReadPartFile
	add r13,r13,#0x4
no_trap_read:
	ldr r0,=BufferTrapAnim
	ldrsh r0,[r0]
	ldmia r13!, {r15}
	.pool
AnimFileName:
	.ascii "BALANCE/anim.bin"
	.fill 0x2, 0x0
BufferTrapAnim: 
	.fill 0x2, 0x0
CurrentGlobalAnim: 
	.fill 0x2, 0xFF
CurrentMoveAnim: 
	.fill 0x2, 0xFF
CurrentTrapAnim: 
	.fill 0x2, 0xFF
CurrentItemAnim: 
	.fill 0x2, 0xFF
CurrentSpecialMoveAnim: 
	.fill 0x4, 0xFF
BufferItemAnim: 
	.fill 0x4, 0x0
BufferFilePtr: 
	.fill 0x4, 0x0
BufferGlobalAnim: 
	.fill 0x1C, 0x0
BufferMoveAnim: 
	.fill 0x18, 0x0
BufferSpecialMoveAnim: 
	.fill 0x3000, 0x0
	.fill (AnimationSector+0x14560-.), 0xCC
.endarea
