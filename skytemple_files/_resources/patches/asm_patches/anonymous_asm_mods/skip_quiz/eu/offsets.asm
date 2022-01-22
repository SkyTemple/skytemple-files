; For use with ARMIPS
; 2021/03/23
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Adds a menu to choose the starter after the quiz
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel SetGameVariable, 0x0204BB58
.definelabel HookBeforeQuestions, 0x0238B240
.definelabel HookAfterQuestions, 0x0238B7BC
