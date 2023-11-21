.org 0x023A7080+0x1970
.area 0x1A2C-0x1970

FaceTagHook:
	push r5
	ldr r0,[r13, StackThing+4]
	ldr r1,=FACE_TAG
	bl TagCheck
	cmp r0,#0
	popeq r5
	beq TagCodeError
	mov r0,#13
	bl OverlayIsLoaded
	cmp r0,#1
	ldreq r5,=ScriptPortraitPointer
	beq change_face
	mov r0,#14
	bl OverlayIsLoaded
	ldr r5,[DUNGEON_PORTRAIT_PTR]
	cmp r0,#0
	cmpne r5,#0
	beq ret
change_face:
	ldr r0,[r13, StackThing+8]
 	bl GetTagParameter
	mov r1,r0
	mov r0,r5
	bl SetPortraitExpressionID
	mov r0,r5
	mov r1,#1
	bl AllowPortraitDefault
	add r0,=PORTRAIT_DBOX_ID
	ldrb r0,[r0]
	mov r1,r5
	bl ShowPortrait
ret:
	pop r5
	b AfterTagIsFound

DBoxHook:
	ldrsb r0,[r5,#0x0] ; Original instruction
	add r1,=PORTRAIT_DBOX_ID
	strb r0,[r1]
	bx r14

DungeonHook:
	mov r4,r2 ; Original instruction
	str r6,[DUNGEON_PORTRAIT_PTR]
	bx r14

.pool
	DUNGEON_PORTRAIT_PTR:
		.word 0x0
	PORTRAIT_DBOX_ID:
		.byte 0x0
	FACE_TAG:
		.asciiz "FACE"
.endarea
