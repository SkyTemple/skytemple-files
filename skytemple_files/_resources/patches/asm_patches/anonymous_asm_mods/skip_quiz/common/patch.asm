; For use with ARMIPS
; 2021/03/23
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Gets rid of the personality quiz
; ------------------------------------------------------------------------------
	
	.org HookBeforeQuestions
	.area 0x4*14
		mov  r1,#0xE
		ldr r3,[r0, #+0x0]
		mov  r0,#0x0
		strb r1,[r3, #+0x0]
		mov r1,#9
		str r1,[r3, #+0x24]
		strb r0,[r3, #+0x5e]
		strb r0,[r3, #+0x5f]
		ldr r1,[r3, #+0x20]
		add  r1,r1,#0x1
		str r1,[r3, #+0x20]
		mov  r1,#0x6F
		mov  r2,#0x1
		bl SetGameVariable
	.endarea
	
	.org HookAfterQuestions
	.area 0x4
		mov r2,#0x48
	.endarea
