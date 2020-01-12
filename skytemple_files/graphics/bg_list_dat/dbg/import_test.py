"""Checks, that models can be imported again"""
import os

from ndspy.rom import NintendoDSRom

from skytemple_files.graphics.bg_list_dat.handler import BgListDatHandler

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))

bin_before = rom.getFileByName('MAP_BG/bg_list.dat')
bg_list = BgListDatHandler.deserialize(bin_before)

bin_after = BgListDatHandler.serialize(bg_list)

assert bin_after == bin_before

rom.setFileByName('MAP_BG/bg_list.dat', bin_after)

rom.saveToFile(os.path.join(base_dir, 'skyworkcopy_edit.nds'))