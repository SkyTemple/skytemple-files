; ///////////////////////// overlay_0010.bin

; Hook Animations

 .org HookAnim1
.area 0xC
	bl GetFirstFormIfValid
	nop
	mov  r1,r0,lsl #0x10
.endarea

 .org HookAnim2
.area 0xC
	bl GetFirstFormIfValid
	nop
	mov  r1,r0,lsl #0x10
.endarea

 .org HookAnim3
.area 0xC
	bl GetFirstFormIfValid
	nop
	mov  r1,r0,lsl #0x10
.endarea

 .org HookAnim4
.area 0xC
	bl GetFirstFormIfValid
	nop
	mov  r1,r0,lsl #0x10
.endarea
