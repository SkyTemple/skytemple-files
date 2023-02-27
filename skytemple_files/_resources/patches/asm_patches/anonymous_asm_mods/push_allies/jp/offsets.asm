; For use with ARMIPS
; 2023/01/20
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Allows pushing allies in dungeons
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

; TODO

.definelabel ChangeString, 0x022E2AD8
.definelabel SetupAction, 0x022EB408
.definelabel HookPush1, 0x022F2680
.definelabel CheckMove, 0x022F2748
.definelabel CheckEntityStatus, 0x022F35E0
.definelabel CheckEntityUnk1, 0x022FBAF0
.definelabel CheckAllowedMove, 0x022FF958
.definelabel CheckMoveCorners, 0x0230105C
.definelabel CheckEntityUnk2, 0x0232461C
.definelabel GetTile, 0x023360FC
.definelabel SendMessageWithIDLog, 0x0234B498
.definelabel dungeon_main_ptr, 0x02353538
.definelabel direction_struct, 0x0235171C
.definelabel ctrl_struct, 0x0237C694
