
ov_36 equ 023A7080h	;CHANGE THIS IF END45'S OVERLAY IS CHANGED

ov_29 equ 022DD8E0h
ENTITY_TABLE_OFFSET equ 0A84h
CTC_AUTO_STRINGID equ 25AEh
CTC_MANUAL_STRINGID equ 25AFh
.definelabel NA_022EB408, 022ECA70h	;Function - team submenu option recorder
.definelabel NA_022EBD10, 022ED378h	;Operation - the round function's third operation
.definelabel NA_022EBD50, 022ED3B8h	;Operation - calls the function which lowers the gusting wind counter
.definelabel NA_022EBD78, 022ED3E0h	;Operation - the moment the turns of partners start in the round function
.definelabel NA_022EC094, 022ED6FCh	;Operation - the moment the turns of enemies start
.definelabel NA_022EC350, 022ED9B8h	;Operation - the end of the leader's turn verification algorithm
.definelabel NA_022EC488, 022EDAF0h	;Operation - the jump to the function which executes the leader's action
.definelabel NA_022EC4C0, 022EDB28h	;Operation - leader's wait bit setter
.definelabel NA_022EC5F0, 022EDC58h	;Operation - resets the round counter when you get a speed boost
.definelabel NA_022ECB48, 022EE1ACh	;Function - lowers the gusting wind counter
.definelabel NA_022F1178, 022F2770h	;Operation - partner direction setter 1
.definelabel NA_022F1EE0, 022F34D8h	;Operation - checks if you're holding Y or start on your turn
.definelabel NA_022F488C, 022F5E84h	;Operation - skips partner's turn when it gets an item
.definelabel NA_022F499C, 022F5F98h	;Operation - skips partner's turn when you take its item
.definelabel NA_022F989C, 022FAE54h	;Operation - checks how far away a partner is to determine whether or not to focus the PoV on it, when far-off pals is enabled
.definelabel NA_022F9920, 022FAED8h	;Operation - the number of frames the game pauses for when changing PoV
.definelabel NA_022FE4BC, 022FF8A4h	;Function - executes the leader's action
.definelabel NA_022FFF4C, 0230137Ch	;Function - used in turn verification algorithm
.definelabel NA_02301D10, 02303268h	;Function - Checks a specific property of a pokemon, sometimes r12 is equal to this
.definelabel NA_023023AC, 023038FCh	;Operation - part which checks whether or not to display a pokemon's moves
.definelabel NA_02304FE0, 02306530h	;Function - executes all moves in the movement buffer simultaneously
.definelabel NA_0230506C, 023065BCh	;Operation - partner direction setter 2
.definelabel NA_02305160, 023066B0h	;Operation - some line at the end of the partner direction setter
.definelabel NA_0230579C, 02306CECh	;Operation - prevents partners from triggering hidden traps
.definelabel NA_0234B714, 0234C984h	;Function - puts a message in the dialogue
.definelabel NA_02352284, 02353504h	;Variable - used in turn verification algorithm
.definelabel NA_02353538, 023547B8h	;Variable - pointer to beginning of dungeon data. beginning of dungeon data +12B28 is the beginning of the list of pokemon entity addresses.
.definelabel NA_0235355C, 023547DCh	;Variable - points to the current team leader
ov_31 equ 02383AA0h
.definelabel NA_02387530, 023887ACh	;Operation - jump to team submenu option recorder
.definelabel NA_023888A4, 02389B04h	;Operation - checks which option you selected in the rest menu
