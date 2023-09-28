; For use with ARMIPS
; 2021/07/18
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel ConvertOverwoldToDungeonMoveset, 0x020146B4
.definelabel GetPPIncrease, 0x020151B4
.definelabel GetMovePPWithBonus, 0x02013A20
.definelabel CommonPart, 0x020535E4
.definelabel HookAssemblyRecruit1, 0x02053640
.definelabel HookAssemblyRecruit2, 0x0205370C

.definelabel HookMoveDisplay1, 0x0204004C
.definelabel GetGameVarPos, 0x0204B9D8
.definelabel SetConquest, 0x0204D298
.definelabel RefillTeam, 0x020580EC
.definelabel UnknownFunc, 0x020588B4
.definelabel HookHPDisplay1, 0x0205B164
.definelabel HookHPDisplay2, 0x0205B29C

.definelabel Ov10PatchZone, 0x022DD698-0xC00

.definelabel HookHPDisplay3, 0x022DDC9C
.definelabel ContinueExecution, 0x022E1760

.definelabel HookConquest, 0x022EA1F4

.definelabel HookInterrupt1, 0x022E1740
.definelabel HookInterrupt2, 0x022E1964
.definelabel HookInterrupt3, 0x022FDCC4
.definelabel HookInterrupt4, 0x022FEA58
.definelabel HookInterrupt5, 0x022E1908
.definelabel HookInterrupt6, 0x0234D3C4

.definelabel FuncFadeOut1, 0x022EC514
.definelabel FuncFadeOut2, 0x022DF4A0
.definelabel FuncStop1, 0x02017BC8
.definelabel FuncStop2, 0x02017C44

.definelabel DungeonBaseStructurePtr, 0x023547B8
