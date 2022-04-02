; For use with ARMIPS
; 2022/02/27
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Changes the way object attributes are loaded
; ------------------------------------------------------------------------------

; TODO: Change offsets

.relativeinclude on
.nds
.arm

.definelabel HookGetObjectData1, 0x022FBED4
.definelabel HookGetObjectData2, 0x022FC108
.definelabel HookGetObjectData3, 0x022FC2C0
.definelabel HookGetObjectData4, 0x022F6E78
.definelabel HookGetObjectData5, 0x022F6EF0

.definelabel ObjectData, 0x0231DE40
.definelabel SizeObjectData, 0x2A18
