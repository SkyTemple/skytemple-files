; For use with ARMIPS
; 2021/01/30
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Selects the correct version to use
; ------------------------------------------------------------------------------

.relativeinclude on

; Selects the correct region to apply the patch
.if PPMD_GameVer == GameVer_EoS_NA
	.include "na/patch_overlay10.asm"
.elseif PPMD_GameVer == GameVer_EoS_EU
	.include "eu/patch_overlay10.asm"
.elseif PPMD_GameVer == GameVer_EoS_JP
	.include "jp/patch_overlay10.asm"
.endif

.relativeinclude off
