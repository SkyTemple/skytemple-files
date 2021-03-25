; For use with ARMIPS
; 2021/03/23
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Adds a menu to choose the starter after the quiz
; ------------------------------------------------------------------------------


	.org BegSwitch
	.area 0x4
		cmp r1,#0x48
	.endarea
	.org BegSwitch+0xC
	.area 0x4
		b move_beg_switch
	.endarea
	
	.org EndSwitch
	.area 11*0x4
		b SwitchCase42
		b SwitchCase43
		b SwitchCase44
		b SwitchCase45
		b SwitchCase46
		b SwitchCase47
		b SwitchCase48
		.fill 11*0x4+EndSwitch-., 0xCC
	.endarea

	.org HookEventSeq
	.area 0xC
		mov  r0,#0x42 ; 0x26 Originally
	.endarea

	.org OldGetPersonalityResult
	.area 0x48
		stmdb  r13!,{r14}
		ldr r0,[player_id]
		mvn r1,#0
		cmp r0,r1
		bne end_ogpr
		bl GetPersonalityResult
		str r0,[player_id]
	end_ogpr:
		ldmia  r13!,{r15}
	player_id:
		.word 0xFFFFFFFF
		.pool
		.fill 0x48+OldGetPersonalityResult-., 0xCC
	.endarea
	
	.org OverlayStart+OrgSize
	.area ExtendSize
	
	GetPersonalityResult:
		stmdb  r13!,{r3,r14}
		ldr r0,=GlobalStructPointer
		mov  r12,#0x0
		ldr r14,[r0, #+0x0]
		mov  r0,r12
		mov  r3,r12
	loop_players:
		add  r1,r14,r3
		ldrb r2,[r1, #+0x34]
		ldrb r1,[r1, #+0x44]
		add  r1,r2,r1
		cmp r12,r1
		movlt  r0,r3
		add  r3,r3,#0x1
		movlt  r12,r1
		cmp r3,#0x10
		blt loop_players
		ldmia  r13!,{r3,r15}
	move_beg_switch:
		mov  r0,#0x64
		bl RandMax
		cmp r0,#0x4B
		blt case0_alt1
		add  r0,r13,#0x14
		bl UnknownFuncCase0
		ldrb r1,[r13, #+0x19]
		ldr r0,[r15, #+0xe20]
		ldr r0,[r0, #+0x0]
		and  r1,r1,#0xF
		b case0_alt2
	SwitchCase42:
		add  r0,r13,#0x128
		bl PrepDBUnk1
		bl OldGetPersonalityResult
		bl GetPlayerPkmnID
		str r0,[r13, #+0x128]
		ldr r0,=GlobalStructPointer
		ldr r1,[r0]
		ldrsb r0,[r1, #+0x2]
		bl ShowDB
		ldr r0,=GlobalStructPointer
		mov  r1,#0x4
		ldr r0,[r0, #+0x0]
		add  r3,r13,#0x128
		ldrsb r0,[r0, #+0x2]
		add  r2,r1,#0x6C0
		bl ShowMessageInDB
		ldr r1,=GlobalStructPointer
		ldr r1,[r1, #+0x0]
		ldr r0,[r1, #+0x20]
		add  r0,r0,#0x1
		str r0,[r1, #+0x20]
		b EndCodeSwitch
	SwitchCase43:
		ldrsb r0,[r0, #+0x2]
		bl IsDBActive
		cmp r0,#0x0
		bne EndCodeSwitch
		ldr r0,=DBLayout5
		mov  r4,#0x2
		ldr r1,=0x00300013
		ldr r3,=QuizMenu1
		mov  r2,#0x0
		str r4,[r13, #+0x0]
		bl CreateNormalMenu
		ldr r1,=GlobalStructPointer
		ldr r2,[r1, #+0x0]
		strb r0,[r2, #+0x3]
		ldr r1,[r1, #+0x0]
		ldr r0,[r1, #+0x20]
		add  r0,r0,#0x1
		str r0,[r1, #+0x20]
		b EndCodeSwitch
	SwitchCase44:
		ldrsb r0,[r0, #+0x3]		;r0+0x3=*(000f1e03)
		bl GetNormalMenuResult
		cmp r0,#0x1
		beq case44_yes
		cmp r0,#0x2
		beq case44_no
		b EndCodeSwitch
	case44_yes:
		ldr r0,=GlobalStructPointer
		ldr r0,[r0, #+0x0]
		ldrsb r0,[r0, #+0x3]
		bl FreeNormalMenu
		mvn  r2,#0x1
		ldr r0,=GlobalStructPointer
		ldr r1,[r0, #+0x0]
		strb r2,[r1, #+0x3]
		ldr r1,=GlobalStructPointer
		ldr r1,[r1, #+0x0]
		mov r0,#0x26
		str r0,[r1, #+0x20]
		b EndCodeSwitch
	case44_no:
		ldr r0,=GlobalStructPointer
		ldr r0,[r0, #+0x0]
		ldrsb r0,[r0, #+0x3]
		bl FreeNormalMenu
		mvn  r2,#0x1
		ldr r0,=GlobalStructPointer
		ldr r1,[r0, #+0x0]
		strb r2,[r1, #+0x3]
		ldr r1,=GlobalStructPointer
		ldr r1,[r1, #+0x0]
		mov r0,#0x45
		str r0,[r1, #+0x20]
		b EndCodeSwitch
	SwitchCase45:
		ldrsb r0,[r0, #+0x2]
		bl ShowDB
		ldr r1,=GlobalStructPointer
		ldr r1,[r1, #+0x0]
		ldrsb r0,[r1, #+0x5]
		bl HidePortraitBox
		ldr r1,=GlobalStructPointer
		ldr r3,[r1, #+0x0]
		ldrsb r0,[r3, #+0x2]
		ldr  r2,=SpecialStringID
		mov  r1,#0x8
		mov  r3,#0x0
		bl ShowMessageInDB
		ldr r1,=GlobalStructPointer
		ldr r1,[r1, #+0x0]
		mov r0,#0x46
		str r0,[r1, #+0x20]
		b EndCodeSwitch
	SwitchCase46:
		ldrsb r0,[r0, #+0x2]
		bl IsDBActive
		cmp r0,#0x0
		bne EndCodeSwitch
		ldr r1,=GlobalStructPointer
		ldr r0,=DBLayout6
		ldr r2,[r1, #+0x0]
		ldr r1,=0x00001011
		mov r2,#0x10
		ldr r3,=PlayerMenuDisp
		str r2,[r13, #+0x0]
		mov  r4,#0x6
		mov  r2,#0x0
		str r4,[r13, #+0x4]
		bl CreateAdvancedMenu
		ldr r2,=GlobalStructPointer
		ldr r1,[r2, #+0x0]
		strb r0,[r1, #+0x3]
		ldr r3,[r1, #+0x20]
		add  r3,r3,#0x1
		str r3,[r1, #+0x20]
		
		;For Portraits
		mov  r0,#0x0
		sub  r1,r0,#0x2
		str r0,[r2, #+0x4]
		str r0,[r2, #+0x8]
		ldr r2,[r2]
		ldrsb r2,[r2, #+0x5]
		cmp r2,r1
		bne no_pt_box
		mov  r1,#0x3
		mov  r2,#0x1
		bl CreatePortraitBox
		ldr r1,=GlobalStructPointer
		ldr r1,[r1]
		strb r0,[r1, #+0x5]
	no_pt_box:
		ldr r1,=GlobalStructPointer
		ldr r1,[r1]
		add r4,r1,#0x3B4
		mov r0,#0
		bl GetPlayerPkmnID
		mov r1,r0
		mov r0,r4
		bl SetPortraitPkmnID
		mov r0,r4
		mov r1,#0
		bl SetPortraitExpressionID
		mov r0,r4
		mov r1,#4
		bl SetPortraitUnknownAttr
		mov r0,r4
		ldr r1,=PortraitAttrStruct
		bl SetPortraitAttrStruct
		ldr r1,=GlobalStructPointer
		ldr r1,[r1]
		ldrsb r0,[r1, #+0x5]
		mov r1,r4
		bl ShowPortraitBox
		b EndCodeSwitch
	SwitchCase47:
		ldrsb r0,[r0, #+0x3]
		ldr r4,[r2, #+0x4]
		bl GetAdvancedMenuCurrentOption
		cmp r4,r0
		beq case47_same_pkmn
		ldr r0,=GlobalStructPointer
		mov  r1,#0x0
		str r1,[r0, #+0x8]
		ldr r0,[r0, #+0x0]
		ldrsb r0,[r0, #+0x3]
		bl GetAdvancedMenuCurrentOption
		ldr r1,=GlobalStructPointer
		str r0,[r1, #+0x4]
		ldr r1,[r1]
		add r4,r1,#0x3B4
		bl GetPlayerPkmnID
		mov r1,r0
		mov r0,r4
		bl SetPortraitPkmnID
		mov r1,0x0
		mov r0,r4
		bl SetPortraitExpressionID
		mov r1,0x4
		mov r0,r4
		bl SetPortraitUnknownAttr
		ldr r1,=PortraitAttrStruct
		mov r0,r4
		bl SetPortraitAttrStruct
		ldr r1,=GlobalStructPointer
		ldr r1,[r1]
		ldrsb r0,[r1, #+0x5]
		mov r1,r4
		bl ShowPortraitBox
		b case47_after_portraits
	case47_same_pkmn:
		ldr r0,=GlobalStructPointer
		ldr r1,[r0, #+0x8]
		cmp r1,#0x20
		addne  r1,r1,#0x1
		strne r1,[r0, #+0x8]
		bne case47_after_portraits
		ldr r1,[r0]
		mov r0,r4
		add r4,r1,#0x3B4
		bl GetPlayerPkmnID
		mov r1,r0
		mov r0,r4
		bl SetPortraitPkmnID
		mov r1,0x1
		mov r0,r4
		bl SetPortraitExpressionID
		mov r1,0x4
		mov r0,r4
		bl SetPortraitUnknownAttr
		ldr r1,=PortraitAttrStruct
		mov r0,r4
		bl SetPortraitAttrStruct
		ldr r1,=GlobalStructPointer
		ldr r1,[r1]
		ldrsb r0,[r1, #+0x5]
		mov r1,r4
		bl ShowPortraitBox
	case47_after_portraits:
		ldr r0,=GlobalStructPointer
		ldr r0,[r0, #+0x0]
		ldrsb r0,[r0, #+0x3]
		bl IsAdvancedMenuActive
		cmp r0,#0x0
		bne EndCodeSwitch
		ldr r0,=GlobalStructPointer
		ldr r4,[r0, #+0x0]
		ldrsb r0,[r4, #+0x3]
		bl GetAdvancedMenuResult
		ldr r1,=player_id
		str r0,[r1]
		
		ldr r1,=GlobalStructPointer
		ldr r1,[r1]
		add r4,r1,#0x3B4
		bl GetPlayerPkmnID
		mov r1,r0
		mov r0,r4
		bl SetPortraitPkmnID
		mov r1,0x1
		mov r0,r4
		bl SetPortraitExpressionID
		mov r1,0x4
		mov r0,r4
		bl SetPortraitUnknownAttr
		ldr r1,=PortraitAttrStruct
		mov r0,r4
		bl SetPortraitAttrStruct
		ldr r1,=GlobalStructPointer
		ldr r1,[r1]
		ldrsb r0,[r1, #+0x5]
		mov r1,r4
		bl ShowPortraitBox
		
		ldr r0,=GlobalStructPointer
		ldr r0,[r0, #+0x0]
		ldrsb r0,[r0, #+0x3]
		bl FreeAdvancedMenu
		mvn  r0,#0x1
		ldr r2,=GlobalStructPointer
		ldr r1,[r2, #+0x0]
		strb r0,[r1, #+0x3]
		ldr r1,[r2, #+0x0]
		mov r0,#0x42
		str r0,[r1, #+0x20]
		b EndCodeSwitch
	SwitchCase48: ;Special Case to skip the quiz
		mov  r0,#0x0
		mov  r1,#0x3
		mov  r2,#0x1
		bl CreatePortraitBox
		ldr r1,=GlobalStructPointer
		ldr r1,[r1]
		strb r0,[r1, #+0x5]
		ldr r1,=GlobalStructPointer
		ldr r0,[r1]
		ldrb r1,[r0, #+0x5f]
		ldr r0,=BorderColorTable
		ldrb r0,[r0, +r1]
		bl ChangeBorderColor
		ldr r1,=GlobalStructPointer
		ldr r1,[r1]
		mov r0,#0x45
		str r0,[r1, #+0x20]
		b EndCodeSwitch
		.pool
	GetPlayerPkmnID:
		ldr r1,=GlobalStructPointer
		ldr r1,[r1]
		ldrb r1,[r1, #+0x5f]
		add  r0,r1,r0,lsl #0x1
		mov  r0,r0,lsl #0x1
		ldr r2,=PlayersListPkmnID
		ldrsh r0,[r2, r0]
		bx r14
	PlayerMenuDisp:
		stmdb  r13!,{r3,r4,r14}
		sub  r13,r13,#0x54
		add  r12,r13,#0x4
		mov  r4,r0
		mov  r0,r1
		bl GetPlayerPkmnID
		ldr r3,=0x0000c402
		orr  r14,r0,#0x10000
		str r0,[r13, #+0x4]
		str r14,[r13, #+0x14]
		mov  r1,#0x400
		ldr r2,=MenuOptionString
		str r12,[r13, #+0x0]
		mov  r0,r4
		bl MenuCreateOptionString
		mov  r0,r4
		add  r13,r13,#0x54
		ldmia  r13!,{r3,r4,r15}
		.pool
		.fill OverlayStart+OrgSize+ExtendSize-., 0xCC
	.endarea
