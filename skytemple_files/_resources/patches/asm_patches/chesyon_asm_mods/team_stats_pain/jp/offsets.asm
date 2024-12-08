.relativeinclude on
.nds
.arm

.definelabel SetPortraitEmotion, 0x204DB54 ; from pmdsky-debug
.definelabel AllowPortraitDefault, 0x204DBF4 ; from pmdsky-debug
.definelabel HookPoint, 0x22C2634 ; location of SetPortraitEmotion in UpdateTeamStats
.definelabel UpdateCheck, 0x22C2590 ; location of tst r9,0x4. we need to change it to tst r9,0x5, so the portrait will update when hp changes as well.
.definelabel ReturnPoint, 0x22C2638 ; after SetPortraitEmotion in UpdateTeamStats
