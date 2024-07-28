; For use with ARMIPS
; 2024/07/27
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Use filestreams to partially load mappa files instead of loading entirely
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel MonsterFilePtr, 0x020B2228
.definelabel HookMdAccess7, 0x02052B1C
.definelabel HookMdAccess8, 0x02052B54