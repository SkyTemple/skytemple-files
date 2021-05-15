; ///////////////////////// overlay_0031.bin

; Recruitment search

.org HookRecSearch1
.area 0x8
	sub  r13,r13,NbIndepEntries
	nop
.endarea

.org HookRecSearch2
.area 0x8
	nop
	add  r13,r13,NbIndepEntries
.endarea

.org HookRecSearch3
.area 0x4
	.word NbIndepEntries
.endarea
