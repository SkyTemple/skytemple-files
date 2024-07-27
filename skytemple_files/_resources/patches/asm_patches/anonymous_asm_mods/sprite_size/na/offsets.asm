; For use with ARMIPS
; 2024/07/27
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Use filestreams to partially load mappa files instead of loading entirely
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel MonsterFilePtr, 0x020B09B4
.definelabel HookMdAccess7, 0x020527E4
.definelabel HookMdAccess8, 0x0205281C