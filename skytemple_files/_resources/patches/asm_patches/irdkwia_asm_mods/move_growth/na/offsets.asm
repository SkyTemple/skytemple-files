; For use with ARMIPS
; 2021/06/09
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Implements Move Growth
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel MoveStringIDStartL, 0xEE
.definelabel MoveStringIDStartH, 0x1F00

.definelabel HookGetPPOW1, 0x020137D4
.definelabel HookGetPPOW2, 0x02013814
.definelabel HookGetPPOW3, 0x0203FB78
.definelabel HookGetPPOW4, 0x0203FCAC
.definelabel HookGetPPOW5, 0x02041678
.definelabel HookGetPPOW6, 0x02057DC8
.definelabel HookGetPPOW7, 0x02057F80

.definelabel FillWithZeros4BytesArray, 0x02003288
.definelabel IsLoadedOverlay, 0x02003ED0
.definelabel FGetSize, 0x02008244
.definelabel SPrintF, 0x0200D634

.definelabel HookProcessGinsengOW1, 0x0201162C
.definelabel HookProcessGinsengOW2, 0x020116A4
.definelabel HookDisplayAccuracy1, 0x02024388
.definelabel HookDisplayAccuracy2, 0x020243D4
.definelabel HookDisplayPower1, 0x02024450
.definelabel HookDisplayPower2, 0x0202448C

.definelabel PrintMoveString, 0x02013478
.definelabel MoveSPrintF, 0x02013758
.definelabel PrintMoveStringMore, 0x02013780
.definelabel GetMoveBasePower, 0x020139CC
.definelabel GetMoveAccuracy, 0x02013A0C
.definelabel GetMovePPWithBonus, 0x02013A50
.definelabel GetMoveActualAccuracy, 0x02013B90
.definelabel GetMovePowerWithID, 0x02013BE8

.definelabel Is2TurnsMove, 0x02014C64

.definelabel CopyMoveTo, 0x02014A4C
.definelabel CopyMoveFrom, 0x02014A84

.definelabel StrCpy, 0x02025100
.definelabel GetStringFromFile, 0x020258C4

.definelabel GetGameVar2, 0x0204B678

.definelabel CopyNBitsTo, 0x020509C0
.definelabel CopyNBitsFrom, 0x02050A40

.definelabel HookInitData, 0x02052C60
.definelabel HookClearData, 0x02052C78

.definelabel UnknownDataFunc, 0x020550E0

.definelabel OrgEndInit, 0x20560B8
.definelabel DebugFunc, 0x020509BC

.definelabel HookWriteTo, 0x0205920C
.definelabel HookReadFrom, 0x02059318

.definelabel StrCat, 0x020897AC
.definelabel EuclidianDivision, 0x0208FEA4

.definelabel MoveEmptyStruct, 0x02098D68
.definelabel MoveDispStrings, 0x02098DE4

.definelabel PrintSpecialChar, 0x02099CD4

.definelabel MoveLevelPtr, 0x020A5D84
.definelabel InitData, MoveLevelPtr-0x2C
.definelabel ClearData, InitData-0x20
.definelabel CopyMoveLevelTo, ClearData-0x44
.definelabel CopyMoveLevelFrom, CopyMoveLevelTo-0x44
.definelabel GetMoveLevelProxy, CopyMoveLevelFrom-0x2C
.definelabel GetMovePPProxy, GetMoveLevelProxy-0x2C
.definelabel ProxyExtendAccuracy, GetMovePPProxy-0x2C
.definelabel ProxyExtendPower, ProxyExtendAccuracy-0x2C
.definelabel IsLoadedFile, MoveLevelPtr+0x4
.definelabel MGrowFileStream, IsLoadedFile+0x4

.definelabel HookGetActualPower, 0x02302340
.definelabel HookGetActualAccuracy, 0x02323C5C
.definelabel HookPP1, 0x022FABD8
.definelabel HookPP2, 0x022FB8DC
.definelabel HookPP3, 0x02317C60
.definelabel HookPP4, 0x02317D94
.definelabel HookPP5, 0x02317EBC
.definelabel HookPP6, 0x0231E9F4
.definelabel HookPP6_1, 0x022E056C
.definelabel HookPP6_2, 0x022F9A78
.definelabel HookPP6_3, 0x022FAABC
.definelabel HookPP6_6, 0x0231E3FC
.definelabel HookPP7, 0x0232D574
.definelabel HookPP8_1, 0x02348100
.definelabel HookPP8_2, 0x02348128
.definelabel HookPP8_3, 0x02348138
.definelabel HookPP8, 0x023481F8

.definelabel HookSetMoveString1, 0x02321720
.definelabel HookSetMoveString2, 0x0232190C
.definelabel HookSetMoveString3, 0x023224F4
.definelabel HookSetMoveString4, 0x0232265C
.definelabel HookSetMoveString5, 0x02322E6C
.definelabel HookSetMoveString6, 0x02326460
.definelabel HookSetMoveString7, 0x023264E0

.definelabel HookSetMovePoints1, 0x023326D0
.definelabel HookSetMovePoints2, 0x02332830

.definelabel HookProcessGinseng1, 0x0231CE80
.definelabel HookProcessGinseng2, 0x0231CE9C
.definelabel HookProcessGinseng3, 0x0231CEC8
.definelabel HookProcessGinseng4, 0x0231CF3C

.definelabel PrepareMoveString, 0x0234B084
.definelabel SendMessageWithIDLog, 0x0234B498

.definelabel UnknownSubFunction, 0x0232E840

.definelabel Ov10PatchZone, 0x022DBFB0-0x800

.definelabel DungeonBaseStructurePtr, 0x02353538

.definelabel HookMenuPP1, 0x02388B80
