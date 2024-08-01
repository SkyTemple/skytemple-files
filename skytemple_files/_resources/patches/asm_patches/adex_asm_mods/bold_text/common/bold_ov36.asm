.org 0x023A7080+0xA70
.area 0xAF8-0xA70

HookBLetter:
	ldr r0,[r13, StackThing]
	add r1,=char_BS
	bl TagCheck
	cmp r0,#0
	beq check_BR ; If not [BS], check for [BR].
	mov r0,#1
	str r0,[bold]
	b AfterTagIsFound
check_BR:
	ldr r0,[r13, StackThing]
	add r1,=char_BR
	bl TagCheck
	cmp r0,#0
	beq TagCodeError ; If neither [BS] nor [BR], this is an invalid tag!
	mov r0,#0
	str r0,[bold]
	b AfterTagIsFound
RepeatRender:
	; r7 contains the address to a function that displays a character.
	push r14,r0-r3
	blx r7
	ldr r0,[bold]
	cmp r0,#0
	pop r0-r3
	popeq r15
	subs r1,r1,#1 ; r1 = X-coordinate of character to display
	movmi r1,#0
	blx r7
	pop r15
TryIncreaseBoldCharWidth:
.if PPMD_GameVer == GameVer_EoS_JP
	ldrsh r0,[r0,#0x6] ; Original instruction, sorta
.else
	ldrb r0,[r0,#0x2] ; Original instruction, sorta
.endif
	ldr r1,[bold]
	cmp r1,#0
	addne r0,r0,#1
	pop r3,r15
.pool
	bold:
		.word 0x0
	char_BS:
		.asciiz "BS"
	char_BR:
		.asciiz "BR"
.endarea