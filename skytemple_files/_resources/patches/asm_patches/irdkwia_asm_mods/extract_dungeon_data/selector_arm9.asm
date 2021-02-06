; For use with ARMIPS
; 2021/01/30
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Selects the correct version to use
; ------------------------------------------------------------------------------

.relativeinclude on

; Selects the correct region to apply the patch
.if PPMD_GameVer == GameVer_EoS_NA
	.include "na/patch_floor_ranks.asm"
	.include "na/patch_forbidden_floors.asm"
	.include "na/patch_available_items.asm"
.elseif PPMD_GameVer == GameVer_EoS_EU
	.include "eu/patch_floor_ranks.asm"
	.include "eu/patch_forbidden_floors.asm"
	.include "eu/patch_available_items.asm"
.endif

.relativeinclude off
