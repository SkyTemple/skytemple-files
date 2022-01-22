; For use with ARMIPS
; 2021/03/09
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Edit Type Table Access
; ------------------------------------------------------------------------------

; For Gummies

.org 0x020118FC
.area 0x4
	mov  r2,#0x19 ; Now it's 25x25
.endarea
.org 0x02011908
.area 0xC
	ldrb r2,[r10, r3]
	ldrb r0,[r10, r1]
	nop
.endarea
