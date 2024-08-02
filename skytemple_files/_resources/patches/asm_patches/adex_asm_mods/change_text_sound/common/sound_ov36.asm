.org 0x023A7080+0xB20
.area 0xBA8-0xB20

HookTLetter:
	ldr r0,[r13, StackThing]
	add r1,=char_TS
	bl TagCheck
	cmp r0,#0
	beq check_TR ; If not [TS], check for [TR].
	ldr r0,[r13, StackThing+4]
	bl GetTagParameter
	str r0,[new_sound] ; Change the text sound to ID X from [TS:X:Y].
	cmp r6,#2
	moveq r0,#0x100 ; If there is no second parameter, assume a default volume of 0x100.
	ldrne r0,[r13, StackThing+8]
	blne GetTagParameter
	str r0,[new_volume]
	b AfterTagIsFound
check_TR:
	ldr r0,[r13, StackThing]
	add r1,=char_TR
	bl TagCheck
	cmp r0,#0
	beq TagCodeError ; If neither [TS] nor [TR], this is an invalid tag!
	ldr r0,=#16133
	str r0,[new_sound] ; Restore the default textbox sound effect.
	mov r0,#0x100
	str r0,[new_volume] ; Restore the default textbox volume.
	b AfterTagIsFound
CustomPlaySeByIdVolume:
	ldr r0,[new_sound]
	ldr r1,[new_volume]
	b PlaySeByIdVolume ; Original instruction, sorta
.pool
	new_sound:
		.word 0x3F05
	new_volume:
		.word 0x100
	char_TS:
		.asciiz "TS"
	char_TR:
		.asciiz "TR"
.endarea