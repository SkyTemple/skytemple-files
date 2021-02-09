; For use with ARMIPS
; 2021/02/09
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Adds Exp. Share
; ------------------------------------------------------------------------------

.definelabel GetSpecialEpisode, 0x0204C938
.definelabel PartyPkmnStructPtr, 0x020B0A48
.definelabel GetLvlStats, 0x0205379C
.definelabel HookSummary, 0x0205A588
.definelabel ExpShare, 0x02097E38
.definelabel ReadjustExpFunc, 0x02097E28
.definelabel SummaryFunc, 0x02097E1C

.definelabel ExpGainAll, 0x0230A7CC
.definelabel ReadjustExp, 0x023030B8
.definelabel HookLvlUp, 0x023027F8

;.definelabel BuffRead, 0x0 ; Add it if it is even implemented

.definelabel PartyPkmnNb, 0x22B
.definelabel MaxLvl, 0x64
.definelabel PartyPkmnSize, 0x44


.org HookSummary
.area 0x4
	b SummaryFunc
.endarea

.org ExpShare
.area 0x80 ; Haven't really checked the size
	; Remove this area if you want ExpShare to be enabled during
	; Special Episodes
	bl GetSpecialEpisode
	mvn  r1,#0x0
	cmp r0,r1 ; Check the special episode value
	bne end_loop
	; End of the area to remove
	ldr r6,=PartyPkmnStructPtr
	ldr r6,[r6, #+0x0]
	;ldr r11,=BuffRead
	ldr r11,=0x98967F ; 9999999
	ldr r4,=PartyPkmnNb
	mov r10, #0x0
loop_start: 
	ldrh r1,[r6,#+0x4]
	cmp r1,#0x0
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
	cmp r10,r4
	add r6,r6,PartyPkmnSize
	blt loop_start
end_loop:
	mov  r6,#0x1
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

