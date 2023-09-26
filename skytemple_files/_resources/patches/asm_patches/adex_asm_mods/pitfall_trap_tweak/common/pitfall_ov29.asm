.org AdvanceFloor
.area 0x4
	bl FallenAndCantGetUp ; Was originally strb r1,[r0,6h]
.endarea

.org DisplayUiStart
.area 0x4
	b ShouldDisplayUi ; Was originally sub sp,sp,#0x44
.endarea

.org AfterFadeToBlack
.area 0x4
	bl ResetPitfallFlag ; Was originally mov r0,#0x2
.endarea
