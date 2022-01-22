; For use with ARMIPS
; 2021/03/23
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Adds a menu to choose the starter after the quiz
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel SetGameVariable, 0x0204B820
.definelabel HookBeforeQuestions, 0x0238A700
.definelabel HookAfterQuestions, 0x0238AC7C
