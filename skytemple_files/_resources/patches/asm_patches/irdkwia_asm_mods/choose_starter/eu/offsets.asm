; For use with ARMIPS
; 2021/03/23
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Adds a menu to choose the starter after the quiz
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel SpecialStringID, 0xA35

.definelabel OrgSize, 0x2E80
.definelabel ExtendSize, 0x1000
.definelabel OverlayStart, 0x0238AC80


.definelabel RandMax, 0x02002274

.definelabel MenuCreateOptionString, 0x020225EC

.definelabel ChangeBorderColor, 0x02027D74

.definelabel CreateNormalMenu, 0x0202B3E0
.definelabel FreeNormalMenu, 0x0202B7B8
.definelabel GetNormalMenuResult, 0x0202B870

.definelabel CreateAdvancedMenu, 0x0202BD14
.definelabel FreeAdvancedMenu, 0x0202BF38
.definelabel IsAdvancedMenuActive, 0x0202BFD0
.definelabel GetAdvancedMenuCurrentOption, 0x0202BFF0
.definelabel GetAdvancedMenuResult, 0x0202C004

.definelabel IsDBActive, 0x0202F474
.definelabel ShowMessageInDB, 0x0202F4A8
.definelabel ShowDB, 0x0202F698

.definelabel CreatePortraitBox, 0x0202F8A0
.definelabel ShowPortraitBox, 0x0202F984
.definelabel HidePortraitBox, 0x0202F9D0

.definelabel PrepDBUnk1, 0x020238B4

.definelabel UnknownFuncCase0, 0x0204A4D0

.definelabel SetPortraitPkmnID, 0x0204DB0C
.definelabel SetPortraitExpressionID, 0x0204DB2C
.definelabel SetPortraitUnknownAttr, 0x0204DB3C
.definelabel SetPortraitAttrStruct, 0x0204DB80


.definelabel BegSwitch, 0x0238B0E0
.definelabel EndSwitch, 0x0238B1F4

.definelabel case0_alt1, 0x0238B220
.definelabel case0_alt2, 0x0238B234

.definelabel HookEventSeq, 0x0238B908

.definelabel EndCodeSwitch, 0x0238C8B4

.definelabel WaitForNextStep, 0x0238C98C

.definelabel OldGetPersonalityResult, 0x0238C8E8

.definelabel BorderColorTable, 0x0238CB50
.definelabel PortraitAttrStruct, 0x0238CB54
.definelabel QuizMenu1, 0x0238CBB4
.definelabel PlayersListPkmnID, 0x0238CBF8
.definelabel MenuOptionString, 0x0238D9B0

.definelabel GlobalStructPointer, 0x0238D9E0
;0x2 = CurrentDialogueBoxID [0x1]
;0x3 = CurrentMenuID [0x1]
;0x5 = CurrentPortraitBoXID [0x1]
;0x20 = NextSwitchCase [0x4]
;0x30 = WaitingCase [0x4]
;0x5F = Gender [0x1]

.definelabel DBLayout5, 0x0238D9EC
.definelabel DBLayout6, 0x0238D9FC
