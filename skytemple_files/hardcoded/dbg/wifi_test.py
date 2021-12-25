from ndspy.rom import NintendoDSRom
from skytemple_files.common.util import get_binary_from_rom_ppmdu, get_ppmdu_config_for_rom, set_binary_in_rom_ppmdu
from skytemple_files.hardcoded.wifi import HardcodedWifi

CERT = bytes.fromhex("""
B3 CD 79 97 77 5D 8A AF 86 A8 E8 D7 73 1C 77 DF
10 90 1F 81 F8 41 9E 21 55 DF BC FC 63 FB 19 43
F1 F6 C4 72 42 49 BD AD 44 68 4E F3 DA 1D E6 4D
D8 F9 59 88 DC AE 3E 9B 38 09 CA 7F FF DC 24 A2
44 78 78 49 93 D4 84 40 10 B8 EC 3E DB 2D 93 C8
11 C8 FD 78 2D 61 AD 31 AE 86 26 B0 FD 5A 3F A1
3D BF E2 4B 49 EC CE 66 98 58 26 12 C0 FB F4 77
65 1B EA FB CB 7F E0 8C CB 02 A3 4E 5E 8C EA 9B
""".replace(" ", "").replace("\n", ""))

with open('/tmp/out.bin', 'wb') as f:
    f.write(CERT)

rom = NintendoDSRom.fromFile("/home/marco/dev/skytemple/skytemple/CLEAN_ROM/pmdsky.nds")
ppmdu = get_ppmdu_config_for_rom(rom)
ov00 = get_binary_from_rom_ppmdu(rom, ppmdu.binaries['overlay/overlay_0000.bin'])

assert CERT == HardcodedWifi.get_nas_nintendowifi_net_pubkey(ov00, ppmdu)

with open('/home/marco/.config/wingull-flight-center/tls.der.pub.nds', 'rb') as f:
    tls = f.read()

HardcodedWifi.set_nas_nintendowifi_net_pubkey(tls, ov00, ppmdu)
set_binary_in_rom_ppmdu(rom, ppmdu.binaries['overlay/overlay_0000.bin'], ov00)
rom.saveToFile("/home/marco/dev/skytemple/skytemple/skyworkcopy_edit.nds")

with open('/tmp/ov00_after.bin', 'wb') as f:
    f.write(ov00)

# US: Ov 0: 0x5cdc8, 0x5da34
# EU: Ov 0: 0x5cca8, 0x5d914
