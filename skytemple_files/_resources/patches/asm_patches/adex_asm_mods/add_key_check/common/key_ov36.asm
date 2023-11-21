.org 0x023A7080+0x18B0
.area 0x18E0-0x18B0

NewKeyCheck:
	beq CanUseItemReturnTrue ; Original instruction
	ldrsh r0,[r4,#+0x4]
	cmp r0,#182 ; Key Item ID
	bne CanUseItemActionBranch+0x4
	; The following code is the same way the game checks if a Key Door should be opened!
	ldrsh r1,[r5,#+0x6]
	ldrsh r0,[r5,#+0x4]
	sub r1,r1,#0x1
	bl GetTileSafe
	ldrh r0,[r0]
	tst r0,#0x1000
	beq CanUseItemReturnFalse
	b CanUseItemActionBranch+0x4
.endarea
