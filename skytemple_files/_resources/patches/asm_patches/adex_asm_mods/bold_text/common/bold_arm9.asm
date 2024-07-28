.org NoBARFound
.area 0x4
	beq HookBLetter
.endarea

.org CallDisplayChar
.area 0x4
	bl RepeatRender
.endarea

.org ReturnCharWidth
.area 0x4
	bne TryIncreaseBoldCharWidth
.endarea