; For use with ARMIPS
; 2021/03/09
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Edit Type Table Access
; ------------------------------------------------------------------------------

; For Gummies

.org 0x0231E5D8
.area 0x4
	mov  r0,#0x19 ; Now it's 25x25
.endarea
.org 0x0231E5EC
.area 0x4
	mov  r0,r2
.endarea
.org 0x0231E5F4
.area 0x8
	ldrb r12,[r0, r12]
	ldrb r0,[r0, r11]
.endarea
.org 0x0231E60C
.area 0x4
	mov  r0,r2
.endarea
.org 0x0231E618
.area 0x8
	ldrb r2,[r0, r2]
	ldrb r0,[r0, r1]
.endarea

;For Matchups

.org 0x0230C25C
.area 0x4
	mov  r0,#0x19 ; Now it's 25x25
.endarea
.org 0x0230C26C
.area 0x8
	ldrb r0,[r1, +r0]
	nop
.endarea
