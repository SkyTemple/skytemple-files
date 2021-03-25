; For use with ARMIPS
; 2021/03/23
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Adds a menu to choose the starter after the quiz
; ------------------------------------------------------------------------------

; WARNING! Not tested!

.relativeinclude on
.nds
.arm

.definelabel SpecialStringID, 0xA35 ;Guess

.definelabel OrgSize, 0x2E80
.definelabel ExtendSize, 0x1000
.definelabel OverlayStart, 0x0238B6A0


.definelabel RandMax, 0x02002274

.definelabel MenuCreateOptionString, 0x02022440

.definelabel ChangeBorderColor, 0x02027DE0

.definelabel CreateNormalMenu, 0x0202B444
.definelabel FreeNormalMenu, 0x0202B81C
.definelabel GetNormalMenuResult, 0x0202B8D4

.definelabel CreateAdvancedMenu, 0x0202BD78
.definelabel FreeAdvancedMenu, 0x0202BF9C
.definelabel IsAdvancedMenuActive, 0x0202C034
.definelabel GetAdvancedMenuCurrentOption, 0x0202C054
.definelabel GetAdvancedMenuResult, 0x0202C068

.definelabel IsDBActive, 0x0202F4C4
.definelabel ShowMessageInDB, 0x0202F4F8
.definelabel ShowDB, 0x0202F6E8

.definelabel CreatePortraitBox, 0x0202F8F0
.definelabel ShowPortraitBox, 0x0202F9D4
.definelabel HidePortraitBox, 0x0202FA20

.definelabel PrepDBUnk1, 0x020236E0

.definelabel UnknownFuncCase0, 0x0204A500

.definelabel SetPortraitPkmnID, 0x0204DB34
.definelabel SetPortraitExpressionID, 0x0204DB54
.definelabel SetPortraitUnknownAttr, 0x0204DB64
.definelabel SetPortraitAttrStruct, 0x0204DBA8


.definelabel BegSwitch, 0x0238BB00
.definelabel EndSwitch, 0x0238BC14

.definelabel case0_alt1, 0x0238BC40
.definelabel case0_alt2, 0x0238BC54

.definelabel HookEventSeq, 0x0238C328

.definelabel EndCodeSwitch, 0x0238D2D8

.definelabel WaitForNextStep, 0x0238D3B0

.definelabel OldGetPersonalityResult, 0x0238D30C

.definelabel BorderColorTable, 0x0238D578
.definelabel PortraitAttrStruct, 0x0238D57C
.definelabel QuizMenu1, 0x0238D5DC
.definelabel PlayersListPkmnID, 0x0238D620
.definelabel MenuOptionString, 0x0238E3D8

.definelabel GlobalStructPointer, 0x0238E408
;0x2 = CurrentDialogueBoxID [0x1]
;0x3 = CurrentMenuID [0x1]
;0x5 = CurrentPortraitBoXID [0x1]
;0x20 = NextSwitchCase [0x4]
;0x30 = WaitingCase [0x4]
;0x5F = Gender [0x1]

.definelabel DBLayout5, 0x0238E414
.definelabel DBLayout6, 0x0238E424
