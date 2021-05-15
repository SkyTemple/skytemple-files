; ///////////////////////// overlay_0019.bin

; Spinda recruit tables

.org HookSpindaRecruitTable1
.area 0x4
	mov r0,NbIndepEntries*2
.endarea

.org HookSpindaRecruitTable2
.area 0x3C
	mov  r6,#0x0
	mov  r5,r0
	mov  r7,r6
loop_spinda_recruit_table_1:
	mov  r0,r7
	bl IsSpecialSpindaEggRecruitPkmn
	cmp r0, #0
	movne  r0,r7
	blne GotoCheckValidPkmnIDForMissions
	cmp r0,#0x0
	movne r0,r6,lsl #0x1
	strneh r7,[r5,r0]
	addne  r6,r6,#0x1
next_step_recruit_table_1:
	add  r7,r7,#0x1
	cmp r7,NbIndepEntries
	blt loop_spinda_recruit_table_1
.endarea

.org HookSpindaRecruitTable3
.area 0x4
	mov r0,NbIndepEntries*2
.endarea

.org HookSpindaRecruitTable4
.area 0x4C
	mov  r6,#0x0
	mov  r5,r0
	mov  r7,r6
loop_spinda_recruit_table_2:
	mov  r0,r7
	bl IsSpecialSpindaNormalRecruitPkmn
	cmp r0, #0
	movne  r0,r7
	blne GotoCheckValidPkmnIDForMissions
	cmp r0,#0x0
	beq next_step_recruit_table_2
	mov  r0,r7
	bl 0x020527C4
	cmp r0,#0x1
	moveq r0,r6,lsl #0x1
	streqh r7,[r5,r0]
	addeq  r6,r6,#0x1
next_step_recruit_table_2:
	add  r7,r7,#0x1
	cmp r7,NbIndepEntries
	blt loop_spinda_recruit_table_2
.endarea

.org RecruitablePokemonsTable
.area 0xD8
	.fill 0xD8, 0xCC
.endarea

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
