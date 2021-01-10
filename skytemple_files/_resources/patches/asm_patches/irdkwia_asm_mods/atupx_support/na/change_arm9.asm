; For use with ARMIPS
; 2021/01/09
; For Explorers of Sky North American ONLY!
; Should not be used with any other version!
; ------------------------------------------------------------------------------
; This file is auto-generated!
; ------------------------------------------------------------------------------
;
.relativeinclude on
.nds
.arm



.org 0x0201F6AC
.area 0x8
	mov  r1,r0
	b 0x20a4d88

.endarea


.org 0x0201FB10
.area 0x8
	mov  r1,r0
	b 0x20a4de0

.endarea


.org 0x0202005C
.area 0x4
	b 0x20a4e38

.endarea


.org 0x02020568
.area 0x8
	ldreqb r1,[r0, #+0x2]
	cmpeq r1,#0x33

.endarea


.org 0x02020574
.area 0x4
	bne 0x20a4e94

.endarea


.org 0x020A48F8
.area 0x5e0
	tst r5,#0x4
	beq 0x20a4918
	mov  r0,r5,lsr #0x3
	and  r0,r0,#0x3
	add  r8,r0,#0x3
	add  r4,r4,#0x5
	mov  r5,r5,lsr #0x5
	bx r14
	tst r5,#0x8
	beq 0x20a4938
	mov  r0,r5,lsr #0x4
	and  r0,r0,#0x7
	add  r8,r0,#0x7
	add  r4,r4,#0x7
	mov  r5,r5,lsr #0x7
	bx r14
	tst r5,#0x10
	beq 0x20a4958
	mov  r0,r5,lsr #0x5
	and  r0,r0,#0xF
	add  r8,r0,#0xF
	add  r4,r4,#0x9
	mov  r5,r5,lsr #0x9
	bx r14
	tst r5,#0x20
	beq 0x20a4978
	mov  r0,r5,lsr #0x6
	and  r0,r0,#0x1F
	add  r8,r0,#0x1F
	add  r4,r4,#0xB
	mov  r5,r5,lsr #0xb
	bx r14
	tst r5,#0x40
	beq 0x20a4998
	mov  r0,r5,lsr #0x7
	and  r0,r0,#0x3F
	add  r8,r0,#0x3F
	add  r4,r4,#0xD
	mov  r5,r5,lsr #0xd
	bx r14
	tst r5,#0x80
	beq 0x20a49b8
	mov  r0,r5,lsr #0x8
	and  r0,r0,#0x7F
	add  r8,r0,#0x7F
	add  r4,r4,#0xF
	mov  r5,r5,lsr #0xf
	bx r14
	tst r5,#0x100
	beq 0x20a4a04
	add  r4,r4,#0x9
	sub  r2,r11,r4
	cmp r2,#0x10
	mov  r5,r5,lsr #0x9
	bge 0x20a49f0
	ldr r0,[r13, #+0x4]
	mov  r4,#0x0
	mvn  r10,r0,lsl r2
	ldrh r0,[r9],#+0x2
	and  r10,r5,r10
	add  r11,r2,#0x10
	orr  r5,r10,r0,lsl r2
	and  r0,r5,#0xFF
	add  r8,r0,#0xFF
	add  r4,r4,#0x8
	mov  r5,r5,lsr #0x8
	bx r14
	mov  r8,#0x0
	stmdb  r13!,{r14}
	bl 0x207bc20
	ldmia  r13!,{r15}
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
	sub  r3,r11,r4
	cmp r3,#0x10
	bge 0x20a4a7c
	ldr r0,[r13, #+0x4]
	add  r11,r3,#0x10
	mvn  r2,r0,lsl r3
	ldrh r0,[r9],#+0x2
	and  r2,r5,r2
	mov  r4,#0x0
	orr  r5,r2,r0,lsl r3
	tst r5,#0x1
	beq 0x20a4a94
	add  r4,r4,#0x1
	mov  r5,r5,lsr #0x1
	bl 0x20a4b10
	b 0x20a4af8
	tst r5,#0x2
	beq 0x20a4acc
	mov  r0,r5,lsr #0x2
	and  r0,r0,#0x1
	add  r8,r0,#0x1
	cmp r8,#0x1
	add  r4,r4,#0x3
	mov  r5,r5,lsr #0x3
	bne 0x20a4ad0
	mov  r2,r10
	mov  r10,r6
	mov  r6,r2
	bl 0x20a4b10
	b 0x20a4af8
	bl 0x20a48f8
	tst r8,#0x1
	moveq  r8,r8,asr #0x1
	subne  r0,r8,#0x2
	mvnne  r0,r0
	movne  r0,r0,asr #0x1
	orrne  r8,r0,#0x80
	add  r0,r8,r6
	mov  r10,r6
	and  r6,r0,#0xF
	bl 0x20a4b10
	ldr r0,[r13, #+0x0]
	add  r7,r7,#0x1
	cmp r0,r7,asr #0x1
	bgt 0x20a4a54
	add  r13,r13,#0x8
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
	tst r7,#0x1
	mov  r7,r7,asr #0x1
	bne 0x20a4b28
	strb r6,[r1, +r7]
	mov  r7,r7,lsl #0x1
	bx r14
	ldrb r2,[r1, +r7]
	mov  r6,r6,lsl #0x4
	orr  r2,r2,r6
	strb r2,[r1, +r7]
	mov  r6,r6,asr #0x4
	mov  r7,r7,lsl #0x1
	orr  r7,r7,#0x1
	bx r14
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
	bl 0x20a4c48
	cmp r2,#0x1
	ble 0x20a4c40
	mov  r7,#0x1
	mvn  r0,#0x0
	str r0,[r13, #+0x4]
	sub  r3,r11,r4
	cmp r3,#0x10
	bge 0x20a4bb4
	ldr r0,[r13, #+0x4]
	add  r11,r3,#0x10
	mvn  r2,r0,lsl r3
	ldrh r0,[r9],#+0x2
	and  r2,r5,r2
	mov  r4,#0x0
	orr  r5,r2,r0,lsl r3
	tst r5,#0x1
	beq 0x20a4bcc
	add  r4,r4,#0x1
	mov  r5,r5,lsr #0x1
	bl 0x20a4c48
	b 0x20a4c30
	tst r5,#0x2
	beq 0x20a4c04
	mov  r0,r5,lsr #0x2
	and  r0,r0,#0x1
	add  r8,r0,#0x1
	cmp r8,#0x1
	add  r4,r4,#0x3
	mov  r5,r5,lsr #0x3
	bne 0x20a4c08
	mov  r2,r10
	mov  r10,r6
	mov  r6,r2
	bl 0x20a4c48
	b 0x20a4c30
	bl 0x20a48f8
	tst r8,#0x1
	moveq  r8,r8,asr #0x1
	subne  r0,r8,#0x2
	mvnne  r0,r0
	movne  r0,r0,asr #0x1
	orrne  r8,r0,#0x80
	add  r0,r8,r6
	mov  r10,r6
	and  r6,r0,#0xF
	bl 0x20a4c48
	ldr r0,[r13, #+0x0]
	add  r7,r7,#0x1
	cmp r0,r7,asr #0x1
	bgt 0x20a4b8c
	add  r13,r13,#0xC
	ldmia  r13!,{r4,r5,r6,r7,r8,r9,r10,r11,r15}
	cmp r6,#0x0
	ldrneb r2,[r13, #+0x8]
	moveq r2, #0x0
	orr  r2,r2,r6
	strb r2,[r1, +r7]
	bx r14
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
	sub  r3,r11,r4
	cmp r3,#0x10
	bge 0x20a4cc8
	ldr r0,[r13, #+0x4]
	add  r11,r3,#0x10
	mvn  r2,r0,lsl r3
	ldrh r0,[r9],#+0x2
	and  r2,r5,r2
	mov  r4,#0x0
	orr  r5,r2,r0,lsl r3
	tst r5,#0x1
	beq 0x20a4ce0
	add  r4,r4,#0x1
	mov  r5,r5,lsr #0x1
	bl 0x20a4d5c
	b 0x20a4d44
	tst r5,#0x2
	beq 0x20a4d18
	mov  r0,r5,lsr #0x2
	and  r0,r0,#0x1
	add  r8,r0,#0x1
	cmp r8,#0x1
	add  r4,r4,#0x3
	mov  r5,r5,lsr #0x3
	bne 0x20a4d1c
	mov  r2,r10
	mov  r10,r6
	mov  r6,r2
	bl 0x20a4d5c
	b 0x20a4d44
	bl 0x20a48f8
	tst r8,#0x1
	moveq  r8,r8,asr #0x1
	subne  r0,r8,#0x2
	mvnne  r0,r0
	movne  r0,r0,asr #0x1
	orrne  r8,r0,#0x80
	add  r0,r8,r6
	mov  r10,r6
	and  r6,r0,#0xF
	bl 0x20a4d5c
	ldr r0,[r13, #+0x0]
	add  r7,r7,#0x1
	cmp r0,r7,asr #0x1
	bgt 0x20a4ca0
	add  r13,r13,#0xC
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
	tst r7,#0x1
	bne 0x20a4d6c
	strb r6,[r13, #+0x8]
	bx r14
	ldrb r2,[r13, #+0x8]
	mov  r6,r6,lsl #0x4
	orr  r0,r2,r6
	stmdb  r13!,{r14}
	bl 0x2020470
	mov  r6,r6,asr #0x4
	ldmia  r13!,{r15}
	mov  r0,#0x0
	ldrb r5,[r2, #+0x0]
	cmp r5,#0x41
	ldreqb r5,[r2, #+0x1]
	cmpeq r5,#0x54
	ldreqb r5,[r2, #+0x2]
	cmpeq r5,#0x55
	ldreqb r5,[r2, #+0x3]
	cmpeq r5,#0x50
	bne 0x201fa08
	ldrb r6,[r2, #+0x7]
	ldrb r5,[r2, #+0x8]
	ldrb r7,[r2, #+0x9]
	ldrb r4,[r2, #+0xa]
	add  r5,r6,r5,lsl #0x8
	add  r5,r5,r7,lsl #0x10
	add  r4,r5,r4,lsl #0x18
	add  r0,r2,#0xB
	mov  r2,r4
	bl 0x20a4a14
	mov  r0,r4
	b 0x201fa08
	ldrb r5,[r2, #+0x0]
	cmp r5,#0x41
	ldreqb r5,[r2, #+0x1]
	cmpeq r5,#0x54
	ldreqb r5,[r2, #+0x2]
	cmpeq r5,#0x55
	ldreqb r5,[r2, #+0x3]
	cmpeq r5,#0x50
	mov  r0,#0x0
	bne 0x201ff44
	ldrb r6,[r2, #+0x7]
	ldrb r5,[r2, #+0x8]
	ldrb r7,[r2, #+0x9]
	ldrb r4,[r2, #+0xa]
	add  r5,r6,r5,lsl #0x8
	add  r5,r5,r7,lsl #0x10
	add  r4,r5,r4,lsl #0x18
	add  r0,r2,#0xB
	mov  r2,r4
	bl 0x20a4b48
	mov  r0,r4
	b 0x201ff44
	ldrb r1,[r5, #+0x0]
	cmp r1,#0x41
	ldreqb r1,[r5, #+0x1]
	cmpeq r1,#0x54
	ldreqb r1,[r5, #+0x2]
	cmpeq r1,#0x55
	ldreqb r1,[r5, #+0x3]
	cmpeq r1,#0x50
	mov  r0,#0x0
	bne 0x2020464
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
	bl 0x20a4c60
	mov  r2,r0
	b 0x2020464
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


