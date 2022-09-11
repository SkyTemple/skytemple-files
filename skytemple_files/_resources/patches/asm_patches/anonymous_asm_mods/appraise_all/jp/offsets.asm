; For use with ARMIPS
; 2022/09/10
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Adds a menu to appraise all items
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

; TODO

.definelabel IsThrowable, 0x0200CB10

.definelabel CreateItem, 0x0200D0A0

.definelabel PrintItem, 0x0200D670

.definelabel GetItemCategory, 0x0200E808

.definelabel GetGold, 0x0200ECFC
.definelabel AddGold, 0x0200ED58

.definelabel GetNbItemsInBag, 0x0200EDFC

.definelabel RemoveItemByIDAndStackNoHole, 0x0200F4D4
.definelabel AddItemToBagNoHeld, 0x0200F874

.definelabel PlaySE, 0x02017C80

.definelabel CreateNormalMenu, 0x0202B0EC
.definelabel GetNormalMenuResult, 0x0202B57C
.definelabel ShowMessageInDB, 0x0202F1B4
.definelabel CreateGoldStrMenu, 0x0202F8C4

.definelabel ItemBagStruct, 0x020AF6B8

.definelabel UnkFunc1, 0x022DC504

.definelabel GetNbAppraisableItems, 0x0230B724

.definelabel HookMenu, 0x0238B0E8
.definelabel HookSwitchMain, 0x0238A158
.definelabel HookMenuChoice, 0x0238A494
.definelabel HookSwitchSub, 0x0238A6B8

.definelabel ReturnDefaultHandler, 0x0238A63C
.definelabel ReturnEndHandler, 0x0238A674

.definelabel TriggerSubHandler, 0x0238A694

.definelabel ReturnEndSubHandler, 0x0238B0C8

.definelabel CloseContextDB, 0x0238B380

.definelabel GetGoldStringMenu, 0x0238B414
.definelabel ItemStrStruct, 0x0238B498
.definelabel GoldStrStruct, 0x0238B4A4
.definelabel YesNoMenuChoice, 0x0238B4B4
.definelabel YesNoDBLayout, 0x0238B584

.definelabel BoxMenuStruct, 0x0238B5E0

.definelabel OV25Extend, 0x0238B600
