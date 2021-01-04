import sys
import os
import shutil
import math
import glob
import chara_wan.writer as exWriter



def getWanFilePath(baseDir, dirName, index):
    inDir = os.path.join(baseDir, dirName)
    inFile = None
    for file in glob.glob(os.path.join(inDir, '*_' + format(index, '04d') + '_*')):
        inFile = file
    return inFile

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
        monster = exWriter.ImportWan(monster_file)
    with open(m_groundPath, "rb") as m_ground_file:
        m_ground = exWriter.ImportWan(m_ground_file)
    with open(m_attackPath, "rb") as m_attack_file:
        m_attack = exWriter.ImportWan(m_attack_file)

    wan = exWriter.MergeWan([monster, m_ground, m_attack])

    exWriter.ExportSheets(os.path.join(outDir, format(index, '04d')), sdwImg, wan, anim_name_map)

    # typical import flow; take a sheet, split into 3 sir0, import to those 3 simultaneously
    wan = exWriter.ImportSheets(os.path.join(outDir, format(index, '04d')))

    anim_presence = []
    # monster
    anim_presence.append([True, False, False, False, False, True, True, True, False, False, False, True])
    # ground
    anim_presence.append([True, False, False, False, False, False, True, True, False, False, False, False, True])
    # attack
    anim_presence.append([False, True, True, True, True, False, False, False, True, True, True, True, True])
    split_wan = exWriter.SplitWan(wan, anim_presence)

    monsterBackPath = os.path.join(outDir, os.path.split(monsterPath)[1])
    m_groundBackPath = os.path.join(outDir, os.path.split(m_groundPath)[1])
    m_attackBackPath = os.path.join(outDir, os.path.split(m_attackPath)[1])

    with open(monsterBackPath, 'wb') as file:
        exWriter.ExportWan(file, split_wan[0])
    with open(m_groundBackPath, 'wb') as file:
        exWriter.ExportWan(file, split_wan[1])
    with open(m_attackBackPath, 'wb') as file:
        exWriter.ExportWan(file, split_wan[2])
