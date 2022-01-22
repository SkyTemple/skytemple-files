; For use with ARMIPS
; 2021/06/13
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Provides support for reading ATUPX data
; ------------------------------------------------------------------------------
;
.relativeinclude on
.nds
.arm


.org HookATAlgorithm1
.area 0x8
	mov  r1,r0
	b NextPartATAlgo1
.endarea


.org HookATAlgorithm2
.area 0x8
	mov  r1,r0
	b NextPartATAlgo2
.endarea


.org HookATAlgorithm3
.area 0x4
	b NextPartATAlgo3
.endarea


.org HookCompare
.area 0x8
	ldreqb r1,[r0, #+0x2]
	cmpeq r1,#0x33
.endarea


.org HookATGetSize
.area 0x4
	bne NextPartGetATSize
.endarea

.org NewAlgoStart
.area 0x5E0
SubModule:
	tst r5,#0x4
	beq case_1
	mov  r0,r5,lsr #0x3
	and  r0,r0,#0x3
	add  r8,r0,#0x3
	add  r4,r4,#0x5
	mov  r5,r5,lsr #0x5
	bx r14
case_1:
	tst r5,#0x8
	beq case_2
	mov  r0,r5,lsr #0x4
	and  r0,r0,#0x7
	add  r8,r0,#0x7
	add  r4,r4,#0x7
	mov  r5,r5,lsr #0x7
	bx r14
case_2:
	tst r5,#0x10
	beq case_3
	mov  r0,r5,lsr #0x5
	and  r0,r0,#0xF
	add  r8,r0,#0xF
	add  r4,r4,#0x9
	mov  r5,r5,lsr #0x9
	bx r14
case_3:
	tst r5,#0x20
	beq case_4
	mov  r0,r5,lsr #0x6
	and  r0,r0,#0x1F
	add  r8,r0,#0x1F
	add  r4,r4,#0xB
	mov  r5,r5,lsr #0xb
	bx r14
case_4:
	tst r5,#0x40
	beq case_5
	mov  r0,r5,lsr #0x7
	and  r0,r0,#0x3F
	add  r8,r0,#0x3F
	add  r4,r4,#0xD
	mov  r5,r5,lsr #0xd
	bx r14
case_5:
	tst r5,#0x80
	beq case_6
	mov  r0,r5,lsr #0x8
	and  r0,r0,#0x7F
	add  r8,r0,#0x7F
	add  r4,r4,#0xF
	mov  r5,r5,lsr #0xf
	bx r14
case_6:
	tst r5,#0x100
	beq submodule_end
	add  r4,r4,#0x9
	sub  r2,r11,r4
	cmp r2,#0x10
	mov  r5,r5,lsr #0x9
	bge case_7
	ldr r0,[r13, #+0x4]
	mov  r4,#0x0
	mvn  r10,r0,lsl r2
	ldrh r0,[r9],#+0x2
	and  r10,r5,r10
	add  r11,r2,#0x10
	orr  r5,r10,r0,lsl r2
case_7:
	and  r0,r5,#0xFF
	add  r8,r0,#0xFF
	add  r4,r4,#0x8
	mov  r5,r5,lsr #0x8
	bx r14
submodule_end:
	mov  r8,#0x0
	stmdb  r13!,{r14}
	bl UnknownFunction
	ldmia  r13!,{r15}
ATUPXAlgorithm1:
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r14}
	sub  r13,r13,#0x8
	ldrb r6,[r0, #+0x0]
	mov  r11,#0x0
	str r2,[r13, #+0x0]
	cmp r2,#0x1
	mov  r4,r11
	mov  r5,r11
	add  r9,r0,#0x2
	mov  r7,#0x1
	addle  r13,r13,#0x8
	mov  r10,r6
	strb r6,[r1, #+0x0]
	ldmleia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
	mvn  r0,#0x0
	str r0,[r13, #+0x4]
algo_1_loop:
	sub  r3,r11,r4
	cmp r3,#0x10
	bge algo_1_special_2
	ldr r0,[r13, #+0x4]
	add  r11,r3,#0x10
	mvn  r2,r0,lsl r3
	ldrh r0,[r9],#+0x2
	and  r2,r5,r2
	mov  r4,#0x0
	orr  r5,r2,r0,lsl r3
algo_1_special_2:
	tst r5,#0x1
	beq algo_1_special
	add  r4,r4,#0x1
	mov  r5,r5,lsr #0x1
	bl StoreMidPart
	b algo_1_end_loop
algo_1_special:
	tst r5,#0x2
	beq algo_1_submodule
	mov  r0,r5,lsr #0x2
	and  r0,r0,#0x1
	add  r8,r0,#0x1
	cmp r8,#0x1
	add  r4,r4,#0x3
	mov  r5,r5,lsr #0x3
	bne algo_1_no_submodule
	mov  r2,r10
	mov  r10,r6
	mov  r6,r2
	bl StoreMidPart
	b algo_1_end_loop
algo_1_submodule:
	bl SubModule
algo_1_no_submodule:
	tst r8,#0x1
	moveq  r8,r8,asr #0x1
	subne  r0,r8,#0x2
	mvnne  r0,r0
	movne  r0,r0,asr #0x1
	orrne  r8,r0,#0x80
	add  r0,r8,r6
	mov  r10,r6
	and  r6,r0,#0xF
	bl StoreMidPart
algo_1_end_loop:
	ldr r0,[r13, #+0x0]
	add  r7,r7,#0x1
	cmp r0,r7,asr #0x1
	bgt algo_1_loop
	add  r13,r13,#0x8
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
StoreMidPart:
	tst r7,#0x1
	mov  r7,r7,asr #0x1
	bne full_part
	strb r6,[r1, +r7]
	mov  r7,r7,lsl #0x1
	bx r14
full_part:
	ldrb r2,[r1, +r7]
	mov  r6,r6,lsl #0x4
	orr  r2,r2,r6
	strb r2,[r1, +r7]
	mov  r6,r6,asr #0x4
	mov  r7,r7,lsl #0x1
	orr  r7,r7,#0x1
	bx r14
ATUPXAlgorithm2:
	stmdb  r13!,{r4,r5,r6,r7,r8,r9,r10,r11,r14}
	sub  r13,r13,#0xC
	str r3,[r13, #+0x8]
	ldrb r6,[r0, #+0x0]
	mov  r11,#0x0
	str r2,[r13, #+0x0]
	mov  r4,r11
	mov  r5,r11
	add  r9,r0,#0x2
	mov  r7,#0x0
	mov  r10,r6
	bl StoreMidPart2
	cmp r2,#0x1
	ble algo_2_after_loop
	mov  r7,#0x1
	mvn  r0,#0x0
	str r0,[r13, #+0x4]
algo_2_loop:
	sub  r3,r11,r4
	cmp r3,#0x10
	bge algo_2_special_2
	ldr r0,[r13, #+0x4]
	add  r11,r3,#0x10
	mvn  r2,r0,lsl r3
	ldrh r0,[r9],#+0x2
	and  r2,r5,r2
	mov  r4,#0x0
	orr  r5,r2,r0,lsl r3
algo_2_special_2:
	tst r5,#0x1
	beq algo_2_special
	add  r4,r4,#0x1
	mov  r5,r5,lsr #0x1
	bl StoreMidPart2
	b algo_2_end_loop
algo_2_special:
	tst r5,#0x2
	beq algo_2_submodule
	mov  r0,r5,lsr #0x2
	and  r0,r0,#0x1
	add  r8,r0,#0x1
	cmp r8,#0x1
	add  r4,r4,#0x3
	mov  r5,r5,lsr #0x3
	bne algo_2_no_submodule
	mov  r2,r10
	mov  r10,r6
	mov  r6,r2
	bl StoreMidPart2
	b algo_2_end_loop
algo_2_submodule:
	bl SubModule
algo_2_no_submodule:
	tst r8,#0x1
	moveq  r8,r8,asr #0x1
	subne  r0,r8,#0x2
	mvnne  r0,r0
	movne  r0,r0,asr #0x1
	orrne  r8,r0,#0x80
	add  r0,r8,r6
	mov  r10,r6
	and  r6,r0,#0xF
	bl StoreMidPart2
algo_2_end_loop:
	ldr r0,[r13, #+0x0]
	add  r7,r7,#0x1
	cmp r0,r7,asr #0x1
	bgt algo_2_loop
algo_2_after_loop:
	add  r13,r13,#0xC
	ldmia  r13!,{r4,r5,r6,r7,r8,r9,r10,r11,r15}
StoreMidPart2:
	cmp r6,#0x0
	ldrneb r2,[r13, #+0x8]
	moveq  r2,#0x0
	orr  r2,r2,r6
	strb r2,[r1, +r7]
	bx r14
ATUPXAlgorithm3:
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r14}
	sub  r13,r13,#0xC
	ldrb r6,[r0, #+0x0]
	mov  r11,#0x0
	str r2,[r13, #+0x0]
	cmp r2,#0x1
	mov  r4,r11
	mov  r5,r11
	add  r9,r0,#0x2
	mov  r7,#0x1
	addle  r13,r13,#0xC
	mov  r10,r6
	strb r6,[r13, #+0x8]
	ldmleia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
	mvn  r0,#0x0
	str r0,[r13, #+0x4]
algo_3_loop:
	sub  r3,r11,r4
	cmp r3,#0x10
	bge algo_3_special_2
	ldr r0,[r13, #+0x4]
	add  r11,r3,#0x10
	mvn  r2,r0,lsl r3
	ldrh r0,[r9],#+0x2
	and  r2,r5,r2
	mov  r4,#0x0
	orr  r5,r2,r0,lsl r3
algo_3_special_2:
	tst r5,#0x1
	beq algo_3_special
	add  r4,r4,#0x1
	mov  r5,r5,lsr #0x1
	bl StoreMidPart3
	b algo_3_end_loop
algo_3_special:
	tst r5,#0x2
	beq algo_3_sub_module
	mov  r0,r5,lsr #0x2
	and  r0,r0,#0x1
	add  r8,r0,#0x1
	cmp r8,#0x1
	add  r4,r4,#0x3
	mov  r5,r5,lsr #0x3
	bne algo_3_no_sub_module
	mov  r2,r10
	mov  r10,r6
	mov  r6,r2
	bl StoreMidPart3
	b algo_3_end_loop
algo_3_sub_module:
	bl SubModule
algo_3_no_sub_module:
	tst r8,#0x1
	moveq  r8,r8,asr #0x1
	subne  r0,r8,#0x2
	mvnne  r0,r0
	movne  r0,r0,asr #0x1
	orrne  r8,r0,#0x80
	add  r0,r8,r6
	mov  r10,r6
	and  r6,r0,#0xF
	bl StoreMidPart3
algo_3_end_loop:
	ldr r0,[r13, #+0x0]
	add  r7,r7,#0x1
	cmp r0,r7,asr #0x1
	bgt algo_3_loop
	add  r13,r13,#0xC
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
StoreMidPart3:
	tst r7,#0x1
	bne full_part_3
	strb r6,[r13, #+0x8]
	bx r14
full_part_3:
	ldrb r2,[r13, #+0x8]
	mov  r6,r6,lsl #0x4
	orr  r0,r2,r6
	stmdb  r13!,{r14}
	bl WriteByteFromMemoryPointer
	mov  r6,r6,asr #0x4
	ldmia  r13!,{r15}
NextPartATAlgo1:
	mov  r0,#0x0
	ldrb r5,[r2, #+0x0]
	cmp r5,#0x41
	ldreqb r5,[r2, #+0x1]
	cmpeq r5,#0x54
	ldreqb r5,[r2, #+0x2]
	cmpeq r5,#0x55
	ldreqb r5,[r2, #+0x3]
	cmpeq r5,#0x50
	bne EndNextPartATAlgo1
	ldrb r6,[r2, #+0x7]
	ldrb r5,[r2, #+0x8]
	ldrb r7,[r2, #+0x9]
	ldrb r4,[r2, #+0xa]
	add  r5,r6,r5,lsl #0x8
	add  r5,r5,r7,lsl #0x10
	add  r4,r5,r4,lsl #0x18
	add  r0,r2,#0xB
	mov  r2,r4
	bl ATUPXAlgorithm1
	mov  r0,r4
	b EndNextPartATAlgo1
NextPartATAlgo2:
	ldrb r5,[r2, #+0x0]
	cmp r5,#0x41
	ldreqb r5,[r2, #+0x1]
	cmpeq r5,#0x54
	ldreqb r5,[r2, #+0x2]
	cmpeq r5,#0x55
	ldreqb r5,[r2, #+0x3]
	cmpeq r5,#0x50
	mov  r0,#0x0
	bne EndNextPartATAlgo2
	ldrb r6,[r2, #+0x7]
	ldrb r5,[r2, #+0x8]
	ldrb r7,[r2, #+0x9]
	ldrb r4,[r2, #+0xa]
	add  r5,r6,r5,lsl #0x8
	add  r5,r5,r7,lsl #0x10
	add  r4,r5,r4,lsl #0x18
	add  r0,r2,#0xB
	mov  r2,r4
	bl ATUPXAlgorithm2
	mov  r0,r4
	b EndNextPartATAlgo2
NextPartATAlgo3:
	ldrb r1,[r5, #+0x0]
	cmp r1,#0x41
	ldreqb r1,[r5, #+0x1]
	cmpeq r1,#0x54
	ldreqb r1,[r5, #+0x2]
	cmpeq r1,#0x55
	ldreqb r1,[r5, #+0x3]
	cmpeq r1,#0x50
	mov  r0,#0x0
	bne EndNextPartATAlgo3
	ldrb r1,[r5, #+0x7]
	ldrb r0,[r5, #+0x8]
	ldrb r2,[r5, #+0x9]
	ldrb r3,[r5, #+0xa]
	add  r0,r1,r0,lsl #0x8
	add  r0,r0,r2,lsl #0x10
	add  r0,r0,r3,lsl #0x18
	mov  r2,r0
	mov  r3,r0
	add  r0,r5,#0xB
	bl ATUPXAlgorithm3
	mov  r2,r0
	b EndNextPartATAlgo3
NextPartGetATSize:
	cmp r2,#0x41
	ldreqb r1,[r0, #+0x1]
	cmpeq r1,#0x54
	ldreqb r1,[r0, #+0x2]
	cmpeq r1,#0x55
	ldreqb r1,[r0, #+0x3]
	cmpeq r1,#0x50
	movne  r0,#0x0
	bxne r14
	ldrb r2,[r0, #+0x7]
	ldrb r1,[r0, #+0x8]
	ldrb r3,[r0, #+0x9]
	ldrb r12,[r0, #+0xa]
	add  r0,r2,r1,lsl #0x8
	add  r0,r0,r3,lsl #0x10
	add  r0,r0,r12,lsl #0x18
	bx r14
.endarea

