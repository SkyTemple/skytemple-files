; For use with ARMIPS
; 2023/09/20
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Use filestreams to load move effects code
; ------------------------------------------------------------------------------

.definelabel StartTable, 0x02330C94
.definelabel StartMFunc, 0x02331528
.definelabel EndMFunc, 0x02333AC0
.definelabel FileStream, StartMFunc - 0x48
.definelabel FileName, FileStream - 0x14
.definelabel BufferRead, FileName - 0x8
.definelabel CachedValue, BufferRead - 0x4
.definelabel TemporaryR11, CachedValue - 0x4
.definelabel MetronomeFuncTempArea, TemporaryR11 - 0x20
.definelabel MetronomeFuncTempStruct, MetronomeFuncTempArea - 0x8

.definelabel InvalidateInstructionCache, 0x0207A60C
.definelabel InvalidateAndCleanDataCache, 0x0207A558

.definelabel MetronomeFunc, 0x0232D0B8
.definelabel RandMax, 0x022EC100
.definelabel MetronomeLastMove, 0x0237DD08
.definelabel MetronomeGetMove, 0x022C74C4
.definelabel LastMoveID, MetronomeGetMove+0x540-0x4
.definelabel MetronomeCachedChoice, LastMoveID-0x4
.definelabel MetronomeFileName, MetronomeCachedChoice-0x14
.definelabel GetInfoMove, 0x02013788

.definelabel FGetSize, 0x02008244

.definelabel MetronomeHook, 0x0232389C

.org MetronomeGetMove
.area MetronomeFileName-MetronomeGetMove
	stmdb  r13!,{r5,r6,r7,r8,r14}
	mov r6,r0
	ldr r5, =MetronomeCachedChoice
	ldr r8, =LastMoveID
	mvn r0, #0
	cmp r0,r6
	beq read_move_id
	ldr r0, [r5]
	cmp r0,r6
	beq end_read_move_id
read_move_id:
	str r6, [r5]
	ldr r7,=FileStream
	bl FStreamAlloc
	mov r0,r7
	bl FStreamCtor
	mov r0,r7
	ldr r1,=MetronomeFileName
	bl FStreamFOpen
	
	mvn r0, #0
	cmp r0,r6
	bne no_choice
	; Get the total size of the file
	mov r0,r7
	bl FGetSize
	mov r0,r0,lsr #0x2
	bl RandMax
	mov r6,r0
	str r6,[r5]
no_choice:
	; Get the offset in file
	mov r0,r7
	mov r1,r6,lsl #0x2
	mov r2,#0x0
	bl FStreamSeek
	mov r0,r7
	mov r1,r8
	mov r2,#0x4
	bl FStreamRead
	
	; Close the stream
	mov r0,r7
	bl FStreamClose
	bl FStreamDealloc
end_read_move_id:
	ldr r0, [r8]
	mov r1, r6
	ldmia  r13!,{r5,r6,r7,r8,r15}
	.pool
	.fill (MetronomeFileName-.), 0xCC
.endarea

.org MetronomeFileName
.area 0x14
	.ascii "BALANCE/metrono.bin"
	dcb 0
.endarea

.org MetronomeCachedChoice
.area 0x4
	.fill 0x4, 0xFF
.endarea
.org LastMoveID
.area 0x4
	.fill 0x4, 0x0
.endarea
