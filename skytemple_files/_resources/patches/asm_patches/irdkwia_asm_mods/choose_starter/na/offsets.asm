; For use with ARMIPS
; 2021/03/23
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Adds a menu to choose the starter after the quiz
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel SpecialStringID, 0xA35

.definelabel OrgSize, 0x2E80
.definelabel ExtendSize, 0x1000
.definelabel OverlayStart, 0x0238A140


.definelabel RandMax, 0x02002274

.definelabel MenuCreateOptionString, 0x020223F0

.definelabel ChangeBorderColor, 0x02027A80

.definelabel CreateNormalMenu, 0x0202B0EC
.definelabel FreeNormalMenu, 0x0202B4C4
.definelabel GetNormalMenuResult, 0x0202B57C

.definelabel CreateAdvancedMenu, 0x0202BA20
.definelabel FreeAdvancedMenu, 0x0202BC44
.definelabel IsAdvancedMenuActive, 0x0202BCDC
.definelabel GetAdvancedMenuCurrentOption, 0x0202BCFC
.definelabel GetAdvancedMenuResult, 0x0202BD10

.definelabel IsDBActive, 0x0202F180
.definelabel ShowMessageInDB, 0x0202F1B4
.definelabel ShowDB, 0x0202F3A4

.definelabel CreatePortraitBox, 0x0202F5AC
.definelabel ShowPortraitBox, 0x0202F690
.definelabel HidePortraitBox, 0x0202F6DC

.definelabel PrepDBUnk1, 0x02023690

.definelabel UnknownFuncCase0, 0x0204A198

.definelabel SetPortraitPkmnID, 0x0204D7D4
.definelabel SetPortraitExpressionID, 0x0204D7F4
.definelabel SetPortraitUnknownAttr, 0x0204D804
.definelabel SetPortraitAttrStruct, 0x0204D848


.definelabel BegSwitch, 0x0238A5A0
.definelabel EndSwitch, 0x0238A6B4

.definelabel case0_alt1, 0x0238A6E0
.definelabel case0_alt2, 0x0238A6F4

.definelabel HookEventSeq, 0x0238ADC8

.definelabel EndCodeSwitch, 0x0238BD74

.definelabel WaitForNextStep, 0x0238BE4C

.definelabel OldGetPersonalityResult, 0x0238BDA8

.definelabel BorderColorTable, 0x0238C010
.definelabel PortraitAttrStruct, 0x0238C014
.definelabel QuizMenu1, 0x0238C074
.definelabel PlayersListPkmnID, 0x238C0B8
.definelabel MenuOptionString, 0x0238CE70

.definelabel GlobalStructPointer, 0x0238CEA0
;0x2 = CurrentDialogueBoxID [0x1]
;0x3 = CurrentMenuID [0x1]
;0x5 = CurrentPortraitBoXID [0x1]
;0x20 = NextSwitchCase [0x4]
;0x30 = WaitingCase [0x4]
;0x5F = Gender [0x1]

.definelabel DBLayout5, 0x0238CEAC
.definelabel DBLayout6, 0x0238CEBC
