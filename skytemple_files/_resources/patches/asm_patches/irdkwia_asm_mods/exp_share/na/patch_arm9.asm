; For use with ARMIPS
; 2021/04/25
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Adds Exp. Share
; ------------------------------------------------------------------------------

.org ExpShare
.area 0x120 ; Haven't really checked the size
	; Remove this area if you want ExpShare to be enabled during
	; Special Episodes
	bl GetSpecialEpisode
	mvn  r1,#0x0
	cmp r0,r1 ; Check the special episode value
	bne end_loop
	; End of the area to remove
	
	; No Exp. Share if it's a level 1 or no exp. dungeon
	ldr r11,=DungeonDataStructPtr
	ldr r11,[r11,#+0x0]
	ldrb r11,[r11, #+0x748]
	mov r0,r11
	bl IsLevel1Dungeon
	cmp r0, #0x0
	bne end_loop
	mov r0,r11
	bl IsExpEnabledInDungeon
	cmp r0, #0x0
	beq end_loop
	
	; Add a percentage of exp shared
	; Constant at ExpShare + 0x3C
	mov r0, PercentageShared
	mul r0, r9, r0
	mov r1, MaxPercent
	bl EuclidianDivision
	movs r9, r0
	beq end_loop ; Directly go to the end if the result is 0
	
	ldr r6,=PartyPkmnStructPtr
	ldr r6,[r6, #+0x0]
	;ldr r11,=BuffRead
	ldr r11,=0x98967F ; 9999999
	ldr r4,=PartyPkmnNb
	mov r10, #0x0
loop_start: 
	ldrh r1,[r6,#+0x0]
	tst r1,#0x1
	beq cond_loop
	ldrb r2,[r6,#+0x1]
	cmp r2,MaxLvl
	beq cond_loop
	
	; Should check with the max level exp., but this is too slow for the game
	; 
	;mov r0,r11
	;mov r2,MaxLvl
	;bl GetLvlStats
	;ldr r1,[r11,#+0x0]
	
	ldr r0,[r6,#+0x10]
	add r0,r0,r9
	cmp r0,r11
	movgt r0,r11
	;cmp r0,r1
	;movgt r0,r1
	str r0,[r6,#+0x10]
cond_loop:
	add r10,r10,#0x1
	cmp r10,#2
	addeq r10,r10,#3
	addeq r6,r6,PartyPkmnSize*3
	cmp r10,r4
	add r6,r6,PartyPkmnSize
	blt loop_start
end_loop:
	mov  r6,#0x1
	b ExpGainAll+0x4
	.pool
AddMissingLevels:
	ldr r8, [r4,#0x10]
	ldrb r7, [r4,#0x1]
	mov r9,r7
	b cmp_loop_add_ml
beg_loop_add_ml:
	ldr r0,=BuffRead
	ldrsh r1, [r4,#0x4]
	add r2,r9,#1
	bl GetLvlStats
	ldr r0,=BuffRead
	ldr r1,[r0,#+0x0]
	cmp r1,r8
	bgt end_add_missing_lvls
	add r9,r9,#1
cmp_loop_add_ml:
	cmp r9,MaxLvl
	blt beg_loop_add_ml
end_add_missing_lvls:
	b return_add_missing_levels
	.pool
	.fill (ExpShare+0x120-.), 0xCC
.endarea
