; ///////////////////////// overlay_0011.bin

; TblTalk

.org HookTblTalk1
.area 0x8
	add r0,r0,NbIndepEntries
	sub r0,r0,#1
	;add  r0,r0,#0xAF
	;add  r0,r0,#0x400
.endarea

