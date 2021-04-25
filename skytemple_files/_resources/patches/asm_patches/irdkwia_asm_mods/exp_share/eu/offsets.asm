; For use with ARMIPS
; 2021/04/25
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Adds Exp. Share
; ------------------------------------------------------------------------------


.definelabel GetSpecialEpisode, 0x0204CC70
.definelabel PartyPkmnStructPtr, 0x020B138C
.definelabel IsLevel1Dungeon, 0x02051650
.definelabel IsExpEnabledInDungeon, 0x02051A54
.definelabel GetLvlStats, 0x02053B18
.definelabel HookSummary, 0x0205A904
.definelabel EuclidianDivision, 0x0209023C

.definelabel ExpGainAll, 0x0230B238
.definelabel ReadjustExp, 0x02303AE4
.definelabel HookLvlUp, 0x02303224

.definelabel DungeonDataStructPtr, 0x02354138

.definelabel BuffRead, 0x020981E4-0xC ; Add it if it is even implemented
.definelabel SummaryFunc, BuffRead-0xC
.definelabel ReadjustExpFunc, SummaryFunc-0x10
.definelabel ExpShare, ReadjustExpFunc-0x120

.definelabel PartyPkmnNb, 0x22B
.definelabel MaxLvl, 0x64
.definelabel PartyPkmnSize, 0x44
.definelabel PercentageShared, 0x64
.definelabel MaxPercent, 0x64


.definelabel HookLvlUpJump1, 0x0230323C
.definelabel HookLvlUpJump2, 0x02059018
.definelabel HookLvlUpJump4, 0x0234BC9C
.definelabel HookLvlUpJump5, 0x0234BC34
.definelabel HookLvlUpJump6, 0x02300E38
.definelabel HookLvlUpJump7, 0x0234C098
.definelabel HookLvlUpJump8, 0x02303A68


.definelabel SwitchCaseGS, 0x0238C29C
.definelabel CaseJS, 0x0238C440
.definelabel IsMaxLevel, 0x0230B718
.definelabel SetDialogueMaxLevel, 0x0238D660
.definelabel AddLevels, 0x0230ACB8
.definelabel EndSwitch, 0x0238C824
