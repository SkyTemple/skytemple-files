; For use with ARMIPS
; 2022/09/10
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Adds a menu to appraise all items
; ------------------------------------------------------------------------------


.relativeinclude on
.nds
.arm

.definelabel IsThrowable, 0x0200CB98

.definelabel CreateItem, 0x0200D128

.definelabel PrintItem, 0x0200D6F8

.definelabel GetItemCategory, 0x0200E8D8

.definelabel GetGold, 0x0200EDA4
.definelabel AddGold, 0x0200EE00

.definelabel GetNbItemsInBag, 0x0200EEA4

.definelabel RemoveItemByIDAndStackNoHole, 0x0200F57C
.definelabel AddItemToBagNoHeld, 0x0200F91C

.definelabel PlaySE, 0x02017D1C

.definelabel CreateNormalMenu, 0x0202B3E0
.definelabel GetNormalMenuResult, 0x0202B870
.definelabel ShowMessageInDB, 0x0202F4A8
.definelabel CreateGoldStrMenu, 0x0202FBB8

.definelabel ItemBagStruct, 0x020AFF70

.definelabel UnkFunc1, 0x022DCE44

.definelabel GetNbAppraisableItems, 0x0230C0C0

.definelabel HookMenu, 0x0238BC28
.definelabel HookSwitchMain, 0x0238AC98
.definelabel HookMenuChoice, 0x0238AFD4
.definelabel HookSwitchSub, 0x0238B1F8

.definelabel ReturnDefaultHandler, 0x0238B17C
.definelabel ReturnEndHandler, 0x0238B1B4

.definelabel TriggerSubHandler, 0x0238B1D4

.definelabel ReturnEndSubHandler, 0x0238BC08

.definelabel CloseContextDB, 0x0238BEC0

.definelabel GetGoldStringMenu, 0x0238BF54
.definelabel ItemStrStruct, 0x0238BFD8
.definelabel GoldStrStruct, 0x0238BFE4
.definelabel YesNoMenuChoice, 0x0238BFF4
.definelabel YesNoDBLayout, 0x0238C0C4

.definelabel BoxMenuStruct, 0x0238C120

.definelabel OV25Extend, 0x0238C140
