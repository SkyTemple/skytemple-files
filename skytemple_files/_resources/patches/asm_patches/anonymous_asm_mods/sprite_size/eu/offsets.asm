; For use with ARMIPS
; 2024/07/27
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Use filestreams to partially load mappa files instead of loading entirely
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel MonsterFilePtr, 0x020B12D0
.definelabel HookMdAccess7, 0x02052B1C
.definelabel HookMdAccess8, 0x02052B54