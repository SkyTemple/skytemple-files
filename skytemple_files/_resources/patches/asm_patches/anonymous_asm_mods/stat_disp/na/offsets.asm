; For use with ARMIPS
; 2021/04/20
; For Explorers of Sky NA Only
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

.definelabel MoveDescStartID, 0x000027A2
.definelabel MoveDescEndID, 0x000029D1
.definelabel SureShotID, 0x000027A0
.definelabel NoDamageID, 0x000027A1

.definelabel SPrintF, 0x0200D634
.definelabel GetMoveActualAccuracy, 0x02013B90
.definelabel GetMoveBasePowerWithID, 0x02013BE8
.definelabel SetStringAccuracy, 0x02024360
.definelabel SetStringPower, 0x02024428
.definelabel StrCpyFromFile, 0x020258B8
.definelabel StrCat, 0x020897AC
.definelabel EuclidianDivision, 0x0208FEA4
.definelabel PrintAttr, 0x02099CD4
.definelabel NullString, 0x02099D50
.definelabel SpecialCharString, 0x02099D84
