; ///////////////////////// overlay_0029.bin

; Change StoreSpriteFileIndexBothGenders

.org StoreSpriteFileIndexBothGenders
.area 0xC8
	stmdb  r13!,{r3,r14}
	ldr r2,=DungeonBaseStructurePtr
	ldr r2,[r2, #+0x0]
	mov  r3,r1
	add  r1,r2,MDDSpr_L
	add  r2,r1,MDDSpr_H
	mov  r1,r0,lsl #0x1
	strh r3,[r2, r1]
	ldmia  r13!,{r3,r15}
	.pool
	.fill (StoreSpriteFileIndexBothGenders+0xC8-.), 0xCC
.endarea

; Change Loading Sprites

.org LoadPokemonSpriteFiles
.area 0x114
	stmdb  r13!,{r4,r5,r14}
	mov  r4,r0
	cmp r1,#0x0
	bne no_deoxys
	ldr r0,=0xFFFFFE5E
	add  r0,r4,r0
	mov  r0,r0,lsl #0x10
	mov  r0,r0,lsr #0x10
	cmp r0,#0x3
	bhi no_deoxys
	ldr r0,=DungeonBaseStructurePtr
	ldr r0,[r0, #+0x0]
	add  r0,r0,#0x3E00
	ldrsh r0,[r0, #+0x3a]
	bl LoadSpriteForPkmn
	ldmia  r13!,{r4,r5,r15}
no_deoxys:
	mov  r0,r4
	bl LoadSpriteForPkmn
	mov r5,#0x17C
	cmp r4,r5
	subne  r0,r5,#0x1
	cmpne r4,r0
	addne  r0,r5,#0x1
	cmpne r4,r0
	addne  r0,r5,#0x2
	cmpne r4,r0
	beq castform
	ldr r0,=0xFFFFFC2D
	add  r0,r4,r0
	mov  r0,r0,lsl #0x10
	mov  r0,r0,lsr #0x10
	cmp r0,#0x3
	bhi no_castform
	add r5,r5,#0x258
castform:
	subne  r0,r5,#0x1
	bl LoadSpriteForPkmn
	mov r0,r5
	bl LoadSpriteForPkmn
	addne  r0,r5,#0x1
	bl LoadSpriteForPkmn
	addne  r0,r5,#0x2
	bl LoadSpriteForPkmn
no_castform:
	mov r5,#0x1CC
	cmp r4,r5
	addne r0,r5,#0x1
	cmpne r4,r0
	beq cherrim
	ldr r0,=0xFFFFFBDC
	add  r0,r4,r0
	mov  r0,r0,lsl #0x10
	mov  r0,r0,lsr #0x10
	cmp r0,#0x1
	ldmhiia  r13!,{r4,r5,r15}
	add r5,r5,#0x258
cherrim:
	mov  r0,r5
	bl LoadSpriteForPkmn
	add r0,r5,#0x1
	bl LoadSpriteForPkmn
	ldmia  r13!,{r4,r5,r15}
	.pool
	.fill (LoadPokemonSpriteFiles+0x114-.), 0xCC
.endarea

; Kecleon

.org SetKecleonEntryForFloor
.area 0x38
	str r0, [kecleon_hold]
	bx r14
	.fill 0x30, 0xCC
.endarea

.org GetKecleonEntryForFloor
.area 0x1C
	ldr r0, [kecleon_hold]
	bx r14
kecleon_hold:
	.word 0x0
	.fill 0x10, 0xCC
.endarea

; Monster Modulo

.org HookDungeonMonsterMod1
.area 0x8
	mov r1, r0
	nop
.endarea
.org HookDungeonMonsterMod2
.area 0x14
	mov r1, r0
	mov  r8,r2
	mov  r7,r3
	ldr r6,[r13, #+0x34]
	nop
.endarea
.org HookDungeonMonsterMod3
.area 0x8
	mov r1, r0
	nop
.endarea

; Limits

.org HookDungeonMonsterLimit1
.area 0x4
	.word NbIndepEntries
.endarea
.org HookDungeonMonsterLimit2
.area 0x4
	.word NbIndepEntries
.endarea
.org HookDungeonMonsterLimit3
.area 0x4
	.word NbIndepEntries
.endarea

; Limit 4: Change other things

.org HookDungeonMonsterLimit4C1
.area 0x8
	ldr r2,[r15, #+0x78] ;527
	cmp r0,r2
.endarea
.org HookDungeonMonsterLimit4C2
.area 0x4
	sub r1,r2,#0x2 ;525
.endarea
.org HookDungeonMonsterLimit4
.area 0x4
	.word NbIndepEntries
.endarea

; Dungeon Data Structure Size

.org HookDungeonStructSize1
.area 0x4
	.word DungeonDataStructSize
.endarea
.org HookDungeonStructSize2
.area 0x4
	.word DungeonDataStructSize
.endarea

; Sprite File Index

.org HookDungeonSpriteFile1
.area 0x8
	add  r0,r0,MDDSpr_L
	add  r4,r0,MDDSpr_H
.endarea
; 2 is in StoreSpriteFileIndexBothGenders
.org HookDungeonSpriteFile3
.area 0xC
	add  r1,r1,MDDSpr_L
	mov  r0,r5
	add  r4,r1,MDDSpr_H
.endarea
.org HookDungeonSpriteFile4
.area 0x4
	.word MDDSpr_L+MDDSpr_H
.endarea
.org HookDungeonSpriteFile5
.area 0x4
	.word MDDSpr_L+MDDSpr_H
.endarea
.org HookDungeonSpriteFile6
.area 0x4
	.word MDDSpr_L+MDDSpr_H
.endarea
.org HookDungeonSpriteFile7
.area 0x4
	.word MDDSpr_L+MDDSpr_H
.endarea

; Dungeon Recruit Index

.org HookDungeonRec1
.area 0x10
	add  r0,r0,MDDRec_H
	add  r2,r2,#0x1
	strb r10,[r0, MDDRec_L]
	cmp r2,NbIndepEntries
.endarea
.org HookDungeonRec2
.area 0x8
	add  r0,r0,MDDRec_H
	ldrb r0,[r0, MDDRec_L]
.endarea
.org HookDungeonRec3
.area 0x8
	add  r1,r0,MDDRec_H
	strb r0,[r1, MDDRec_L]
.endarea
.org HookDungeonRec4
.area 0x8
	add  r0,r0,MDDRec_H
	strb r1,[r0, MDDRec_L]
.endarea
.org HookDungeonRec5
.area 0x18
	add  r0,r0,MDDRec_H
	ldrb r3,[r0, MDDRec_L]
	add  r4,r4,#0x1
	cmp r3,#0x0
	streqb r2,[r0, MDDRec_L]
	cmp r4,NbIndepEntries
.endarea
.org HookDungeonRec6
.area 0x8
	add  r0,r0,MDDRec_H
	ldrb r4,[r0, MDDRec_L]
.endarea

; TblTalk

.org HookTblTalk2
.area 0x4
	.word NbIndepEntries+0x23
.endarea

.org HookTblTalk3
.area 0x4
	moveq  r4,NbIndepEntries
.endarea

.org HookTblTalk4
.area 0x4
	ldr r4,[r15, #+0x18c]
	;ldreq r4,[r15, #+0x18c]
.endarea

.org HookTblTalk5
.area 0x4
	addeq  r4,r4,#1
	;addeq  r4,r1,#0x31C
.endarea

.org HookTblTalk6
.area 0x4
	moveq  r4,NbIndepEntries+0x20
.endarea

.org HookTblTalk7
.area 0x8
	.word NbIndepEntries+0x1
	.word NbIndepEntries+0x2
.endarea
.org HookTblTalk8
.area 0x10
	.word NbIndepEntries+0x1D
	.word NbIndepEntries+0x1F
	.word NbIndepEntries+0x21
	.word NbIndepEntries+0x3
.endarea
.org HookTblTalk9
.area 0x20
	.word NbIndepEntries+0x14
	.word NbIndepEntries+0x16
	.word NbIndepEntries+0x17
	.word NbIndepEntries+0x18
	.word NbIndepEntries+0x19
	.word NbIndepEntries+0x1A
	.word NbIndepEntries+0x1B
	.word NbIndepEntries+0x1C
.endarea
.org HookTblTalk10
.area 0x10
	.word NbIndepEntries+0x8
	.word NbIndepEntries+0x23
.endarea
.org HookTblTalk11
.area 0x40
	.word (NbIndepEntries+0x8)*0x10000+0x00FA
	.word (NbIndepEntries+0x5)*0x10000+0x00D9
	.word (NbIndepEntries+0x6)*0x10000+0x00DB
	.word (NbIndepEntries+0x4)*0x10000+0x00DC
	.word (NbIndepEntries+0x7)*0x10000+0x00DD
	.word (NbIndepEntries+0xE)*0x10000+0x00DE
	.word (NbIndepEntries+0x10)*0x10000+0x00DF
	.word (NbIndepEntries+0x11)*0x10000+0x00E0
	.word (NbIndepEntries+0x22)*0x10000+0x00E1
	.word (NbIndepEntries+0xD)*0x10000+0x00E2
	.word (NbIndepEntries+0xF)*0x10000+0x00EC
	.word (NbIndepEntries+0x15)*0x10000+0x00EE
	.word (NbIndepEntries+0x12)*0x10000+0x00EF
	.word (NbIndepEntries+0x13)*0x10000+0x00F0
	.word (NbIndepEntries+0x14)*0x10000+0x00E3
	.word (NbIndepEntries+0x8)*0x10000+0x00FA
.endarea


