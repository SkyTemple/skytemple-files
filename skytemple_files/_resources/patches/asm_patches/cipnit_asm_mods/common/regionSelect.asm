
 _REGION equ "US"
;_REGION equ "EU"
;_REGION equ "JP"


.relativeinclude on
.if _REGION == "US"
	.notice "Applying patch for rom region: USA"
.elseif _REGION == "EU"
	.notice "Applying patch for rom region: EUROPE"
.elseif _REGION == "JP"
	.notice "Applying patch for rom region: JAPAN"
.else
	.error "Invalid region specified"
.endif

.include "offsets" + _REGION + ".asm"

.relativeinclude off
