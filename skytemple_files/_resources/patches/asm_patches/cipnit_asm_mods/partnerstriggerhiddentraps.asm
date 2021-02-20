; In vanilla EoS, partners can't trigger hidden traps. This makes it possible for them to be triggered by partners. Recommended to balance the game, especially with the team control hack, but not recommended for mods which use pitfall traps - when a partner steps on one, it's removed from your party for the rest of the dungeon.
; Made by Cipnit
; https://www.pokecommunity.com/showthread.php?t=437108
; Build this file using armips: https://github.com/Kingcom/armips

.nds
.include "common/regionSelect.asm"

.open "overlay_0029.bin", ov_29

.org NA_0230579C
	mov r0,1h		;original: ldrb r0,[r4,20h]

.close
