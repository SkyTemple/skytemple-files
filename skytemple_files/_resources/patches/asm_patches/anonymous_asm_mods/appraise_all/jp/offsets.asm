; For use with ARMIPS
; 2022/09/10 - Updated 2023/09/20
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Adds a menu to appraise all items
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel DBOX_STRING_ID0, 0x000032C6
.definelabel DBOX_STRING_ID1, 0x000032C5

.definelabel MENU_STRING_ID0, 0x32B7
.definelabel MENU_STRING_ID1, 0x32B9
.definelabel MENU_STRING_ID2, 0x32BA

.definelabel IsThrowable, 0x0200CB10

.definelabel CreateItem, 0x0200D0A0

.definelabel PrintItem, 0x0200D670

.definelabel GetItemCategory, 0x0200E838

.definelabel GetGold, 0x0200ED2C
.definelabel AddGold, 0x0200ED88

.definelabel GetNbItemsInBag, 0x0200EE2C

.definelabel RemoveItemByIDAndStackNoHole, 0x0200F4A4
.definelabel AddItemToBagNoHeld, 0x0200F844

.definelabel PlaySE, 0x02017CD8

.definelabel CreateNormalMenu, 0x0202B444
.definelabel GetNormalMenuResult, 0x0202B8D4
.definelabel ShowMessageInDB, 0x0202F4F8
.definelabel CreateGoldStrMenu, 0x0202FC08

.definelabel ItemBagStruct, 0x020B0AF8

.definelabel UnkFunc1, 0x022DDBA4

.definelabel GetNbAppraisableItems, 0x0230CCCC

.definelabel HookMenu, 0x0238C64C
.definelabel HookSwitchMain, 0x0238B6B8
.definelabel HookMenuChoice, 0x0238B9F4
.definelabel HookSwitchSub, 0x0238BC1C

.definelabel ReturnDefaultHandler, 0x0238BB9C
.definelabel ReturnEndHandler, 0x0238BBD4

.definelabel TriggerSubHandler, 0x0238BBF8

.definelabel ReturnEndSubHandler, 0x0238C62C

.definelabel CloseContextDB, 0x0238C8E4

.definelabel GetGoldStringMenu, 0x0238C978
.definelabel ItemStrStruct, 0x0238C9F8
.definelabel GoldStrStruct, 0x0238CA04
.definelabel YesNoMenuChoice, 0x0238CA14
.definelabel YesNoDBLayout, 0x0238CAE4

.definelabel BoxMenuStruct, 0x0238CB40

.definelabel OV25Extend, 0x0238CB60
