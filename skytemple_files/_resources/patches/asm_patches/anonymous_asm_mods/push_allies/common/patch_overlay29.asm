; For use with ARMIPS
; 2023/01/20
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Allows pushing allies in dungeons
; ------------------------------------------------------------------------------

.org HookPush1
.area 0x4
	b HookPush
EndHookPush:
.endarea
