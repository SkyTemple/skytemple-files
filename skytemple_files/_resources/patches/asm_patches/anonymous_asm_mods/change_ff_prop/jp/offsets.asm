; For use with ARMIPS
; 2021/08/07
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Change fixed floor properties functions
; ------------------------------------------------------------------------------

; WARNING! Not Tested!

.relativeinclude on
.nds
.arm

.definelabel FixedRoomOffset, 0x36

.definelabel FixedFloorProperties, 0x022C8358

.definelabel IsBossFight, 0x022E1EF4
.definelabel IsFreeLayout, 0x022E1A7C
.definelabel BranchFreeLayout, 0x022E1AA8

.definelabel IsFixedFloor, 0x023375A4

.definelabel HookIsNotFixedFloor, 0x0233BA78
.definelabel BranchIsNotFixedFloor, 0x0233BA90

.definelabel IsNotFixedFloor, 0x0233D6D4
.definelabel AreOrbsUsable, 0x02345470
.definelabel IsWarpingAllowed, 0x023454A0
.definelabel IsTrawlingAllowed, 0x023454D0

.definelabel DungeonBaseStructurePtr, 0x023547B8
