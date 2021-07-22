; For use with ARMIPS
; 2021/07/18
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel HookMoveDisplay1, 0x0203FFBC
.definelabel GetGameVarPos, 0x0204B9B0
.definelabel SetConquest, 0x0204D270
.definelabel RefillTeam, 0x020580D4
.definelabel UnknownFunc, 0x02058930
.definelabel HookHPDisplay1, 0x0205B1E8
.definelabel HookHPDisplay2, 0x0205B318

.definelabel Ov10PatchZone, 0x022DC908-0xC00

.definelabel HookHPDisplay3, 0x022DCF3C
.definelabel ContinueExecution, 0x022E0A08

.definelabel HookConquest, 0x022E9500

.definelabel HookInterrupt1, 0x022E09E8
.definelabel HookInterrupt2, 0x022E0C0C
.definelabel HookInterrupt3, 0x022FD2D0
.definelabel HookInterrupt4, 0x022FE064
.definelabel DungeonBaseStructurePtr, 0x02354138
