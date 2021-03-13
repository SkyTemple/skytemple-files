; For use with ARMIPS
; 2021/03/09
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Edit Type Table Access
; ------------------------------------------------------------------------------

; For Gummies

.org 0x0231D110
.area 0x4
	mov  r0,#0x19 ; Now it's 25x25
.endarea
.org 0x0231D124
.area 0x4
	mov  r0,r2
.endarea
.org 0x0231D12C
.area 0x8
	ldrb r12,[r0, r12]
	ldrb r0,[r0, r11]
.endarea
.org 0x0231D144
.area 0x4
	mov  r0,r2
.endarea
.org 0x0231D150
.area 0x8
	ldrb r2,[r0, r2]
	ldrb r0,[r0, r1]
.endarea

;For Matchups

.org 0x0230ACE4
.area 0x4
	mov  r0,#0x19 ; Now it's 25x25
.endarea
.org 0x0230ACF4
.area 0x8
	ldrb r0,[r1, r0]
	nop
.endarea
