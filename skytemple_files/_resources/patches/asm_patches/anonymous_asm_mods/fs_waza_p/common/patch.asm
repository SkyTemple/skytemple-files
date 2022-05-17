; For use with ARMIPS
; 2021/04/07
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Use filestreams to access waza_p/waza_p2 instead of loading it entirely
; Useless in itself
; ------------------------------------------------------------------------------

; ///////////////////////////////////////////////////// WazaP load functions


.org UnloadCurrentWazaP
.area 0x40
	b TrueUnloadCurrentWazaP
here:
	ldr r2,=ReadMoveBuffer
	ldr r1,[r2]
	add r9,r9,r1
	add r1,r1,#0x1C
	cmp r1,#0x8C0
	movge r1,#0
	str r1,[r2]
	strh r4,[r9]
	b there
	.pool
	.fill 0x14, 0xCC
.endarea

.org LoadWazaP
.area 0x28
	stmdb  r13!,{r3,r14}
	ldr r1,=CurrentWazaInfo
	mov  r0,#0x0
	str r0,[r1, #+0x4]
	bl OpenWaza
	ldr r0,=CurrentWazaInfo
	ldr r0,[r0, #+0x4]
	bl SelectWaza
	ldmia  r13!,{r3,r15}
	.pool
.endarea

.org LoadWazaP2
.area 0x28
	stmdb  r13!,{r3,r14}
	ldr r1,=CurrentWazaInfo
	mov  r0,#0x1
	str r0,[r1, #+0x4]
	bl OpenWaza
	ldr r0,=CurrentWazaInfo
	ldr r0,[r0, #+0x4]
	bl SelectWaza
	ldmia  r13!,{r3,r15}
	.pool
.endarea


; TODO: Change Position
.org OpenWaza
.area 0x68
	b TrueOpenWaza
MVAlloc:
	stmdb r13!, {r4,r14}
	ldr r4,=buffer_ptr
	ldr r0,[r4]
	cmp r0,#0
	bne after_alloc
	mov r0,#0x8C0
	mov r1,#0
	bl MemAlloc
after_alloc:
	str r0,[r4]
	mov r1,#0xFF
	mov r2,#0x8C0
	bl FillWithConstant1ByteArray
	ldr r1,=ReadMoveBuffer
	mov r0,#0
	str r0,[r1]
	ldmia r13!, {r4,r15}
	.pool
string_ms:
	.ascii "MS: %d for %d"
	dcb 0
string_mv:
	.ascii "MV: %d"
	dcb 0
	.fill 0x7, 0xCC
.endarea

.org SelectWaza
.area 0x2C
	ldr r1,=MoveInfoTableAddr
	ldr r2,=MovesetTableAddr
	ldr r3,[r1,+r0, lsl #0x2]
	ldr r1,=CurrentWazaInfo
	ldr r0,[r2,+r0, lsl #0x2]
	str r3,[r1, #+0x8]
	str r0,[r1, #+0x0]
	bx r14
	.pool
.endarea


; ///////////////////////////////////////////////////// WazaP read functions

.org TrueUnloadCurrentWazaP
.area 0x120
	stmdb  r13!,{r4,r14}
	bl FStreamAlloc
	ldr r0,=CurrentWazaInfo
	ldr r1,=WazaFileInfo
	ldr r0,[r0, #+0x4]
	add  r4,r1,r0,lsl #0x3
	mov  r0,r4
	bl FStreamClose
	bl FStreamDealloc
	mov  r0,r4
	bl MemFree
	mov  r0,r4
	bl FillWithZeros8Bytes
	ldr r1,=CurrentWazaInfo
	mov  r0,#0x0
	str r0,[r1, #+0x4]
	bl SelectWaza
	ldmia  r13!,{r4,r15}
	.pool
TrueOpenWaza:
	stmdb  r13!,{r3,r4,r5,r14}
	sub  r13,r13,#0x4
	mov  r4,r0
	mov  r0,#0x48 ;TODO: Change if we need more size
	mov  r1,#0x0
	bl MemAlloc
	ldr r1,=WazaFileInfo
	mov r5,r0
	str r5,[r1,+r4, lsl #0x3]
	
	bl MVAlloc
	bl FStreamAlloc
	mov r0,r5
	bl FStreamCtor
	mov r0,r5
	ldr r1,=WazaFileNamesPtr
	ldr r1,[r1,+r4, lsl #0x2]
	add r1,r1,#6
	bl FStreamFOpen
	mov r0,r5
	mov r1,#4
	mov r2,#0
	bl FStreamSeek
	mov r0,r5
	mov r1,r13
	mov r2,#4
	bl FStreamRead
	mov r0,r5
	ldr r1,[r13]
	mov r2,#0
	bl FStreamSeek
	
	ldr r1,=MoveInfoTableAddr
	mov r0,r5
	add r1,r1,r4,lsl #0x2
	mov r2,#4
	bl FStreamRead
	ldr r1,=MovesetTableAddr
	mov r0,r5
	add r1,r1,r4,lsl #0x2
	mov r2,#4
	bl FStreamRead
	bl FStreamDealloc
	add  r13,r13,#0x4
	ldmia  r13!,{r3,r4,r5,r15}
	.pool
	.fill (TrueUnloadCurrentWazaP+0x120-.), 0xCC
.endarea
.org ReadMoveValue
.area 0xD4
	stmdb  r13!,{r4,r5,r6,r7,r8,r9,r10,r14}
	mov r4,r0
	mov r5,r1
	mov r6,r2
	ldr r3,=CurrentWazaInfo
	ldr r1,=WazaFileInfo
	ldr r2,[r3, #+0x4]
	ldr r7,[r1,+r2, lsl #0x3]
	ldr r3,[r3, #+0x8] ;r3 contains the start table address
	mov  r0,#0x1A
	mla  r8,r4,r0,r3 ;r8 contains the move offset
	mov r0,r7
	bl FGetSize
	add r0,r0,#0x1A
	cmp r0,r8
	blt no_read_move
	ldr r9,[buffer_ptr]
	mov r10,#0
loop_buffer:
	ldrh r0,[r9]
	cmp r4,r0
	beq no_read_move
	add r10,r10,#1
	add r9,r9,#0x1C
	cmp r10,#80
	blt loop_buffer
	ldr r9,[buffer_ptr]
	b here
there:
	ldr r0,=string_mv
	mov r1,r4
	;bl PrintF - Can cause a stack overflow
	bl FStreamAlloc
	mov r0,r7
	mov r1,r8
	mov r2,#0
	bl FStreamSeek
	mov r0,r7
	add r1,r9,#2
	mov r2,#0x1A
	bl FStreamRead
	bl FStreamDealloc
no_read_move:
	add r9,r9,#2
	cmp r6,#0
	moveq r0,r9
	beq end_read
	cmp r6,#1
	ldreqb r0,[r9,r5]
	beq end_read
	ldrsh r0,[r9,r5]
end_read:
	ldmia  r13!,{r4,r5,r6,r7,r8,r9,r10,r15}
	.pool
	.fill (ReadMoveValue+0xD4-.), 0xCC
.endarea

.org ReadMoveBuffer
.area 0x8
	.word 0x0
buffer_ptr:
	.word 0x0
.endarea

; r0: result = ReadMoveset(r0: pkmn_id, r1: moveset_id)
.org ReadMoveset
.area 0xA0
	stmdb  r13!,{r4,r5,r6,r7,r14}
	
	mov r4,r0
	mov r5,r1
	ldr r7,=ReadMovesetBuffer
	;mov r2,LSSize
	;mla r7,r2,r1,r7
	ldr r0,=string_ms
	mov r1,r5
	mov r2,r4
	;bl PrintF - Can cause a stack overflow
	bl FStreamAlloc
	ldr r3,=CurrentWazaInfo
	ldr r1,=WazaFileInfo
	ldr r2,[r3, #+0x4]
	ldr r6,[r1,+r2, lsl #0x3]
	ldr r3,[r3, #+0x0] ;r3 contains the start table address
	mov  r0,#0xC
	mla  r1,r4,r0,r3 ;r1 contains the move offset
	add r1,r1,r5,lsl #0x2
	mov r0,r6
	mov r2,#0
	bl FStreamSeek
	mov r0,r6
	mov r1,r7
	mov r2,#0x4
	bl FStreamRead
	mov r0,r6
	ldr r1,[r7]
	mov r2,#0
	bl FStreamSeek
	mov r0,r6
	mov r1,r7
	mov r2,LSSize
	bl FStreamRead
	bl FStreamDealloc
	mov r0,r7
	ldmia  r13!,{r4,r5,r6,r7,r15}
	.pool
	.fill (ReadMoveset+0xA0-.), 0xCC
.endarea

.org ReadMovesetBuffer
.area LSSize
	.fill LSSize, 0x0
.endarea

; ///////////////////////////////////////////////////// WazaP access functions



.org GetMoveFlags
.area 0x24
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,r1,lsl #0x1
	add  r1,r1,#4
	mov  r2,#2
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMoveType
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,#2
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMovesetLevelUpPtr
.area 0x48
	stmdb  r13!,{r4,r14}
	mov  r4,r0
	cmp r4,#0x258
	subge  r0,r4,#0x258
	movge  r0,r0,lsl #0x10
	movge  r4,r0,asr #0x10
	mov  r0,r4
	bl IsInvalidMoveset
	cmp r0,#0x0
	ldrne r0,=NullMoveset
	mov r0,r4
	mov r1,#0
	bl ReadMoveset
	ldmia  r13!,{r4,r15}
	.pool
.endarea

.org IsInvalidMoveset
.area 0x28
	cmp r0,#0x0
	ble below_lower_bound
	ldr r1,=0x00000229
	cmp r0,r1
	blt below_upper_bound
below_lower_bound:
	mov  r0,#0x1
	bx r14
below_upper_bound:
	mov  r0,#0x0
	bx r14
	.pool
.endarea

.org GetMovesetHMTMPtr
.area 0x4C
	stmdb  r13!,{r4,r14}
	mov  r4,r0
	cmp r4,#0x258
	subge  r0,r4,#0x258
	movge  r0,r0,lsl #0x10
	movge  r4,r0,asr #0x10
	mov  r0,r4
	bl IsInvalidMoveset
	cmp r0,#0x0
	ldrne r0,=NullMoveset
	ldmneia  r13!,{r4,r15}
	mov r0,r4
	mov r1,#1
	bl ReadMoveset
	ldmia  r13!,{r4,r15}
	.pool
.endarea

.org GetMovesetEggPtr
.area 0x4C
	stmdb  r13!,{r4,r14}
	mov  r4,r0
	cmp r4,#0x258
	subge  r0,r4,#0x258
	movge  r0,r0,lsl #0x10
	movge  r4,r0,asr #0x10
	mov  r0,r4
	bl IsInvalidMoveset
	cmp r0,#0x0
	ldrne r0,=NullMoveset
	ldmneia  r13!,{r4,r15}
	mov r0,r4
	mov r1,#2
	bl ReadMoveset
	ldmia  r13!,{r4,r15}
	.pool
.endarea

.org GetMoveUnk09
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,#0x9
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMoveNbHits
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,#0xD
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMoveBasePower
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,#0x0
	mov  r2,#2
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMoveBasePowerOverworld
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x2]
	mov  r1,#0x0
	mov  r2,#2
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMoveAccuracy
.area 0x24
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	add  r1,r1,#0xA
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMoveBasePP
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,#0x8
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMovePPWithBonus
.area 0x80
	stmdb  r13!,{r4,r14}
	mov r4,r0
	ldrh r0,[r0, #+0x4]
	mov  r1,#0x8
	mov  r2,#1
	bl ReadMoveValue
	ldrh r2,[r4, #+0x2]
	tst r2,#0x100
	ldrne r1,=IQSkillPPUp
	ldrnesh r1,[r1, #+0x0]
	addne  r0,r0,r1
	movne  r0,r0,lsl #0x10
	movne  r0,r0,asr #0x10
	tst r2,#0x200
	ldrne r1,=ExclusiveItemPPUp2
	ldrnesh r1,[r1, #+0x0]
	addne  r0,r0,r1
	movne  r0,r0,lsl #0x10
	movne  r0,r0,asr #0x10
	tst r2,#0x400
	ldrne r1,=ExclusiveItemPPUp4
	ldrnesh r1,[r1, #+0x0]
	addne  r0,r0,r1
	movne  r0,r0,lsl #0x10
	movne  r0,r0,asr #0x10
	cmp r0,#0x63
	movgt  r0,#0x63
	ldmia  r13!,{r4,r15}
	.pool
.endarea

.org GetMoveMaxGinsengBoost
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,#0xE
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMoveMaxGinsengBoostOverworld
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x2]
	mov  r1,#0xE
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMoveCriticalRate
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,#0xF
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org IsIceBreaker
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,#0x13
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org IsAffectedByTaunt
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,#0x14
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMoveRangeID
.area 0x20
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,#0x15
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org GetMoveActualAccuracy
.area 0x58
	stmdb  r13!,{r3,r14}
	mov  r1,#0
	mov  r2,#0
	bl ReadMoveValue
	mov r1,r0
	ldrb r0,[r1, #+0xe]
	cmp r0,#0x0
	ldreqb r0,[r1, #+0xa]
	ldmeqia  r13!,{r3,r15}
	cmp r0,#0x63
	bne status_move
	ldrb r2,[r1, #+0xa]
	ldrb r0,[r1, #+0xb]
	cmp r2,#0x7D
	ldmeqia  r13!,{r3,r15}
	mul  r0,r2,r0
	mov  r1,#0x64
	bl EuclidianDivision
	ldmia  r13!,{r3,r15}
status_move:
	mov  r0,#0x0
	ldmia  r13!,{r3,r15}
.endarea

.org GetMoveBasePowerWithID
.area 0x1C
	stmdb  r13!,{r14}
	mov  r1,#0x0
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org IsMoveRangeID13
.area 0x2C
	stmdb  r13!,{r14}
	ldrh r0,[r0, #+0x4]
	mov  r1,#0x15
	mov  r2,#1
	bl ReadMoveValue
	cmp r0,#0x13
	moveq  r0,#0x1
	movne  r0,#0x0
	ldmia  r13!,{r15}
.endarea

.org GetMoveMessageID
.area 0x34
	stmdb  r13!,{r14}
	mov  r1,#0x18
	mov  r2,#2
	bl ReadMoveValue
	add  r0,r0,#0x314
	add  r0,r0,#0xC00
	mov  r0,r0,lsl #0x10
	mov  r0,r0,lsr #0x10
	bl UnkGetString
	ldmia  r13!,{r15}
.endarea

.org IsAffectedByMagicCoat
.area 0x1C
	stmdb  r13!,{r14}
	mov  r1,#0x10
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org IsSnatchable
.area 0x1C
	stmdb  r13!,{r14}
	mov  r1,#0x11
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea

.org IsMouthMove
.area 0x1C
	stmdb  r13!,{r14}
	mov  r1,#0x12
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea



.org ConvertOverwoldToDungeonMoveset
.area 0x94
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r14}
	mov  r6,r0
	mov  r8,r1
	mov  r4,#0x0
	mov  r5,#0x6
	mov  r9,#0x0
loop_process_moveset:
	mul  r2,r4,r5
	ldrb r2,[r8, +r2]
	tst r2,#0x1
	streqb r9,[r6,+r4, lsl #0x3]
	beq end_loop_process_moveset
	strb r2,[r6,+r4, lsl #0x3]
	mla  r7,r4,r5,r8
	ldrh r0,[r7, #+0x2]
	mov  r1,#0x8
	mov  r2,#1
	bl ReadMoveValue
	add  r2,r6,r4,lsl #0x3
	strb r0,[r2, #+0x6]
	ldrh r10,[r7, #+0x2]
	strh r10,[r2, #+0x4]
	ldrb r7,[r7, #+0x4]
	strb r7,[r2, #+0x7]
end_loop_process_moveset:
	add  r4,r4,#0x1
	cmp r4,#0x4
	blt loop_process_moveset
	mov  r1,#0x0
	strb r1,[r6, #+0x20]
	mov r0,r6
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
	.pool
.endarea

.org GetMoveCategory
.area 0x1C
	stmdb  r13!,{r14}
	mov  r1,#3
	mov  r2,#1
	bl ReadMoveValue
	ldmia  r13!,{r15}
.endarea
