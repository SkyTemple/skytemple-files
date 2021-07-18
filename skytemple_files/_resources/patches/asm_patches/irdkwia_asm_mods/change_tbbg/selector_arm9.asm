; For use with ARMIPS
; 2021/03/23
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Selects the correct version to use
; ------------------------------------------------------------------------------

.relativeinclude on

; Selects the correct region to apply the patch
.if PPMD_GameVer == GameVer_EoS_NA
	.include "na/offsets.asm"
	.include "common/patch.asm"
.elseif PPMD_GameVer == GameVer_EoS_EU
	.include "eu/offsets.asm"
	.include "common/patch.asm"
.elseif PPMD_GameVer == GameVer_EoS_JP
	.include "jp/offsets.asm"
	.include "common/patch.asm"
.endif

.relativeinclude off
