; For use with ARMIPS
; 2021/04/20
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Change the way stats are displayed
; ------------------------------------------------------------------------------

.org SetStringAccuracy
.area 0xC8
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r14}
	bl CheckMove
	bl GetMoveActualAccuracy ; Get Move Accuracy
	cmp r0,#0x64
	ble no_sureshot
	ldr r1,=SureShotID
	mov  r0,r4
	bl StrCpyFromFile
	b end_string_accuracy
no_sureshot:
	mov r10,r0
	.notice "Accu1: "
	.notice (.)
	nop
	bl SetValue
	mov r7,r0
	mov  r2,StartPowerPos
	mov r9,#0
	bl PrintAttr
	b end_loop_print_accuracy
loop_print_accuracy:
	subs r0,r7,r6
	movlt r2, StartAccuracyPos
	blt print_accuracy
	cmp  r0,#10
	add r2, r0, StartAccuracyPos+1
	movgt r2, StartAccuracyPos+11
print_accuracy:
	bl PrintAttr
	add  r6,r6,#10
end_loop_print_accuracy:
	.if DisplayVal == 1
		cmp r6,#80
	.else
		cmp r6,#100
	.endif
	blt loop_print_accuracy
	mov  r2,StartPowerPos
	bl PrintAttr
	.notice "Accu2: "
	.notice (.)
	nop
end_string_accuracy:
	mov  r0,r4
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r15}
	.pool
SetValue:
	stmdb r13!, {r14}
	mov r6,#0
	strb r6,[r4, #+0x0]
	.notice "SetValue: "
	.notice (.)
	.if DisplayVal == 1
		mov r9,#1
		cmp r0,#10
		movlt r3,#14
		blt no_ten
		cmp r0,#100
		movlt r3,#8
		movge r3,#2
	no_ten:
		mov r2,r0
		bl PrintAttr
		mov r0,r10,lsl 0x3
		mov r1,#10
		bl EuclidianDivision
	.endif
	ldmia r13!, {r15}
	.fill (SetStringAccuracy+0xC8-.), 0xCC
.endarea

.org SetStringPower
.area 0xCC
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r14}
	bl CheckMove
	bl GetMoveBasePowerWithID ; Get Move Power
	cmp r0,#0x0
	bne no_status
	ldr r1,=NoDamageID
	mov  r0,r4
	bl StrCpyFromFile
	b end_string_power
no_status:
	mov r10,r0
	.notice "Power1: "
	.notice (.)
	nop
	bl SetValue
	add r7,r0,#2
	mov  r2,StartPowerPos
	mov r9,#0
	bl PrintAttr
	b end_loop_print_power
loop_print_power:
	sub r0,r7,r6
	cmp  r0,#10
	add r2, r0, StartPowerPos-1
	movgt r2, StartPowerPos+10
print_power:
	bl PrintAttr
	add  r6,r6,#10
end_loop_print_power:
	cmp r6,r7
	blt loop_print_power
	.notice "Power2: "
	.notice (.)
	nop
end_string_power:
	mov  r0,r4
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r15}
CheckMove:
	ldr r2,=MoveDescStartID
	mov  r4,r0
	cmp r1,r2
	bcc empty_string
	ldr r0,=MoveDescEndID
	cmp r1,r0
	bcs empty_string
	sub  r0,r1,r2
	mov  r8,r0
	bx r14
empty_string:
	ldr r0,=NullString
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r15}
	.pool
ValueString:
	.ascii "%d[S:%d]",0
	.fill (SetStringPower+0xCC-.), 0xCC
.endarea

.org PrintAttr
.area 0x38
	stmdb  r13!,{r14}
	sub r13,r13, #0x40
	cmp r9,#0
	ldreq r1,=SpecialCharString
	ldrne r1,=ValueString
	mov r0,r13
	bl SPrintF
	mov  r0,r4
	mov  r1,r13
	bl StrCat
	add r13,r13, #0x40
	ldmia  r13!,{r15}
	.pool
.endarea

.org SpecialCharString
.area 0x8
	.ascii "[M:B%d]",0
.endarea
