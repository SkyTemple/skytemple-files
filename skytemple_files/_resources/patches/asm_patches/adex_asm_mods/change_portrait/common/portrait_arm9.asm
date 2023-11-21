.org NoValidFTagFound
.area 0x4
	beq FaceTagHook
.endarea

.org LoadPortraitDBoxID
.area 0x4
	bl DBoxHook
.endarea
