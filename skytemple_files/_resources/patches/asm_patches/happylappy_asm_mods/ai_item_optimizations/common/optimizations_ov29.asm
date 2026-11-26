.org GetAiUseItemProbability
.area AreaEnd - GetAiUseItemProbability 
; Changelog
;   - Removed Unused Warp Seed Ally Code (saved 8 instructions)

    stmdb sp!,{r3,r4,r5,r6,r7,r8,r9,lr}; Push a bunch of registers, we need room to "function"
    mov r7,r0; Keep our precious monster pointer safe
    mov r0,#0x0;
    mov r4,#0x0;
    and r5,r2,0x1; If r5 is 0x1, the item is being thrown!
    ldr r6,[r7,#0xb4]; Extract the monster pointer, or smthn. We'll use r6 to check the monster's data  
    ldrsh r1,[r1,#0x4]; Extract the item ID
    
    cmp r1,#0x5e; Vile seed.
    cmplt r1,#0x0a; Sticks and Stones...
    cmple r5,#0x1;
        beq odds_70; 

    cmp r1,#0x0e; Y-Ray Specs
    cmpne r1,#0x0f; Gaggle Specs
    cmpne r1,#0x6b; Via Seed ???
    cmpne r1,#0x75; Oren Berry ???
    cmpne r1,#0xa8; Wander Gummi ???
        beq IsGaggleOrYRaySpecs; If Throwing, 80%

    cmp r1,#0x14; Patsy Band
        beq odds_40; In general, 40% (shouldn't be usable though)

    cmp r1,#0x22; Diet Ribbon
        beq IsDietRibbon; If Throwing at non-zero belly, 50%

    cmp r1,#0x2F; Whiff Specs
    cmpne r1, 0x30; No-Aim Scope
        beq IsWhifforNoAim; If Throwing, 50%

    subs r2, r1,#0x45
    bmi Continue
    cmp r1, #0x5D
    addlt pc, pc, r2, lsl #0x2
        b Continue
        b IsHealSeed; If Negative Status, 80%
        b IsOranOrSitrusBerry; If HP >= Max, 0%. If Below Quarter health...
        b IsOranOrSitrusBerry; If HP >= Max, 0%. If Below Quarter health...
        b IsEyeDropSeed; If not EyeDropped (Goggle Specs counts!): If adjacent to enemy, 80%, else 5%.
        b odds_0; Reviver Seed
        b IsBlinkerSeed; If not blinded: If adjacent to enemy, 80%, else 5%.
        b IsDoomSeed; If not level 1, 80%
        b IsXEyeSeed; If not Cross-Eyed: If adjacent to enemy, 80%, else 5%.
        b IsLifeSeed; If Thrown: If Adjacent to Enemy, 100%, else 10%.
        b IsRawstBerry; If Burned, 50% chance.
        b IsHungerSeed; If non-zero belly, 50% chance.
        b IsQuickSeed; If +3 or slower: if Adjacent to enemy, 80%, else 5%.
        b IsPechaBerry; If Poisoned or Badly Poisoned: If Adjacent to enemy, 50%, else 100%.
        b IsCheriBerry; If Paralyzed: If Adjacent to enemy, 30%, else 80%.
        b IsTotterSeed; If Not Confused: If Adjacent to enemy, 15%, else 80%.
        b IsSleepSeed; If Not Asleep/Nightmared/Napping: If Adjacent to Enemy, 5%, else 80%. (Just check the list instead, the Ai is better off)
        b odds_0; Plain Seed
        b IsWarpSeed; If Adjacent, 40% else 5%.
        b IsBlastSeed; If Adjacent to Enemy, 80%, else 30%
        b odds_80; IN GENERAL, 80%
        b IsJoySeed; If level <= 99, 80%
        b IsChestoBerry; If Not Sleepless, 5%
        b IsStunSeed; If not stunned: If Adjacent to Enemy, 80%, else 5%.
        b IsHealSeed; If Negative Status, 80%
Continue:
    cmp r1,#0x60; Violent Seed
        beq IsViolentSeed; If below +20 (+10) SPA, 80%. (Never checks ATK)
    
    cmp r1,#0x61; Vanish Seed
        beq IsVanishSeed; If not invisible, 80%.
    
    cmp r1,#0x63; Max Elixir
        beq IsMaxElixir; Scales with PP use: (+30% per empty move slot, +6% for not-filled move slots). Caps at 99%... for some reason

    cmp r1,#0x74; Mix Elixir
        beq IsMixElixir; If target is a linoone, same as Max Elixir!

    cmp r1,#0x6c; Zinc
        addeq r4, #0x1; SPDEF is stat 4
    cmpne r1,#0x66; Iron
        addeq r4, #0x1; DEF is stat 3
    cmpne r1,#0x65; Calcium
        addeq r4, #0x1; SPA is stat 2
    cmpne r1,#0x64; Protein
        addeq r4, #0x1a; Stat offset is 0x1a (+1 for each subsequent stat!)  
        beq VitaminCheck;  If STAT < 250, 100%.

    cmp r1,#0x68; DropEye Seed
        beq IsDropEye; If Throwing and Not Drop-Eyed, 80%.

    cmp r1,#0x6a; Slip Seed
        beq IsSlipSeed; If mobility type isn't 0 or 4, and not slipping: If Adjacent to Enemy, 100%, else 10%.

    cmp r1,#0x6d; Apple
    cmpne r1,#0x6e; Big Apple
    cmpne r1,#0x70; Huge Apple
        beq IsApple; If Belly < 10, 100%.

    cmp r1,#0x6f; Grimy Food
        beq odds_30; IN GENERAL, 30%. 
     
    cmp r1,#0x76; Dough Seed
        beq IsDoughSeed; If on the team, 100%. (In other words, wild dungeon pokemon cannot use this!)

    cmp r1,#0x89; Gravelyrock
        beq IsGravelyrock; If Bonsly or Sudowoodo, If thrown 70%, Used 100%.
    
    cmp r1,#0xa7; Gone Pebble
        beq IsGonePebble; If not enduring, and adjacent to an enemy, 80%.

    eor r1,#0x100; If 0x14F, becomes 0x4F.
    cmp r1,#0x4F; Rollcall Orb
        cmpeq r5,#0x0; If using...    
            moveq r0,#20; Add 20%   
            beq exit; Exit with whatever % we have!
    ; See the Optimizations patch for info on how to better set up item IDs above 0xFF;
    ; Any item NOT listed above will never be used by the AI.
odds_0:
    mov r0, #0; reset it just to prevent random 1% use chances...
    b exit;   


ComputeHunger:
; Returns hunger in r4, leaves r0 as it was found!
    push r0,r2,r14;
    add r0, r6, #0x100
    ldrh r1, [r0, #0x46]
    sub r2, sp, #4
    strh r1, [r2]
    ldrh r0, [r0, #0x48]
    strh r0, [r2, #2]
    ldr r0, [r2]
    bl CeilFixedPoint
    mov r4, r0;
    pop r0,r2,r15;

IsDietRibbon:
    cmp r5,#0x0; If using...
    beq odds_0;
IsHungerSeed:
    bl ComputeHunger; Custom function above. Returns hunger in r4.
    cmp r4,#0
    beq odds_0;
    b odds_50;  
 
IsWhifforNoAim:
    cmp r5,#0x1; If throwing... 
True_50_False_0:
    beq odds_50;    
    b odds_0;

; These lines are stupidly common. Might as well make a proper function!
Adjacent2Enemy:
    push r14;
    mov r0,r7; 
    bl IsAdjacentToEnemy
    cmp r0,#0x1;
    mov r0,#0; Setting r0 to zero here to ensure that non-zero probabilities will return uninflated probabilities!
    pop r15;

IsOranOrSitrusBerry:
    mov r0,r7;
    bl HasLowHealth;
    cmp r0,#0x1; If true, has low health
    mov r0,#0x0;
    bne odds_0; If not below 1/4 HP, don't bother!  
    cmp r5,#0x1; If throwing...
    beq odds_50;
Adjacent_100_50:
    bl Adjacent2Enemy;
    beq odds_100; 
    b odds_50;

IsMixElixir:
; I'm not touching that loop. I WILL make Mix Elixirs use their own label though!  
    ldrsh r0,[r6,#0x4]; Get apparent species 
    bl FemaleToMaleForm;
    cmp r0,#0x124; Is it Linoone?
    bne odds_0; No, so 0%.
IsMaxElixir:
    mov r8,#0x0; Counts the number of moves examined so far
    add r7,r6,#0x124; Despite coincidentally being Zigzagoon's ID, this is an offest for move slots!
ElixirBeginLoop:
    add r9,r7,r8, lsl #0x3; r9 = r7 + (r8 << 3); Adjust the pointer to the "r8th" move slot.
    ldrb r2, [r9,#0x0]; Loads move data bitfield for the "r8th" move the mon knows
    ands r2,#0x1; Returns True of r2 & 0x1 == 0
    beq ElixirEndLoop; The mon has no move in this slot!
    ldrh r3, [r9,#0x6]; Loads remaining PP for the "r8th" move move the mon knows
    cmp r3,#0;
    addeq r4,#30; Add 30 if the mon is out of PP for this move!
    mov r0,r9; r0 is reset here, so we don't need to erase it
    bl GetMaxPpWrapper
    cmp r0,r3; If Max PP > Current PP...
    addgt r4,#6; Add 6 if the mon is not at full PP for this move!
    add r8,#1;
    cmp r8,#4;
    ble ElixirBeginLoop;
ElixirEndLoop:
    cmp r4,#99; If the odds are over 99%...
    movgt r4,#99; Make the odds 99%. (This is base-game, and stupid!) 
    mov r0,r4; Put the odds into r0!
    b exit; Custom odds, so go to exit directly!  

IsHealSeed:
    mov r0,r7    
    mov r1,#0x1    
    bl MonsterHasNegativeStatus
    cmp r0,#0x1; If has negative status...
True_80_False_0:
    mov r0,#0;
    beq odds_80; 
    b odds_0;

VitaminCheck:
    ldrb r4,[r6,r4]; Extract SPDEF stat
    cmp r4,#0xFA; If STAT >= 250...  
    bcs odds_0;
    b odds_100;

IsLifeSeed:
    cmp r5,#0x1; If throwing...     
False_Adjacent_10_100:
    bne odds_0;
    bl Adjacent2Enemy;
    beq odds_10;  
    b odds_100;    
 
IsEyedropSeed:
    mov r0,r7    
    bl CanSeeInvisibleMonsters
    cmp r0,#0x1; Can see invisible Mons. AKA Has Eyedrop Status!
False_Adjacent_80_5:
    beq odds_0;
Adjacent_80_5:
    bl Adjacent2Enemy;
    beq odds_80;   
    b odds_5;

IsQuickSeed:
    ldr r4,[r6,#0x110]; Get current speed stage   
    cmp r4,#0x3; Compare against 3.
    bgt odds_0; If above 3, don't use!  
    b Adjacent_80_5; 

IsXEyeSeed:
    ldrb r4,[r6,#0xf1]; Get BlindClass Status   
    cmp r4,#0x2; If Cross-Eyed...
    b False_Adjacent_80_5;
  
IsCheriBerry:
    ldrb r4,[r6,#0xbf]; Get BurnClass Status (which contains paralysis) 
    cmp r4,#0x4; If Paralyzed...
    bne odds_0;   
IsBlastSeed:
Adjacent_80_30:
    bl Adjacent2Enemy;
    beq odds_80;   
    b odds_30; 

IsTotterSeed:
    ldrb r4,[r6,#0xd0]; Get CringeClass Status (which contains Confusion)   
    cmp r4,#0x2; If Confused...
    beq odds_0;   
Adjacent_80_15:
    bl Adjacent2Enemy;
    subne r0,#65;
    b odds_80;

IsPechaBerry:
    ldrb r4,[r6,#0xbf]; Get BurnClass Status (which contains all poison types)   
    cmp r4,#0x2; If Poisoned
    cmpne r4,#0x3; Else If Badly Poisoned
    bne odds_0; Only bother using if Poisoned!  
    b Adjacent_100_50;

IsBlinkerSeed:
    mov r0,r7    
    mov r1,#0x1    
    bl IsBlinded
    cmp r0,#0x1    
    b False_Adjacent_80_5;

IsWarpSeed:
    bl Adjacent2Enemy;
    beq odds_40;    
    b odds_5;   

IsSleepSeed:
    mov r0,r7;
    bl IsMonsterSleeping
    b False_Adjacent_80_5;

IsChestoBerry:
    ldrb r4,[r6,#0xbd]; Get SleepClass Statuses   
    cmp r4,#0x2; Is Sleepless?
    beq odds_0; Don't try it!    
    b odds_5; Otherwise, 5% at all times (???)

IsJoySeed: 
    ldrb r4,[r6,#0xa]; Get current level   
    cmp r4,#0x63; Compare against 99...
    bgt odds_0;
IsGinseng:
    b odds_80;

IsRawstBerry:
    ldrb r4,[r6,#0xbf]; Get BurnClass Statuses   
    cmp r4,#0x1; If Burned...
    beq odds_50;
    b odds_0;

IsDoomSeed:
    ldrb r4,[r6,#0xa]; Get current level   
    cmp r4,#0x1; If level greater than 1...
    bgt odds_80;
    b odds_0;

IsStunSeed:
    ldrb r4,[r6,#0xc4]; Get FreezeClass Statuses  
    cmp r4,#0x6; If Stunned...
    b False_Adjacent_80_5;

IsDoughSeed:
    ldrb r4,[r6,#0x6]; Check if on the team   
    cmp r4,#0x0; If on team...
    bne odds_0; Enemies will never use this!!!
    b odds_100;
   
IsSlipSeed:
    ldrsh r0,[r6,#0x2]; Get true species (Ditto)  
    ldrb r1,[r6,0xef]; Get Invisibility Class Status (Slip is 0x4, 0x5 and beyond is unused!)
    lsr r1,#0x2; Is Slipping?
    bl GetMobilityTypeCheckSlip
    cmp r0,#0x0
    cmpne r0,#0x4
    b False_Adjacent_10_100;

IsGonePebble: 
    ldrb r4,[r6,#0xd5]; Get ReflectClass Statuses   
    cmp r4,#0x9; If Enduring...
    beq odds_0;    
Adjacent_0_80:
    bl Adjacent2Enemy;
    b True_80_False_0;

IsViolentSeed:
    ldrsh r4,[r6,#0x26]; Retrieve SPA value (Bug? Should also check ATK)   
    cmp r4,#0x14; 
    bge odds_0;    
    b odds_80;
  
IsVanishSeed:
    ldrb r4,[r6,#0xef]; Get InvisibleClass Statuses   
    cmp r4,#0x1; If Invisible...
    bne odds_0;
    b odds_80;
  
IsApple:
    bl ComputeHunger;
    cmp r4,#0xa; If belly below 10...
    blt odds_100;
    b odds_0;  

IsDropEye:
    ldrb r4,[r6,#0xf1]; Get BlindClass Status 
    cmp r4,#0x4; If DropEyed...
    beq odds_0;
    b odds_80;

IsGaggleOrYRaySpecs:
    cmp r5,#0x1; If throwing...
    b True_80_False_0;

IsGravelyrock:
    ldrsh r4,[r6,#0x4]; Get Apparant Species, This is bugged to only check males!
    cmp r4,#0x1e0; Is Bonsly?    
    cmpne r4,#0xb9; Is Sudowoodo?
    bne odds_0;   
    cmp r5,#0x1; If Throwing...   
    beq odds_70;
    ; Else continue to odds_100
; This is an instruction-efficient way to get the probability for a specific label. 
odds_100:
    add r0,#20; 20 + 10 + 20 + 10 + 10 + 20 + 5 + 5 = 100
odds_80:
    add r0,#10; 10 + 20 + 10 + 10 + 20 + 5 + 5 = 80
odds_70:
    add r0,#20; 20 + 10 + 10 + 20 + 5 + 5 = 70
odds_50:
    add r0,#10; 10 + 10 + 20 + 5 + 5 = 50
odds_40:
    add r0,#10; 10 + 20 + 5 + 5 = 40
odds_30:
    add r0,#20; 20 + 5 + 5 = 30
odds_10:
    add r0,#5; 5 + 5 = 10
odds_5:
    add r0,#5; 5 = 5
exit:     
    ldmia sp!,{r3,r4,r5,r6,r7,r8,r9,pc} 
FreeSpaceStart:
    .fill AreaEnd - FreeSpaceStart, 0
.endarea