; For use with ARMIPS
; 2024/08/04
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Makes Chimecho Assembly Menu Faster
; ------------------------------------------------------------------------------

; Make Leader
.org LD1
.area 0x4
	mov  r3,#0x0
.endarea

.org LD2
.area 0x8
	nop
	nop
.endarea

.org LD3
.area 0x10
	nop
	nop
	nop
	nop
.endarea

.org LD4
.area 0x4
	mov  r1,#0xC
.endarea

; Add to party
.org AP1
.area 0x4
	mov  r3,#0x0
.endarea

.org AP2
.area 0x4
	mov  r1,#0xC
.endarea


; Remove from party
.org RP1
.area 0x4
	mov  r3,#0x0
.endarea

.org RP2
.area 0x4
	nop
.endarea

.org RP3
.area 0xC
	nop
	nop
	nop
.endarea

.org RP4
.area 0x8
	nop
	nop
.endarea

.org RP5
.area 0x10
	nop
	nop
	nop
	nop
.endarea

.org RP6
.area 0x4
	mov  r1,#0xC
.endarea


; Remove permanently

.org DL1
.area 0x4
	mov  r0,#0xC
.endarea

.org DL2
.area 0x4
	moveq  r1,#0xC
.endarea