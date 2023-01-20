; For use with ARMIPS
; 2023/01/20
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Allows pushing allies in dungeons
; ------------------------------------------------------------------------------

.orga 0xE00
.area 0x320 ; Needed
HookPush:
	ldr r0,=ctrl_struct
	ldrh r0,[r0]
	tst r0,#0x2
	ldrne r0,[r13, #+0x14]
	bne EndHookPush
	bl ClearStack
	ldr r0,[r13, #+0x14]
	ldrb r1,[r11, #+0x4c]
	bl CheckPush
	cmp r0,#0
	beq no_push
	add  r0,r11,#0x4A
	mov  r1,#0x2
	bl SetupAction
	mov r0,#0
	mov r1,r6
	mov r2,#0
	bl ChangeString
	mov r0,#1
	ldr r1,[r13, #+0x14]
	mov r2,#0
	bl ChangeString
	mov r0,r6
	ldr r1,=PushStringID
	bl SendMessageWithIDLog
	ldr r0,=ctrl_struct
	ldrh r0,[r0, #+0x0]
	tst r0,#0x2
	movne  r0,#0x0
	moveq  r0,#0x1
	strb r0,[r11, #+0x4e]
	ldrh r2,[r11, #+0x0]
	orr  r2,r2,#0x8000
	strh r2,[r11, #+0x0]
	ldr r1,=dungeon_main_ptr
	ldr r2,[r1, #+0x0]
	mov r0,#1
	strb r0,[r2, #+0x10]
	b CheckMove
no_push:
	mov r0,#0
	b CheckMove
CheckPush:
	stmdb r13!,{r4,r5,r6,r7,r8,r9,r14}
	sub r13,r13,#0x4
	mov r4,r0
	mov r5,r1
	bl CheckStack
	cmp r0,#0
	moveq r0,#0
	addeq r13,r13,#0x4
	ldmeqia r13!,{r4,r5,r6,r7,r8,r9,r15}
	mov r9,r0
	mov r6,r5
	mov r7,#0
push_start_loop:
	ldr r2,=direction_struct
	mov r3,r6
	ldrsh r0,[r4, #+0x4]
	ldrsh r1,[r4, #+0x6]
	add r3,r2,r3,lsl #0x2
	ldrsh r2,[r3]
	ldrsh r3,[r3, #+0x2]
	add  r0,r0,r2
	strh r0,[r13]
	add  r1,r1,r3
	strh r1,[r13,#+0x2]
	bl GetTile
	ldr r8,[r0,#+0xc]
	mov r0,r4
	mov r1,r13
	bl CheckAllowedMove
	cmp r0,#0
	bne push_check_loop
	mov r0,r4
	mov r1,r6
	bl CheckMoveCorners
	cmp r0,#0
	beq push_check_loop
	cmp r8,#0
	beq skip_add_check
	ldr r0,[r8,#+0xb4]
	bl CheckValidity
	cmp r0,#0
	beq push_check_loop
	mov r0,r8
	mov r1,#0
	bl CheckEntityUnk2
	cmp r0,#0
	bne push_check_loop
	mov r0,r8
	mov r1,r6
	bl CheckPush
	cmp r0,#0
	beq push_check_loop
skip_add_check:
	mov r0,r4
	mov r1,r6
	bl MoveDirection
	mov r0,#0
	str r0,[r9]
	mov r0,#1
	add r13,r13,#0x4
	ldmia r13!,{r4,r5,r6,r7,r8,r9,r15}
push_check_loop:
	ldr r0,=dir_list
	add r0,r0,r5,lsl #0x2
	ldrb r6,[r0,r7]
	add r7,r7,#1
	cmp r7,#0x4
	ble push_start_loop
	mov r0,#0
	str r0,[r9]
	add r13,r13,#0x4
	ldmia r13!,{r4,r5,r6,r7,r8,r9,r15}
CheckValidity:
	stmdb r13!,{r4,r14}
	mov r4,r0
	ldrb r0,[r4, #+0x6]
	cmp r0,#0x0
	ldrneb r0,[r4, #+0x9]
	cmpne r0,#0x1
	cmpne r0,#0x2
	beq skip_validity
	mov  r0,r4
	bl CheckEntityUnk1
	cmp r0,#0x0
	bne skip_validity
	ldrb r0,[r4, #+0xbc]
	cmp r0,#0x7
	bne end_check_validity
skip_validity:
	mov r0,r4
	bl CheckEntityStatus
	cmp r0,#0x0
	beq end_check_validity
	ldrb r0,[r4, #+0xd0]
	cmp r0,#0x2
	beq end_check_validity
	ldrb r0,[r4, #+0xbd]
	cmp r0,#0
	cmpne r0,#2
	cmpne r0,#4
	moveq  r0,#1
	ldmeqia r13!,{r4,r15}
end_check_validity:
	mov r0,#0
	ldmia r13!,{r4,r15}
MoveDirection:
	stmdb r13!,{r4,r5,r6,r14}
	mov r4,r0
	mov r6,r1
	ldr r5,[r4,#+0xb4]
	add  r0,r5,#0x4A
	mov  r1,#0x2
	bl SetupAction
	mov  r0,#0x0
	strb r0,[r5, #+0x4e]
	add  r2,r5,#0x100
	mov  r1,r6
	strb r1,[r5, #+0x4c]
	ldrh r1,[r5, #+0x0]
	orr  r1,r1,#0x8000
	strh r1,[r5, #+0x0]
	ldrsh r1,[r4, #+0x4]
	strh r1,[r2, #+0x7e]
	ldrsh r1,[r4, #+0x6]
	strh r1,[r2, #+0x80]
	ldmia r13!,{r4,r5,r6,r15}
CheckStack:
	ldr r2,=push_stack
	mov r3,#0
loop_check_stack:
	ldr r1,[r2]
	cmp r1,#0
	streq r0,[r2]
	moveq r0,r2
	bxeq r14
	cmp r1,r8
	moveq r0,#0
	bxeq r14
	add r2,r2,#4
	add r3,r3,#1
	cmp r3,#4
	blt loop_check_stack
	mov r0,#0
	bx r14
ClearStack:
	mov r0,#0
	str r0,[push_stack]
	str r0,[push_stack+0x4]
	str r0,[push_stack+0x8]
	str r0,[push_stack+0xC]
	bx r14
	.pool
dir_list:
	.dcb 7,1,6,2
	.dcb 0,2,7,3
	.dcb 1,3,0,4
	.dcb 2,4,1,5
	.dcb 3,5,2,6
	.dcb 4,6,3,7
	.dcb 5,7,4,0
	.dcb 6,0,5,1
push_stack:
	.word 0x0,0x0,0x0,0x0
.endarea
