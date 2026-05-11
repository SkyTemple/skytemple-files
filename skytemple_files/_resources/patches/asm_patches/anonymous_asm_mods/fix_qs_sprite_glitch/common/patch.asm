; For use with ARMIPS
; 2026/05/11
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Fixes the Sprite Glitch that happens when quicksaving and reloading
; ------------------------------------------------------------------------------

; Make Leader
.org FixLocation
.area 0x2C
	; Some optimizations that save 5 instructions
	add  r10,r13,#0x18
	mov  r9,r4
	mov  r8, STRUCT_SIZE
	ldr r1,[r13, #+0x14]
	str r1,[r7, #+0x8]
	str r1,[r7, #+0x4]
	; Save the VRAM table values, which have been recomputed earlier
	; to the structure that contains the quicksaved data
	; Otherwise those values would be overwritten by quicksaved data
	; leading to a mismatch
	; This takes 4 instructions
	add r2, r4, #0x100
	add r3, r10, #0x100
	ldrh r1, [r2,FIX_START-0x100]
	strh r1, [r3,FIX_START-0x100]
	; One extra
	nop
.endarea