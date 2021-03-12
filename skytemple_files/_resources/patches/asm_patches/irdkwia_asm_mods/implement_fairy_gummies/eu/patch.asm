; For use with ARMIPS
; 2021/03/12
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Implement Fairy-type gummies
; ------------------------------------------------------------------------------

.definelabel IsGummi, 0x0200CC7C
.definelabel GummiStatUp, 0x0201196C
.definelabel GetType, 0x02052D3C
.definelabel WonderGummiIQBoost, 0x020A1E14
.definelabel WonderGummiStatBoost, 0x020A1E34
.definelabel GummiStatBoost, 0x020A1E0C
.definelabel GummiIQBoostTable, 0x020A2834
.definelabel GummiStatUpPool, 0x02011B48


; Edit IsGummi

.org IsGummi
.area 0x20
	cmp r0,#0x77
	movlt  r0,#0x7F000000
	cmp r0,#0x88
	movle  r0,#0x8A
	cmp r0,#0x8A
	moveq  r0,#0x1
	movne  r0,#0x0
	bx r14
.endarea

.org GummiStatUp
.area 0x8C
	sub  r11,r0,#0x76
	strh r4,[r6, #+0x2]
	bl IsGummi
	cmp r0,#0x0
	ldmeqia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
	ldrsh r0,[r13, #+0x28]
	cmp r0,#0x8A
	moveq r11,#0x12
	cmp r0,#0x88
	bne no_wonder_gummi
	ldr r1,=WonderGummiIQBoost
	ldr r0,=WonderGummiStatBoost
	ldrsh r1,[r1, #+0x0]
	ldrsh r5,[r0, #+0x0]
	add  r4,r4,r1
	b end_iq_inc
no_wonder_gummi:
	ldrsh r0,[r10, #+0x0]
	ldr r2,=GummiStatBoost
	mov  r1,r4
	ldrsh r5,[r2, #+0x0]
	bl GetType
	str r0,[r13, #+0x0]
	ldrsh r0,[r10, #+0x0]
	mov  r1,#0x1
	bl GetType
	ldr r10,=GummiIQBoostTable
	ldr r1,[r13, #+0x0]
	mov  r2,#0x19
	mla  r3,r1,r2,r10
	mla  r1,r0,r2,r10
	ldrb r2,[r11, r3]
	ldrb r0,[r11, r1]
	cmp r2,r0
	addgt  r4,r4,r2
	addle  r4,r4,r0
end_iq_inc:
.endarea

.org GummiStatUpPool
.area 0x10
	.pool
.endarea
