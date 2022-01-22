; For use with ARMIPS
; 2021/04/10
; For Explorers of Sky EU Only
; ------------------------------------------------------------------------------
; Change the evo system
; ------------------------------------------------------------------------------

.relativeinclude on
.nds
.arm

.definelabel FillWithZeros2BytesArray, 0x0200326C

.definelabel GetItemPosition, 0x0200D300

.definelabel GetGender, 0x02052AE0
.definelabel GetSpriteSize, 0x02052B18
.definelabel CanEvolve, 0x02052CB4
.definelabel GetEvoParameters, 0x02052DE8

.definelabel GetEvolutions, 0x02054204

.definelabel IsRecruited, 0x020554C4

.definelabel GetEvolutionPossibilities, 0x02059E94

.definelabel EuclidianDivision, 0x0209023C

.definelabel EvoAddStats1, 0x0238B734
.definelabel EvoAddStats2, 0x0238C734
.definelabel MainEvoMenuStruct, 0x0238D980

.definelabel RandMax, 0x022EB448
.definelabel GetRandomSpawnPkmnID, 0x02338B68
.definelabel GenerateMissionEggPkmn, 0x0234A4A0
.definelabel GMEPSize, 0x1D0
