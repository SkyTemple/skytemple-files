; For use with ARMIPS
; 2021/02/09
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Adds Exp. Share
; ------------------------------------------------------------------------------

.definelabel GetSpecialEpisode, 0x0204CC70
.definelabel PartyPkmnStructPtr, 0x020B138C
.definelabel IsLevel1Dungeon, 0x02051650
.definelabel IsExpEnabledInDungeon, 0x02051A54
.definelabel GetLvlStats, 0x02053B18
.definelabel HookSummary, 0x0205A904
.definelabel EuclidianDivision, 0x0209023C
.definelabel ExpShare, 0x020981F4
.definelabel ReadjustExpFunc, 0x020981E4
.definelabel SummaryFunc, 0x020981D8

.definelabel ExpGainAll, 0x0230B238
.definelabel ReadjustExp, 0x02303AE4
.definelabel HookLvlUp, 0x02303224

.definelabel DungeonDataStructPtr, 0x02354138

;.definelabel BuffRead, 0x0 ; Add it if it is even implemented

.definelabel PartyPkmnNb, 0x22B
.definelabel MaxLvl, 0x64
.definelabel PartyPkmnSize, 0x44
.definelabel PercentageShared, 0x64
.definelabel MaxPercent, 0x64


.org HookSummary
.area 0x4
	b SummaryFunc
.endarea

.org ExpShare
.area 0xC0 ; Haven't really checked the size
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
	mul r0, r5, r0
	mov r1, MaxPercent
	bl EuclidianDivision
	movs r5, r0
	beq end_loop ; Directly go to the end if the result is 0
	
	ldr r3,=PartyPkmnStructPtr
	ldr r3,[r3, #+0x0]
	;ldr r11,=BuffRead
	ldr r11,=0x98967F ; 9999999
	ldr r4,=PartyPkmnNb
	mov r7, #0x0
loop_start: 
	ldrh r1,[r3,#+0x4]
	cmp r1,#0x0
	beq cond_loop
	ldrb r2,[r3,#+0x1]
	cmp r2,MaxLvl
	beq cond_loop
	
	; Should check with the max level exp., but this is too slow for the game
	; 
	;mov r0,r11
	;mov r2,MaxLvl
	;bl GetLvlStats
	;ldr r1,[r11,#+0x0]
	
	ldr r0,[r3,#+0x10]
	add r0,r0,r5
	cmp r0,r11
	movgt r0,r11
	;cmp r0,r1
	;movgt r0,r1
	str r0,[r3,#+0x10]
cond_loop:
	add r7,r7,#0x1
	cmp r7,r4
	add r3,r3,PartyPkmnSize
	blt loop_start
end_loop:
	mov  r4,#0x1
	b ExpGainAll+0x4
	.pool
.endarea

.org ReadjustExpFunc
.area 0x10
	strb r5,[r7, #+0xa]
	; If we reach the max. level, readjust exp to match that level
	cmp r5,MaxLvl
	moveq r8,r0
	b ReadjustExp+0x4
.endarea

.org SummaryFunc
.area 0xC
	; Set 0 to next level value for display in the summary
	; if the current exp value is above the one for the next level
	subs  r0,r1,r0
	movlt r0, #0x0
	b HookSummary+0x4
.endarea

;.org BuffRead
;.area 0xC
;	.fill 0x4, 0;
;.endarea

