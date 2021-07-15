; For use with ARMIPS
; 2021/07/10
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Provides a way to change the textbox bg
; ------------------------------------------------------------------------------

.org HookSetBGColor
.area 0x1C
	ldr r0,[color]
	str r0,[r5, #+0x60]
	b after
color:
	.dcb Red
	.dcb Green
	.dcb Blue
	.dcb Alpha
	.word 0x0
	.word 0x0
after:
	add  r0,r5,#0x74
.endarea
