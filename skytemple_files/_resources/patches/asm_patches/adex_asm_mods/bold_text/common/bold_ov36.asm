.org 0x023A7080+0xA70
.area 0xAEC-0xA70

HookBLetter:
	ldr r0,[r13, StackThing]
	add r1,=char_BS
	bl TagCheck
	cmp r0,#0
	beq check_BR ; If not [BS], check for [BR].
	add r1,=bold
	mov r0,#1
	strb r0,[r1]
	b AfterTagIsFound
check_BR:
	ldr r0,[r13, StackThing]
	add r1,=char_BR
	bl TagCheck
	cmp r0,#0
	beq TagCodeError ; If neither [BS] nor [BR], this is an invalid tag!
	add r1,=bold
	mov r0,#0
	strb r0,[r1]
	b AfterTagIsFound
RepeatRender:
	; r7 contains the address to a function that displays a character.
	push r14,r0-r3
	blx r7
	add r0,=bold
	ldrb r0,[r0]
	cmp r0,#0
	pop r0-r3
	popeq r15
	subs r1,r1,#1 ; r1 = X-coordinate of character to display
	movmi r1,#0
	blx r7
	pop r15
.pool
	bold:
		.byte 0x0
	char_BS:
		.asciiz "BS"
	char_BR:
		.asciiz "BR"
.endarea