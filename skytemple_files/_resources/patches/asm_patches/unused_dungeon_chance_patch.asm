.if (PPMD_GameVer == GameVer_EoS_NA)
  .definelabel Offset, 0x2340264
.elseif (PPMD_GameVer == GameVer_EoS_EU)
  .definelabel Offset, 0x2340E48
.endif

.org Offset
.area 4
    nop
.endarea
