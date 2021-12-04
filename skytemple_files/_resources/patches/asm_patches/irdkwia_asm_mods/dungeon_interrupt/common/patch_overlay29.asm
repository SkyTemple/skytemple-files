; For use with ARMIPS
; 2021/07/18
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------

.org HookInterrupt1
.area 0x4
	b CheckDungeonInterrupt
EndExecution:
.endarea

.org HookInterrupt2
.area 0x4
	bl CheckEndDungeon
.endarea

.org HookInterrupt3
.area 0x4
	bl ClearInterruption
.endarea

.org HookInterrupt4
.area 0x4
	bl FillIfNotInterrupted
.endarea

.org HookInterrupt5
.area 0x10
	b MusicFadeOut
	nop
	nop
	nop
EndMusicFadeOut:
.endarea

.org HookInterrupt6
.area 0x8
	b MusicInterrupt
	nop
EndMusicInterrupt:
.endarea
