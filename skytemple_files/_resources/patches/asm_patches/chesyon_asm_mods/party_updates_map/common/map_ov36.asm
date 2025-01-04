.orga 0x1C10
.area 0x20
PartyCheck:
    popeq r4
    beq IfCheckFails
    add r0,r9,#0x4
    bl DiscoverMinimap
    cmp r4,#0x0
    pop r4
    beq IfCheckFails
    b ReturnPoint
.endarea
