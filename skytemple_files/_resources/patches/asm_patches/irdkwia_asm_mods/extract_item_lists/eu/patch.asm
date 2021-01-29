; For use with ARMIPS
; 2021/01/27
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Use filestreams instead of hardcoded lists 
; ------------------------------------------------------------------------------

.org 0x0200E0DC
.area 0xF4
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r14}
	mov  r6,r0
	mov  r5,r1
	mov  r0,#0x2F8
	mov  r1,#0x0
	mov  r4,r2
	bl MemAlloc
	mov  r7,r0
	mov  r0,#0x48
	mov  r1,#0x0
	bl MemAlloc
	mov r8,r0
	cmp r6,#0x0
	ldr r0,=0x020b1264
	subne  r1,r6,#0x1
	moveq r1,r6
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
.endarea

; Remove the second block allocation
.org 0x0200E268
.area 0x8
	nop
	nop
.endarea

.org 0x0200E274
.area 0xC
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
	.pool
.endarea
