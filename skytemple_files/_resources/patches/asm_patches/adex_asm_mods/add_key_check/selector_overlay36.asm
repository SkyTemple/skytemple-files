.relativeinclude on

.if PPMD_GameVer == GameVer_EoS_NA
	.include "common/key_ov36.asm"
.elseif PPMD_GameVer == GameVer_EoS_EU
	.include "common/key_ov36.asm"
.elseif PPMD_GameVer == GameVer_EoS_JP
	.include "common/key_ov36.asm"
.endif

.relativeinclude off