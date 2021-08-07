; For use with ARMIPS
; 2021/08/07
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Change fixed floor properties functions
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel FixedRoomOffset, 0xDA

.definelabel FixedFloorProperties, 0x022C6C70

.definelabel IsBossFight, 0x022E0864
.definelabel IsFreeLayout, 0x022E03E4
.definelabel BranchFreeLayout, 0x022E0410

.definelabel IsFixedFloor, 0x023361D4

.definelabel HookIsNotFixedFloor, 0x0233A6B4
.definelabel BranchIsNotFixedFloor, 0x0233A6CC

.definelabel IsNotFixedFloor, 0x0233C310
.definelabel AreOrbsUsable, 0x023440AC
.definelabel IsWarpingAllowed, 0x023440DC
.definelabel IsTrawlingAllowed, 0x0234410C

.definelabel DungeonBaseStructurePtr, 0x02353538
