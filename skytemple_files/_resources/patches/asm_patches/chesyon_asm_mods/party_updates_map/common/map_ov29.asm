.org PartyLeaderCheck
.area 0x14
    ; this code may look really weird! if you're having difficulty reading it, just move everything but "b PartyCheck" to the start of the overlay36 code. we're just taking full advantage of our ov29 space, to minimize the amount of ov36 space used.
    push r4
    ldrb r4,[r0,#0x7] ; is_team_leader to r4
    ldrb r0,[r0,#0x6] ; is_not_team_member to r0
    cmp r0,#0x1
    b PartyCheck
.endarea
