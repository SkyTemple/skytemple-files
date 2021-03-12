; For use with ARMIPS
; 2021/03/12
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Edit Type Table Access
; ------------------------------------------------------------------------------

; Fix Fairy type's mask, in the original game, it also removes Electric types.

.org 0x0238D6A8
.area 0x4
	.word 0x00020000
.endarea
