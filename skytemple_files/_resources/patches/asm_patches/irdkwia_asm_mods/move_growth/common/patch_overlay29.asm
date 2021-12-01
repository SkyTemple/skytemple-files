; For use with ARMIPS
; 2021/06/09
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Implements Move Growth
; ------------------------------------------------------------------------------

.org HookGetActualPower
.area 0x8
	mov r0,r5
	bl GetPowerWithLevelBonus
.endarea

.org HookGetActualAccuracy
.area 0xC
	mov r1,r11
	mov r2,r3
	bl GetAccuracyWithLevelBonus
.endarea

.org HookPP1
.area 0x30
label_hpp1_1:
	mov  r0,r9
	add  r1,r5,r7,lsl #0x3
	bl GetPPWithLevelBonus
	add  r1,r6,r7,lsl #0x3
	ldrb r1,[r1, #+0x12a]
	cmp r1,r0
	blt label_hpp1_0
	add  r7,r7,#0x1
	cmp r7,#0x4
	blt label_hpp1_1
label_hpp1_0:
	nop
	cmp r7,#0x4
.endarea

.org HookPP2
.area 0x3C
label_hpp2_1:
	ldrb r0,[r6,+r9, lsl #0x3]
	add  r7,r6,r9,lsl #0x3
	tst r0,#0x1
	movne  r0,r5
	moveq  r0,r4
	tst r0,#0xFF
	beq label_hpp2_0
	mov  r0,r10
	mov  r1,r7
	bl GetPPWithLevelBonus
	strb r0,[r7, #+0x6]
label_hpp2_0:
	add  r9,r9,#0x1
	cmp r9,#0x4
	blt label_hpp2_1
	nop
.endarea

.org HookPP3
.area 0x2C
	tst r0,#0x1
	beq HookPP3+0x70
	ldrb r1,[r7, #+0x6]
	str r1,[r13, #+0x4]
	mov  r0,r9
	mov  r1,r7
	bl GetPPWithLevelBonus
	str r0,[r13, #+0x0]
	nop
	mov  r0,r9
	mov  r1,r7
.endarea

.org HookPP4
.area 0x2C
	tst r0,#0x1
	beq HookPP4+0xE4
	ldrb r1,[r5, #+0x6]
	str r1,[r13, #+0x4]
	mov  r0,r7
	mov  r1,r5
	bl GetPPWithLevelBonus
	str r0,[r13, #+0x0]
	nop
	mov  r0,r7
	mov  r1,r5
.endarea

.org HookPP5
.area 0x20
	tst r1,#0x1
	beq HookPP5+0x44
	ldrb r1,[r0, #+0x6]
	str r1,[r13, #+0x8]
	mov r1,r0
	mov r0,r9
	bl GetPPWithLevelBonus
	nop
.endarea

.org HookPP6
.area 0x4
	bl GetPPWithLevelBonus
.endarea

.org HookPP6_1
.area 0x18
	tst r0,#0x1
	beq HookPP6_1+0x20
	mov  r0,r6
	mov  r1,r7
	nop
	nop
.endarea

.org HookPP6_2
.area 0x64
	mov r5,r0
	ldr r0,[r0, #+0xb4]
	mov  r7,#0x0
	add  r6,r0,#0x124
	nop
	ldrb r0,[r6,+r7, lsl #0x3]
	add  r8,r6,r7,lsl #0x3
	tst r0,#0x1
	beq HookPP6_2+0x6C
	ldrh r1,[r8, #+0x2]
	bic  r1,r1,#0x8
	strh r1,[r8, #+0x2]
	ldrh r1,[r8, #+0x2]
	bic  r1,r1,#0x10
	strh r1,[r8, #+0x2]
	ldrh r1,[r8, #+0x2]
	bic  r1,r1,#0x40
	strh r1,[r8, #+0x2]
	ldrh r1,[r8, #+0x2]
	orr  r1,r1,#0x4
	strh r1,[r8, #+0x2]
	mov  r0,r5
	mov  r1,r8
	nop
	nop
.endarea

.org HookPP6_3
.area 0x18
	tst r1,#0x1
	beq HookPP6_3+0x44
	mov r0,r5
	ldr r1,[r13, #+0x0]
	nop
	nop
.endarea

.org HookPP6_6
.area 0x24
	tst r0,#0x1
	beq HookPP6_6+0x34
	ldrb r0,[r9, #+0x6]
	cmp r0,#0x0
	addeq  r4,r4,#0x1E
	mov  r0,r7
	mov  r1,r9
	nop
	nop
.endarea

.org HookPP7
.area 0x10
	mov  r7,r1
	mov  r1,r6
	mov  r5,r3
	bl GetPPWithLevelBonus
.endarea

.org HookPP8_1
.area 0x4
	stmdb  r13!,{r4,r5,r6,r7,r8,r9,r14}
.endarea
.org HookPP8_2
.area 0x4
	ldmeqia  r13!,{r4,r5,r6,r7,r8,r9,r15}
.endarea
.org HookPP8_3
.area 0x4
	ldmneia  r13!,{r4,r5,r6,r7,r8,r9,r15}
.endarea

.org HookPP8
.area 0xB4
	add  r9,r7,#0x124
label_hpp8_2:
	add  r0,r7,r8,lsl #0x3
	cmp r5,#0x0
	addne  r0,r0,#0x100
	ldrneh r1,[r0, #+0x26]
	orrne  r1,r1,#0x200
	strneh r1,[r0, #+0x26]
	bne label_hpp8_0
	add  r1,r0,#0x100
	ldrh r2,[r1, #+0x26]
	bic  r2,r2,#0x200
	strh r2,[r1, #+0x26]
	mov r0,r4
	add  r1,r9,r8,lsl #0x3
	bl GetPPWithLevelBonus
	add  r2,r7,r8,lsl #0x3
	mov  r0,r0,lsl #0x10
	ldrb r1,[r2, #+0x12a]
	mov  r3,r0,asr #0x10
	cmp r1,r0,asr #0x10
	strgtb r3,[r2, #+0x12a]
label_hpp8_0:
	add  r0,r7,r8,lsl #0x3
	cmp r6,#0x0
	addne  r0,r0,#0x100
	ldrneh r1,[r0, #+0x26]
	orrne  r1,r1,#0x400
	strneh r1,[r0, #+0x26]
	bne label_hpp8_1
	add  r1,r0,#0x100
	ldrh r2,[r1, #+0x26]
	bic  r2,r2,#0x400
	strh r2,[r1, #+0x26]
	mov r0,r4
	add  r1,r9,r8,lsl #0x3
	bl GetPPWithLevelBonus
	add  r2,r7,r8,lsl #0x3
	mov  r0,r0,lsl #0x10
	ldrb r1,[r2, #+0x12a]
	mov  r3,r0,asr #0x10
	cmp r1,r0,asr #0x10
	strgtb r3,[r2, #+0x12a]
label_hpp8_1:
	add  r8,r8,#0x1
	cmp r8,#0x4
	blt label_hpp8_2
	ldmia  r13!,{r4,r5,r6,r7,r8,r9,r15}
.endarea


; TODO
.org HookSetMoveString1
.area 0x10
	add  r1,r13,#0x2C
	mov  r2,r10
	bl SetMoveStringCheck
	nop
.endarea
.org HookSetMoveString2
.area 0x10
	add  r1,r13,#0x2C
	mov  r2,r10
	bl SetMoveStringCheck
	nop
.endarea
.org HookSetMoveString3
.area 0x10
	mov  r1,r8
	mov  r2,r6
	bl SetMoveStringCheck
	nop
.endarea
.org HookSetMoveString4
.area 0x10
	mov  r1,r8
	mov  r2,r6
	bl SetMoveStringCheck
	nop
.endarea
.org HookSetMoveString5
.area 0x10
	mov  r1,r9
	mov  r2,r10
	bl SetMoveStringCheck
	nop
.endarea
.org HookSetMoveString6
.area 0x10
	add  r2,r5,r4
	mov  r2,r9
	bl SetMoveStringCheck
	nop
.endarea
.org HookSetMoveString7
.area 0x10
	add  r2,r13,#0x0
	mov  r2,r9
	bl SetMoveStringCheck
	nop
.endarea

.org HookSetMovePoints1
.area 0x14
	ldrne r0,=NoMiss
	strne r10,[r0]
	ldreq r0,[r13, #+0x74]
	addeq  r0,r0,#0x1
	streq r0,[r13, #+0x74]
.endarea
.org HookSetMovePoints2
.area 0x28
	mov r0,r9
	mov r1,r8
	mov r2,r7
	bl IncreasePoints
	ldr r0,[r13, #+0x80]
	cmp r0,#0x0
	movne r0,r9
	blne UnknownFunction
	b HookSetMovePoints2+0x28
	.pool
.endarea

.org HookProcessGinseng1
.area 0x4
	mov  r5,#0x12C
.endarea
.org HookProcessGinseng2
.area 0x4
	movlt  r5,#0x3E8
.endarea
.org HookProcessGinseng3
.area 0x40
	ldrh r0, [r7, #+0x4]
	mov  r1,r5
	bl IncrementPointsGinseng
	cmp r0,#0
	movne r4,#1
	b HookProcessGinseng3+0x40
	.pool
	.fill (HookProcessGinseng3+0x40-.), 0xCC
.endarea
.org HookProcessGinseng4
.area 0x4
	cmp r5,#0x12C
.endarea
