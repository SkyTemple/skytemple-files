; Target: 2048 indep. entries
.definelabel NbIndepEntries, 0x800
.definelabel DungeonDataStructSize, 0x2CA70+NbIndepEntries*3
.definelabel MDDRec_H, 0x2C800 ; TODO EXPAND_POKE_LIST: Unsure this is correct
.definelabel MDDRec_L, 0x314-DUNGEON_DIFF_A4 ; TODO EXPAND_POKE_LIST: Unsure this is correct
.definelabel MDDSpr_H, 0x2D000 ; TODO EXPAND_POKE_LIST: Unsure this is correct
.definelabel MDDSpr_L, 0x314-DUNGEON_DIFF_A4 ; TODO EXPAND_POKE_LIST: Unsure this is correct
.definelabel Pkmn_StrID_H, 0x4A00
.definelabel Pkmn_StrID_L, 0x42
.definelabel Cate_StrID_H, 0x5200
.definelabel Cate_StrID_L, 0x42
.definelabel PokedexMax, 0x4A0
