; For use with ARMIPS
; 2021/06/09
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------

;.org 0x020587D8
;.area 0x4
;	nop
;.endarea

;.org 0x020587F8
;.area 0x4
;	nop
;.endarea

.org HookHPDisplay1
.area 0x4
	ldrsh r0,[r8,#+0x10]
.endarea
.org HookHPDisplay2
.area 0x10
	ldr r1,[r9,#+0x28]
	cmp r1,r0
	movgt r1,r0
	nop
.endarea
.org HookMoveDisplay1
.area 0x4
	nop
.endarea

.org HookAssemblyRecruit1
.area 0x4
	b CheckMove
EndCheckMove:
.endarea

.org HookAssemblyRecruit2
.area 0xC8
	b CommonPart
CheckMove:
	bl ConvertOverwoldToDungeonMoveset
	ldrsh r0,[r6, #+0xc]
	add r1,r6,#0x4C
	bl GetPPIncrease
	stmdb r13!, {r4,r5,r6}
	add  r5,r6,#0x1C
	mov r6,r0
	mov r4,#0
loop_move:
	strh r6,[r5,#+0x2]
	mov r0,r5
	bl GetMovePPWithBonus
	strb r0,[r5,#+0x6]
	add r4,r4,#1
	add r5,r5,#8
	blt loop_move
	ldmia r13!, {r4,r5,r6}
	b EndCheckMove
	.fill (HookAssemblyRecruit2+0xC8-.), 0xCC
.endarea
