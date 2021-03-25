; For use with ARMIPS
; 2021/03/23
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Adds a menu to choose the starter after the quiz
; ------------------------------------------------------------------------------

; WARNING! Not tested!

.relativeinclude on
.nds
.arm

.definelabel SetGameVariable, 0x0204BB80
.definelabel HookBeforeQuestions, 0x0238BC60
.definelabel HookAfterQuestions, 0x0238C1DC
