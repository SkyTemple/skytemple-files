; For use with ARMIPS
; 2021/08/07
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Change fixed floor properties functions
; ------------------------------------------------------------------------------

.org AreOrbsUsable
.area 0x30
	mov  r1,#0xC
	mul  r1,r0,r1
	ldr r0,=FixedFloorProperties+0x7
	ldrb r0,[r0, +r1]
	bx r14
	.pool
	.fill (AreOrbsUsable+0x30-.),0xCC
.endarea

.org IsWarpingAllowed
.area 0x30
	mov  r1,#0xC
	mul  r1,r0,r1
	ldr r0,=FixedFloorProperties+0x8
	ldrb r0,[r0, +r1]
	bx r14
	.pool
	.fill (IsWarpingAllowed+0x30-.),0xCC
.endarea

.org IsTrawlingAllowed
.area 0x30
	mov  r1,#0xC
	mul  r1,r0,r1
	ldr r0,=FixedFloorProperties+0x9
	ldrb r0,[r0, +r1]
	bx r14
	.pool
GetAdditionalProperties:
	mov  r1,#0xC
	mul  r1,r0,r1
	ldr r0,=FixedFloorProperties+0xB
	ldrb r0,[r0, +r1]
	bx r14
	.pool
	.fill (IsTrawlingAllowed+0x30-.),0xCC
.endarea

;Is Not Fixed Floor [0x1,0xA5[
; Used to determine the layout
.org IsNotFixedFloor
.area 0x1C
	stmdb r13!,{r14}
	bl GetAdditionalProperties
	tst r0,#0x1
	moveq r0,#1
	movne r0,#0
	ldmia r13!,{r15}
	.word 0xCCCCCCCC
.endarea

;TODO: Is Fixed Floor
; Used for everything else
.org IsFixedFloor
.area 0x30
	stmdb r13!,{r14}
	ldr r0,=DungeonBaseStructurePtr
	ldr r0,[r0, #+0x0]
	add  r0,r0,#0x4000
	ldrb r0,[r0, FixedRoomOffset]
	bl GetAdditionalProperties
	tst r0,#0x1
	moveq r0,#0
	movne r0,#1
	ldmia r13!,{r15}
	.pool
	.word 0xCCCCCCCC
.endarea

.org HookIsNotFixedFloor
.area 0x10
	bl IsNotFixedFloor
	cmp r0,#0x1
	beq BranchIsNotFixedFloor
	nop
.endarea

; TODO: Is Boss Fight / 022E0880 [0x1,0x51[
; Used for: allowing chests, changing Blast Seed damage, setting up floor texture
; removing floor count, changing some move chances, preventing passing off moves
; preventing filling the ground in front, preventing Pickup, preventing start of floor abilities
.org IsBossFight
.area 0x1C
	stmdb r13!,{r14}
	bl GetAdditionalProperties
	tst r0,#0x2
	moveq r0,#0
	movne r0,#1
	ldmia r13!,{r15}
	.word 0xCCCCCCCC
.endarea

; TODO: Is Free Layout [0x1,0x6E]
.org IsFreeLayout
.area 0x20
	bl GetAdditionalProperties
	tst r0,#0x4
	bne BranchFreeLayout
	b IsFreeLayout+0x20
	.word 0xCCCCCCCC
	.word 0xCCCCCCCC
	.word 0xCCCCCCCC
	.word 0xCCCCCCCC
.endarea
