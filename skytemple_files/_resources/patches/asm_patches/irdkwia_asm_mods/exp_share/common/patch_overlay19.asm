; For use with ARMIPS
; 2021/04/25
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Adds Exp. Share
; ------------------------------------------------------------------------------

.org SwitchCaseGS
.area 0x4
	b CaseJS+0x8
.endarea

.org CaseJS
.area 0x68
	mov r0, #1
	b next_phase
	mov r0, #5
next_phase:
	stmdb r13!, {r6,r7,r8,r9}
	mov r6,r0
	mov  r0,r4
	bl IsMaxLevel
	cmp r0,#0x0
	beq level_up_spinda
	mov  r0,r6
	bl SetDialogueMaxLevel
	mov  r5,#0x4
	b end_phase
level_up_spinda:
	b AddMissingLevels
return_add_missing_levels:
	add r6,r6,r9
	sub r6,r6,r7
	mov  r0,r4
	mov  r1,r6
	bl AddLevels
	mov  r5,#0x3
end_phase:
	ldmia r13!, {r6,r7,r8,r9}
	b EndSwitch
.endarea
