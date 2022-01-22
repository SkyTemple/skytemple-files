; For use with ARMIPS
; 2021/07/18
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------

.org HookConquest
.area 0x4
	bl CheckConquest
.endarea

.org HookHPDisplay3
.area 0x44
	ldrsh r1,[r8, #+0x10]
	add  r9,r1,r0
	ldr r0,[r15, #+0xb0]
	cmp r9,r0
	movgt  r9,r0
	add  r0,r13,#0x1C
	mov  r1,r8
	bl UnknownFunc
	ldrb r3,[r8, #+0x2]
	add  r0,r10,r5
	mov  r1,r7
	str r3,[r13]
	str r9,[r13, #+0x8]
	ldrsh r9,[r8, #+0xe]
	nop
	ldr r3,[r15, #+0x80]
	str r9,[r13, #+0x4]
.endarea
