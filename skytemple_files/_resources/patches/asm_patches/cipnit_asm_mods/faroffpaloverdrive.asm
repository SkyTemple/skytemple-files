; In vanilla EoS, even with far-off pals enabled, the game will not cut to partners which are just barely off screen - so if you're in a hallway in a dark dungeon, you won't have any idea what's going on if you're just a couple tiles away from your partner, which is a huge problem in manual mode because the PoV is going to be on your last pokemon most of the time. This makes it so the game always cuts to pokemon which are getting attacked.
; Made by Cipnit
; https://www.pokecommunity.com/showthread.php?t=437108
; Build this file using armips: https://github.com/Kingcom/armips

.nds
.include "common/regionSelect.asm"

.open "overlay_0029.bin", ov_29

.org NA_022F989C
	nop		;original: popeq r3-r5,r15

.close
