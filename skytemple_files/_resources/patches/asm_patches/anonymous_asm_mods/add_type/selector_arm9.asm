; For use with ARMIPS
; 2021/01/30
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Selects the correct version to use
; ------------------------------------------------------------------------------

.relativeinclude on

; Patch parameter pain
.if FairyTypeMatchup == 0
	MATCHUP_BYTE equ 0x2
.elseif FairyTypeMatchup == 1
	MATCHUP_BYTE equ 0x8
.elseif FairyTypeMatchup == 2
	MATCHUP_BYTE equ 0x11
.endif
; Selects the correct region to apply the patch
.if PPMD_GameVer == GameVer_EoS_NA
	.include "na/patch_arm9.asm"
.elseif PPMD_GameVer == GameVer_EoS_EU
	.include "eu/patch_arm9.asm"
.elseif PPMD_GameVer == GameVer_EoS_JP
	.include "jp/patch_arm9.asm"
.endif

.relativeinclude off
