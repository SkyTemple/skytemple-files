#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
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
import sys
import os
import shutil
import math
import glob
import chara_wan.writer as exWriter
import chara_wan.split_merge as exSplitMerge
import chara_wan.sheets as exSheets
from chara_wan.model import WanFile


def getWanFilePath(baseDir, dirName, index):
    inDir = os.path.join(baseDir, dirName)
    inFile = None
    for file in glob.glob(os.path.join(inDir, '*_' + format(index, '04d') + '_*')):
        inFile = file
    return inFile

def ReadbackChara(baseDir, index, anim_name_map, sdwImg):
    print(format(index, '04d'))
    inDir = os.path.join(baseDir, 'Sprite', format(index, '04d'))

    wan = exSheets.ImportSheets(inDir)
    shutil.rmtree(inDir)
    exSheets.ExportSheets(inDir, sdwImg, wan, anim_name_map)


def ConvertJoinSeparateChara(baseDir, index, anim_name_map, sdwImg):
    monsterPath = getWanFilePath(baseDir, 'monster', index)
    m_groundPath = getWanFilePath(baseDir, 'm_ground', index)
    m_attackPath = getWanFilePath(baseDir, 'm_attack', index)

    print(format(index, '04d'))

    if monsterPath is None or m_groundPath is None or m_attackPath is None:
        print("Missing path!")
        return

    # typical export flow; take all 3 sir0, merge into one sheet and export
    outDir = os.path.join(baseDir, 'example')

    with open(monsterPath, "rb") as monster_file:
        monster = WanFile(monster_file.read())
    with open(m_groundPath, "rb") as m_ground_file:
        m_ground = WanFile(m_ground_file.read())
    with open(m_attackPath, "rb") as m_attack_file:
        m_attack = WanFile(m_attack_file.read())

    wan = exSplitMerge.MergeWan([monster, m_ground, m_attack])

    exSheets.ExportSheets(os.path.join(outDir, format(index, '04d')), sdwImg, wan, anim_name_map)

    # typical import flow; take a sheet, split into 3 sir0, import to those 3 simultaneously
    wan = exSheets.ImportSheets(os.path.join(outDir, format(index, '04d')))

    anim_presence = []
    # monster
    anim_presence.append([True, False, False, False, False, True, True, True, False, False, False, True])
    # ground
    anim_presence.append([True, False, False, False, False, False, True, True, False, False, False, False, True])
    # attack
    anim_presence.append([False, True, True, True, True, False, False, False, True, True, True, True, True])
    split_wan = exSplitMerge.SplitWan(wan, anim_presence)

    monsterBackPath = os.path.join(outDir, os.path.split(monsterPath)[1])
    m_groundBackPath = os.path.join(outDir, os.path.split(m_groundPath)[1])
    m_attackBackPath = os.path.join(outDir, os.path.split(m_attackPath)[1])

    with open(monsterBackPath, 'wb') as file:
        file.write(exWriter.ExportWan(split_wan[0]))
    with open(m_groundBackPath, 'wb') as file:
        file.write(exWriter.ExportWan(split_wan[1]))
    with open(m_attackBackPath, 'wb') as file:
        file.write(exWriter.ExportWan(split_wan[2]))
