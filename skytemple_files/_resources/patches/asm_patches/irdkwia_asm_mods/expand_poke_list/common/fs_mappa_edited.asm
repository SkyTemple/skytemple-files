; For use with ARMIPS
; 2021/04/14
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Use filestreams to partially load mappa files instead of loading entirely
; ------------------------------------------------------------------------------

;0x3C - 0x44 = Moves
;0x50 - 0x98 = Filestream
;0x98 - 0xAC = Header
;0xAC - 0xC0 = Lists

.org LoadMappaFileAttributes
.area 0xA74
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r14}
	sub  r13,r13,#0xC0
	ldr r3,=DungeonBaseStructurePtr
	ldr r4,=DungeonAuxilaryStructurePtr
	ldr r9,[r3, #+0x0]
	ldr r7,[r4, #+0xc]
	ldr r8,[r4, #+0x8]
	add  r3,r9,#0x4A
	str r1,[r13, #+0x0]
	add  r4,r9,#0x348
	mov  r5,r0
	add  r1,r4,#0x400
	add  r0,r3,#0x700
	mov  r4,r2
	str r8,[r13, #+0x48]
	str r7,[r13, #+0x4c]
	bl TransformDungeonData
	ldrb r2,[r9, #+0x74a]
	add  r0,r9,#0x28000
	strb r2,[r0, #+0x6b0]
	ldrb r2,[r9, #+0x74b]
	strb r2,[r0, #+0x6b1]
	ldrb r0,[r9, #+0x748]
	bl GetNbPreviousFloors
	mov  r6,#0x0
	strh r0,[r9, #+0x20]
	strh r6,[r9, #+0x1e]
	ldrsh r2,[r9, #+0x20]
	ldrsh r0,[r9, #+0x1e]
	add  r0,r2,r0
	strh r0,[r3, #+0x22]
	str r6,[r13, #+0x28]
	bl FStreamAlloc
	add r0,r13,#0x50
	bl FStreamCtor
	ldr r0,[r9, #+0x7cc]
	cmp r0,#0x1
	ldreq r1,=TimeFilename
	beq load
	cmp r0,#0x2
	ldreq r1,=DarknessFilename
	ldrne r1,=SkyFilename
load:
	add r0,r13,#0x50
	bl FStreamFOpen
	bl FStreamDealloc
	add r0,r13,#0x50
	mov r1,#0x4
	add r2,r13,#0x98
	mov r3,#0x4
	bl ReadAt
	add r0,r13,#0x50
	ldr r1,[r13,#+0x98]
	add r2,r13,#0x98
	mov r3,#0x14
	bl ReadAt
	ldr r1,[r13,#+0x98] ; Header + 0x0
	add  r0,r9,#0x28000
	ldrb r3,[r0, #+0x6b0]
	ldrb r6,[r0, #+0x6b1]
	add r0,r13,#0x50
	add r1,r3,lsl #0x2
	add r2,r13,#0xAC
	mov r3,#0x4
	bl ReadAt
	mov  r3,#0x12
	add r0,r13,#0x50
	ldr r1,[r13,#+0xac]
	mla  r1,r6,r3,r1
	add r2,r13,#0xAC
	bl ReadAt
	ldrb r0,[r9, #+0x748]
	bl GetNbFloorsPlus1
	add  r1,r9,#0x2C000
	strb r0,[r1, #+0xaf4]
	ldrb r0,[r9, #+0x748]
	cmp r0,#0xAE
	moveq  r0,#0x1
	movne  r0,#0x0
	tst r0,#0xFF
	beq no_decrement
	bl UnknownMissionFunc
	cmp r0,#0x0
	bne no_decrement
	add  r0,r9,#0x2C000
	ldrb r1,[r0, #+0xaf4]
	sub  r1,r1,#0x1
	strb r1,[r0, #+0xaf4]
no_decrement: ;///////// Floor Attributes
	ldrsh r2,[r13,#+0xac] ; List + 0x0
	ldr r3,[r13,#+0x9c] ; Header + 0x4
	add  r1,r3,r2,lsl #0x5
	ldr r0,=0x000286B2
	add  r2,r9,r0
	mov  r3,#0x20
	add r0,r13,#0x50
	bl ReadAt
	;///////// End Floor Attributes
	;///////// Trap Attributes
	ldr r2,=0x000286CE
	ldr r3,=0x0002CB08
	ldrsh r7,[r9, r2]
	mov  r0,#0x0
	strh r7,[r9, r3]
	rsb  r8,r2,#0x55000
	add r0,r13,#0x50
	ldrsh r7,[r13,#+0xb0] ; List + 0x4
	ldr  r1,[r13,#+0xa8] ; header + 0x10
	add r1,r1,r7,lsl #0x2
	add r2,r9,r8
	add r2,r2,#2
	mov r3,#0x4
	bl ReadAt
	add r0,r13,#0x50
	add r1,r8,#2
	ldr r1,[r9,r1]
	add r2,r9,r8
	mov r3,#0x32
	bl ReadAt
	cmp r4,#0x0
	beq no_spec_process
	mov  r0,r5
	blx r4
	;///////// End Trap Attributes
no_spec_process:
	ldrsh r0,[r13,#+0xae] ; List + 0x2
	ldr r1,[r13,#+0xa4] ; Header + 0xc
	add r1,r1,r0,lsl #0x2
	add r0,r13,#0x50
	add r2,r13,#0x8
	mov r3,#0x4
	bl ReadAt
	ldr r6,[r13, #+0x8]
	cmp r5,#0x0
	bne quick_saved
	ldr r0,=DungeonAuxilaryStructurePtr
	mov  r4,#0x0
	ldrh r2,[r0, #+0x0]
	ldrh r1,[r0, #+0x2]
	mov  r0,r4
	mov  r8,r4
	str r4,[r13, #+0xc]
	str r4,[r13, #+0x4]
	strh r2,[r13, #+0x44]
	strh r1,[r13, #+0x46]
	mov  r11,#0x1
	bl UnknownFunc1
	bl UnknownFunc2
	str r0,[r13, #+0x10]
	ldr r3,=0x0000FFFF
	ldr r0,=0x0002C9EA
	mov  r5,r4
loop_init_store:
	add  r2,r9,r5,lsl #0x1
	strh r3,[r2, r0]
	add  r5,r5,#0x1
	cmp r5,#0x10
	blt loop_init_store
	bl IsItemForSpecialSpawnInBag
	cmp r0,#0x0
	movne  r0,#0x1
	strne r0,[r13, #+0x4]
	ldrb r0,[r9, #+0x748]
	bl IsDojoDungeon
	cmp r0,#0x0
	movne  r0,#0x1
	strne r0,[r13, #+0x4]
	ldr r0,=NbIndepEntries*2
	mov  r1,#0xF
	bl MemAlloc
	str r0,[r13, #+0x18]
	bl GetNbRecruited
	mov  r0,#0x100
	mov  r1,#0xF
	bl MemAlloc
	mov  r7,r0
	ldr r0,=0x00000229
	mov  r10,#0x0
	sub  r0,r0,#0xAA
	str r0,[r13, #+0x20]
	ldr r0,=0x00000229 
	rsb  r0,r0,#0x600
	str r0,[r13, #+0x24]
monster_loop:
	mov  r0,#0x0
	str r0,[r13, #+0x8]
	add r0,r13,#0x50
	add r1,r6,r10,lsl #0x3
	add r2,r13,#0x3C
	mov r3,#0x8
	bl ReadAt
	add r0,r13,#0x3C
	bl ModMonster
	movs r5,r0
	beq monster_entry_null
	ldr r1,=0x00000229
	cmp r5,r1
	streqh r10,[r13, #+0x44]
	beq end_monster_loop
	ldr r1,[r13, #+0x20]
	cmp r5,r1
	ldrne r1,[r13, #+0x24]
	cmpne r5,r1
	streqh r10,[r13, #+0x46]
	beq end_monster_loop
	bl CanMonsterSpawn
	cmp r0,#0x0
	addeq  r10,r10,#0x1
	beq monster_loop
	add  r0,r9,#0x28000
	ldrb r0,[r0, #+0x6c4]
	bl IsBossFight
	cmp r0,#0x0
	bne end_monster_loop
	mov  r0,r5
	bl IsSatisfyingScenarioConditionToSpawn
	cmp r0,#0x0
	beq end_monster_loop
	mov  r0,r5
	bl NeedItemToSpawn
	cmp r0,#0x0
	beq need_item
	mov  r1,r5
	add  r0,r9,#0x7D0
	bl IsInSpawnList
	cmp r0,#0x0
	ldreq r0,[r13, #+0x10]
	cmpeq r0,#0x0
	ldreq r0,[r13, #+0x18]
	moveq  r1,r5,lsl #0x1
	ldreqsh r0,[r0, r1]
	cmpeq r0,#0x0
	bne end_monster_loop
	ldr r0,[r13, #+0x4]
	cmp r0,#0x0
	beq end_monster_loop
	mov  r8,r5
	add r0,r13,#0x3C
	bl GetSpawnLevel
	and  r0,r0,#0xFF
	str r0,[r13, #+0xc]
	b end_monster_loop
need_item:
	mov  r0,#0x1
	str r0,[r13, #+0x8]
end_monster_loop:
	ldr r0,[r13, #+0x8] ; Need Item to spawn
	cmp r0,#0x0
	strne r10,[r7,+r4, lsl #0x2]
	addne  r4,r4,#0x1
	add  r10,r10,#0x1
	b monster_loop
monster_entry_null:
	add  r0,r9,#0x700
	strh r8,[r0, #+0xa8]
	mov  r0,#0x10
	ldr r1,[r13, #+0xc]
	strb r1,[r9, #+0x7aa]
	bl RandMax
	add  r0,r0,#0x1
	str r0,[r13, #+0x14]
	sub  r0,r4,#0x1
	mov  r10,#0x0
	str r0,[r13, #+0x1c]
	b end_special_pkmn_loop
special_pkmn_loop:
	mov  r5,#0x0
	b end_special_pkmn_inner_loop
special_pkmn_inner_loop:
	mov  r0,r4
	bl RandMax
	ldr r2,[r7,+r5, lsl #0x2]
	ldr r1,[r7,+r0, lsl #0x2]
	str r1,[r7,+r5, lsl #0x2]
	str r2,[r7,+r0, lsl #0x2]
	add  r5,r5,#0x1
end_special_pkmn_inner_loop:
	ldr r0,[r13, #+0x1c]
	cmp r5,r0
	blt special_pkmn_inner_loop
	add  r10,r10,#0x1
end_special_pkmn_loop:
	ldr r0,[r13, #+0x14]
	cmp r10,r0
	blt special_pkmn_loop
	ldr r0,[r13, #+0x0]
	cmp r0,#0x0
	movne  r4,#0x0
	bne no_special_spawn
	cmp r4,#0xE
	movge  r4,#0xE
no_special_spawn:
	ldr r0,=0x00000229
	bl GetSpriteFileSize
	add  r5,r0,#0x0
	ldr r0,=0x0000017F
	bl GetSpriteFileSize
	ldr r1,[r13, #+0x10]
	add  r5,r5,r0
	cmp r1,#0x0
	beq special_file_size
	bl UnknownGetSize
	add  r5,r5,r0
	b no_compute_special_pokemon_size
special_file_size:
	cmp r8,#0x0
	beq no_compute_special_pokemon_size
	mov  r0,r8
	bl GetSpriteFileSize
	add  r5,r5,r0
no_compute_special_pokemon_size:
	mov  r8,#0x0
	b end_compute_file_size_loop
compute_file_size_loop:
	ldr r2,[r7,+r8, lsl #0x2]
	add  r1,r9,r8,lsl #0x1
	ldr r0,=0x0002C9EA
	strh r2,[r1, r0]
	ldr r0,[r7,+r8, lsl #0x2]
	add r1,r6,r0,lsl #0x3
	add r0,r13,#0x50
	add r2,r13,#0x3C
	mov r3,#0x8
	bl ReadAt
	add  r0,r13,#0x3C
	bl ModMonster
	mov  r10,r0
	add  r0,r13,#0x3C
	bl GetSpawnLevel
	cmp r11,r0
	movlt  r11,r0
	mov  r0,r10
	bl GetTotalSpriteFileSize
	add  r5,r5,r0
	add  r8,r8,#0x1
end_compute_file_size_loop:
	cmp r8,r4
	blt compute_file_size_loop
	ldr r1,=0x0002C9E6
	cmp r5,#0x58000
	strh r11,[r9, r1]
	bls total_file_size_ok
	sub  r10,r4,#0x1
	mov  r8,#0x0
	add  r11,r1,#0x4
	b end_reduce_total_file_size_loop
reduce_total_file_size_loop:
	ldr r0,[r7,+r10, lsl #0x2]
	add r1,r6,r0,lsl #0x3
	add r0,r13,#0x50
	add r2,r13,#0x34
	mov r3,#0x8
	bl ReadAt
	add  r0,r13,#0x34
	bl ModMonster
	bl GetTotalSpriteFileSize
	sub  r5,r5,r0
	ldr r0,=0x0000FFFF
	cmp r5,#0x58000
	add  r1,r9,r10,lsl #0x1
	strh r0,[r1, r11]
	add  r8,r8,#0x1
	bcc total_file_size_reduced
	sub  r10,r10,#0x1
end_reduce_total_file_size_loop:
	cmp r10,#0x0
	bge reduce_total_file_size_loop
total_file_size_reduced:
	sub  r4,r4,r8
total_file_size_ok:
	ldrh r2,[r13, #+0x44]
	ldr r0,=0x0000FFFF
	cmp r2,r0
	beq no_statue
	ldr r0,=0x0002C9EA
	add  r1,r9,r4,lsl #0x1
	strh r2,[r1, r0]
	add  r4,r4,#0x1
no_statue:
	ldrh r2,[r13, #+0x46]
	ldr r0,=0x0000FFFF
	cmp r2,r0
	ldrne r0,=0x0002C9EA
	addne  r1,r9,r4,lsl #0x1
	strneh r2,[r1, r0]
	ldr r2,=0x0002C9EA
	mov  r1,#0x0
loop_sort_pkmn_id:
	mov  r0,r1
	b end_inner_loop_sort_pkmn_id
inner_loop_sort_pkmn_id:
	add  r5,r9,r0,lsl #0x1
	add  r4,r9,r1,lsl #0x1
	ldrh r8,[r5, r2]
	ldrh r5,[r4, r2]
	cmp r5,r8
	strhih r8,[r4, r2]
	addhi  r4,r9,r0,lsl #0x1
	strhih r5,[r4, r2]
	add  r0,r0,#0x1
end_inner_loop_sort_pkmn_id:
	cmp r0,#0x10
	blt inner_loop_sort_pkmn_id
	add  r1,r1,#0x1
	cmp r1,#0xF
	blt loop_sort_pkmn_id
	ldr r0,[r13, #+0x18]
	bl MemFree
	mov  r0,r7
	bl MemFree
	bl UnknownFunc3
quick_saved:
	mov  r5,#0x0
	ldrb r0,[r9, #+0x748]
	mov  r8,r5
	bl UnknownFunc4
	cmp r0,#0x0
	beq label_46
	mov  r0,#0xB
	bl UnknownFunc5
	cmp r0,#0x0
	bne label_45
	mov  r0,#0xA
	bl UnknownFunc5
	cmp r0,#0x0
	beq label_46
label_45:
	mov  r5,#0x1
label_46:
	mov  r10,#0x0
	b end_copy_spawn_entry_loop
copy_spawn_entry_loop:
	ldr r0,=0x0002C9EA
	ldr r1,=0x0000FFFF
	add  r2,r9,r10,lsl #0x1
	ldrh r3,[r2, r0]
	cmp r3,r1
	beq break_copy_spawn_entry
	add r1,r6,r3,lsl #0x3
	add r0,r13,#0x50
	add r2,r13,#0x2C
	mov r3,#0x8
	bl ReadAt
	add  r0,r13,#0x2C
	bl ModMonster
	ldr r2,=0x00000229
	cmp r0,r2
	beq no_kecleon
	sub  r1,r2,#0xAA
	cmp r0,r1
	beq kecleon
	rsb  r1,r2,#0x600
	cmp r0,r1
	beq kecleon
	cmp r5,#0x0
	bne no_copy_spawn_entry
	b no_kecleon
kecleon:
	bl SetKecleonEntryForFloor
no_kecleon:
	add  r7,r13,#0x2C
	mov  r2,#0x4
	add  r1,r9,r8,lsl #0x3
	add  r1,r1,#0x164
	add  r3,r1,#0x2C800
copy_monster_spawn_loop:
	ldrh r1,[r7],#+0x2
	subs r2,r2,#0x1
	strh r1,[r3],#+0x2
	bne copy_monster_spawn_loop
	add  r8,r8,#0x1
no_copy_spawn_entry:
	add  r10,r10,#0x1
end_copy_spawn_entry_loop:
	cmp r10,#0x10
	blt copy_spawn_entry_loop
break_copy_spawn_entry:
	bl IsFixedFloor
	cmp r0,#0x0
	beq no_fixed_floor
	ldr r3,=0x0002C9E6
	rsb  r1,r8,#0x10
	add  r2,r9,#0x4000
	add  r0,r9,#0x164
	add  r0,r0,#0x2C800
	ldrb r2,[r2, #+0xda]
	ldrsh r3,[r9, r3]
	add  r0,r0,r8,lsl #0x3
	bl UnknownFunc6
	add  r1,r9,#0x12000
	str r0,[r1, #+0xb20]
	add  r0,r9,#0x12000
	ldr r0,[r0, #+0xb20]
	add  r8,r8,r0
no_fixed_floor:
	ldr r0,=0x0002C9E4
	mov  r5,#0x0
	strh r8,[r9, r0]
	b end_nullify_spawn_entry_loop
nullify_spawn_entry_loop:
	mov  r1,r5
	add  r0,r9,#0x164
	add  r0,r0,#0x2C800
	add  r0,r0,r8,lsl #0x3
	bl StoreMonsterID
	add  r8,r8,#0x1
end_nullify_spawn_entry_loop:
	cmp r8,#0x10
	blt nullify_spawn_entry_loop
	mov  r0,#0xB10
	mov  r1,#0x0
	bl MemAlloc
	mov r6,r0
	ldr r1,=0x0002C9E8
	mov  r4,#0x0
	strh r4,[r9, r1]
all_item_lists_loop:
	; //////// Handle Item lists
	add  r1,r13,r4,lsl #0x1
	ldrsh r2,[r1, #+0xb2] ; List + 0x6 + ???
	ldr r5,[r13,#+0xa0] ; Header + 0x8
	add r1,r5,r2,lsl #0x2
	add r0,r13,#0x50
	add r2,r13,#0x2C
	mov r3,#0x4
	bl ReadAt
	bl FStreamAlloc
	add r0,r13,#0x50
	ldr r1,[r13,#+0x2c]
	mov r2,#0
	bl FStreamSeek
	mov  r1,#0x0
	ldr r5,=0xFFFF8AD0
	mov  r8,r1
	mov  r10,r1
	rsb  r7,r5,#0x0
	b end_item_load_loop
item_load_loop:
	add r0,r13,#0x50
	add r1,r13,#0x2C
	mov r2,#2
	bl FStreamRead
	ldrh r11,[r13,#+0x2c]
	cmp r11,r5,lsr #0x10
	moveq  r0,r8,lsl #0x1
	streqh r11,[r6, r0]
	addeq  r8,r8,#0x1
	beq end_item_load_loop
	cmp r11,r7
	bcc single_value_item
	add  r11,r11,r5
	b end_multiple_zeros_item_loop
multiple_zeros_item_loop:
	mov  r0,r8,lsl #0x1
	strh r10,[r6, r0]
	add  r8,r8,#0x1
	sub  r11,r11,#0x1
end_multiple_zeros_item_loop:
	cmp r11,#0x0
	bne multiple_zeros_item_loop
	b end_item_load_loop
single_value_item:
	mov  r0,r8,lsl #0x1
	strh r11,[r6, r0]
	add  r8,r8,#0x1
end_item_load_loop:
	cmp r8,#0x17C
	blt item_load_loop
	; ////////// End Handle Item Lists
	bl FStreamDealloc
	mov  r1,#0xB10
	mul  r1,r4,r1
	mov  r2,#0x0
	ldr r5,=0x000286D2
	mov  r3,r2
loop_copy_item_cat_chances:
	mov  r10,r2,lsl #0x1
	ldrh r10,[r6, r10]
	add  r8,r1,r9
	add  r8,r8,r2,lsl #0x1
	add  r3,r3,#0x1
	strh r10,[r8, r5]
	cmp r3,#0x10
	add  r2,r2,#0x1
	blt loop_copy_item_cat_chances
	ldr r5,=0x000286F2
	mov  r3,#0x0
loop_copy_item_chances:
	mov  r10,r2,lsl #0x1
	ldrh r10,[r6, r10]
	add  r8,r1,r9
	add  r8,r8,r3,lsl #0x1
	add  r3,r3,#0x1
	strh r10,[r8, r5]
	cmp r3,#0x16C
	add  r2,r2,#0x1
	blt loop_copy_item_chances
	add  r4,r4,#0x1
	cmp r4,#0x6
	blt all_item_lists_loop
	mov  r8,#0x0
	ldr r2,=0x000286F2
	ldr r1,=0x0002C9E8
	ldr r3,=0x0000FFFF
	mov  r0,r8
loop_copy_normal_item_chances:
	add  r7,r9,r8,lsl #0x1
	ldrh r5,[r7, r2]
	cmp r5,r3
	streqh r0,[r7, r2]
	streqh r8,[r9, r1]
	add  r8,r8,#0x1
	cmp r8,#0x16C
	blt loop_copy_normal_item_chances
	mov r0,r6
	bl MemFree
	bl FStreamAlloc
	add r0,r13,#0x50
	bl FStreamClose
	bl FStreamDealloc
	add  r13,r13,#0xC0
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
	.pool
ReadAt: ;ReadAt(r0: fstream, r1: start, r2: buffer, r3: offset)
	stmdb  r13!,{r4,r5,r6,r7,r14}
	mov r4,r0
	mov r7,r1
	mov r5,r2
	mov r6,r3
	bl FStreamAlloc
	mov r0,r4
	mov r1,r7
	mov r2,#0
	bl FStreamSeek
	mov r0,r4
	mov r1,r5
	mov r2,r6
	bl FStreamRead
	bl FStreamDealloc
	ldmia  r13!,{r4,r5,r6,r7,r15}
	.fill (LoadMappaFileAttributes+0xA74-.), 0xCC
.endarea
