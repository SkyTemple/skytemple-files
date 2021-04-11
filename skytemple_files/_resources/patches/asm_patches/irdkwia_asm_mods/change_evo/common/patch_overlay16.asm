; For use with ARMIPS
; 2021/04/10
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Change the evo system
; ------------------------------------------------------------------------------

.org EvoAddStats1
.area 0xE8
	ldr r1,=MainEvoMenuStruct
	ldr r3,[r1, #+0x0]
	ldr r0,[r3, #+0x3c]
	ldrsh r1,[r3, #+0xa]
	bl AddStats
	ldr r2,=MainEvoMenuStruct
	b end_evo_add_stats1
	.pool
	.fill (EvoAddStats1+0xE8-.), 0xCC
end_evo_add_stats1:
.endarea

.org EvoAddStats2
.area 0xE8
	ldr r1,=MainEvoMenuStruct
	ldr r3,[r1, #+0x0]
	ldr r0,[r3, #+0x3c]
	ldrsh r1,[r3, #+0xa]
	bl AddStats
	ldr r2,=MainEvoMenuStruct
	b end_evo_add_stats2
	.pool
	.fill (EvoAddStats2+0xE8-.), 0xCC
end_evo_add_stats2:
.endarea
