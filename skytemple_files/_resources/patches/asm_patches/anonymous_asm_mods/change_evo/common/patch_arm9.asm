; For use with ARMIPS
; 2021/04/10
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Change the evo system
; ------------------------------------------------------------------------------

.org GetEvolutions
.area 0x88
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r14}
	sub r13,r13,#0x14
	mov  r10,r0
	mov  r9,r1
	mov  r8,r2
	mov  r11,r3
	bl GetSpriteSize
	mov  r4,r0
	mov  r5,#0x0
	mov  r6,#0x0
	mov r0,r13
	mov r1,r10
	bl GetEvos
	str r0, [r13, #+0x10]
loop_get_evos:
	mov r0,r6,lsl #0x1
	ldr r7,[r13,r0]
	cmp r8,#0x0
	bne no_check_sprite_size
	mov  r0,r7
	bl GetSpriteSize
	cmp r4,r0
	bne end_loop_get_evos
no_check_sprite_size:
	cmp r11,#0x0
	cmpeq r7,#0x140
	movne  r0,r5,lsl #0x1
	strneh r7,[r9,r0]
	addne  r5,r5,#0x1
end_loop_get_evos:
	ldr r0,[r13, #+0x10]
	add  r6,r6,#0x1
	cmp r6,r0
	blt loop_get_evos
	mov  r0,r5
	add r13,r13,#0x14
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
.endarea

.org GetEvolutionPossibilities
.area 0x6F8
	stmdb  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r14}
	sub  r13,r13,#0x8
	mov  r9,r0
	mov  r8,r1
	mov  r5,#0x0
	strh r5,[r8, #+0x6]
	strh r5,[r8, #+0x8]
	add r0,r8,#0xA
	mov r1, #0x30
	bl FillWithZeros2BytesArray
	ldrsh r0,[r9, #+0x4]
	bl CanEvolve
	cmp r0,#0x0
	moveq  r0,#0x4
	streqh r0,[r8, #+0x6]
	beq return_evo_possibilities
	add r0,r8,#0xA
	ldrsh r1,[r9, #+0x4]
	bl GetEvos
	mov r5,r0
	cmp r5,#0x0
	moveq  r0,#0x4
	streqh r0,[r8, #+0x6]
	beq return_evo_possibilities
	mov  r7,#0x0
	b end_loop_check_cond
loop_check_cond:
	add  r0,r8,r7,lsl #0x1
	ldrsh r10,[r0, #+0xa]
	add  r0,r13,#0x0
	mov  r1,r10
	bl GetEvoParameters
	ldrh r0,[r13, #+0x2]
	mov  r4,#0x0
	cmp r0,#0x4
	addls  r15,r15,r0,lsl #0x2
	b main_no_req
	b main_no_req
	b main_lvl
	b main_iq
	b main_item
	b main_recruit
main_lvl:
	ldrb r1,[r9, #+0x1]
	ldrsh r0,[r13, #+0x4]
	cmp r1,r0
	ldrlth r0,[r8, #+0x6]
	movlt  r4,#0x1
	orrlt  r0,r0,#0x2
	strlth r0,[r8, #+0x6]
	b main_no_req
main_iq:
	ldrsh r1,[r9, #+0x8]
	ldrsh r0,[r13, #+0x4]
	cmp r1,r0
	ldrlth r0,[r8, #+0x6]
	movlt  r4,#0x1
	orrlt  r0,r0,#0x10
	strlth r0,[r8, #+0x6]
	b main_no_req
main_item:
	ldrsh r0,[r13, #+0x4]
	bl GetItemPosition
	cmp r0,#0x0
	ldrlth r0,[r8, #+0x6]
	movlt  r4,#0x1
	orrlt  r0,r0,#0x8
	strlth r0,[r8, #+0x6]
	ldrgesh r1,[r13, #+0x4]
	addge  r0,r8,r7,lsl #0x1
	strgeh r1,[r0, #+0x1a]
	b main_no_req
main_recruit:
	ldrsh r0,[r13, #+0x4]
	mov  r6,r4
	mov  r1,#1
	bl IsRecruited
	cmp r0,#0x0
	movne  r6,#0x1
	cmp r6,#0x0
	moveq  r4,#0x1
main_no_req:
	ldrh r0,[r13, #+0x6]
	cmp r0,#0xF
	addls  r15,r15,r0,lsl #0x2
	b add_none
	b add_none
	b add_link_cable
	b add_atk_g_def
	b add_atk_l_def
	b add_atk_e_def
	b add_sun_ribbon
	b add_lunar_ribbon
	b add_beauty_scarf
	b add_val_1
	b add_val_0
	b add_male
	b add_female
	b add_move_ancientpower
	b add_move_rollout
	b add_move_double_hit
	b add_move_mimic
add_move_ancientpower:
	mov  r6,#0x0
	mov  r4,#0x1
	mov  r1,r6
	mov  r0,#0x6
loop_move_ancientpower:
	mla  r3,r6,r0,r9
	ldrb r2,[r3, #+0x22]
	tst r2,#0x1
	beq end_loop_move_ancientpower
	ldrh r2,[r3, #+0x24]
	cmp r2,#0x5D
	moveq  r4,r1
end_loop_move_ancientpower:
	add  r6,r6,#0x1
	cmp r6,#0x4
	blt loop_move_ancientpower
	b add_none
add_move_rollout:
	mov  r6,#0x0
	mov  r4,#0x1
	mov  r1,r6
	mov  r0,#0x6
loop_move_rollout:
	mla  r3,r6,r0,r9
	ldrb r2,[r3, #+0x22]
	tst r2,#0x1
	beq end_loop_move_rollout
	ldrh r2,[r3, #+0x24]
	cmp r2,#0x69
	moveq  r4,r1
end_loop_move_rollout:
	add  r6,r6,#0x1
	cmp r6,#0x4
	blt loop_move_rollout
	b add_none
add_move_double_hit:
	mov  r0,#0x0
	ldr r1,=0x000001E7
	mov  r4,#0x1
	mov  r3,r0
	mov  r2,#0x6
loop_move_double_hit:
	mla  r11,r0,r2,r9
	ldrb r6,[r11, #+0x22]
	tst r6,#0x1
	beq end_loop_move_double_hit
	ldrh r6,[r11, #+0x24]
	cmp r6,r1
	moveq  r4,r3
end_loop_move_double_hit:
	add  r0,r0,#0x1
	cmp r0,#0x4
	blt loop_move_double_hit
	b add_none
add_move_mimic:
	mov  r0,#0x0
	ldr r1,=0x00000147
	mov  r4,#0x1
	mov  r3,r0
	mov  r2,#0x6
loop_move_mimic:
	mla  r11,r0,r2,r9
	ldrb r6,[r11, #+0x22]
	tst r6,#0x1
	beq end_loop_move_mimic
	ldrh r6,[r11, #+0x24]
	cmp r6,r1
	moveq  r4,r3
end_loop_move_mimic:
	add  r0,r0,#0x1
	cmp r0,#0x4
	blt loop_move_mimic
	b add_none
add_link_cable:
	mov  r0,#0x97
	bl GetItemPosition
	cmp r0,#0x0
	ldrlth r0,[r8, #+0x6]
	movge  r1,#0x97
	movlt  r4,#0x1
	orrlt  r0,r0,#0x8
	strlth r0,[r8, #+0x6]
	addge  r0,r8,r7,lsl #0x1
	strgeh r1,[r0, #+0x2a]
	b add_none
add_atk_g_def:
	ldrb r1,[r9, #+0xc]
	ldrb r0,[r9, #+0xe]
	cmp r1,r0
	movls  r4,#0x1
	b add_none
add_atk_l_def:
	ldrb r1,[r9, #+0xc]
	ldrb r0,[r9, #+0xe]
	cmp r1,r0
	movcs  r4,#0x1
	b add_none
add_atk_e_def:
	ldrb r1,[r9, #+0xc]
	ldrb r0,[r9, #+0xe]
	cmp r1,r0
	movne  r4,#0x1
	b add_none
add_sun_ribbon:
	mov  r0,#0x37
	bl GetItemPosition
	cmp r0,#0x0
	ldrlth r0,[r8, #+0x6]
	movge  r1,#0x37
	movlt  r4,#0x1
	orrlt  r0,r0,#0x8
	strlth r0,[r8, #+0x6]
	addge  r0,r8,r7,lsl #0x1
	strgeh r1,[r0, #+0x2a]
	b add_none
add_lunar_ribbon:
	mov  r0,#0x38
	bl GetItemPosition
	cmp r0,#0x0
	ldrlth r0,[r8, #+0x6]
	movge  r1,#0x38
	movlt  r4,#0x1
	orrlt  r0,r0,#0x8
	strlth r0,[r8, #+0x6]
	addge  r0,r8,r7,lsl #0x1
	strgeh r1,[r0, #+0x2a]
	b add_none
add_val_1:
	ldrb r0,[r8, #+0x4]
	tst r0,#0x1
	movne  r4,#0x1
	b add_none
add_val_0:
	ldrb r0,[r8, #+0x4]
	tst r0,#0x1
	moveq  r4,#0x1
	b add_none
add_beauty_scarf:
	mov  r0,#0x36
	bl GetItemPosition
	cmp r0,#0x0
	addge  r0,r8,r7,lsl #0x1
	movge  r1,#0x36
	movlt  r4,#0x1
	strgeh r1,[r0, #+0x2a]
	b add_none
add_male:
	ldrsh r0,[r9, #+0x4]
	bl GetGender
	cmp r0,#1
	movne  r4,#0x1
	b add_none
add_female:
	ldrsh r0,[r9, #+0x4]
	bl GetGender
	cmp r0,#2
	movne  r4,#0x1
add_none:
	cmp r4,#0x0
	ldreqh r0,[r8, #+0x6]
	movne  r1,#0x0
	orreq  r0,r0,#0x1
	streqh r0,[r8, #+0x6]
	addne  r0,r8,r7,lsl #0x1
	streqh r10,[r8, #+0x8]
	strneh r1,[r0, #+0xa]
	add  r7,r7,#0x1
end_loop_check_cond:
	cmp r7,r5
	blt loop_check_cond
return_evo_possibilities:
	add  r13,r13,#0x8
	ldmia  r13!,{r3,r4,r5,r6,r7,r8,r9,r10,r11,r15}
	.pool
CheckOpen:
	stmdb  r13!,{r14}
	ldr r1,=already_loaded
	ldrb r0, [r1]
	cmp r0,#0
	bne no_open
	mov r0, #1
	strb r0, [r1]
	ldr r0,=filestream
	bl FStreamCtor
	ldr r0,=filestream
	ldr r1,=filename
	bl FStreamFOpen
no_open:
	ldmia  r13!,{r15}
GetEvos:
	stmdb  r13!,{r4,r5,r14}
	mov r4,r0
	mov r5,r1
	bl FStreamAlloc
	bl CheckOpen
	mov r1,r5,lsl #0x5
	add r1,r1,#4
	ldr r0,=filestream
	mov r2, #0
	bl FStreamSeek
	ldr r0,=filestream
	mov r1,r4
	mov r2,#0x2
	bl FStreamRead
	ldrh r5,[r4]
	ldr r0,=filestream
	mov r1,r4
	mov r2,#0x10
	bl FStreamRead
	bl FStreamDealloc
	mov r0,r5
	ldmia  r13!,{r4,r5,r15}
	.pool
AddStats:
	stmdb  r13!,{r4,r5,r14}
	sub r13,r13,#0xC
	mov r4,r0 ; Pkmn Str
	mov r5,r1 ; Evo ID
	bl FStreamAlloc
	bl CheckOpen
	ldr r0,=filestream
	mov r1, #0
	mov r2, #0
	bl FStreamSeek
	ldr r0,=filestream
	mov r1,r13
	mov r2,#0x4
	bl FStreamRead
	ldr r1,[r13]
	ldr r0,=filestream
	mov r2,#0xA
	mla r1,r2,r5,r1
	mov r2,#0x0
	bl FStreamSeek
	ldr r0,=filestream
	mov r1,r13
	mov r2,#0xA
	bl FStreamRead
	bl FStreamDealloc
	;r13 contains the stat entries (0x2: HP, 0x2: Atk + 0x2: SpAtk + 0x2: Def + 0x2: SpDef)
	; HP Bonus
	ldrsh r0,[r4, #+0xa]
	ldrsh r1,[r13]
	add r0,r1,r0
	ldr r1,=0x3e7
	cmp r0,r1
	movgt r0,r1
	cmp r0,#1
	movlt r0,#1
	strh r0,[r4, #+0xa]
	mov r3,#0x0
stats_loop:
	add r2,r3,#0xC
	ldrb r0,[r4, r2]
	mov r1,r3,lsl #0x1
	add r1,r1,#0x2
	ldrsh r1,[r13, r1]
	add r0,r1,r0
	cmp r0,#0xFF
	movgt r0,#0xFF
	cmp r0,#1
	movlt r0,#1
	strb r0,[r4, r2]
	add r3,r3,#1
	cmp r3,#0x4
	blt stats_loop
	add r13,r13,#0xC
	ldmia  r13!,{r4,r5,r15}
	.pool
filename:
	.ascii "BALANCE/md_evo.bin"
	dcb 0
already_loaded:
	.byte 0x0
filestream:
	.fill 0x48, 0x0
	.fill (GetEvolutionPossibilities+0x6F8-.), 0xCC
.endarea
