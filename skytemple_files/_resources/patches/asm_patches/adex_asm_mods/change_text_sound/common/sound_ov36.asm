.org 0x023A7080+0xB20
.area 0xB7C-0xB20

HookTLetter:
	ldr r0,[r13, StackThing]
	add r1,=char_TS
	bl TagCheck
	cmp r0,#0
	beq check_TR ; If not [TS], check for [TR].
	ldr r0,[r13, StackThing+4]
	bl GetTagParameter
	ldr r1,=TextboxSE
	str r0,[r1] ; Change the text sound to ID X from [TS:X]
	b AfterTagIsFound
check_TR:
	ldr r0,[r13, StackThing]
	add r1,=char_TR
	bl TagCheck
	cmp r0,#0
	beq TagCodeError ; If neither [TS] nor [TR], this is an invalid tag!
	ldr r1,=TextboxSE
	ldr r0,=#16133
	str r0,[r1] ; Restore the default textbox sound effect.
	b AfterTagIsFound
.pool
	char_TS:
		.asciiz "TS"
	char_TR:
		.asciiz "TR"
.endarea