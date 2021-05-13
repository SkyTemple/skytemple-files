; For use with ARMIPS
; 2021/04/10
; For Explorers of Sky NA Only
; ------------------------------------------------------------------------------
; Change the evo system
; ------------------------------------------------------------------------------

.relativeinclude on
.nds
.arm

.definelabel FillWithZeros2BytesArray, 0x0200326C

.definelabel GetItemPosition, 0x0200D278

.definelabel GetGender, 0x020527A8
.definelabel GetSpriteSize, 0x020527E0
.definelabel CanEvolve, 0x0205297C
.definelabel GetEvoParameters, 0x02052AB0

.definelabel GetEvolutions, 0x02053E88

.definelabel IsRecruited, 0x02055148

.definelabel GetEvolutionPossibilities, 0x02059B18

.definelabel EuclidianDivision, 0x0208FEA4

.definelabel EvoAddStats1, 0x0238ABF4
.definelabel EvoAddStats2, 0x0238BBF4
.definelabel MainEvoMenuStruct, 0x0238CE40

.definelabel RandMax, 0x022EAA98
.definelabel GetRandomSpawnPkmnID, 0x02337F98
.definelabel GenerateMissionEggPkmn, 0x023498A0
.definelabel GMEPSize, 0x1D0
