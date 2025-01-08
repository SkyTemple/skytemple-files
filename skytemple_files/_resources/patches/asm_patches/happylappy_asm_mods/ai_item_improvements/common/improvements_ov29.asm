.org AiOrbCheck
.area 0x4
    cmp r9,#16; This will always return false. Used to be a check for whether the item-category was "Orbs", but is completely neutered! 
.endarea

.org GetAiUseItemProbability
.area IsAdjacentToEnemy - GetAiUseItemProbability 
; Changelog
;   - Made Gold Thorns and Rare Fossils Throwable by the Ai!
;   - Fixed Gravelyrock bug that only checked male Bonsly and Sudowoodo.
;   - Fixed Violent Seed Bug that only checked SPA instead of both ATK and SPA
;   - Vile Seed now runs a check similar to Violent Seed to ensure foe is not at minimum defenses already
;   - Via Seeds now behave like Warp Seeds
;   - Gravelyrocks will be thrown unless the user or target is Sudowoodo/Bonsly
;   - Favored Gummis (Resisted or Better) will be eaten. Wonder/Wander/Nectar will always be eaten!
;   - Violent Seeds, Rebound Orbs, and All-Hit Orbs will be used at enemies over 3/4 HP!
;   - Warp/Via Seeds, Gone Pebbles, Vanish Seeds, Invisify Orbs, Rollcall Orbs (Enemies only), and Pure Seeds will be used if below 1/4 HP!
;   - Sleep Seeds now check for sleeplessness and yawning!
;   - Chesto Berries will only ever be used if sleeping, nightmared, or yawning!
;   - For Sticks and Stones, Team members have a throw chance that depends on the foe's HP!
;       - Allies have a 5% chance, unless the foe has low HP. If they do, it's an 80% chance! 
;       - Foes still have 70% throw chance.
;   - Allies will always use Rollcall Orbs if given one! Enemies will use them at low health!
;   - Grimy Food will be eaten at sufficiently low hunger, or thrown: 80% if the target is healthy, and 30% otherwise.
;   - Will use Weather Orbs if it would change the weather, and they "benefit" from the weather change
;       - Hail: Ice types only   Sandstorm: Rock, Ground, Steel     Sunny: Fire, Grass      Rainy: Water, Electric
;   - Will use Keys if they are in front of a Key Door
;   - Will use Drought Orbs if they cannot swim and secondary terrain is water!
;   - Will eat Blast Seeds if next to enemies!
;   - Will use Ginseng on themselves, rather than being forced to throw at an ally
;   - Oren Berries can be used or thrown on any low HP pokemon! (The Ai may eat or throw them!!!)
;   - Foes will only use Trawl Orbs if a Kec shop is NOT on the floor!

    stmdb sp!,{r3,r4,r5,r6,r7,r8,r9,lr}; Push a bunch of registers, we need room to "function"
    mov r7,r0; Keep our precious monster pointer safe
    and r5,r2,0x1; If r5 is 0x1, the item is being thrown!
    and r4,r2,0x2; If r4 is 0x2, the item is being used on an enemy!
    ldr r6,[r7,#0xb4]; Extract the monster pointer, or smthn. We'll use r6 to check the monster's data  
    mov r3, r1; Retain the Item Pointer in case we need it!
    ldrsh r1,[r1,#0x4]; Extract the Item ID.
    b label1
ItemChecks:
    cmp r1,#0x0a; Sticks and Stones
        ble SticksAndStones; If Throwing, 70% (If teammate, 20% + 0.5 * ItemsHeld)

    cmp r1,#0x0e; Y-Ray Specs
    cmpne r1,#0x0f; Gaggle Specs
        beq IsGaggleOrYRaySpecs; If Throwing, 80%

    cmp r1,#0x14; Patsy Band
        beq odds_40; In general, 40% (shouldn't be usable though)

    cmp r1,#0x22; Diet Ribbon
        beq IsDietRibbon; If Throwing at non-zero belly, 50%

    cmp r1,#0x2F; Whiff Specs
    cmpne r1, 0x30; No-Aim Scope
        beq IsWhifforNoAim; If Throwing, 50%

    cmp r1,#0x45; Heal Seed
    cmpne r1,0x5C; Gabite Scale
        beq IsHealSeed; If Negative Status, 80%

    cmp r1,#0x46; Oran Berry
    cmpne r1,#0x47; Sitrus Berry
    cmpne r1,#0x75; Oren Berry
        beq IsOranOrSitrusBerry; If HP >= Max, 0%. If Below Quarter health...
        ; If below 1/4 and Throwing: 50%
	    ; If below 1/4 and Using: if adjacent to Enemy 100%, else 50%

    cmp r1,#0x48; EyeDrop Seed
        beq IsEyeDropSeed; If not EyeDropped (Goggle Specs counts!): If adjacent to enemy, 80%, else 5%.
    
    cmp r1,#0x4a; Blinker Seed
        beq IsBlinkerSeed; If not blinded: If adjacent to enemy, 80%, else 5%.
    
    cmp r1,#0x4B; Doom Seed
        beq IsDoomSeed; If not level 1, 80%

    cmp r1,#0x4c; X-Eye Seed
        beq IsXEyeSeed; If not Cross-Eyed: If adjacent to enemy, 80%, else 5%.
    
    cmp r1,#0x4d; Life Seed
        beq IsLifeSeed; If Thrown: If Adjacent to Enemy, 10%, else 100%.
    
    cmp r1,#0x4e; Rawst Berry
        beq IsRawstBerry; If Burned, 50% chance.     
    
    cmp r1,#0x4f; Hunger Seed
        beq IsHungerSeed; If non-zero belly, 50% chance.
    
    cmp r1,#0x50; Quick Seed
        beq IsQuickSeed; If +3 or slower: if Adjacent to enemy, 80%, else 5%.   
    
    cmp r1,#0x51; Pecha Berry
        beq IsPechaBerry; If Poisoned or Badly Poisoned: If Adjacent to enemy, 50%, else 100%.
    
    cmp r1,#0x52; Cheri Berry
        beq IsCheriBerry; If Paralyzed: If Adjacent to enemy, 30%, else 80%.
    
    cmp r1,#0x53; Totter Seed
        beq IsTotterSeed; If Not Confused: If Adjacent to enemy, 15%, else 80%.
    
    cmp r1,#0x54; Sleep Seed
        beq IsSleepSeed; If Not immune to sleep or sleeping (Sleepless, Nightmared, Napping, Yawning, Asleep), Adjacent 80/5 Use!

    cmp r1,#0x56; Warp Seed
        cmpne r1,#0x6b; Via Seed
        beq IsWarpSeed; If Using, HP must be low. If throwing, Adjacent 40/5. 

    cmp r1,#0x57; Blast Seed
        beq IsBlastSeed; If Adjacent to Enemy, 80%, else 30%

    cmp r1,#0x58; Ginseng
        beq IsGinseng; If first move slot can be Ginsenged, 80% chance. Else 0. 
    
    cmp r1,#0x59; Joy Seed
        beq IsJoySeed; If level <= 99, 80%
    
    cmp r1,#0x5a; Chesto Berry
        beq IsChestoBerry; If Not Sleepless, 5%
    
    cmp r1,#0x5b; Stun Seed
        beq IsStunSeed; If not stunned: If Adjacent to Enemy, 80%, else 5%.
    
    cmp r1,#0x5e; Vile Seed
        beq IsVileSeed; If Throwing, and target would lose defense, 70% 
    
    cmp r1,#0x5f; Pure Seed
        beq IsPureSeed; Use if HP low enough

    cmp r1,#0x60; Violent Seed
        beq IsViolentSeed; If above 3/4 HP and below +20 (+10) SPA OR ATK, 80%.
    
    cmp r1,#0x61; Vanish Seed
        beq IsVanishSeed; If not invisible and below 1/4 HP, 80%.
    
    cmp r1,#0x63; Max Elixir
        beq IsMaxElixir; Scales with PP use: (+30% per empty move slot, +6% for not-filled move slots). Caps at 99%... for some reason

    cmp r1,#0x74; Mix Elixir
        beq IsMixElixir; If target is a linoone, same as Max Elixir!

    cmp r1,#0x64; Protein
        beq IsProtein; If ATK < 250, 100%. 
        
    cmp r1,#0x65; Calcium
        beq IsCalcium; If SPATK < 250, 100%.
        
    cmp r1,#0x66; Iron
        beq IsIron; If DEF < 250, 100%.

    cmp r1,#0x68; DropEye Seed
        beq IsDropEye; If Throwing and Not Drop-Eyed, 80%.

    cmp r1,#0x6a; Slip Seed
        beq IsSlipSeed; If mobility type isn't 0 or 4, and not slipping: If Adjacent to Enemy, 100%, else 10%.
       

    cmp r1,#0x6c; Zinc
        beq IsZinc; If SPDEF < 250, 100%.
        
    cmp r1,#0x6d; Apple
    cmpne r1,#0x6e; Big Apple
    cmpne r1,#0x70; Huge Apple
        beq IsApple; If Belly < 10, 100%.

    cmp r1,#0x6f; Grimy Food
        beq IsGrimyFood; If thrown, 30%. If using, only use at low belly!
     
    cmp r1,#0x76; Dough Seed
        beq IsDoughSeed; If on the team, 100%. (In other words, wild dungeon pokemon cannot use this!)

    cmp r1,#0x89; Gravelyrock
        beq IsGravelyrock; If Bonsly or Sudowoodo, If thrown 70%, Used 100%.
    
    cmp r1,#0xa7; Gone Pebble
        beq IsGonePebble; If not enduring, and adjacent to an enemy, 80%. 5% throw chance
    
    cmp r1,#0xa8; Wander Gummi
    cmpne r1,#0x67; Nectar
    moveq r1,#0x88; Pretend is Wonder Gummi
    .if AddTypesApplied
    cmpne r1,#0x8A; All Gummis! (Will not catch Gravelyrock bc that was checked above!)
    .else
    cmpne r1,#0x87; All Gummis! (Will not catch Gravelyrock bc that was checked above!)
    .endif
        movle r2,#0x77; 
        cmple r2,r1; ID between 0x77 and 0x8A (or 0x87 if Fairy Gummi doesn't exist!)
        ble IsGummi;
    
    cmp r1,#0xB6; Key
        beq IsKey;

    cmp r1,#0xFF; Giga Impact TM (has no actual interaction, yet...)
        ble odds_0; If not above #0xFF, the ride ends here!
    
    sub r1,#0x100; Now do the same checks for IDs 0x100-0x1FF, except the immediates are all legal again!

    cmp r1,#0x2D; Hail Orb
        beq IsHailOrb; If Ice-Type and not hailing, 80% to use. Neglects abilities

    cmp r1,#0x2E; Sunny Orb
        beq IsSunnyOrb; If Fire or Grass and not Sunny, 80% to use. Neglects abilities

    cmp r1,#0x2F; Rainy Orb
        beq IsRainyOrb; If Water or Electric and not Raining, 80% to use. Neglects abilities

    cmp r1,#0x31; Sandy Orb
        beq IsSandyOrb; If Ground, Rock, or Steel and not Sandy, 80% to use. Neglects abilities

    cmp r1,#0x30; Evasion Orb
        beq IsEmergencyOrb; Use if below 1/4 HP

    cmp r1,#0x36; Rebound Orb 
        cmpne r1,#0x66;  All-Hit Orb
        beq IsBolsteringOrb; If above 3/4 HP: 80% if Adjacent to an enemy, else 5%.
    
    cmp r1,#0x3E; Luminous Orb
        beq IsLuminousOrb; Same as Dough Seed. Only Teammates can use it.

    cmp r1,#0x42; Trawl Orb
        beq IsTrawlOrb; If Kec shop is on floor, 0%. Else 80%.

    cmp r1,#0x4D; Drought Orb 
    cmpne r1,#0x5C; Mobile Orb
        beq IsDroughtOrb; Same as Slip Seed.
    
    cmp r1,#0x4F; Rollcall orb
        beq IsRollCallOrb; 

    cmp r1,#0x50; Invisify Orb
        beq IsInvisifyOrb; Same as Vanish Seed

    cmp r1,#0xAB; All Unown Rocks
        movle r2,#0x90; 
        cmple r2,r1; ID between 0x77 and 0x8A
        ble SticksAndStones;
    ; Any item NOT listed above will never be used by the AI.
odds_0:
    mov r0, #0; reset it just to prevent random 1% use chances...
    b exit;   

WeatherOrbTypeCheck:
; Checks if the mon is the type specified in r1. Adds the result to r4, ensuring a cumulative check for use. 
    cmp r5,#0x1; If Throwing...
    beq odds_0; Don't bother
    push r0,r14;
    mov r0,r7
    bl MonsterIsType
    add r4,r0; If r0 is true, it is added to r4. 
    pop r0, r15;



;SmartCheckIfHoldingItem:
;    push r0, r14;
;    cmp r3,
;    ldr r0, [r6,#0x68]; Retrieve Target's held item pointer
;    ldrsh r0, [r0,#0x4]; Retrieve Target's held item ID.
;    cmp r0,#0x0; Is there a held item?
;    pop r0, r15;


SticksAndStones:
    cmp r5,#0x1; True if Thrown
    bne odds_0;
    ldrb r4,[r6,#0x6]; Check if on the team   
    cmp r4,#0x0; If not on team...
    beq odds_70;
    bl GetMaxAndRemainingHP;
    cmp r3,r2, LSR #0x2; If Remaining HP > Max HP Divided By 4...
    bge odds_5; If not below 1/4 HP, Low throwing chance!  
    b odds_80;

ComputeHunger:
; Returns hunger in r4, leaves r0 as it was found!
    push r0,r14;
    add r0, r6, #0x100
    ldrh r1, [r0, #0x46]
    sub r2, sp, #4
    strh r1, [r2]
    ldrh r0, [r0, #0x48]
    strh r0, [r2, #2]
    ldr r0, [r2]
    bl CeilFixedPoint
    mov r4, r0;
    pop r0,r15;

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

GetMaxAndRemainingHP:
; Returns Max HP in r2, and Remaining HP in r3. Leaves r0, r1, and r4 untouched!!!
    push r0,r1,r4,r14;
    ldr r4,=#999; +1 pool
    ldrsh r0,[r6,#0x12]; Get "Base Max" HP  
    ldrsh r1,[r6,#0x16]; Get Boosts to Max HP
    add r2,r0,r1; r2 = r0 + r1
    ldrsh r3,[r6,#0x10]; Get remaining HP
    cmp r2,r4;
    movgt r2,r4;
    cmp r3,r4;
    movgt r3,r4;
    pop r0,r1,r4,r15;

IsRollCallOrb:
    ldrb r4,[r6,#0x6]; Get team status
    cmp r4,#0x0; If on team...
    beq odds_100; Always use!
IsEmergencyOrb:
    cmp r5,#0x1; If Throwing
    beq odds_0; Don't use
IsOranOrSitrusBerry:
    bl GetMaxAndRemainingHP;
    cmp r3,r2, LSR #0x2; If Remaining HP > Max HP Divided By 4...
    bge odds_0; If not below 1/4 HP, don't bother!  
    cmp r5,#0x1; If throwing...
    beq odds_50;
Adjacent_100_50:
    mov r0,r7   
    bl IsAdjacentToEnemy
    cmp r0,#0x1; If true, IS Adjacent    
True_100_False_50:
    mov r0,#0;
    beq odds_100; 
    b odds_50;

IsBolsteringOrb:
    bl GetMaxAndRemainingHP;
    mov r1,#0x3;
    mul r2,r2,r1; Multiply HP by 3!
    cmp r3,r2, LSR #0x2; If Remaining HP > Max HP Divided By 4...
    ble odds_0; If not above 3/4 HP, don't bother!  
    b Adjacent_80_5;

IsMixElixir:
; I'm not touching that loop. I WILL make Mix Elixirs use their own label though!  
    ldrsh r1,[r6,#0x4]; Get apparent species 
    cmp r1,#0x124; Is it Linoone M?
    cmpne r1,#0x37c; No, but is it Linoone F?
    bne odds_0; No, so 0%.
IsMaxElixir:
    mov r8,#0x0; Counts the number of moves examined so far
    add r7,r6,#0x124; Despite coincidentally being Zigzagoon's ID, this is an offest for move slots!
    mov r4,#0x0;
ElixirBeginLoop:
    add r9,r7,r8, lsl #0x3; r9 = r7 + (r8 << 3); Adjust the pointer to the "r8th" move slot.
    ldrb r2, [r9,#0x0]; Loads move data bitfield for the "r8th" move the mon knows
    and r2,#0x1;
    cmp r2,#0x1; Does the mon have a move in this slot?
    beq ElixirEndLoop;
    ldrh r3, [r9,#0x6]; Loads remaining PP for the "r8th" move move the mon knows
    cmp r3,#0;
    addeq r4,#30; Add 30 if the mon is out of PP for this move!
    mov r0,r9;
    bl GetMaxPpWrapper
    cmp r0,r3; If Max PP > Current PP...
    addgt r4,#6; Add 6 if the mon is not at full PP for this move!
    add r8,#1;
    cmp r8,#4;
    ble ElixirBeginLoop;
ElixirEndLoop:
    cmp r4,#100; If the odds are over 99%...
    movgt r4,#100; Make the odds 99%. (This is base-game, and stupid!) 
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

IsProtein:
    ldrb r4,[r6,#0x1a]; Extract ATK stat   
    b VitaminCheck;

IsCalcium:
    ldrb r4,[r6,#0x1b]; Extract SPATK stat   
    b VitaminCheck;
    
IsIron:
    ldrb r4,[r6,#0x1c]; Extract DEF stat
    b VitaminCheck;

IsZinc:
    ldrb r4,[r6,#0x1d]; Extract SPDEF stat   
VitaminCheck:
    cmp r4,#0xFA; If STAT >= 250...  
    bcs odds_0;
    b odds_100;

IsLifeSeed:
    cmp r5,#0x1; If throwing...     
False_Adjacent_10_100:
    beq odds_0;
    mov r0,r7
    bl IsAdjacentToEnemy
    cmp r0,#0x1
    mov r0,#0;
    beq odds_10;  
    b odds_100;    
 
IsEyedropSeed:
    mov r0,r7    
    bl CanSeeInvisibleMonsters
    cmp r0,#0x1; Can see invisible Mons. AKA Has Eyedrop Status!
False_Adjacent_80_5:
    beq odds_0;
Adjacent_80_5:
    mov r0,r7   
    bl IsAdjacentToEnemy
    cmp r0,#0x1;
    mov r0,#0;
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
    mov r0,r7    
    bl IsAdjacentToEnemy
    cmp r0,#0x1 
    mov r0,#0x0
    beq odds_80;
    cmp r5,#0x1; If Throwing
    beq odds_30;
    b odds_0;

IsTotterSeed:
    ldrb r4,[r6,#0xd0]; Get CringeClass Status (which contains Confusion)   
    cmp r4,#0x2; If Confused...
    beq odds_0;   
Adjacent_80_15:
    mov r0,r7    
    bl IsAdjacentToEnemy
    cmp r0,#0x1 
    mov r0,#0x0
    beq odds_80;   
    b odds_15;

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
    mov r0,#0;
    b False_Adjacent_80_5;

IsPureSeed:
    cmp r5,#0x0; If using...
    cmpne r4,#0x2; If throwing at an ally...
    beq IsOranOrSitrusBerry; Treat as low HP item
    b odds_0;

IsWarpSeed:
    cmp r5,#0x0; If using...
    cmpne r4,#0x2; If throwing at an ally...
    beq IsOranOrSitrusBerry; Treat as low HP item
Adjacent_40_5:
    mov r0,r7    
    bl IsAdjacentToEnemy
    cmp r0,#0x0   
    mov r0,#0x0
    bne odds_40;    
    b odds_5;   

IsTrawlOrb:
    ldrb r4,[r6,#0x6]; Check if on the team   
    cmp r4,#0x0; If on team...
    beq odds_0; Don't use! (This way you can't test for Kec shops with trawl orbs!)
    ldr r4, =DUNGEON_PTR; +1 pool
    ldr r4,[r4];
    ldr r3,=0x40c6; +1 pool
    ldrb r4, [r4,r3];
    cmp r4, 0x0; If true, no Kec shop present!!!
    bne odds_0;
    b odds_80;

IsSleepSeed:
    ldrb r4,[r6,#0xbd]; Get SleepClass Statuses
    cmp r4,#0x0; If not Sleepless, Asleep, Napping, Nightmared, or Yawning...
    bne odds_0;
    b Adjacent_80_5;

IsChestoBerry:
    ldrb r4,[r6,#0xbd]; Get SleepClass Statuses   
    cmp r4,#0x2; Is Sleepless?
    cmpne r4,#0x0; Is Wide Awake?
    cmpne r4,#0x5; Is napping? (Aka using rest to restore HP)
    beq odds_0; Don't try it! 
    b odds_100; Otherwise, is afflicted with some kind of sleep, so use!

IsJoySeed: 
    ldrb r4,[r6,#0xa]; Get current level   
    cmp r4,#0x63; Compare against 99...
    bgt odds_0;
    b odds_80;

IsGinseng:
    add r7,r6,#0x124; Despite coincidentally being Zigzagoon's ID, this is an offest for move slots!
    mov r0,r7
    bl HasMaxGinsengBoost99;
    cmp r0,#0x1; 
    beq odds_80;
    b odds_0;

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

IsGrimyFood:
    cmp r5,#0x0; If Using...
    cmpne r4,#0x0; If Allied...
    beq IsApple; Treat like an apple
    mov r0,r7; Monster Struct   
    mov r1,#0x1; 
    bl MonsterHasNegativeStatus
    cmp r0,#0x1; If has negative status...
    beq odds_30; 30% chance to throw.
    b odds_80; 

IsLuminousOrb:
    cmp r5,#0x1; If Throwing
    beq odds_0; Don't bother
IsDoughSeed:
    ldrb r4,[r6,#0x6]; Check if on the team   
    cmp r4,#0x1; If not on team...
    beq odds_0; Enemies will never use this!!!
    b odds_100;

IsDroughtOrb:
    cmp r5,#0x1; If Throwing
    beq odds_0; Don't bother
IsSlipSeed:
    ldrsh r0,[r6,#0x2]; Get true species (Ditto)  
    bl GetMobilityType
    cmp r0,#0x0
    cmpne r0,#0x4    
    moveq r0,#0x1    
    movne r0,#0x0    
    tst r0,#0xff 
    mov r0,#0;
; "ldrneb" is fucking weird
    ldrneb r4,[r6,#0xef]; Get InvisibleClass Statuses  
    cmpne r4,#0x4; Is Slipping?
    b False_Adjacent_10_100;

IsGonePebble: 
    cmp r5,#0x1; If throwing...
    beq odds_5; 5% use chance
    ldrb r4,[r6,#0xd5]; Get ReflectClass Statuses   
    cmp r4,#0x9; If Enduring...
    beq odds_0;
    b IsEmergencyOrb;

IsVileSeed:
    ldr r4,[r6,#0x28]; Retrieve both DEF and SPDEF  
    cmp r5,#0x0; False if Thrown
    cmpne r4,#0x0; If both stats are zero...
    bne odds_70;    
    b odds_0;
    

IsViolentSeed:
    ldr r4,[r6,#0x24]; Retrieve both Atk and SPA
    ldr r3,=#0x140014; +1 pool
    cmp r4,r3; If ATK boosts are 20 or more...
    bge odds_0;
    b IsBolsteringOrb;
  
IsInvisifyOrb:
    cmp r5,#0x1; If Throwing...
    beq odds_0; Don't bother
IsVanishSeed:
    ldrb r4,[r6,#0xef]; Get InvisibleClass Statuses   
    cmp r4,#0x0; If NOT invisible... 
    beq IsOranOrSitrusBerry; Treat as low HP item
    b odds_0;
  
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

label1:
    ldrsh r0,[r6,#0x4]; Get Apparant Species
    push r1-r3;
    bl FemaleToMaleForm
    pop r1-r3;
    cmp r0,#0x83
    mov r0,#0x0;
    bne ItemChecks
    mov r2,#0x138;
    cmp r1,r2;
    addne r2,#1;
    cmpne r1,r2;
    addne r2,#8;
    cmpne r1,r2;
    beq odds_0; Fine I'll remove it Ches
    b ItemChecks;

IsHailOrb:
    mov r4,#0x0;
    mov r1,#0x6; Ice Type
    bl WeatherOrbTypeCheck
    mov r5,#0x5; Hail
    b WeatherOrbsCheck

IsSunnyOrb:
    mov r4,#0x0;
    mov r1,#0x2; Fire Type
    bl WeatherOrbTypeCheck
    mov r1,#0x4; Grass Type
    bl WeatherOrbTypeCheck
    mov r5,#0x1; Sunny
    b WeatherOrbsCheck

IsRainyOrb:
    mov r4,#0x0;
    mov r1,#0x3; Water Type
    bl WeatherOrbTypeCheck
    mov r1,#0x5; Electric Type
    bl WeatherOrbTypeCheck
    mov r5,#0x4; Rain
    b WeatherOrbsCheck

IsSandyOrb:
    mov r4,#0x0;
    mov r1,#0x9; Ground Type
    bl WeatherOrbTypeCheck
    mov r1,#0xD; Rock Type
    bl WeatherOrbTypeCheck
    mov r1,#0x11; Steel Type
    bl WeatherOrbTypeCheck
    mov r5,#0x2; Sandstorm
WeatherOrbsCheck:
    mov r0,r7;
    bl GetApparentWeather
    cmp r4,#0x0; Is the mon the wrong type?
    cmpne r0,r5; Is the weather already out?
    mov r0,#0x0;
    bne odds_80;
    b odds_0;

IsKey:
	cmp r5,0x1; If throwing...
    beq odds_0;
    ldrsh r1,[r7,#+0x6]; Get Y-Coord of monster
	ldrsh r0,[r7,#+0x4]; Get X-Coord of monster
	sub r1,r1,#0x1; Look one tile above
	bl GetTileSafe; Get that tile
	ldrh r0,[r0]; Load the tle
	tst r0,#0x1000; Is the tile a Key-Door? (False if so)
    mov r0,#0x0;
    bne odds_100;
    b odds_0;

IsGravelyrock:
    ldrsh r0,[r6,#0x4]; Get Apparant Species
    bl FemaleToMaleForm
    cmp r0,#0x1e0; Is Bonsly?    
    cmpne r0,#0xb9; Is Sudowoodo?
    mov r0,#0;
    bne SticksAndStones;
    cmp r4,#0x2; If Using/Throwing at a foe...   
    beq odds_0;
    ; Else continue to odds_100

; This is an instruction-efficient way to get the probability for a specific label. 
odds_100:
    add r0,#20; 20 + 10 + 20 + 10 + 10 + 10 + 5 + 5 + 5 + 5 = 100
odds_80:
    add r0,#10; 10 + 20 + 10 + 10 + 10 + 5 + 5 + 5 + 5 = 80
odds_70:
    add r0,#20; 20 + 10 + 10 + 10 + 5 + 5 + 5 + 5 = 70
odds_50:
    add r0,#10; 10 + 10 + 10 + 5 + 5 + 5 + 5 = 50
odds_40:
    add r0,#10; 10 + 10 + 5 + 5 + 5 + 5 = 40
odds_30:
    add r0,#10; 10 + 5 + 5 + 5 + 5 = 30
odds_20:
    add r0,#5; 5 + 5 + 5 + 5 = 20
odds_15:
    add r0,#5; 5 + 5 + 5 = 15
odds_10:
    add r0,#5; 5 + 5 = 10
odds_5:
    add r0,#5; 5 = 5
exit:     
    ldmia sp!,{r3,r4,r5,r6,r7,r8,r9,pc} 
IsGummi:
    .if AddTypesApplied
        cmp r1,#0x88; Wonder Gummi
        subgt r1,#0x2; Put Fairy Gummi in the right slot
        beq odds_80; If Wonder Gummi, 80% use chance!
        sub r1,#0x76; Convert Item ID to Gummi Type
        ;lsl r1,#0x1; Double Gummi Type to increment by half-words
        ldrb r2,[r6,#0x5E]; Get type 1
        ldrb r3,[r6,#0x5F]; Get type 2
        ldr r4,=IQ_GUMMI_GAIN_TABLE;
        mov r5,#0x19; Waste a register and an instruction bc MUL doesn't allow immediates :(
        ; Gummi Type 1
        smulbb r2,r2,r5; Multiply by 25 bytes (one table row)
        add r2,r2,r1; Add Gummi Type
        ldrb r2,[r4,r2]; Load the "r2th" entry of the Gummi IQ Table!
        ; Gummi Type 2
        smulbb r3,r3,r5; Multiply by 25 bytes (one table row)
        add r3,r3,r1; Add Gummi Type
        ldrb r3,[r4,r3]; Load the "r2th" entry of the Gummi IQ Table!
        cmp r2,r3; Compare the type results
        movlt r2,r3; Take the bigger gummi boost
        cmp r2, NeutralGummiBoost;
    .else
        cmp r1,#0x88; Wonder Gummi
        beq odds_80; If Wonder Gummi, 80% use chance!
        sub r1,#0x76; Convert Item ID to Gummi Type
        lsl r1,#0x1; Double Gummi Type to increment by half-words
        ldrb r2,[r6,#0x5E]; Get type 1
        ldrb r3,[r6,#0x5F]; Get type 2
        ldr r4,=IQ_GUMMI_GAIN_TABLE;
        mov r5,#0x24; Waste a register and an instruction bc MUL doesn't allow immediates :(
        ; Gummi Type 1
        smulbb r2,r2,r5; Multiply by 36 bytes (one table row)
        add r2,r2,r1; Add Gummi Type
        ldrsh r2,[r4,r2]; Load the "r2th" entry of the Gummi IQ Table!
        ; Gummi Type 2
        smulbb r3,r3,r5; Multiply by 36 bytes (one table row)
        add r3,r3,r1; Add Gummi Type
        ldrsh r3,[r4,r3]; Load the "r2th" entry of the Gummi IQ Table!
        cmp r2,r3; Compare the type results
        movlt r2,r3; Take the bigger gummi boost
        cmp r2, NeutralGummiBoost;
    .endif
    bgt odds_80; 80% Chance
    b odds_0;

.pool; Constants will go here. Currently 4 things in the pool!
; Put at the end because it has a variable amount of instructions.

FreeSpaceStart:
    .fill IsAdjacentToEnemy - FreeSpaceStart, 0
.endarea