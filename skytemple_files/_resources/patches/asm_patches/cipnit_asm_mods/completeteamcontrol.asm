; PMD EOS - Complete Team Control Code v1.2.3
; Made by Cipnit
; https://www.pokecommunity.com/showthread.php?t=437108
; Build this file using armips: https://github.com/Kingcom/armips
; Amount of space needed in the custom overlay: 470h bytes

.nds
.include "common/regionSelect.asm"


.open "overlay_0029.bin", ov_29

.org NA_022F1EE0	;the place where the game checks if you're pressing start on your turn
	bl @Mode_Switch	;original: ldrh r0,[r0,2h]

.org NA_022EC350	;end of leader's turn verification algorithm
	bl @WaitChecker	;original: ldrsh r0,[r0,r1]

.org NA_022EC488	;Jump to the function which executes the leader's action
	bl @Leader_Prepper	;original: bl NA_022FE4BC

.org NA_022EBD78	;When the turns of your partners start
	bl @Change_Leader	;original: mov r5,0h

.org NA_022EC4C0	;Leader's wait bit setter - this is actually a bug in the original game, where the leader's wait bit would also raise when you trade places with a partner, which the developers never noticed because the game never checks the leader's wait bit. The wait bit is used to skip a partner's next turn when you trade places with it, which is a big deal in this hack since leadership is constantly changing.
	nop		;original: orrne r0,r0,4000h

.org NA_022F9920	;The pause between turns - changed so it's not ridiculously long
	cmp r0,0Ch	;original: cmp r0,3Ch

.org NA_022EC5F0	;Round counter resetter - nopping this prevents a bug when you get a speed boost, explained in a reply to this mod's pokecommunity post.
	nop		;original: strneh r1,[r0,80h]

.org NA_022F1178	;Sets the partner to look at you. Had to remove because it sets the pokemon's graphical direction but not its mechanical direction, so when you started manual mode, your partner would suddenly change directions.
	nop		;original: bl NA_023055B0
;if I ever want to fix this in the future:
;direction you're facing is pokemon's nonentity data + 4C
;0230567C: r0 is pokemon's entity address, r2 is new direction
;I'm not fixing it because I think pokemon looking in different directions looks cool, but if I wanted to fix it so pokemon look at you at the start of every turn like in the original game, I've got to put a blop at 0230567C to custom code which corrects the problem

.org NA_0230506C	;Another partner direction setter
	b NA_02305160	;original: ldrsh r1,[r0,7Eh]
;023050E4: r1 is new direction, r0 is pokemon's address

.org NA_022F488C	;Equip penalty - when you give a pokemon an item in the original game, its turn is skipped if it's a partner, but if the leader gives itself an item, its next turn isn't skipped. This causes a bug where, if a partner gives itself an item, its next turn is skipped, and if a partner gives the leader an item, the leader's next turn isn't skipped. Fixed so it works fairly: a pokemon doesn't lose its next turn if it gives itself an item, but if it gives an item to another pokemon, the other pokemon's turn is skipped.
	bl @EquipPenalty	;original: ldrb r0,[r9,7h]

.org NA_022F499C	;All of the above also applies to taking items from pokemon
	bl @EquipPenalty	;original: ldrb r0,[r5,7h]

.org NA_022EBD50	;Spot where the game originally calls a function which decreases the gusting wind counter.
	bl @RoundCounterCounter	;original: bl NA_022ECB48

.org NA_023023AC	;Spot where the game checks if you have a temporary party member - in the original game, you're not allowed to see a temporary party member's moves, but with team control, it's possible to see them while you're controling them - however, bugs would occur if you looked at their info. This fixes it so temp party members are treated like regular party members when it comes to moves.
	nop
	mov r0,1h
	pop r4,r15

.close


.open "overlay_0031.bin", ov_31
.org NA_02387530	;Jump to team submenu function
	bl @paranoia_agent	;original: bl NA_022EB408
.org NA_023888A4	;The part of the Rest menu function which checks what option you selected
	bl @paranoia_agent_two	;original: ldr r0,[r1,8h]
.close


.open "overlay_0036.bin", ov_36
.orga 0x10
.area 480h -10h

@ManualModeOn:
	.byte 0h
@ModeSwitchTimer:
	.byte 0h
	.align 4
@CurrentLeader:
	.word 0h

@Message_SetToAuto:
	.ascii "[CS:S]Control mode set to[CR] [CS:C]automatic[CR][CS:S].[CR]", 0
@Message_SetToManual:
	.ascii "[CS:S]Control mode set to[CR] [CS:E]manual[CR][CS:S].[CR]", 0
	.align 4

@Mode_Switch:	;Switches modes when you press start on the leader's turn
	push r1-r5,r12,r14
	ldr r1,=@ModeSwitchTimer
	ldrb r2,[r1]
	cmp r2,0h
	subgt r2,r2,1h
	strb r2,[r1]	;decreasing input lockout timer by 1
	ldrh r0,[r0,2h]
	tst r0,8h
	beq @@modeswitch_return	;return if start isn't held
	mov r0,0h
	ldr r2,=NA_02353538
	ldr r2,[r2]
	add r2,r2,12000h
	ldr r4,[r2,0B28h]	;first pokemon's entity address
	ldr r3,[r4]
	cmp r3,0h
	beq @@modeswitch_return		;if first pokemon doesn't exist, return
	ldr r2,[r4,0B4h]	;fist pokemon's data address
	ldrb r2,[r2,4Ah]	;first pokemon's action ID
	cmp r2,0h			;if it's equal to 0, it's the first pokemon's turn
	bne @@modeswitch_return		;else, it's someone else's turn. This makes it impossible to switch to automatic mode on another pokemon's turn, and makes it impossible to switch to manual mode if the player decided to change leaders via the hidden option in the game's team submenu - both of these circumstances lead to bugs.
	ldrb r2,[r1]
	cmp r2,0h
	bgt @@modeswitch_return		;if the input lockout timer is greater than 0, return - without this, modes would be switched on every frame start is held for
	mov r2,20h
	strb r2,[r1]
	sub r1,r1,1h	;=@ManualModeOn
	ldrb r2,[r1]
	cmp r2,0h
	mov r2,0h		;changing to auto
	moveq r2,1h		;changing to manual
	strb r2,[r1]
	ldr r1,=@Message_SetToAuto
	addeq r1,r1,@Message_SetToManual -@Message_SetToAuto
	mov r0,r4
	mov r2,1h
	mov r3,0h
	bl NA_0234B508	;this function puts a message in the dialogue
	mov r0,0h
@@modeswitch_return:
	pop r1-r5,r12,r15
.pool

@EquipPenalty:
	ldr r0,=@CurrentLeader
	ldr r0,[r0]
	cmp r0,r4
	mov r0,0h
	moveq r0,1h
	bx r14
.pool

@Leader_Prepper:	;Changes the pokemon in control to your leader before executing your action, so the game does a proper game over when your leader dies on a partner's turn instead of bugging out, and so a partner dying doesn't lead to a game over. 
	push r14
	push r0-r1
	push r5-r7
	ldr r5,=NA_0235355C		;pointer to pokemon currently in control
	sub r6,r5,NA_0235355C -NA_02353538
	ldr r6,[r6]
	add r6,12000h
	ldr r6,[r6,0B28h]		;first pokemon's address
	ldr r7,[r5]				;address of currently controled pokemon
	ldr r0,=@CurrentLeader	;temporarally storing current pokemon's MDA here
	str r7,[r0]
	sub r0,r0,@CurrentLeader -@ManualModeOn
	ldrb r1,[r0]
	cmp r1,0h		;if it isn't manual mode, leaders aren't switched. If the player decides to change leaders via the hidden option in the team submenu, then without this check, the first pokemon would be made the leader every time the new leader moves. This is a problem because, if the new leader dies on its turn from a self-damaging attack, and my code changed the leader to another pokemon, the game will bug up.
	bne @@leaderprepper_everythingsfine
	pop r5-r7
	pop r0-r1
	bl NA_022FE4BC
	pop r15
@@leaderprepper_everythingsfine:
	bl @leaderchanger
	pop r5-r7
	pop r0-r1
	bl NA_022FE4BC	;this function executes the lead Pokemon's action. It does not wait for player input, it just executes the action that the player chose earlier, in a prior function which waits for player input.
	push r0-r1
	push r5-r7
	ldr r5,=NA_0235355C
	ldr r7,[r5]
	cmp r7,0h				;if this is 0, leader is die forever
	beq @@leaderprepper_end
	ldr r0,=@CurrentLeader
	ldr r6,[r0]
	bl @leaderchanger
@@leaderprepper_end:
	pop r0-r1
	pop r5-r7
	pop r15
.pool

@paranoia_agent:	;This prevents the player from sending pokemon home during manual mode, which causes the game to bug out if you send the leader home, and from changing leaders using the hidden option during manual mode. 
	push r14
	push r0
	cmp r1,34h		;farewell decision
	cmpne r1,3Bh	;change leader decision
	bne @@paranoiaagent_nvm
	ldr r0,=@ManualModeOn
	ldrb r0,[r0]
	cmp r0,1h
	bne @@paranoiaagent_nvm
	mov r1,0h
@@paranoiaagent_nvm:
	pop r0
	bl NA_022EB408	;this records the player's decision in the team submenu
	pop r15
.pool

@paranoia_agent_two:	;Prevents the player from quicksaving while controling another partner in manual mode
	push r14
	ldr r0,[r1,8h]
	cmp r0,1h
	popne r15
	ldr r0,=@ManualModeOn
	ldrb r0,[r0]
	cmp r0,1h
	bne @paranoiaover
	ldr r0,=NA_02353538
	ldr r0,[r0]
	add r0,r0,12000h
	ldr r0,[r0,0B28h]
	ldr r0,[r0,0B4h]
	ldrb r0,[r0,7h]
	cmp r0,1h
	beq @paranoiaover
	mov r0,0h
	pop r15
@paranoiaover:
	ldr r0,[r1,8h]
	pop r15
.pool

@WaitChecker:		;This skips a pokemon's turn if the pokemon swapped places with another pokemon previously. In the original game, swapping places with a partner skips the partner's next turn, as if the partner "used its move" when it swapped places with you. (A bug in the game raises this skip flag for the leader too, which I nopped earlier.) The game has nothing to prevent a leader from moving if this flag is raised, so this exists to make the game play as it's supposed to.
	push r1-r3,r14
	ldrsh r0,[r0,r1]
	cmp r0,0h
	popeq r1-r3,r15		;If this is equal to 0, the Pokemon wasn't going to take a turn anyway
	ldr r1,[r4,0B4h]	;r4 has the current pokemon's entity address
	ldrh r2,[r1]
	mov r3,4000h
	tst r2,r3
	movne r0,0h
	subne r2,r2,r3
	strh r2,[r1]
	pop r1-r3,r15
	
@RoundCounterCounter:		;If you just moved a partner in manual mode, this makes it so the game's gusting wind counter won't go down - it'll only go down for the leader, once per round.
	push r0,r1,r14
	mov r0,r14
	ldr r1,=@ManualModeOn
	ldrb r1,[r1]
	cmp r1,1h
	bne @justcounttheround
	ldr r1,=NA_02353538
	ldr r1,[r1]
	add r1,r1,12000h
	ldr r1,[r1,0B28h]	;first pokemon's entity address
	ldr r1,[r1,0B4h]
	ldrb r1,[r1,7h]
	cmp r1,1h
	beq @justcounttheround
	add r0,0Ch
	str r0,[sp,8h]
	pop r0,r1,r15
@justcounttheround:
	pop r0,r1
	bl NA_022ECB48
	pop r15
.pool

@leaderchanger:		;r5 is the leader pointer, r6 is the new leader's address, r7 is the old leader's address
	push r14
	ldr r0,[r7,0B4h]
	mov r1,0h
	strb r1,[r0,7h]
	ldr r0,[r6,0B4h]
	mov r1,1h
	strb r1,[r0,7h]
	str r6,[r5]
	pop r15

@Change_Leader:	;Before the turns of partners are executed, if manual mode is on, this code either changes control to your next pokemon and jumps back to the start of the round function, or, if your last pokemon moved, it changes control to your first pokemon, then skips the turns of partners. 
	push r14
	mov r5,0h
	push r0-r12
	ldr r0,=@ManualModeOn
	ldrb r0,[r0]
	cmp r0,0h
	popeq r0-r12,r15	;if manual mode isn't true, return
	ldr r5,=NA_0235355C
	ldr r7,[r5]
	cmp r7,0h
	popeq r0-r12,r15	;if the leader pointer is 0 (ur dead), return
	sub r0,r5,NA_0235355C -NA_02353538
	ldr r0,[r0]
	mov r6,r0
	add r0,r0,1D8h
	mov r1,0h
	sub r1,r1,1h
	str r1,[r0]		;disabling moving using the touch screen to prevent a funny bug, nop this line to see it
	add r6,12000h
	ldr r6,[r6,0B28h]	;first pokemon's entity address
	mov r8,r6
	bl @leaderchanger
	ldr r12,=NA_02301D10
	mov r0,0h
	bl NA_02304FE0	;executing the movement buffer while the leader is the first Pokemon, to prevent bugs
	mov r0,r7		;for example, if your first pokemon dies from poison damage while it isn't the leader, the game bugs out.
	mov r7,r6
	mov r6,r0
	ldr r0,[r5]
	cmp r0,0h
	popeq r0-r12,r15
	bl @leaderchanger
	mov r7,r6		;r7 is the current leader, r6 is the new leader, r8 is the first pokemon in the dungeon
	mov r4,0h
find:
	add r6,0B8h
	add r4,1h
	cmp r4,10h
	bge roundover
	ldr r0,[r6]
	cmp r0,1h
	bne find		;if this pokemon doesn't exist, go to the next pokemon
	ldr r0,[r6,0B4h]
	ldrb r1,[r0,6h]
	cmp r1,0h
	bne roundover	;if the pokemon isn't on your team, then there's no more allies
	mov r0,r6		;start of turn verification algorithm
	bl NA_022FFF4C
	ldr r1,=NA_02353538
	ldr r3,=NA_02352284
	ldr r2,[r1]
	mov r1,32h
	add r2,r2,700h
	mla r1,r0,r1,r3
	ldrsh r2,[r2,80h]
	mov r0,r2,lsl 1h
	ldrsh r0,[r0,r1]
	cmp r0,0h
	beq find			;if the result is 0, this pokemon doesn't have the speed to take a turn now
	bl @leaderchanger	;else, it's in charge now
	pop r0-r12
	add r13,r13,4h
	mov r1,r2
	mov r8,0h
	ldr r12,=NA_02301D10
	b NA_022EBD10		;jumping to the start of the round function
roundover:
	mov r6,r8
	bl @leaderchanger	;first pokemon gets to be the leader again
	pop r0-r12
	add r13,r13,4h
	mov r3,0h
	b NA_022EC094		;skipping the turns of partners
.pool

	.endarea
.close
