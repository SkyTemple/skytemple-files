; For use with ARMIPS
; 2026/05/11
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Fixes the Sprite Glitch that happens when quicksaving and reloading
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel FixLocation, 0x02386554

.definelabel STRUCT_SIZE, 0x24
.definelabel FIX_START, 0x17A