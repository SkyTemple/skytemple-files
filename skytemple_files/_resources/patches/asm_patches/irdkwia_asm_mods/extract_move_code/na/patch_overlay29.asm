; For use with ARMIPS
; 2021/03/04
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Use filestreams to load move effects code
; ------------------------------------------------------------------------------

.org StartTable
.area MetronomeFuncTempStruct-StartTable
invalidate_cache:
	str r11,[TemporaryR11]
	ldr r11,=end_m_func
	mov r1,#0x1
	strb r1,[r5, #+0x162]
hook_start_table: 
	stmdb  r13!,{r5,r7,r8}
	
	; Bonjour, est-ce que vous connaissez le C-A-C-H-E ?
	bl InvalidateInstructionCache
	bl InvalidateAndCleanDataCache
	mov  r0,#0x0
	mcr p15,0,r0,c7,c5,4
	mcr p15,0,r0,c7,c5,6
	mcr p15,0,r0,c7,c0,4
	
	ldr r5, =CachedValue
	ldr r0, [r5, #+0x0]
	cmp r0,r6
	beq end_read_code
read_code:
	str r6, [r5, #+0x0]
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
	mov r1,r6,lsl #0x1
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
	
	ldmia  r13!,{r5,r7,r8}
	mov r1,#1
	b StartMFunc
	.pool
return_effect:
	bx r11
end_m_func:
	ldr r11,[TemporaryR11]
	cmp r10,#0x0
	b end_m_func_next
	.fill (MetronomeFuncTempStruct-.), 0xCC
.endarea

.org MetronomeFuncTempStruct
.area 0x8
	.fill 0x8, 0x0
.endarea

.org MetronomeFuncTempArea
.area 0x20
	.fill 0x20, 0x0
.endarea

.org TemporaryR11
.area 0x4
	.fill 0x4, 0x0
.endarea

.org CachedValue
.area 0x4
	.fill 0x4, 0xFF
.endarea

.org BufferRead
.area 0x8
	.fill 0x8, 0
.endarea

.org FileName
.area 0x14
	.ascii "BALANCE/waza_cd.bin"
	dcb 0
.endarea

.org FileStream
.area 0x48
	.fill 0x48, 0
.endarea

.org StartMFunc
.area EndMFunc-StartMFunc
	.fill (EndMFunc-StartMFunc), 0x0
.endarea
.org EndMFunc
.area 0x4
	b return_effect
end_m_func_next:
.endarea

.org MetronomeHook
.area 0xC
	mvn r0,#0
	bl MetronomeGetMove
	mov r2,r1
.endarea
.org MetronomeHook+0x10
.area 0x14
	str r2,[r1]
	mov r1,r0
	add  r0,r13,#0x28
	nop
	nop
.endarea

.org MetronomeFunc
.area 0x60
	mov  r9,r0
	ldr r0,=MetronomeFuncTempArea
	stmia  r0,{r3,r4,r6,r7,r8,r9,r11}
	ldr r0,=MetronomeLastMove
	ldr r0,[r0, #+0x0]
	mov r6,r0
	mov  r4,r1
	bl MetronomeGetMove
	mov r1,r0
	mov r6,r1
	ldr r0,=MetronomeFuncTempStruct
	mov  r7,r3
	bl GetInfoMove
	ldr r8,=MetronomeFuncTempStruct
	ldr r11,=after_metronome
	bl hook_start_table
after_metronome:
	ldr r0,=MetronomeFuncTempArea
	ldmia  r0,{r3,r4,r6,r7,r8,r9,r11}
	b end_m_func
	.pool
	.fill (MetronomeFunc+0x60-.), 0xCC
.endarea
