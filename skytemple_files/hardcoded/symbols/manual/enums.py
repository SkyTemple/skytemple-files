#  Copyright 2020-2025 SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.

# Contains information about the values of some enum types

from skytemple_files.hardcoded.symbols.unsupported_type_error import UnsupportedTypeError


class EnumValue:
    """
    Represents one of the possible value of an enum
    """

    # Integer representation of the value
    int_value: int
    # Name of the value
    name: str

    def __init__(self, int_value: int, name: str):
        self.int_value = int_value
        self.name = name


# List containing information about all enums that have been manually implemented.
# Each entry maps the name of the enum (without the "enum" prefix) to a list containing all its values.
KNOWN_ENUM_DATA = {
    "secondary_terrain_type": [
        EnumValue(0, "Water"),
        EnumValue(1, "Lava"),
        EnumValue(2, "Chasm"),
    ],
    "type_id": [
        EnumValue(0, "None"),
        EnumValue(1, "Normal"),
        EnumValue(2, "Fire"),
        EnumValue(3, "Water"),
        EnumValue(4, "Grass"),
        EnumValue(5, "Electric"),
        EnumValue(6, "Ice"),
        EnumValue(7, "Fighting"),
        EnumValue(8, "Poison"),
        EnumValue(9, "Ground"),
        EnumValue(10, "Flying"),
        EnumValue(11, "Psychic"),
        EnumValue(12, "Bug"),
        EnumValue(13, "Rock"),
        EnumValue(14, "Ghost"),
        EnumValue(15, "Dragon"),
        EnumValue(16, "Dark"),
        EnumValue(17, "Steel"),
        EnumValue(18, "Neutral"),
    ],
    "type_matchup": [
        EnumValue(0, "Immune"),
        EnumValue(1, "Not Very Effective"),
        EnumValue(2, "Neutral"),
        EnumValue(3, "Super Effective"),
    ],
    "nature_power_variant": [
        EnumValue(0, "Surf"),
        EnumValue(1, "Stun Spore"),
        EnumValue(2, "Shadow Ball"),
        EnumValue(3, "Swift"),
        EnumValue(4, "Earthquake"),
        EnumValue(5, "Razor Leaf"),
        EnumValue(6, "Bubblebeam"),
        EnumValue(7, "Rock Slide"),
        EnumValue(8, "Earthquake 2"),
        EnumValue(9, "Tri Attack"),
        EnumValue(10, "Hydro Pump"),
        EnumValue(11, "Blizzard"),
        EnumValue(12, "Ice Beam"),
        EnumValue(13, "Seed Bomb"),
        EnumValue(14, "Mud Bomb"),
    ],
    "status_two_turn_id": [
        EnumValue(0, "None"),
        EnumValue(1, "Bide"),
        EnumValue(2, "Solarbeam"),
        EnumValue(3, "Sky Attack"),
        EnumValue(4, "Razor Wind"),
        EnumValue(5, "Focus Punch"),
        EnumValue(6, "Skull Bash"),
        EnumValue(7, "Flying"),
        EnumValue(8, "Bouncing"),
        EnumValue(9, "Diving"),
        EnumValue(10, "Digging"),
        EnumValue(11, "Charging"),
        EnumValue(12, "Enraged"),
        EnumValue(13, "Shadow Force"),
    ],
    "exclusive_item_effect_id": [
        EnumValue(0, "Nothing"),
        EnumValue(1, "No Paralysis"),
        EnumValue(2, "No Confusion"),
        EnumValue(3, "No Infatuation"),
        EnumValue(4, "No Freeze"),
        EnumValue(5, "No Critical Hits"),
        EnumValue(6, "Halved Explosion Damage"),
        EnumValue(7, "No Explosion Damage"),
        EnumValue(8, "No Move Disabling"),
        EnumValue(9, "No Weather Damage"),
        EnumValue(10, "No Sleep"),
        EnumValue(11, "May Poison, Paralyze or Sleep Attackers"),
        EnumValue(12, "Unused 0xC"),
        EnumValue(13, "May Sleep Attackers"),
        EnumValue(14, "May Nightmare Attackers"),
        EnumValue(15, "May Burn Attackers"),
        EnumValue(16, "May Paralyze Attackers"),
        EnumValue(17, "May Confuse Attackers"),
        EnumValue(18, "May Infatuate Attackers"),
        EnumValue(19, "May Freeze Attackers"),
        EnumValue(20, "May Shadow Hold Attackers"),
        EnumValue(21, "May Constrict Attackers"),
        EnumValue(22, "May Cringe Attackers"),
        EnumValue(23, "May Blinker Attackers"),
        EnumValue(24, "May Seal Attacker Moves"),
        EnumValue(25, "May Go Invisible When Attacked"),
        EnumValue(26, "May Boost Movement Speed When Attacked"),
        EnumValue(27, "May Warp When Attacked"),
        EnumValue(28, "May Perish Song Attackers"),
        EnumValue(29, "May Slow Attackers"),
        EnumValue(30, "Halved Physical Damage"),
        EnumValue(31, "Halved Special Damage"),
        EnumValue(32, "Counter Physical Damage"),
        EnumValue(33, "May Bounce Status Moves"),
        EnumValue(34, "May Endure"),
        EnumValue(35, "Counter 25% Physical Damage"),
        EnumValue(36, "Long Toss"),
        EnumValue(37, "May Bounce Moves"),
        EnumValue(38, "No Stat Drops"),
        EnumValue(39, "Conversion 2 When Hit"),
        EnumValue(40, "No Status When Clear"),
        EnumValue(41, "No Status When Sunny"),
        EnumValue(42, "No Status When Sandstorm"),
        EnumValue(43, "No Status When Cloudy"),
        EnumValue(44, "No Status When Rainy"),
        EnumValue(45, "No Status When Hail"),
        EnumValue(46, "No Status When Foggy"),
        EnumValue(47, "Movement Speed Boost When Clear"),
        EnumValue(48, "Movement Speed Boost When Sunny"),
        EnumValue(49, "Movement Speed Boost When Sandstorm"),
        EnumValue(50, "Movement Speed Boost When Cloudy"),
        EnumValue(51, "Movement Speed Boost When Rainy"),
        EnumValue(52, "Movement Speed Boost When Hail"),
        EnumValue(53, "Movement Speed Boost When Foggy"),
        EnumValue(54, "Attack Speed Boost When Clear"),
        EnumValue(55, "Attack Speed Boost When Sunny"),
        EnumValue(56, "Attack Speed Boost When Sandstorm"),
        EnumValue(57, "Attack Speed Boost When Cloudy"),
        EnumValue(58, "Attack Speed Boost When Rainy"),
        EnumValue(59, "Attack Speed Boost When Hail"),
        EnumValue(60, "Attack Speed Boost When Foggy"),
        EnumValue(61, "Evasion Boost When Clear"),
        EnumValue(62, "Evasion Boost When Sunny"),
        EnumValue(63, "Evasion Boost When Sandstorm"),
        EnumValue(64, "Evasion Boost When Cloudy"),
        EnumValue(65, "Evasion Boost When Rainy"),
        EnumValue(66, "Evasion Boost When Hail"),
        EnumValue(67, "Evasion Boost When Foggy"),
        EnumValue(68, "Bypass Reflect Light Screen"),
        EnumValue(69, "Scrappy"),
        EnumValue(70, "Miracle Eye"),
        EnumValue(71, "Restore PP On New Floors"),
        EnumValue(72, "Restore HP On New Floors"),
        EnumValue(73, "Increased HP Recovery"),
        EnumValue(74, "Max PP Boost"),
        EnumValue(75, "Unused 0x4B"),
        EnumValue(76, "Max HP +10"),
        EnumValue(77, "Max HP +20"),
        EnumValue(78, "Max HP +30"),
        EnumValue(79, "Exp Boost"),
        EnumValue(80, "Exp From Damage"),
        EnumValue(81, "May Restore PP From Damage"),
        EnumValue(82, "May Not Consume PP"),
        EnumValue(83, "Thrown Item Protection"),
        EnumValue(84, "Bounce Thrown Items"),
        EnumValue(85, "Extend Self Effects To Team"),
        EnumValue(86, "More Treasure Drops"),
        EnumValue(87, "Hp Drain Recovery Boost"),
        EnumValue(88, "Pressure Boost"),
        EnumValue(89, "No Status"),
        EnumValue(90, "Halved Damage"),
        EnumValue(91, "Damage Boost +50%"),
        EnumValue(92, "Absorb Teammate Poison"),
        EnumValue(93, "Recover Hp From Apples And Berries"),
        EnumValue(94, "More Kecleon Shops"),
        EnumValue(95, "More Hidden Stairs"),
        EnumValue(96, "No Friendly Fire"),
        EnumValue(97, "Pickup Boost"),
        EnumValue(98, "More Money Drops"),
        EnumValue(99, "Unused 0x63"),
        EnumValue(100, "Recover HP From Watery Terrain"),
        EnumValue(101, "Heal Status From Watery Terrain"),
        EnumValue(102, "No Fire Damage"),
        EnumValue(103, "No Water Damage"),
        EnumValue(104, "No Grass Damage"),
        EnumValue(105, "No Electric Damage"),
        EnumValue(106, "No Fighting Damage"),
        EnumValue(107, "No Ground Damage"),
        EnumValue(108, "No Flying Damage"),
        EnumValue(109, "No Psychic Damage"),
        EnumValue(110, "No Ghost Damage"),
        EnumValue(111, "No Dragon Damage"),
        EnumValue(112, "No Dark Damage"),
        EnumValue(113, "No Steel Damage"),
        EnumValue(114, "Absorb Fire Damage"),
        EnumValue(115, "Absorb Water Damage"),
        EnumValue(116, "Absorb Grass Damage"),
        EnumValue(117, "Absorb Electric Damage"),
        EnumValue(118, "Absorb Ice Damage"),
        EnumValue(119, "Absorb Fighting Damage"),
        EnumValue(120, "Absorb Ground Damage"),
        EnumValue(121, "Absorb Flying Damage"),
        EnumValue(122, "Absorb Psychic Damage"),
        EnumValue(123, "Absorb Bug Damage"),
        EnumValue(124, "Absorb Rock Damage"),
        EnumValue(125, "Absorb Ghost Damage"),
        EnumValue(126, "Absorb Dragon Damage"),
        EnumValue(127, "Absorb Dark Damage"),
        EnumValue(128, "Absorb Steel Damage"),
        EnumValue(129, "Nothing"),
    ],
}


def get_enum_values(type_str: str) -> list[EnumValue]:
    """
    Given a string representing an enum type, returns its possible values
    :param type_str: Enum type
    :return: List of values for the given enum type
    :raises ValueError: If the given type is not an enum type
    :raises UnsupportedTypeError: If the given type is not supported
    """
    if type_str.startswith("enum "):
        type_str_short = type_str.removeprefix("enum ")

        try:
            return KNOWN_ENUM_DATA[type_str_short]
        except KeyError:
            raise UnsupportedTypeError('Unsupported C type "' + type_str + '".')
    else:
        raise ValueError("The specified type is not an enum type.")


def get_all_enum_types() -> list[str]:
    """
    :return: List with the names of all enum types defined in this file
    """
    return ["enum " + k for k in KNOWN_ENUM_DATA.keys()]
