; For use with ARMIPS
; 2023/01/20 - Updated 2023/09/24
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Allows pushing allies in dungeons
; ------------------------------------------------------------------------------

.relativeinclude on
.nds
.arm

.definelabel JP_OFFSET, 0x4

.definelabel ChangeString, 0x022E416C
.definelabel SetupAction, 0x022ECA70
.definelabel HookPush1, 0x022F3C78
.definelabel CheckMove, 0x022F3D40
.definelabel CheckEntityStatus, 0x022F4BD8
.definelabel CheckEntityUnk1, 0x022FCFC4
.definelabel CheckAllowedMove, 0x02300D28
.definelabel CheckMoveCorners, 0x02302400
.definelabel CheckEntityUnk2, 0x02325AAC
.definelabel GetTile, 0x023374CC
.definelabel SendMessageWithIDLog, 0x0234C708
.definelabel dungeon_main_ptr, 0x023547B8
.definelabel direction_struct, 0x0235299C
.definelabel ctrl_struct, 0x0237D914
