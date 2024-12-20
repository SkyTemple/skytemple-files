.relativeinclude on
.nds
.arm

.definelabel SetPortraitEmotion, 0x204DB2C ; from pmdsky-debug
.definelabel AllowPortraitDefault, 0x204DBCC ; from pmdsky-debug
.definelabel HookPoint, 0x22C17CC ; location of SetPortraitEmotion in UpdateTeamStats
.definelabel UpdateCheck, 0x22C1728 ; location of tst r9,0x4. we need to change it to tst r9,0x5, so the portrait will update when hp changes as well.
.definelabel ReturnPoint, 0x22C17D0 ; after SetPortraitEmotion in UpdateTeamStats
