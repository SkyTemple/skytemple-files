; For use with ARMIPS
; 2021/05/12
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Use filestreams to load process effects code
; ------------------------------------------------------------------------------

.definelabel StartTable, 0x022E7140
.definelabel StartMFunc, 0x022E7248
.definelabel EndMFunc, 0x022E7AC0
.definelabel FileStream, EndMFunc - 0x48
.definelabel FileName, FileStream - 0x14
.definelabel BufferRead, FileName - 0x8
.definelabel CachedValue, BufferRead - 0x4

.definelabel InvalidateInstructionCache, 0x0207A324
.definelabel InvalidateAndCleanDataCache, 0x0207A270

.org StartTable
.area StartMFunc-StartTable
	stmdb  r13!,{r6,r7,r8}
	
	; Bonjour, est-ce que vous connaissez le C-A-C-H-E ?
	bl InvalidateInstructionCache
	bl InvalidateAndCleanDataCache
	;mov  r0,#0x0
	mcr p15,0,r0,c7,c5,4
	mcr p15,0,r0,c7,c5,6
	mcr p15,0,r0,c7,c0,4
	
	ldr r6, =CachedValue
	ldr r0, [r6, #+0x0]
	cmp r0,r5
	beq end_read_code
read_code:
	str r5, [r6, #+0x0]
	ldr r7,=FileStream
	ldr r8,=BufferRead
	bl FStreamAlloc
	mov r0,r7
	bl FStreamCtor
	mov r0,r7
	ldr r1,=FileName
	bl FStreamFOpen
	
	mov r0,r7
	mov r1,r8
	mov r2,#0x4
	bl FStreamRead
	
	; Get the offset in file
	mov r0,r7
	mov r1,r5,lsl #0x1
	mov r2,#0x1 ; Relative seek
	bl FStreamSeek
	mov r0,r7
	add r1,r8,#0x4
	mov r2,#0x2
	bl FStreamRead
	
	
	ldrh r1,[r8, #+0x4]
	ldr r0,[r8, #+0x0]
	add r1,r0,r1,lsl #0x3
	mov r0,r7
	mov r2,#0x0
	bl FStreamSeek
	mov r0,r7
	mov r1,r8
	mov r2,#0x8
	bl FStreamRead
	
	; Read the code
	mov r0,r7
	ldr r1,[r8, #+0x0]
	mov r2,#0x0
	bl FStreamSeek
	mov r0,r7
	ldr r1,=StartMFunc
	ldr r2,[r8, #+0x4]
	bl FStreamRead
	
	; Close the stream
	mov r0,r7
	bl FStreamClose
	bl FStreamDealloc
end_read_code:

	; Non mais, est-ce que vous connaissez VRAIMENT le C-A-C-H-E ?
	bl InvalidateInstructionCache
	bl InvalidateAndCleanDataCache
	mov  r0,#0x0
	mcr p15,0,r0,c7,c5,4
	mcr p15,0,r0,c7,c5,6
	mcr p15,0,r0,c7,c0,4
	
	ldmia  r13!,{r6,r7,r8}
	b StartMFunc
	.pool
	.fill (StartMFunc-.), 0xCC
.endarea

.org CachedValue
.area 0x8
	.fill 0x4, 0xFF
.endarea

.org BufferRead
.area 0x8
	.fill 0x8, 0
.endarea

.org FileName
.area 0x14
	.ascii "BALANCE/process.bin"
	dcb 0
.endarea

.org FileStream
.area 0x48
	.fill 0x48, 0
.endarea

.org StartMFunc
.area CachedValue-StartMFunc
	.fill (CachedValue-StartMFunc), 0x0
.endarea
