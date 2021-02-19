
 _REGION equ "US"
;_REGION equ "EU"


.relativeinclude on
.if _REGION == "US"
	.notice "Applying patch for rom region: USA"
.elseif _REGION == "EU"
	.notice "Applying patch for rom region: EUROPE"
.else
	.error "Invalid region specified"
.endif

.include "offsets" + _REGION + ".asm"

.relativeinclude off
