; For use with ARMIPS
; 2021/04/20
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Change the way stats are displayed
; ------------------------------------------------------------------------------

.org SetStringAccuracy
.area 0xC8
	stmdb  r13!,{r3,r4,r5,r6,r7,r14}
	ldr r2,=MoveDescStartID
	mov  r4,r0
	cmp r1,r2
	bcc empty_string_accuracy
	ldr r0,=MoveDescEndID
	cmp r1,r0
	bcs empty_string_accuracy
	rsb  r0,r2,#0x0
	add  r0,r1,r0
	bl GetMoveActualAccuracy ; Get Move Accuracy
	cmp r0,#0x64
	ble no_sureshot
	ldr r1,=SureShotID
	mov  r0,r4
	bl StrCpyFromFile
	b end_string_accuracy
no_sureshot:
	mov r7,r0
	mov r6,#0
	mov  r0,#0x0
	strb r0,[r4, #+0x0]
	mov  r1,StartPowerPos
	mov  r0,r4
	bl PrintSpecialChar
	b end_loop_print_accuracy
loop_print_accuracy:
	subs r0,r7,r6
	movlt r1, StartAccuracyPos
	blt print_accuracy
	cmp  r0,#10
	addle r1, r0, StartAccuracyPos
	movgt r1, StartAccuracyPos+11
print_accuracy:
	mov  r0,r4
	bl PrintSpecialChar
	add  r6,r6,#10
end_loop_print_accuracy:
	cmp r6,#100
	blt loop_print_accuracy
	mov  r1,StartPowerPos
	mov  r0,r4
	bl PrintSpecialChar
end_string_accuracy:
	mov  r0,r4
	ldmia  r13!,{r3,r4,r5,r6,r7,r15}
empty_string_accuracy:
	ldr r0,=NullString
	ldmia  r13!,{r3,r4,r5,r6,r7,r15}
	.pool
	.fill (SetStringAccuracy+0xC8-.), 0xCC
.endarea

.org SetStringPower
.area 0xCC
	stmdb  r13!,{r3,r4,r5,r6,r7,r14}
	ldr r2,=MoveDescStartID
	mov  r4,r0
	cmp r1,r2
	bcc empty_string_power
	ldr r0,=MoveDescEndID
	cmp r1,r0
	bcs empty_string_power
	rsb  r0,r2,#0x0
	add  r0,r1,r0
	bl GetMoveBasePowerWithID ; Get Move Power
	cmp r0,#0x0
	bne no_status
	ldr r1,=NoDamageID
	mov  r0,r4
	bl StrCpyFromFile
	b end_string_power
no_status:
	mov r7,r0
	mov r6,#0
	mov  r0,#0x0
	strb r0,[r4, #+0x0]
	mov  r1,StartPowerPos
	mov  r0,r4
	bl PrintSpecialChar
	b end_loop_print_power
loop_print_power:
	sub r0,r7,r6
	cmp  r0,#10
	addle r1, r0, StartPowerPos-1
	movgt r1, StartPowerPos+10
print_power:
	mov  r0,r4
	bl PrintSpecialChar
	add  r6,r6,#10
end_loop_print_power:
	cmp r6,r7
	blt loop_print_power
end_string_power:
	mov  r0,r4
	ldmia  r13!,{r3,r4,r5,r6,r7,r15}
empty_string_power:
	ldr r0,=NullString
	ldmia  r13!,{r3,r4,r5,r6,r7,r15}
	.pool
	.fill (SetStringPower+0xCC-.), 0xCC
.endarea

.org PrintSpecialChar
.area 0x38
	stmdb  r13!,{r3,r4,r14}
	sub r13,r13, #0x40
	mov r4,r0
	mov r2,r1
	ldr r1,=SpecialCharString
	mov r0,r13
	bl SPrintF
	mov  r0,r4
	mov  r1,r13
	bl StrCat
	add r13,r13, #0x40
	ldmia  r13!,{r3,r4,r15}
	.pool
.endarea

.org SpecialCharString
.area 0x8
	.ascii "[M:B%d]"
	dcb 0
.endarea
