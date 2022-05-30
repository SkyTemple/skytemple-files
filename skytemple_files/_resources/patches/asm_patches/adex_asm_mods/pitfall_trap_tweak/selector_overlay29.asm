.relativeinclude on

.if PPMD_GameVer == GameVer_EoS_NA
	.include "na/offsets.asm"
	.include "common/pitfall_ov29.asm"
.elseif PPMD_GameVer == GameVer_EoS_EU
	.include "eu/offsets.asm"
	.include "common/pitfall_ov29.asm"
.endif

.relativeinclude off
