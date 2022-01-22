; For use with ARMIPS
; 2021/04/25
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Selects the correct version to use
; ------------------------------------------------------------------------------

.relativeinclude on

; Selects the correct region to apply the patch
.if PPMD_GameVer == GameVer_EoS_NA
	.include "na/offsets.asm"
	.include "na/patch_arm9.asm"
	.include "common/patch_arm9.asm"
.elseif PPMD_GameVer == GameVer_EoS_EU
	.include "eu/offsets.asm"
	.include "eu/patch_arm9.asm"
	.include "common/patch_arm9.asm"
.endif

.relativeinclude off
