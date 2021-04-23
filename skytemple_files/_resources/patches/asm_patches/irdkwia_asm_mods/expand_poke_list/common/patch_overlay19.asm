; ///////////////////////// overlay_0019.bin

; SpindaRecruit2

.org HookSpindaRecruitGender1
.area 0x34
	ldrsh r4,[r5, r1]
	b end_spinda_recruit_g1
	.fill 0x28, 0xCC
	mov  r4,#0x0
end_spinda_recruit_g1:
.endarea

.org HookSpindaRecruitGender2
.area 0x34
	ldrsh r4,[r5, r1]
	b end_spinda_recruit_g2
	.fill 0x28, 0xCC
	mov  r4,#0x0
end_spinda_recruit_g2:
.endarea

.org HookSpindaRecruitGender3
.area 0x34
	ldrsh r4,[r5, r1]
	b end_spinda_recruit_g3
	.fill 0x28, 0xCC
	mov  r4,#0x0
end_spinda_recruit_g3:
.endarea

; SpindaRecruit

.org HookSpindaRecruit1
.area 0x4
	mov r0,NbIndepEntries*2
.endarea
.org HookSpindaRecruit2
.area 0x4
	cmp r6,NbIndepEntries
.endarea
