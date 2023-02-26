; For use with ARMIPS
; 2023/01/20
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Allows pushing allies in dungeons
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel ChangeString, 0x022E3418
.definelabel SetupAction, 0x022EBDB8
.definelabel HookPush1, 0x022F3034
.definelabel CheckMove, 0x022F30FC
.definelabel CheckEntityStatus, 0x022F3F98
.definelabel CheckEntityUnk1, 0x022FC4EC
.definelabel CheckAllowedMove, 0x02300384
.definelabel CheckMoveCorners, 0x02301A88
.definelabel CheckEntityUnk2, 0x02325084
.definelabel GetTile, 0x02336CCC
.definelabel SendMessageWithIDLog, 0x0234C098
.definelabel dungeon_main_ptr, 0x02354138
.definelabel direction_struct, 0x02352328
.definelabel ctrl_struct, 0x0237D294
