; For use with ARMIPS
; 2022/02/27
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Changes the way object attributes are loaded
; ------------------------------------------------------------------------------

.org HookGetObjectData1
.area 0x18
	mov  r9,r0
	mov  r7,r2
	mov  r10,r3
	mov  r0,r4
	bl GetObjectData
	mov  r5,r0
.endarea

.org HookGetObjectData2
.area 0x4
	ldrb r0,[r5, #+0x4]
.endarea

.org HookGetObjectData3
.area 0x4
	.word 0x0
.endarea

.org HookGetObjectData4
.area 0x18
	moveq  r5,#0xE
	mov r0,r1
	bl GetObjectData
	add r2,r0,#0x5
	ldrb r0,[r2]
	cmp r0,#0x0
.endarea

.org HookGetObjectData5
.area 0x4
	.word 0x0
.endarea

.org ObjectData
.area SizeObjectData
GetObjectData:
	stmdb r13!,{r4,r14}
	sub r13,r13,#0x48
	mov r4,r0
	; Open File Stream
	bl FStreamAlloc
	mov r0,r13
	bl FStreamCtor
	mov r0,r13
	ldr r1,=filename
	bl FStreamFOpen
	mov r0,r13
	mov r1,r4,lsl #0x4
	mov r2,#0
	bl FStreamSeek
	mov r0,r13
	ldr r1,=object_buffer
	mov r2,#0x10
	bl FStreamRead
	mov r0,r13
	bl FStreamClose
	bl FStreamDealloc
	ldr r0,=object_buffer
	add r13,r13,#0x48
	ldmia r13!,{r4,r15}
	.pool
object_buffer:
	.fill 0x10,0x0
filename:
	.ascii "BALANCE/objects.bin",0
	.fill (ObjectData+SizeObjectData-.), 0xCC
.endarea
