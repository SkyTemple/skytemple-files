; For use with ARMIPS
; 2021/04/20
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Change the way stats are displayed
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

;.definelabel StartAccuracyPos, 0x45
;.definelabel StartPowerPos, 0x51
.definelabel StartAccuracyPos, StartGraphicPos
.definelabel StartPowerPos, StartAccuracyPos+12

.definelabel MoveDescStartID, 0x00003F9F
.definelabel MoveDescEndID, 0x000041CE
.definelabel SureShotID, 0x00003F9D
.definelabel NoDamageID, 0x00003F9E

.definelabel SPrintF, 0x0200D634
.definelabel GetMoveActualAccuracy, 0x02013B60
.definelabel GetMoveBasePowerWithID, 0x02013BB8
.definelabel SetStringAccuracy, 0x020243B0
.definelabel SetStringPower, 0x02024478
.definelabel StrCpyFromFile, 0x02025898
.definelabel StrCat, 0x02089A94
.definelabel EuclidianDivision, 0x0209018C
.definelabel PrintAttr, 0x02099FC8
.definelabel NullString, 0x0209A044
.definelabel SpecialCharString, 0x0209A078
