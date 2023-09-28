; For use with ARMIPS
; 2022/02/27 - Updated 2023/09/20
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Changes the way object attributes are loaded
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel HookGetObjectData1, 0x022FD54C
.definelabel HookGetObjectData2, 0x022FD780
.definelabel HookGetObjectData3, 0x022FD938
.definelabel HookGetObjectData4, 0x022F84FC
.definelabel HookGetObjectData5, 0x022F8574

.definelabel ObjectData, 0x0231F3A4
.definelabel SizeObjectData, 0x2A18
