; For use with ARMIPS
; 2021/06/09
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Implements Move Growth
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel MoveStringIDStartL, 0xF0
.definelabel MoveStringIDStartH, 0x1F00

.definelabel HookGetPPOW1, 0x0201387C
.definelabel HookGetPPOW2, 0x020138BC
.definelabel HookGetPPOW3, 0x0203FE74
.definelabel HookGetPPOW4, 0x0203FFA8
.definelabel HookGetPPOW5, 0x02041974
.definelabel HookGetPPOW6, 0x02058144
.definelabel HookGetPPOW7, 0x020582FC

.definelabel FillWithZeros4BytesArray, 0x02003288
.definelabel IsLoadedOverlay, 0x02003ED0
.definelabel FGetSize, 0x02008244
.definelabel SPrintF, 0x0200D6BC

.definelabel HookProcessGinsengOW1, 0x020116D4
.definelabel HookProcessGinsengOW2, 0x0201174C
.definelabel HookDisplayAccuracy1, 0x020245E8
.definelabel HookDisplayAccuracy2, 0x02024634
.definelabel HookDisplayPower1, 0x020246B0
.definelabel HookDisplayPower2, 0x020246EC

.definelabel PrintMoveString, 0x02013520
.definelabel MoveSPrintF, 0x02013800
.definelabel PrintMoveStringMore, 0x02013828
.definelabel GetMoveBasePower, 0x02013A74
.definelabel GetMoveAccuracy, 0x02013AB4
.definelabel GetMovePPWithBonus, 0x02013AF8
.definelabel GetMoveActualAccuracy, 0x02013C38
.definelabel GetMovePowerWithID, 0x02013C90

.definelabel Is2TurnsMove, 0x02014D0C

.definelabel CopyMoveTo, 0x02014AF4
.definelabel CopyMoveFrom, 0x02014B2C

.definelabel StrCpy, 0x020253CC
.definelabel GetStringFromFile, 0x02025B90

.definelabel GetGameVar2, 0x0204B9B0

.definelabel CopyNBitsTo, 0x02050CF8
.definelabel CopyNBitsFrom, 0x02050D78

.definelabel HookInitData, 0x02052FDC
.definelabel HookClearData, 0x02052FF4

.definelabel UnknownDataFunc, 0x0205545C

.definelabel OrgEndInit, 0x02056434
.definelabel DebugFunc, 0x02050CF4

.definelabel HookWriteTo, 0x02059588
.definelabel HookReadFrom, 0x02059694

.definelabel StrCat, 0x02089B44
.definelabel EuclidianDivision, 0x0209023C

.definelabel MoveEmptyStruct, 0x020991AC
.definelabel MoveDispStrings, 0x02099228

.definelabel PrintSpecialChar, 0x0209A150

.definelabel MoveLevelPtr, 0x020A6624
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

.definelabel HookGetActualPower, 0x02302D6C
.definelabel HookGetActualAccuracy, 0x023246C4
.definelabel HookPP1, 0x022FB5E4
.definelabel HookPP2, 0x022FC2E8
.definelabel HookPP3, 0x023186C0
.definelabel HookPP4, 0x023187F4
.definelabel HookPP5, 0x0231891C
.definelabel HookPP6, 0x0231F45C
.definelabel HookPP6_1, 0x022E0EAC
.definelabel HookPP6_2, 0x022FA484
.definelabel HookPP6_3, 0x022FB4C8
.definelabel HookPP6_6, 0x0231EE64
.definelabel HookPP7, 0x0232DFE4
.definelabel HookPP8_1, 0x02348D00
.definelabel HookPP8_2, 0x02348D28
.definelabel HookPP8_3, 0x02348D38
.definelabel HookPP8, 0x02348DF8

.definelabel HookSetMoveString1, 0x02322188
.definelabel HookSetMoveString2, 0x02322374
.definelabel HookSetMoveString3, 0x02322F5C
.definelabel HookSetMoveString4, 0x023230C4
.definelabel HookSetMoveString5, 0x023238D4
.definelabel HookSetMoveString6, 0x02326EC8
.definelabel HookSetMoveString7, 0x02326F48

.definelabel HookSetMovePoints1, 0x02333110
.definelabel HookSetMovePoints2, 0x02333270

.definelabel HookProcessGinseng1, 0x0231D8E8
.definelabel HookProcessGinseng2, 0x0231D904
.definelabel HookProcessGinseng3, 0x0231D930
.definelabel HookProcessGinseng4, 0x0231D9A4

.definelabel PrepareMoveString, 0x0234BC84
.definelabel SendMessageWithIDLog, 0x0234C098

.definelabel UnknownSubFunction, 0x0232F280

.definelabel Ov10PatchZone, 0x022DC908-0x800

.definelabel DungeonBaseStructurePtr, 0x02354138

.definelabel HookMenuPP1, 0x023897A4
