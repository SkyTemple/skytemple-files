; For use with ARMIPS
; 2021/04/10
; For Explorers of Sky JP Only
; ------------------------------------------------------------------------------
; Change the evo system
; ------------------------------------------------------------------------------

.relativeinclude on
.nds
.arm

.definelabel FillWithZeros2BytesArray, 0x0200326C

.definelabel GetItemPosition, 0x0200D278

.definelabel GetGender, 0x02052AE0
.definelabel GetSpriteSize, 0x02052B18
.definelabel CanEvolve, 0x02052CB4
.definelabel GetEvoParameters, 0x02052DE8

.definelabel GetEvolutions, 0x020541C0

.definelabel IsRecruited, 0x02055480

.definelabel GetEvolutionPossibilities, 0x02059E14

.definelabel EuclidianDivision, 0x0209018C

.definelabel EvoAddStats1, 0x0238C154
.definelabel EvoAddStats2, 0x0238D164
.definelabel MainEvoMenuStruct, 0x0238E3C0

.definelabel RandMax, 0x022EC100
.definelabel GetRandomSpawnPkmnID, 0x0233935C
.definelabel GenerateMissionEggPkmn, 0x023498A0
.definelabel GMEPSize, 0x180
