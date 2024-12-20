.orga 0x1B70
.area 0x20

CheckHpForPortrait:
    ldrsh r2,[r7,0x4A] ; load hp to r2 (r7 points to the team member, 0x4A is HP)
    ldrsh r3,[r7,0x4C] ; load max hp to r3 (r7 points to the team member, 0x4C is max HP) 
    cmp r2,r3,lsr 0x2 ; check if hp is < max hp /4 (lsr 0x2 divides by 4) 
    movlt r1,#0x2 ; set portrait to pain if hp is < max hp / 4. we know r1 will be 0 going into this code, so if r1 isn't set to pain here it'll just stay as normal.
    bl SetPortraitEmotion ; do the thing. we're lucky that r0 isn't overwritten here, otherwise we'd need to store it to r4 before this and restore it to r0 after. (which would also require pushing and popping r4)
    mov r1,0x1 ; set allow default to true for AllowPortraitDefault
    bl AllowPortraitDefault ; use normal portrait if pain is missing
    b ReturnPoint ; go back to the vanilla code where we left off! could alternatively do push r14 / pop r15 but that's LAME
.endarea
