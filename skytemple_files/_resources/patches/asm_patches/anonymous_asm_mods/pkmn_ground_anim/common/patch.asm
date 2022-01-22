; For use with ARMIPS
; 2021/10/07
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Changes the way individual animations are implemented
; ------------------------------------------------------------------------------

.org Function
.area 0x1110
	b ActualFunction
anim_table:
	.skip 2048
ActualFunction:
	cmp r0,#2048
	bge Choice4
	ldr r2,=anim_table
	ldrb r2,[r2,r0]
	cmp r2,#0x4
	addls  r15,r15,r2,lsl #0x2
	b Choice4
	b Choice1
	b Choice2
	b Choice3
	b Choice4
Choice1:
	ldr r0,=0x00000807
	bx r14
Choice2:
	ldr r0,=0x00000307
	bx r14
Choice3:
	ldr r0,=0x00000807
	cmp r1,r0
	subne  r0,r0,#0x500
	cmpne r1,r0
	ldreq r0,=0x00000807
	movne  r0,#0x300
	bx r14
Choice4:
	mov  r0,#0x300
	bx r14
	.pool
	.fill (Function+0x1110-.),0xCC
.endarea
