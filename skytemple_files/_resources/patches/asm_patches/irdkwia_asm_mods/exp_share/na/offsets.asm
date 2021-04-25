; For use with ARMIPS
; 2021/04/25
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Adds Exp. Share
; ------------------------------------------------------------------------------


.definelabel GetSpecialEpisode, 0x0204C938
.definelabel PartyPkmnStructPtr, 0x020B0A48
.definelabel IsLevel1Dungeon, 0x02051318
.definelabel IsExpEnabledInDungeon, 0x0205171C
.definelabel GetLvlStats, 0x0205379C
.definelabel HookSummary, 0x0205A588
.definelabel EuclidianDivision, 0x0208FEA4

.definelabel ExpGainAll, 0x0230A7CC
.definelabel ReadjustExp, 0x023030B8
.definelabel HookLvlUp, 0x023027F8

.definelabel DungeonDataStructPtr, 0x02353538

.definelabel BuffRead, 0x02097DE8-0xC ; Add it if it is even implemented
.definelabel SummaryFunc, BuffRead-0xC
.definelabel ReadjustExpFunc, SummaryFunc-0x10
.definelabel ExpShare, ReadjustExpFunc-0x120

.definelabel PartyPkmnNb, 0x22B
.definelabel MaxLvl, 0x64
.definelabel PartyPkmnSize, 0x44
.definelabel PercentageShared, 0x64
.definelabel MaxPercent, 0x64


.definelabel HookLvlUpJump1, 0x02302810
.definelabel HookLvlUpJump2, 0x02058C9C
.definelabel HookLvlUpJump4, 0x0234B09C
.definelabel HookLvlUpJump5, 0x0234B034
.definelabel HookLvlUpJump6, 0x0230040C
.definelabel HookLvlUpJump7, 0x0234B498
.definelabel HookLvlUpJump8, 0x0230303C


.definelabel SwitchCaseGS, 0x0238B760
.definelabel CaseJS, 0x0238B904
.definelabel IsMaxLevel, 0x0230AD7C
.definelabel SetDialogueMaxLevel, 0x0238CB2C
.definelabel AddLevels, 0x0230A31C
.definelabel EndSwitch, 0x0238BCE8
