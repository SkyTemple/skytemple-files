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

.org HookPush2
.area 0x18
    mov  r0,#0x1
    mov  r1,#0x2
    nop
    nop
    nop
    nop
.endarea