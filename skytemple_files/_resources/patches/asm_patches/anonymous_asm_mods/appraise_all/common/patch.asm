
.org HookMenu
.area 0x4
	.word new_menu
.endarea

.org HookSwitchMain
.area 0x4
	b SwitchMain
.endarea

.org HookSwitchSub
.area 0x4
	b SwitchSub
.endarea

.org HookMenuChoice
.area 0x4
	bne MenuAppraiseAll
.endarea


.org OV25Extend
.area 0x1000
SwitchMain:
	cmp r1,#0x20
	beq ReturnDefaultHandler
	cmp r1,#0x21
	bne switch_main_no_21
	add r0,r2,#0x100
	ldrsb r0,[r0, #+0x3a]
	bl GetNormalMenuResult
	cmp r0,#0x1
	beq cancel_buy
	cmp r0,#0x4
	beq confirm_buy
	cmp r0,#0x5
	beq cancel_buy
	b ReturnEndHandler
confirm_buy:
	bl CloseContextDB
	bl GetBagPokeValue
	stmdb r13!,{r4}
	mov r4,r0
	bl GetGold
	cmp r0,r4
	ldmia r13!,{r4}
	bge has_money
	mov r0,#0x9
	bl TriggerSubHandler
	b ReturnEndHandler
has_money:
	mov r0,#0x22
	bl TriggerSubHandler
	ldr r0,=0x00001308
	bl PlaySE
	b ReturnEndHandler
cancel_buy:
	bl CloseContextDB
	mov r0,#0x1
	bl TriggerSubHandler
	b ReturnEndHandler
switch_main_no_21:
	cmp r1,#0x22
	beq ReturnDefaultHandler
	cmpne r1,#0x23
	bne switch_main_no_23
	ldr r3,[r0, #+0x0]
	mov  r2,#0x24
	str r2,[r3, #+0x4]
	mov  r1,#0x1B
	str r1,[r3]
	ldr r1,=0x00003008
	add  r0,r3,#0x100
	ldrsb r0,[r0, #+0x38]
	ldr r2,=0x000003E2
	add  r3,r3,#0x28
	bl ShowMessageInDB
	b ReturnEndHandler
switch_main_no_23:
	cmpne r1,#0x24
	bne switch_main_no_24
	ldr r3,[r0, #+0x0]
	mov  r2,#0x25
	str r2,[r3, #+0x4]
	mov  r1,#0x1B
	str r1,[r3]
	ldr r1,=0x00003018
	add  r0,r3,#0x100
	ldrsb r0,[r0, #+0x38]
	ldr  r2,=AppraiseRevealBeforeStringID
	add  r3,r3,#0x28
	bl ShowMessageInDB
	b ReturnEndHandler
switch_main_no_24:
	cmpne r1,#0x25
	bne ReturnDefaultHandler
	ldr r3,[r0, #+0x0]
	mov  r1,#0x4
	str r1,[r3, #+0x50]
	mov  r2,#0x1
	str r2,[r3, #+0x4]
	mov  r1,#0x1B
	str r1,[r3]
	ldr r1,=0x00003018
	add  r0,r3,#0x100
	ldrsb r0,[r0, #+0x38]
	ldr  r2,=AppraiseRevealItemStringID
	add  r3,r3,#0x28
	bl ShowMessageInDB
	bl IterNext
	ldr r1,=iter_next
	ldr r2,[r1]
	cmp r2,#0
	beq ReturnEndHandler
	ldr r0,=BoxMenuStruct
	ldr r3,[r0, #+0x0]
	mov  r2,#0x25
	str r2,[r3, #+0x4]
	b ReturnEndHandler
SwitchSub:
	cmp r0,#0x20
	bne switch_sub_no_20
	bl GetBagPokeValue
	mov r2,r0
	ldr r0,=BoxMenuStruct
	ldr r1,[r0, #+0x0]
	str r2,[r1, #+0x4c]
	mov r3,#0x20
	mov r2,#0x21
	str r3,[r1, #+0x0]
	str r2,[r1, #+0x4]
	ldr r1,=0x00003008
	ldr r12,[r0, #+0x0]
	ldr r2,=AppraiseAllConfirmStringID
	ldrsh r3,[r12, #+0xc]
	str r3,[r12, #+0x3c]
	ldr r12,[r0, #+0x0]
	ldrh r3,[r12, #+0xe]
	str r3,[r12, #+0x50]
	ldr r3,[r0, #+0x0]
	add r0,r3,#0x100
	ldrsb r0,[r0, #+0x38]
	add r3,r3,#0x28
	bl ShowMessageInDB
	b ReturnEndSubHandler
switch_sub_no_20:
	cmp r0,#0x21
	bne switch_sub_no_21
	ldr r0,=GoldStrStruct
	ldr r1,=GetGoldStringMenu
	bl CreateGoldStrMenu
	ldr r1,=BoxMenuStruct
	ldr r3,=YesNoMenuChoice
	ldr r1,[r1, #+0x0]
	mov r12,#0x2
	strb r0,[r1, #+0x13d]
	ldr r0,=YesNoDBLayout
	mov r1,#0x80000013
	mov r2,#0x0
	str r12,[r13, #+0x0]
	bl CreateNormalMenu
	ldr r1,=BoxMenuStruct
	ldr r1,[r1, #+0x0]
	strb r0,[r1, #+0x13a]
	b ReturnEndSubHandler
switch_sub_no_21:
	cmp r0,#0x22
	bne switch_sub_no_22
	bl GetBagPokeValue
	rsb r0,r0,#0
	bl AddGold
	bl IterNext
	ldr r0,=BoxMenuStruct
	mov  r2,#0x23
	ldr r1,[r0, #+0x0]
	mov  r3,#0x6
	str r2,[r1, #+0x4]
	str r3,[r1, #+0x24]
	ldr r1,=0x00003018
	ldr r3,[r0, #+0x0]
	ldr r2,=0x000003E1
	add  r0,r3,#0x100
	ldrsb r0,[r0, #+0x38]
	add  r3,r3,#0x28
	bl ShowMessageInDB
	b ReturnEndSubHandler
switch_sub_no_22:
	cmp r0,#0x23
	bne switch_sub_no_23
	mov  r0,#0x7
	str r0,[r1, #+0x24]
	b ReturnEndSubHandler
switch_sub_no_23:
	cmp r0,#0x24
	bne ReturnEndSubHandler
	mov  r0,#0x8
	str r0,[r1, #+0x24]
switch_sub_no_24:
	b ReturnEndSubHandler
MenuAppraiseAll:
	cmp r0,#8
	bne ReturnEndHandler	
	bl CloseContextDB
	bl GetNbItemsInBag
	cmp r0,#0x0
	bne has_items
	mov r0,#0x5
	bl TriggerSubHandler
	b ReturnEndHandler
has_items:
	bl GetNbAppraisableItems
	cmp r0,#0x0
	bne has_appraisable_items
	mov r0,#0x6
	bl TriggerSubHandler
	b ReturnEndHandler
has_appraisable_items:
	mov r0,#0x20
	bl TriggerSubHandler
	b ReturnEndHandler
GetBagPokeValue:
	stmdb r13!,{r4,r5,r6,r14}
	ldr r1,=ItemBagStruct
	ldr r0,[r1, #+0x0]
	ldr r5,[r0, #+0x384]
	mov r4,#0
	mov r6,#0
loop_getboxvalue:
	ldrb r0,[r5, #+0x0]
	tst r0,#0x1
	beq check_getboxvalue
	ldrsh r0,[r5, #+0x4]
	bl GetItemCategory
	cmp r0,#0xC
	cmpne r0,#0xD
	cmpne r0,#0xE
	ldreq r0,=BoxCost
	addeq r4,r4,r0
check_getboxvalue:
	add r6,r6,#0x1
	cmp r6,#0x32
	add r5,r5,#0x6
	blt loop_getboxvalue
	mov r0,r4
	ldmia r13!,{r4,r5,r6,r15}
IterNext:
	stmdb r13!,{r14}
	bl SearchForBox
	str r0,[iter_next]
	ldr r0,=BoxMenuStruct
	ldr r2,[r0, #+0x0]
	add  r1,r2,#0xB8
	str r1,[r2, #+0x60]
	ldrsh r2,[r13, #+0x4]
	ldr r1,[r0, #+0x0]
	str r2,[r1, #+0x3c]
	ldr r2,[r0, #+0x0]
	ldrh r1,[r2, #+0xe]
	str r1,[r2, #+0x50]
	ldmia r13!,{r15}
iter_next:
	.word 0x0
SearchForBox:
	stmdb r13!,{r3,r5,r6,r14}
	ldr r1,=ItemBagStruct
	ldr r0,[r1, #+0x0]
	ldr r5,[r0, #+0x384]
	mov r6,#0
loop_searchboxvalue:
	ldrb r0,[r5, #+0x0]
	tst r0,#0x1
	beq check_searchboxvalue
	ldrsh r0,[r5, #+0x4]
	bl GetItemCategory
	cmp r0,#0xC
	cmpne r0,#0xD
	cmpne r0,#0xE
	bne check_searchboxvalue
	mov r0,r13
	ldrh r1,[r5,#+0x2]
	ldrh r2,[r5,#+0x4]
	strh r1,[r13,#+0x2]
	strh r2,[r13]
	bl OpenBox
	mov r0,#1
	ldmia r13!,{r3,r5,r6,r15}
check_searchboxvalue:
	add r6,r6,#0x1
	cmp r6,#0x32
	add r5,r5,#0x6
	blt loop_searchboxvalue
	mov r0,#0
	ldmia r13!,{r3,r5,r6,r15}
OpenBox:
	stmdb r13!,{r4,r14}
	sub r13,r13,#0xC
	mov r4,r0
	ldr r1,=BoxMenuStruct
	add r0,r13,#0x6
	ldr r12,[r1, #+0x0]
	mov r1,r13
	ldrsh r3,[r4, #+0x0]
	mov r2,#0x1
	strh r3,[r13, #+0x4]
	ldrh r3,[r4, #+0x2]
	strh r3,[r13, #+0x2]
	strb r2,[r13]
	bl CreateItem
	add r0,r13,#0x6
	bl RemoveItemByIDAndStackNoHole
	ldrsh r0,[r4, #+0x2]
	mov r1,#0x0
	strh r0,[r13, #+0x4]
	strh r1,[r13, #+0x2]
	bl IsThrowable
	cmp r0,#0x0
	movne r0,#0xA
	strneh r0,[r13, #+0x2]
	bne check_valid_item_0
	ldrsh r0,[r13, #+0x4]
	cmp r0,#0xBB
	moveq r0,#0x55
	streqh r0,[r13, #+0x4]
	ldrsh r1,[r13, #+0x4]
	cmp r1,#0x16C
	blt check_valid_item_1
	ldr r0,=0x0000018F
	cmp r1,r0
	movle r0,#0x55
	strleh r0,[r13, #+0x4]
 check_valid_item_1:
	ldrsh r0,[r13, #+0x4]
	cmp r0,#0xB7
	moveq r0,#0x55
	streqh r0,[r13, #+0x4]
 check_valid_item_0:
	mov r1,#0x1
	mov r0,r13
	strb r1,[r13]
	bl AddItemToBagNoHeld
	bl UnkFunc1
	ldr r0,=BoxMenuStruct
	mov r1,r13
	ldr r0,[r0, #+0x0]
	ldr r2,=ItemStrStruct
	add r0,r0,#0xB8
	bl PrintItem
	add r13,r13,#0xC
	ldmia r13!, {r4,r15}
	.pool
new_menu:
	.word 0x3D3, 7
	.word MenuOptionStringID, 8
	.word 0x3D5, 6
	.word 0x3D6, 1
	.word 0, 1
.endarea
