; For use with ARMIPS
; 2023/09/20
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Use filestreams instead of hardcoded lists 
; ------------------------------------------------------------------------------

.definelabel ExternalFunctionCall, 0x0204F9A4

.definelabel HookFunction, 0x020518B8
.definelabel LoadForbid, 0x020A0AE8
.definelabel BufferReadF, 0x020A0B50
.definelabel ForbidFName, 0x020A0B54
.definelabel FStreamStruct, 0x020A0B68

.org HookFunction
.area 0x5C
	stmdb  r13!,{r3,r5,r6,r7,r8,r14}
	mov  r1,r0
	add  r0,r13,#0x0
	bl ExternalFunctionCall
	ldrb r6,[r13, #+0x0]
	ldrb r5,[r13, #+0x1]
	ldr r7,=RanksFStream
	ldr r8,=BufferRead
	
	bl FStreamAlloc
	mov r0,r7
	bl FStreamCtor
	mov r0,r7
	ldr r1,=ForbidFName
	bl FStreamFOpen
	
	b LoadForbid
end_forbid:
	ldrb r0,[r8, #+0x0]
	ldmia  r13!,{r3,r5,r6,r7,r8,r15}
	
	.pool
	.fill (HookFunction + 0x5C - .), 0xCC;
.endarea

.org LoadForbid
.area 0x68
	
	; Get the offset in file
	mov r0,r7
	mov r1,r6,lsl #0x2
	mov r2,#0x0
	bl FStreamSeek
	mov r0,r7
	mov r1,r8
	mov r2,#0x4
	bl FStreamRead
	
	; Get the mission floor byte
	mov r0,r7
	ldr r1,[r8, #+0x0]
	add r1,r1,r5
	mov r2,#0x0
	bl FStreamSeek
	mov r0,r7
	mov r1,r8
	mov r2,#0x1
	bl FStreamRead
	
	; Close the stream
	mov r0,r7
	bl FStreamClose
	bl FStreamDealloc
	
	b end_forbid
	
	.pool
	.fill (BufferReadF - .), 0xCC;
.endarea

.org BufferReadF
.area 0x4
	.fill 0x4, 0;
.endarea

.org ForbidFName
.area 0x14
	.ascii "BALANCE/fforbid.bin"
	dcb 0
.endarea

.org FStreamStruct
.area 0x48
	.fill 0x48, 0;
.endarea
