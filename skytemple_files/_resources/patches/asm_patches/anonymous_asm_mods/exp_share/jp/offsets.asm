; For use with ARMIPS
; 2023/09/22
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Adds Exp. Share
; ------------------------------------------------------------------------------


.definelabel GetSpecialEpisode, 0x0204CC98
.definelabel PartyPkmnStructPtr, 0x020B22BC
.definelabel IsLevel1Dungeon, 0x02051668
.definelabel IsExpEnabledInDungeon, 0x02051A6C
.definelabel GetLvlStats, 0x02053AD4
.definelabel HookSummary, 0x0205A884
.definelabel EuclidianDivision, 0x0209018C

.definelabel ExpGainAll, 0x0230BD50
.definelabel ReadjustExp, 0x02304604
.definelabel HookLvlUp, 0x02303D48

.definelabel DungeonDataStructPtr, 0x023547B8

.definelabel BuffRead, 0x020980DC-0xC ; Add it if it is even implemented
.definelabel SummaryFunc, BuffRead-0xC
.definelabel ReadjustExpFunc, SummaryFunc-0x10
.definelabel ExpShare, ReadjustExpFunc-0x120

.definelabel PartyPkmnNb, 0x22B
.definelabel MaxLvl, 0x64
.definelabel PartyPkmnSize, 0x44
; .definelabel PercentageShared, 0x64
.definelabel MaxPercent, 0x64

.definelabel ValueMaxHP, 0x02303F80
.definelabel ValueText, 0x02303F84
.definelabel GetTacticsLearned, 0x02058F98
.definelabel StoreExp, 0x0234C30C
.definelabel HookLvlUpJump5, 0x0234C2A4
.definelabel HookLvlUpJump6, 0x02301814
.definelabel HookLvlUpJump7, 0x0234C708
.definelabel HookLvlUpJump8, 0x02304588


.definelabel SwitchCaseGS, 0x0238CCC0
.definelabel CaseJS, 0x0238CE64
.definelabel IsMaxLevel, 0x0230C320
.definelabel SetDialogueMaxLevel, 0x0238E084
.definelabel AddLevels, 0x0230B8BC
.definelabel EndSwitch, 0x0238D248
