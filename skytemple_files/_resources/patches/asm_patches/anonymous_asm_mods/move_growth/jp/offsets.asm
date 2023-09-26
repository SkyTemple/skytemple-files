; For use with ARMIPS
; 2021/06/07 - Updated 2023/09/23
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Use filestreams to load animation specs
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel JP_OFFSET, 0x4
.definelabel ENTITY_TABLE_OFFSET, 0xA84

.definelabel MoveStringIDStartL, 0xB
.definelabel MoveStringIDStartH, 0x1300

.definelabel HookGetPPOW1, 0x020137A4
.definelabel HookGetPPOW2, 0x020137E4
.definelabel HookGetPPOW3, 0x0203FF04
.definelabel HookGetPPOW4, 0x02040038
.definelabel HookGetPPOW5, 0x020419E4
.definelabel HookGetPPOW6, 0x0205815C
.definelabel HookGetPPOW7, 0x02058280

.definelabel FillWithZeros4BytesArray, 0x02003288
.definelabel IsLoadedOverlay, 0x02003ED0
.definelabel FGetSize, 0x02008244
.definelabel SPrintF, 0x0200D634

.definelabel HookProcessGinsengOW1, 0x020115FC
.definelabel HookProcessGinsengOW2, 0x02011674
.definelabel HookDisplayAccuracy1, 0x020243D8
.definelabel HookDisplayAccuracy2, 0x02024424
.definelabel HookDisplayPower1, 0x020244A0
.definelabel HookDisplayPower2, 0x020244DC

.definelabel PrintMoveString, 0x02013448
.definelabel MoveSPrintF, 0x02013728
.definelabel PrintMoveStringMore, 0x02013750
.definelabel GetMoveBasePower, 0x0201399C
.definelabel GetMoveAccuracy, 0x020139DC
.definelabel GetMovePPWithBonus, 0x02013A20
.definelabel GetMoveActualAccuracy, 0x02013B90
.definelabel GetMovePowerWithID, 0x02013B60

.definelabel Is2TurnsMove, 0x02014C34

.definelabel CopyMoveTo, 0x02014A1C
.definelabel CopyMoveFrom, 0x02014A54

.definelabel StrCpy, 0x02025150
.definelabel GetStringFromFile, 0x020258A4

.definelabel GetGameVar2, 0x0204B9D8

.definelabel CopyNBitsTo, 0x02050D0C
.definelabel CopyNBitsFrom, 0x02050D8C

.definelabel HookInitData, 0x02052F98
.definelabel HookClearData, 0x02052FB0

.definelabel UnknownDataFunc, 0x02055418

.definelabel OrgEndInit, 0x2056454
.definelabel DebugFunc, 0x02050D08

.definelabel HookWriteTo, 0x02059508
.definelabel HookReadFrom, 0x02059614

.definelabel StrCat, 0x02089A94
.definelabel EuclidianDivision, 0x0209018C

.definelabel MoveEmptyStruct, 0x0209905C
.definelabel MoveDispStrings, 0x020990D8

.definelabel PrintSpecialChar, 0x02099FC8

.definelabel MoveLevelPtr, 0x020A7190
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

.definelabel HookGetActualPower, 0x02303890
.definelabel HookGetActualAccuracy, 0x023250FC
.definelabel HookPP1, 0x022FC160
.definelabel HookPP2, 0x022FCDB0
.definelabel HookPP3, 0x02319130
.definelabel HookPP4, 0x02319264
.definelabel HookPP5, 0x0231938C
.definelabel HookPP6, 0x0231FEA0
.definelabel HookPP6_1, 0x022E1C00 ; The registers differ on this one--see patch_overlay29.asm for more details!
.definelabel HookPP6_2, 0x022FB030
.definelabel HookPP6_3, 0x022FC044
.definelabel HookPP6_6, 0x0231F8A8
.definelabel HookPP7, 0x0232E9B8
.definelabel HookPP8_1, 0x02349488
.definelabel HookPP8_2, 0x023494B0
.definelabel HookPP8_3, 0x023494C0
.definelabel HookPP8, 0x02349580

.definelabel HookSetMoveString1, 0x02322BCC
.definelabel HookSetMoveString2, 0x02322DB8
.definelabel HookSetMoveString3, 0x023239A0
.definelabel HookSetMoveString4, 0x02323B08
.definelabel HookSetMoveString5, 0x0232430C
.definelabel HookSetMoveString6, 0x023278EC
.definelabel HookSetMoveString7, 0x0232796C

.definelabel HookSetMovePoints1, 0x02333AC4
.definelabel HookSetMovePoints2, 0x02333C24

.definelabel HookProcessGinseng1, 0x0231E344
.definelabel HookProcessGinseng2, 0x0231E360
.definelabel HookProcessGinseng3, 0x0231E38C
.definelabel HookProcessGinseng4, 0x0231E400

.definelabel PrepareMoveString, 0x0234C2F4
.definelabel SendMessageWithIDLog, 0x0234C708

.definelabel UnknownSubFunction, 0x0232FC3C

.definelabel Ov10PatchZone, 0x022DD698-0x800

.definelabel DungeonBaseStructurePtr, 0x023547B8


.definelabel HookMenuPP1, 0x02389DF4
