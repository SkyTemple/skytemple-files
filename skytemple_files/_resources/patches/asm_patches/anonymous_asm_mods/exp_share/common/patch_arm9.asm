; For use with ARMIPS
; 2021/04/25
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Adds Exp. Share
; ------------------------------------------------------------------------------

.org HookSummary
.area 0x4
	b SummaryFunc
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

.org BuffRead
.area 0xC
	.fill 0x4, 0;
.endarea

