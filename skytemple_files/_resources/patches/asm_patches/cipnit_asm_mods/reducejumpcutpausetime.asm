; Reduces the amount of time the game pauses for before changing the PoV when far-off pals is enabled, from 60 frames to 12. 
; https://www.pokecommunity.com/showthread.php?t=437108
; Build this file using armips: https://github.com/Kingcom/armips

.nds
.include "common/regionSelect.asm"

.open "overlay_0029.bin", ov_29

.org NA_022F9920
	cmp r0,0Ch	;original: cmp r0,3Ch

.close
