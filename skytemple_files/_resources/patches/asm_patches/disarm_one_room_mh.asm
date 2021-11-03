.if PPMD_GameVer == GameVer_EoS_NA
    .definelabel GenerateMHCall, 0x233C834
.elseif PPMD_GameVer == GameVer_EoS_EU
    .definelabel GenerateMHCall, 0x233D418
.endif

; The giant room will exist by this point, just don't make it a monster house
.org GenerateMHCall
.area 4
    nop
.endarea
