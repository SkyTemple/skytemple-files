; For use with ARMIPS
; 2021/06/09
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Implements Move Growth
; ------------------------------------------------------------------------------

.definelabel StatExtendIconStart, StartGraphicPos

.org Ov10PatchZone
.area 0x800
IsMGrowthActive:
	stmdb r13!, {r14}
	mov r0,#0
	mov r1,#0x4E
	mov r2,#1
	bl GetGameVar2
	ldmia r13!, {r15}
LoadIfNot:
	stmdb r13!, {r0,r1,r2,r3,r14}
	ldr r0,=IsLoadedFile
	ldr r1,[r0]
	cmp r1,#0
	bne no_load
	mov r1,#1
	str r1,[r0]
	bl FStreamAlloc
	ldr r0,=MGrowFileStream
	bl FStreamCtor
	ldr r0,=MGrowFileStream
	ldr r1,=MGrowFileName
	bl FStreamFOpen
	bl FStreamDealloc
no_load:
	ldmia r13!, {r0,r1,r2,r3,r15}
GetMoveStats:
	stmdb r13!, {r4,r5,r6,r7,r14}
	ldrsh r4,[r0, #+0x4]
	bl IsMGrowthActive
	cmp r0,#1
	movne r0,#0 ;pwr
	movne r1,#0 ;pp
	movne r2,#0 ;acc
	mvnne r3,#0 ;lvl
	ldmneia  r13!,{r4,r5,r6,r7,r15}
	bl LoadIfNot
	ldr r1,=CurrentMove
	ldrsh r2, [r1]
	cmp r2,r4
	beq no_move_read
	strh r4,[r1]
	bl FStreamAlloc
	ldr r0,=MGrowFileStream
	bl FGetSize
	mov r1,#0x96
	mul r1,r4,r1
	cmp r1,r0
	bge cancel_move_read
	ldr r0,=MGrowFileStream
	mov r2, #0
	bl FStreamSeek
	ldr r0,=MGrowFileStream
	ldr r1,=BufferMove
	mov r2,#0x96
	bl FStreamRead
cancel_move_read:
	bl FStreamDealloc
no_move_read:
	ldr r0,=MoveLevelPtr
	ldr r0,[r0]
	mov r4,r4,lsl #0x1
	ldrh r4,[r0, r4]
	mov r0,#0 ;pwr
	mov r1,#0 ;pp
	mov r2,#0 ;acc
	mov r3,#0 ;lvl
	mov r5,#0 ;exp_req
	ldr r6,=BufferMove
loop_exp:
	cmp r3, #24
	bgt end_loop_exp
	ldrsh r7,[r6]
	add r5,r5,r7
	ldrsh r7,[r6,#+0x2]
	add r0,r0,r7
	ldrb r7,[r6,#+0x4]
	add r1,r1,r7
	ldrb r7,[r6,#+0x5]
	add r2,r2,r7
	cmp r4,r5
	blt end_loop_exp
	add r3,r3,#1
	add r6,r6,#0x6
	b loop_exp
end_loop_exp:
	cmp r3, #24
	movgt r3, #24
	ldmia  r13!,{r4,r5,r6,r7,r15}
	.pool
IsTargetInTeam: 
	stmdb  r13!,{r14}
	ldr r1,=DungeonBaseStructurePtr
	ldr r1, [r1]
	add r1,r1,#0x12000
	mov r2,#0
loop_in_team:
	ldr r3,[r1, #+0xb28]
	cmp r3,r0
	moveq r0, #1
	ldmeqia  r13!,{r15}
	add r1,r1,#0x4
	add r2,r2,#0x1
	cmp r2,#0x4
	blt loop_in_team
	mov r0, #0
	ldmia  r13!,{r15}
	.pool
SetMoveStringCheck:
	stmdb  r13!,{r4,r5,r14}
	mov  r4,r0
	mov  r5,r1
	mov  r0,r2
	bl IsTargetInTeam
	cmp r0,#0
	bleq ClearMoveLevel
	mov  r0,r4
	mov  r1,#0x0
	mov  r2,r5
	mov  r3,#0x0
	bl PrintMoveStringMore
	ldmia  r13!,{r4,r5,r15}
GetAccuracyWithLevelBonus:
	stmdb  r13!,{r4,r5,r6,r14}
	mov r4,r1
	mov r5,#0
	mov r6,r2
	bl IsTargetInTeam
	cmp r0, #1
	bne no_add_accuracy
	;.word 0x773e3b33 ;Test Add
	mov r0,r4
	bl GetMoveStats
	add r5,r5,r2
no_add_accuracy:
	mov r0,r4
	mov r1,r6
	bl GetMoveAccuracy
	cmp r0,#100
	bgt perfect_accuracy
	add r0,r5,r0
	cmp r0,#100
	movgt r0,#100
perfect_accuracy:
	ldmia  r13!,{r4,r5,r6,r15}
GetMoveLevel:
	stmdb  r13!,{r14}
	bl GetMoveStats
	mvn r0,#0
	cmp r3,r0
	moveq r1,#0
	ldmeqia  r13!,{r15}
	mov r0,r3
	mov r1,#3
	bl EuclidianDivision
	cmp r0,#8
	moveq r1,#3
	ldmia  r13!,{r15}
GetPPWithLevelBonusNoCheck:
	stmdb  r13!,{r4,r5,r14}
	mov r4,r0
	mov r5,#0
	bl GetMoveStats
	add r5,r5,r1
	mov r0,r4
	bl GetMovePPWithBonus
	add r0,r5,r0
	cmp r0,#99
	movgt r0,#99
	ldmia  r13!,{r4,r5,r15}
GetPPWithLevelBonus:
	stmdb  r13!,{r4,r14}
	mov r4,r1
	bl IsTargetInTeam
	cmp r0, #1
	mov r0,r4
	bne no_add_pp
	bl GetPPWithLevelBonusNoCheck
	ldmia  r13!,{r4,r15}
no_add_pp:
	bl GetMovePPWithBonus
	ldmia  r13!,{r4,r15}
GetPowerWithLevelBonus:
	stmdb  r13!,{r4,r5,r14}
	mov r4,r1
	mov r5,#0
	bl IsTargetInTeam
	cmp r0, #1
	bne no_add_power
	;.word 0x773e3b35 ;Test Add
	mov r0,r4
	bl GetMoveStats
	add r5,r5,r0
no_add_power:
	mov r0,r4
	bl GetMoveBasePower
	add r0,r5,r0
	ldmia  r13!,{r4,r5,r15}
IncreasePoints:
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r14}
	cmp r2,#0
	bne no_add_points
	mov r6,r0
	mov r7,r1
	ldrh r4, [r1, #+0x4]
	bl IsTargetInTeam
	cmp r0, #1
	bne no_add_points
	mov r0,r7
	bl GetMoveStats
	mov r5,r3
	mvn r0,#0
	cmp r5,r0
	beq no_add_points
	ldr r1,=NoMiss
	ldr r2,[r1]
	cmp r2,#0
	beq no_add_points
	mov r2,#0
	str r2,[r1]
	ldr r1,=MoveLevelPtr
	ldr r1,[r1]
	mov r0,r4,lsl #0x1
	ldrh r4,[r1, r0]
	ldr r3,=MoveCurrentIncrease
	ldr r2,[r3]
	ldr r8,=0x7530
	cmp r4,r8
	bge no_add_points
	add r4,r4,r2
	cmp r4,r8
	movgt r4,r2
	strh r4,[r1, r0]
	mov r0,r7
	bl GetMoveStats
	cmp r5,r3
	beq no_next_level
	ldrh r1,[r7, #+0x4]
	mov  r0,#0x0
	bl PrepareMoveString
	mov r0,r6
	mov r1,#0xBF0
	bl SendMessageWithIDLog
no_next_level:
	mov r0, #1
	beq add_points
no_add_points:
	mov r0, #0
add_points:
	ldr r3,=MoveCurrentIncrease
	ldr r2,=MoveStableIncrease
	ldr r2,[r2]
	str r2,[r3]
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r15}
	.pool
IncrementPointsGinseng:
	stmdb  r13!,{r4,r5,r14}
	mov r5,r1
	ldr r1,=MoveLevelPtr
	ldr r1,[r1]
	mov r0,r0,lsl #0x1
	ldrh r4,[r1, r0]
	ldr r2,=0x7530
	cmp r4,r2
	add r4,r4,r5
	movlt r5,#0x1
	movge r5,#0x0
	cmp r4,r2
	movgt r4,r2
	strh r4,[r1, r0]
	mov r0,r5
	ldmia  r13!,{r4,r5,r15}
	.pool
ExtendAccuracy:
	stmdb  r13!,{r4,r5,r6,r7,r14}
	sub r13,r13,#0x18
	mov r4,r0
	strh r1,[r13, #+0x4]
	mov r0,r1
	bl GetMoveActualAccuracy
	mov r5,r0
	.if DisplayVal == 1
		mov r0,r0,lsl 0x3
		mov r1,#10
		bl EuclidianDivision
		sub r2,r0,#81
	.else
		sub r2,r0,#101
	.endif
	mov r7,r0
	add r0,r13,#0x8
	ldr r1,=str_off
	bl SPrintF
	mov r0,r4
	add r1,r13,#0x8
	bl StrCat
	mov r0,r13
	bl GetMoveStats
	add r0,r2,r5
	.if DisplayVal == 1
		mov r0,r0,lsl 0x3
		mov r1,#10
		bl EuclidianDivision
		cmp r0,#80
		movgt r0,#80
	.else
		cmp r0,#100
		movgt r0,#100
	.endif
	sub r5,r0,r7
	mov r6,#0
	b end_loop_ext_acc
loop_ext_acc:
	sub r0,r5,r6
	cmp  r0,#10
	addle r2, r0, StatExtendIconStart
	movgt r2, StatExtendIconStart+10
	mov  r0,r4
	bl PrintSpecialChar
	add  r6,r6,#10
end_loop_ext_acc:
	cmp r6,r5
	ble loop_ext_acc
	add r13,r13,#0x18
	ldmia  r13!,{r4,r5,r6,r7,r15}
ExtendPower:
	stmdb  r13!,{r4,r5,r6,r7,r14}
	sub r13,r13,#0x18
	mov r4,r0
	strh r1,[r13, #+0x4]
	mov r0,r1
	bl GetMovePowerWithID
	mov r5,r0
	.if DisplayVal == 1
		mov r0,r0,lsl 0x3
		mov r1,#10
		bl EuclidianDivision
	.endif
	mov r7,r0
	add r0,r13,#0x8
	ldr r1,=str_off
	mvn r2,#0
	bl SPrintF
	mov r0,r4
	add r1,r13,#0x8
	bl StrCat
	mov r0,r13
	bl GetMoveStats
	add r0,r0,r5
	.if DisplayVal == 1
		mov r0,r0,lsl 0x3
		mov r1,#10
		bl EuclidianDivision
	.endif
	sub r5,r0,r7
	mov r6,#0
	b end_loop_ext_pwr
loop_ext_pwr:
	sub r0,r5,r6
	cmp  r0,#10
	addle r2, r0, StatExtendIconStart
	movgt r2, StatExtendIconStart+10
	mov  r0,r4
	bl PrintSpecialChar
	add  r6,r6,#10
end_loop_ext_pwr:
	cmp r6,r5
	ble loop_ext_pwr
	add r13,r13,#0x18
	ldmia  r13!,{r4,r5,r6,r7,r15}
	.pool
UnknownFunction:
	stmdb  r13!,{r4,r14}
	mov r4,r0
	bl UnknownSubFunction
	cmp r0,#0x0
	ldrne r1,[r4, #+0xb4]
	movne  r0,#0x0
	strneb r0,[r1, #+0x166]
	strneb r0,[r1, #+0x167]
	ldmia  r13!,{r4,r15}
MoveCurrentIncrease:
	.word 3
MoveStableIncrease:
	.word 3
CurrentMove:
	.fill 0x2, 0xFF
BufferMove:
	.fill 0x96, 0x0
NoMiss:
	.fill 0x4, 0x0
MGrowFileName: 
	.ascii "BALANCE/mgrowth.bin",0
str_off:
	.ascii "[S:%u]",0
.endarea
