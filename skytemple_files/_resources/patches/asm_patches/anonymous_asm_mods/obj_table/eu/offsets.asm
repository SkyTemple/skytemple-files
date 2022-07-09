; For use with ARMIPS
; 2022/02/27
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Changes the way object attributes are loaded
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel HookGetObjectData1, 0x022FC874
.definelabel HookGetObjectData2, 0x022FCAA8
.definelabel HookGetObjectData3, 0x022FCC60
.definelabel HookGetObjectData4, 0x022F7818
.definelabel HookGetObjectData5, 0x022F7890

.definelabel ObjectData, 0x0231E820
.definelabel SizeObjectData, 0x2B68
