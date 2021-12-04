; For use with ARMIPS
; 2021/07/18
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel ConvertOverwoldToDungeonMoveset, 0x020146E4
.definelabel GetPPIncrease, 0x020151E4
.definelabel GetMovePPWithBonus, 0x02013A50
.definelabel CommonPart, 0x020532AC
.definelabel HookAssemblyRecruit1, 0x02053308
.definelabel HookAssemblyRecruit2, 0x020533D4

.definelabel HookMoveDisplay1, 0x0203FCC0
.definelabel GetGameVarPos, 0x0204B678
.definelabel SetConquest, 0x0204CF38
.definelabel RefillTeam, 0x02057D58
.definelabel UnknownFunc, 0x020585B4
.definelabel HookHPDisplay1, 0x0205AE6C
.definelabel HookHPDisplay2, 0x0205AF9C

.definelabel Ov10PatchZone, 0x022DBFB0-0xC00

.definelabel HookHPDisplay3, 0x022DC5FC
.definelabel ContinueExecution, 0x022E00C8

.definelabel HookConquest, 0x022E8BC0

.definelabel HookInterrupt1, 0x022E00A8
.definelabel HookInterrupt2, 0x022E02CC
.definelabel HookInterrupt3, 0x022FC8D4
.definelabel HookInterrupt4, 0x022FD668
.definelabel HookInterrupt5, 0x022E0270
.definelabel HookInterrupt6, 0x0234C160

.definelabel FuncFadeOut1, 0x022EAEAC
.definelabel FuncFadeOut2, 0x022DDE00
.definelabel FuncStop1, 0x02017B70
.definelabel FuncStop2, 0x02017BEC


.definelabel DungeonBaseStructurePtr, 0x02353538
