; For use with ARMIPS
; 2021/06/07
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Selects the correct version to use
; ------------------------------------------------------------------------------

.relativeinclude on

; Selects the correct region to apply the patch
.if PPMD_GameVer == GameVer_EoS_NA
	.include "common/patch_overlay11.asm"
.elseif PPMD_GameVer == GameVer_EoS_EU
	.include "common/patch_overlay11.asm"
.elseif PPMD_GameVer == GameVer_EoS_JP
	.include "common/patch_overlay11.asm"
.endif

.relativeinclude off
