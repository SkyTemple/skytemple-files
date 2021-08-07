; For use with ARMIPS
; 2021/08/07
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Change fixed floor properties functions
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel FixedRoomOffset, 0xDA

.definelabel FixedFloorProperties, 0x022C75C8

.definelabel IsBossFight, 0x022E11A4
.definelabel IsFreeLayout, 0x022E0D24
.definelabel BranchFreeLayout, 0x022E0D50

.definelabel IsFixedFloor, 0x02336DA4

.definelabel HookIsNotFixedFloor, 0x0233B298
.definelabel BranchIsNotFixedFloor, 0x0233B2B0

.definelabel IsNotFixedFloor, 0x0233CEF4
.definelabel AreOrbsUsable, 0x02344C90
.definelabel IsWarpingAllowed, 0x02344CC0
.definelabel IsTrawlingAllowed, 0x02344CF0

.definelabel DungeonBaseStructurePtr, 0x02354138
