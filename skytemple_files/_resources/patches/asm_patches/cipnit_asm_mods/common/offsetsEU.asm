
ov_36 equ 023A7080h	;CHANGE THIS IF END45'S OVERLAY IS CHANGED

ov_29 equ 022DCB80h
.definelabel NA_022EB408, 022EBDB8h	;Function - team submenu option recorder
.definelabel NA_022EBD10, 022EC6C0h	;Operation - the round function's third operation
.definelabel NA_022EBD50, 022EC700h	;Operation - calls the function which lowers the gusting wind counter
.definelabel NA_022EBD78, 022EC728h	;Operation - the moment the turns of partners start in the round function
.definelabel NA_022EC094, 022ECA44h	;Operation - the moment the turns of enemies start
.definelabel NA_022EC350, 022ECD00h	;Operation - the end of the leader's turn verification algorithm
.definelabel NA_022EC488, 022ECE38h	;Operation - the jump to the function which executes the leader's action
.definelabel NA_022EC4C0, 022ECE70h	;Operation - leader's wait bit setter
.definelabel NA_022EC5F0, 022ECFA0h	;Operation - resets the round counter when you get a speed boost
.definelabel NA_022ECB48, 022ED4F8h	;Function - lowers the gusting wind counter
.definelabel NA_022F1178, 022F1B2Ch	;Operation - partner direction setter 1
.definelabel NA_022F1EE0, 022F2894h	;Operation - checks if you're holding Y or start on your turn
.definelabel NA_022F488C, 022F5248h	;Operation - skips partner's turn when it gets an item
.definelabel NA_022F499C, 022F5358h	;Operation - skips partner's turn when you take its item
.definelabel NA_022F989C, 022FA2A8h	;Operation - checks how far away a partner is to determine whether or not to focus the PoV on it, when far-off pals is enabled
.definelabel NA_022F9920, 022FA32Ch	;Operation - the number of frames the game pauses for when changing PoV
.definelabel NA_022FE4BC, 022FEEDCh	;Function - executes the leader's action
.definelabel NA_022FFF4C, 02300978h	;Function - used in turn verification algorithm
.definelabel NA_02301D10, 0230273Ch	;Function - Checks a specific property of a pokemon, sometimes r12 is equal to this
.definelabel NA_023023AC, 02302DD8h	;Operation - part which checks whether or not to display a pokemon's moves
.definelabel NA_02304FE0, 02305A0Ch	;Function - executes all moves in the movement buffer simultaneously
.definelabel NA_0230506C, 02305A98h	;Operation - partner direction setter 2
.definelabel NA_02305160, 02305B8Ch	;Operation - some line at the end of the partner direction setter
.definelabel NA_0230579C, 023061C8h	;Operation - prevents partners from triggering hidden traps
.definelabel NA_0234B508, 0234C108h	;Function - puts a message in the dialogue
.definelabel NA_02352284, 02352E90h	;Variable - used in turn verification algorithm
.definelabel NA_02353538, 02354138h	;Variable - pointer to beginning of dungeon data. beginning of dungeon data +12B28 is the beginning of the list of pokemon entity addresses.
.definelabel NA_0235355C, 0235415Ch	;Variable - points to the current team leader
ov_31 equ 02383420h
.definelabel NA_02387530, 02388154h	;Operation - jump to team submenu option recorder
.definelabel NA_023888A4, 023894C8h	;Operation - checks which option you selected in the rest menu
