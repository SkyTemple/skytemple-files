import random

from ndspy.rom import NintendoDSRom
from range_typed_integers import u16, u8

from skytemple_files.container.sir0.handler import Sir0Handler
from skytemple_files.data.item_p.handler import ItemPHandler
from skytemple_files.data.item_p.protocol import ItemPEntryProtocol


def randomize_item_p_entry(entry: ItemPEntryProtocol):
    entry.buy_price = u16(random.randint(0, 65_535))
    entry.sell_price = u16(random.randint(0, 65_535))
    entry.category = u8(random.randint(0, 255))
    entry.sprite = u8(random.randint(0, 255))
    entry.item_id = u16(random.randint(0, 65_535))
    entry.move_id = u16(random.randint(0, 65_535))
    entry.range_min = u8(random.randint(0, 255))
    entry.range_max = u8(random.randint(0, 255))
    entry.palette = u8(random.randint(0, 255))
    entry.action_name = u8(random.randint(0, 255))
    entry.is_valid = bool(random.randint(0, 1))
    entry.is_in_td = bool(random.randint(0, 1))
    entry.ai_flag_1 = bool(random.randint(0, 1))
    entry.ai_flag_2 = bool(random.randint(0, 1))
    entry.ai_flag_3 = bool(random.randint(0, 1))


if __name__ == "__main__":
    rom = NintendoDSRom.fromFile("/tmp/rom.nds")

    item_p = ItemPHandler.load_python_model()(rom.getFileByName("BALANCE/item_p.bin"), 0)

    entries = item_p.item_list[0:6]

    randomize_item_p_entry(entries[0])
    randomize_item_p_entry(entries[1])
    randomize_item_p_entry(entries[2])
    randomize_item_p_entry(entries[3])
    randomize_item_p_entry(entries[4])
    randomize_item_p_entry(entries[5])

    item_p.item_list = entries

    with open("./fixture.bin", "wb") as f:
        f.write(Sir0Handler.serialize(Sir0Handler.wrap(*item_p.sir0_serialize_parts())))

    for md_index, entry in enumerate(item_p.item_list):
        print(
            f"ExpectedItemPEntry("
            f"u16({entry.buy_price}),"
            f"u16({entry.sell_price}),"
            f"u8({entry.category}),"
            f"u8({entry.sprite}),"
            f"u16({entry.item_id}),"
            f"u16({entry.move_id}),"
            f"u8({entry.range_min}),"
            f"u8({entry.range_max}),"
            f"u8({entry.palette}),"
            f"u8({entry.action_name}),"
            f"{entry.is_valid},"
            f"{entry.is_in_td},"
            f"{entry.ai_flag_1},"
            f"{entry.ai_flag_2},"
            f"{entry.ai_flag_3}"
            f"),"
        )
