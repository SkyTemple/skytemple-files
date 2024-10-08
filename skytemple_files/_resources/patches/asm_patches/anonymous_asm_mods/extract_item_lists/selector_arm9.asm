; For use with ARMIPS
; 2021/01/27 - Updated 2023/09/13
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Selects the correct version to use
; ------------------------------------------------------------------------------

.relativeinclude on

; Selects the correct region to apply the patch
.if PPMD_GameVer == GameVer_EoS_NA
	.include "na/patch.asm"
.elseif PPMD_GameVer == GameVer_EoS_EU
	.include "eu/patch.asm"
.elseif PPMD_GameVer == GameVer_EoS_JP
	.include "jp/patch.asm"
.endif

.relativeinclude off
