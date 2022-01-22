; ///////////////////////// overlay_0011.bin

;
 .org HookDisplay
.area 0x24
	bl GetPlayerPkmnStr
	cmp r0,#0x0
	moveq r4,#1
	beq label_0
	ldrsh r0,[r0, #+0x4]
	bl GotoGetGender
	cmp r0, #1
	moveq  r4,#0x0
	movne  r4,#0x1
label_0:
.endarea

; TblTalk

.org HookTblTalk1
.area 0x8
	add r0,r0,NbIndepEntries
	sub r0,r0,#1
	;add  r0,r0,#0xAF
	;add  r0,r0,#0x400
.endarea

