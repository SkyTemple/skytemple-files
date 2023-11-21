.org 0x023A7080+0x18F0
.area 0x1958-0x18F0

HookVLetter:
	ldr r0,[r13, StackThing]
	ldr r1,=VAR_TAG
	bl TagCheck
	cmp r0,#0
	beq TagCodeError
	ldr r0,[r13, StackThing+4]
	bl GetTagParameter
	mov r5,r0
	ldr r0,[r13, StackThing+8]
	bl GetTagParameter
	mov r2,r0
	mov r1,r5
	mov r0,#0
	bl GetGameVarIndexed
	mov r2,r0
	add r0,r13,#0x1C8
	ldr r1,=FORMAT
	bl SprintfStatic
	add r7,r13,#0x1C8
	b AfterTagIsFound
.pool
	VAR_TAG:
		.asciiz "var"
	FORMAT:
		.asciiz "%d"
.endarea
