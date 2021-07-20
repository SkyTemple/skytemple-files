; For use with ARMIPS
; 2021/07/18
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

; TODO

.definelabel GetGameVarPos, 0x0204B678
.definelabel SetConquest, 0x0204CF38
.definelabel RefillTeam, 0x02057D58

.definelabel Ov10PatchZone, 0x022DBFB0-0xC00

.definelabel ContinueExecution, 0x022E00C8

.definelabel HookConquest, 0x022E8BC0

.definelabel HookInterrupt1, 0x022E00A8
.definelabel HookInterrupt2, 0x022E02CC
.definelabel HookInterrupt3, 0x022FD668
.definelabel DungeonBaseStructurePtr, 0x02353538
