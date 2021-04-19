; ///////////////////////// arm9.bin

; //// TODO LIST
; 0x02050244: Adventure Log Special Pokémon
; ////

; Change sort by name

.org HookN2MSearch
.area 0x6C
	cmp r0,#0x0
	movlt  r0,#0x0
	bxlt r14
	ldr r2,=MonsterFilePtr
	ldr r2,[r2, #+0x14]
	mov r0,r0,lsl #0x1
	ldrsh r0,[r2,r0]
	bx r14
	.pool
	.fill (HookN2MSearch+0x6C-.), 0xCC
.endarea

.org HookN2MSearchBase
.area 0x1C
	cmp r0,#0x0
	bge n2m_base_continue
	mov  r0,#0x0
	ldmia  r13!,{r3,r15}
	.fill 0xC, 0xCC
n2m_base_continue:
.endarea

.org HookM2NSearch
.area 0x6C
	cmp r0,#0x0
	movlt r0,#0x0
	ldr r1,=MonsterFilePtr
	ldr r3,[r1, #+0x1C]
	mov r0,r0,lsl #0x1
	ldrsh r0,[r3,r0]
	bx r14
	.pool
	.fill (HookM2NSearch+0x6C-.), 0xCC
.endarea

.org HookM2NSearchBase
.area 0x28
	cmp r0,#0x0
	movlt r0,#0x0
	b m2n_base_continue
	.fill 0x1C, 0xCC
m2n_base_continue:
.endarea

; Change sort by Dex Number

.org HookSortNb1
.area 0x4
	bl GetDexNb
.endarea
.org HookSortNb2
.area 0x4
	bl GetDexNb
.endarea

; ModMonster

.org HookModMonster
.area 0x4
	.word NbIndepEntries
.endarea

; Invalid Movesets

.org IsInvalidMoveset
.area 0x28
	cmp r0,#0x0
	ble below_lower_bound
	ldr r1,=NbIndepEntries
	cmp r0,r1
	blt below_upper_bound
below_lower_bound:
	mov  r0,#0x1
	bx r14
below_upper_bound:
	mov  r0,#0x0
	bx r14
	.pool
.endarea
.org IsInvalidMovesetEgg
.area 0x4
	.word NbIndepEntries
.endarea

; Lists

.org HookListForDungeon
.area 0x4
	.word NbIndepEntries*2
.endarea

; Swap Entries

.org IsValid
.area 0x5C
	cmp r0,#0x0
	movle  r0,#0x0
	movgt  r0,#0x1
	bx r14
	.fill 0x4C, 0xCC
.endarea
.org GetSecondFormIfValid
.area 0x3C
	bx r14
	.fill 0x38, 0xCC
.endarea
.org GetFirstFormIfValid
.area 0x44
	ldr r2,=MonsterFilePtr
	mov  r1,#0x44
	ldr r2,[r2, #+0x0]
	smlabb r0,r0,r1,r2
	ldrsh r0,[r0, #+0x0]
	bx r14
	.pool
	.fill (GetFirstFormIfValid+0x44-.), 0xCC
.endarea


; Moves

; Change GetMovesetLevelUpPtr
.org HookGetMovesetLevelUpPtr
.area 0x10
	nop
	nop
	nop
	nop
	;cmp r4,NbIndepEntries
	;subge  r0,r4,NbIndepEntries
	;movge  r0,r0,lsl #0x10
	;movge  r4,r0,asr #0x10
.endarea

; Change GetMovesetHMTMPtr
.org HookGetMovesetHMTMPtr
.area 0x10
	nop
	nop
	nop
	nop
	;cmp r4,NbIndepEntries
	;subge  r0,r4,NbIndepEntries
	;movge  r0,r0,lsl #0x10
	;movge  r4,r0,asr #0x10
.endarea


; Change GetMovesetEggPtr
.org HookGetMovesetEggPtr
.area 0x10
	nop
	nop
	nop
	nop
	;cmp r4,NbIndepEntries
	;subge  r0,r4,NbIndepEntries
	;movge  r0,r0,lsl #0x10
	;movge  r4,r0,asr #0x10
.endarea

; Portraits

.org HookPortrait1
.area 0x4
	cmp r7,#0x0
.endarea
.org HookPortrait2
.area 0x4
	ble HookPortrait3
.endarea
.org HookPortrait3
.area 0x8
	nop
	nop
.endarea
.org HookPortrait4
.area 0x4
	bne HookPortrait1
.endarea

; Strings

.org HookStringsPkmn1
.area 0x8
	add  r0,r1,Pkmn_StrID_L
	add  r0,r0,Pkmn_StrID_H
.endarea
.org HookStringsPkmn2
.area 0x8
	add  r0,r1,Pkmn_StrID_L
	add  r0,r0,Pkmn_StrID_H
.endarea
.org HookStringsPkmn3
.area 0x8
	add  r0,r1,Pkmn_StrID_L
	add  r0,r0,Pkmn_StrID_H
.endarea
.org HookStringsPkmn4
.area 0x8
	add  r0,r1,Pkmn_StrID_L
	add  r0,r0,Pkmn_StrID_H
.endarea
.org HookStringsPkmn5
.area 0x8
	add  r0,r1,Pkmn_StrID_L
	add  r0,r0,Pkmn_StrID_H
.endarea
.org HookStringsCate1
.area 0x8
	add  r0,r1,Cate_StrID_L
	add  r0,r0,Cate_StrID_H
.endarea

; monster.md

.org HookMdAccess1
.area 0x8
	mov r1,r0
	nop
.endarea

.org HookMdAccess2
.area 0xC
	mov r1,r0
	mov r4,r2
	nop
.endarea

.org HookMdAccess3
.area 0xC
	mov r1,r0
	mov r4,r2
	nop
.endarea

.org HookMdAccess4
.area 0x8
	mov r1,r0
	nop
.endarea

.org HookMdAccess5
.area 0x8
	mov r1,r0
	nop
.endarea

.org HookMdAccess6
.area 0x8
	mov r1,r0
	nop
.endarea

; Sprite Size in monster.md (0x2C)
.org HookMdAccess7
.area 0x38
	ldr r2,=MonsterFilePtr
	mov  r1,#0x44
	ldr r2,[r2, #+0x0]
	smlabb r0,r0,r1,r2
	ldrb r0,[r0, #+0x2C]
	cmp r0,#0x0
	ldmeqia  r13!,{r3,r15}
	cmp r0,#0x6
	movls  r0,#0x6
	ldmia  r13!,{r3,r15}
	.pool
.endarea

; Sprite File Size in monster.md (0x2D)
.org HookMdAccess8
.area 0x20
	ldr r2,=MonsterFilePtr
	mov  r1,#0x44
	ldr r2,[r2, #+0x0]
	smlabb r0,r0,r1,r2
	ldrb r0,[r0, #+0x2D]
	mov  r0,r0,lsl #0x9
	bx r14
	.pool
.endarea

.org HookMdAccess9
.area 0xC
	mov r1,r0
	mov r4,r2
	nop
.endarea

.org HookMdAccess10
.area 0x8
	mov r1,r0
	nop
.endarea

; evolution possibilities

; TODO: Different Implementation

