; For use with ARMIPS
; 2021/07/18
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel ConvertOverwoldToDungeonMoveset, 0x0201478C
.definelabel GetPPIncrease, 0x0201528C
.definelabel GetMovePPWithBonus, 0x02013AF8
.definelabel CommonPart, 0x02053628
.definelabel HookAssemblyRecruit1, 0x02053684
.definelabel HookAssemblyRecruit2, 0x02053750

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
.definelabel HookInterrupt5, 0x022E0BB0
.definelabel HookInterrupt6, 0x0234CD60

.definelabel FuncFadeOut1, 0x022EB85C
.definelabel FuncFadeOut2, 0x022DE740
.definelabel FuncStop1, 0x02017C0C
.definelabel FuncStop2, 0x02017C88

.definelabel DungeonBaseStructurePtr, 0x02354138
