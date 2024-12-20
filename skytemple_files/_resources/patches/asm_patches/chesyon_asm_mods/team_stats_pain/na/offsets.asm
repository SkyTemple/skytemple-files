.relativeinclude on
.nds
.arm

.definelabel SetPortraitEmotion, 0x204D7F4 ; from pmdsky-debug
.definelabel AllowPortraitDefault, 0x204D894 ; from pmdsky-debug
.definelabel HookPoint, 0x22C0E8C ; location of SetPortraitEmotion in UpdateTeamStats
.definelabel UpdateCheck, 0x22C0DE8 ; location of tst r9,0x4. we need to change it to tst r9,0x5, so the portrait will update when hp changes as well.
.definelabel ReturnPoint, 0x22C0E90 ; after SetPortraitEmotion in UpdateTeamStats
