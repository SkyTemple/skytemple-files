; For use with ARMIPS
; 2021/01/09
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Selects the correct version to use
; ------------------------------------------------------------------------------

.relativeinclude on

; Selects the correct region to apply the patch
.if PPMD_GameVer == GameVer_EoS_NA
	.include "na/change_arm9.asm"
.elseif PPMD_GameVer == GameVer_EoS_EU
	.include "eu/change_arm9.asm"
.endif

.relativeinclude off
