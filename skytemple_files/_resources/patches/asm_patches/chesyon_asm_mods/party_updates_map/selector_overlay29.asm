.relativeinclude on

.if PPMD_GameVer == GameVer_EoS_NA
	.include "na/offsets.asm"
	.include "common/map_overlay29.asm"
.elseif PPMD_GameVer == GameVer_EoS_EU
	.include "eu/offsets.asm"
	.include "common/map_overlay29.asm"
.elseif PPMD_GameVer == GameVer_EoS_JP
	.include "jp/offsets.asm"
	.include "common/map_overlay29.asm"
.endif

.relativeinclude off
