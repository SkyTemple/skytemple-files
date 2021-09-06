from skytemple_files.common.dungeon_floor_generator.dungeon_eos.RandomGen import *

class Properties: # Floor Properties
    layout = 1
    mh_chance = 0
    kecleon_chance = 0
    middle_room_secondary = 0
    nb_rooms = 4
    bit_flags = 0x1
    floor_connectivity = 15
    maze_chance = 0
    dead_end = 0
    extra_hallways = 0
    secondary_density = 10
    empty_mh_chance = 0
    enemy_density = 0
    item_density = 0
    buried_item_density = 0
    trap_density = 0
    fixed_floor_number = 0
    hidden_stairs_type = 0

class TileData:
    TRANS_TABLE = {0x0: "terrain_flags",
                   0x2: "spawn_flags",
                   0x4: "tex_index",
                   0x6: "unk1",
                   0x7: "room_index",
                   0x8: "normal_movement",
                   0x9: "secondary_movement",
                   0xa: "void_movement",
                   0xb: "wall_movement",
                   0xc: "monster_ptr",
                   0x10: "non_monster_ptr"}
                   
    def __init__(self):
        self[0x0] = 0
        self[0x2] = 0
        self[0x4] = 0
        self[0x6] = 0
        self[0x7] = 0xFF
        self[0x8] = 0
        self[0x9] = 0
        self[0xa] = 0
        self[0xb] = 0
        self[0xc] = 0
        self[0x10] = 0
    def __getitem__(self, index):
        return getattr(self, TileData.TRANS_TABLE[index])
    def __setitem__(self, index, value):
        setattr(self, TileData.TRANS_TABLE[index], value)



class StaticParam:
    MERGE_CHANCE = 5 # Originally 5%
    IMPERFECT_CHANCE = 60 # Originally 60%
    SECONDARY_CHANCE = 80 # Originally 80%
    MH_NORMAL_SPAWN_ENM = 20 # Originally 20
    MH_NORMAL_SPAWN_ITEM = 7 # Originally 7
    MH_MIN_TRAP_DUNGEON = 28 # Originally 28
    PATCH_APPLIED = 0
    FIX_DEAD_END_ERROR = 0
    FIX_OUTER_ROOM_ERROR = 0
    SHOW_ERROR = 0
    
    DEFAULT_TILE = TileData()

    #US: 0235171C
    LIST_DIRECTIONS = {0 :  0,2 :  1,
                   4 :  1,6 :  1,
                   8 :  1,10:  0,
                   12:  1,14: -1,
                   16:  0,18: -1,
                   20: -1,22: -1,
                   24: -1,26:  0,
                   28: -1,30:  1}
    #US: 02353010
    LIST_CHECKS = [1,0,1,0,0,0,0,0,
               1,0,0,0,0,0,1,0,
               0,0,0,0,1,0,1,0,
               0,0,1,0,1,0,0,0]

#US: 0x02353538
class DungeonData: # Dungeon structure
    maze_value = 0
    dungeon_number = 1 #0x748
    floor_dungeon_number = 1 #0x749
    unknown_751 = 1 #0x751
    free_mode = 1 #0x75C
    unknown_798 = 0 #0x798
    create_mh = 0 #0x40C4
    mh_room = -1 #0x40C9
    hidden_stairs_type = 0 #0x40CC
    fixed_floor_number = 0 #0x40DA
    attempts = 0 #0x40DE
    mission_flag = 0 #0x760
    mission_type_1 = 0 #0x761
    mission_type_2 = 0 #0x762
    player_spawn_x = -1 #0xCCE0
    player_spawn_y = -1 #0xCCE2
    stairs_spawn_x = -1 #0xCCE4
    stairs_spawn_y = -1 #0xCCE6
    hidden_stairs_spawn_x = -1 #0xCCE8
    hidden_stairs_spawn_y = -1 #0xCCEA
    kecleon_shop_min_x = 0 #0xCD14
    kecleon_shop_min_y = 0 #0xCD18
    kecleon_shop_max_x = 0 #0xCD1C
    kecleon_shop_max_y = 0 #0xCD20
    nb_items = 0 #0x12AFA
    guaranteed_item_id = 0 #0x2C9E8
    floor_dungeon_max = 4 #0x2CAF4
    def clear_tiles():
        DungeonData.list_tiles = [[TileData() for y in range(32)] for x in range(56)] #0x40E0
    def clear_fixed_room():
        DungeonData.tiles_fr = [[TileData() for y in range(8)] for x in range(8)] #0xCD60
    def clear_active_traps():
        DungeonData.active_traps = [0 for i in range(64)]
class StatusData: # Status structure 0237CFBC
    second_spawn = 0 #0x0
    has_monster_house = 0 #0x1
    stairs_room = 0 #0x2
    has_kecleon_shop = 0 #0x3
    is_not_valid = 0 #0x5
    floor_size = 0 #0x6
    has_maze = 0 #0x7
    no_enemy_spawn = 0 #0x8
    kecleon_chance = 100 #0xC
    mh_chance = 0 #0x10
    nb_rooms = 0 #0x14
    middle_room_secondary = 0 #0x18
    hidden_stairs_spawn_x = 0 #0x1C
    hidden_stairs_spawn_y = 0 #0x1E
    kecleon_shop_middle_x = 0 #0x20
    kecleon_shop_middle_y = 0 #0x22
    unk_val_24 = 0 #0x24
    hidden_stairs_type = 0 #0x2C
    kecleon_shop_min_x = 0 #0x30
    kecleon_shop_min_y = 0 #0x34
    kecleon_shop_max_x = 0 #0x38
    kecleon_shop_max_y = 0 #0x3C

class ReturnData: # Special Return Data
    invalid_generation = False

class GridCell:
    TRANS_TABLE = {0x0: "start_x",
                   0x2: "start_y",
                   0x4: "end_x",
                   0x6: "end_y",
                   0x8: "valid_cell",
                   0x9: "unk1",
                   0xa: "is_room",
                   0xb: "is_connected",
                   0xc: "unk2",
                   0xd: "unk3",
                   0xe: "is_mh",
                   0xf: "unk4",
                   0x10: "is_maze",
                   0x11: "has_been_merged",
                   0x12: "is_merged",
                   0x13: "connected_to_top",
                   0x14: "connected_to_bottom",
                   0x15: "connected_to_left",
                   0x16: "connected_to_right",
                   0x17: "connected_to_top_2",
                   0x18: "connected_to_bottom_2",
                   0x19: "connected_to_left_2",
                   0x1A: "connected_to_right_2",
                   0x1B: "unk5",
                   0x1C: "flag_imperfect",
                   0x1D: "flag_secondary"}
                   
    def __init__(self):
        self[0x0] = 0
        self[0x2] = 0
        self[0x4] = 0
        self[0x6] = 0
        self[0x8] = 0
        self[0x9] = 0
        self[0xa] = 0
        self[0xb] = 0
        self[0xc] = 0
        self[0xd] = 0
        self[0xe] = 0
        self[0xf] = 0
        self[0x10] = 0
        self[0x11] = 0
        self[0x12] = 0
        self[0x13] = 0
        self[0x14] = 0
        self[0x15] = 0
        self[0x16] = 0
        self[0x17] = 0
        self[0x18] = 0
        self[0x19] = 0
        self[0x1A] = 0
        self[0x1B] = 0
        self[0x1C] = 0
        self[0x1D] = 0
    def __getitem__(self, index):
        return getattr(self, GridCell.TRANS_TABLE[index])
    def __setitem__(self, index, value):
        setattr(self, GridCell.TRANS_TABLE[index], value)

#US: 0233CF84
def generate_grid_positions(max_nb_room_x, max_nb_room_y):
    sum_x = 0
    list_x = []
    for x in range(max_nb_room_x+1):
        list_x.append(sum_x)
        sum_x += 0x38//max_nb_room_x
    sum_y = 0
    list_y = []
    for y in range(max_nb_room_y+1):
        list_y.append(sum_y)
        sum_y += 0x20//max_nb_room_y
    return list_x, list_y

#US: 0233D004
def init_grid(max_nb_room_x, max_nb_room_y):
    grid = [[GridCell() for y in range(15)] for z in range(15)]
    for x in range(max_nb_room_x):
        for y in range(max_nb_room_y):
            if StatusData.floor_size==1 and x>=max_nb_room_x//2:
                grid[x][y][8]=1
            elif StatusData.floor_size==2 and x>=max_nb_room_x*3//4:
                grid[x][y][8]=1
            else:
                grid[x][y][8]=0
            grid[x][y][10]=1
    return grid

#US: 0233D104
def place_rooms(grid, max_nb_room_x, max_nb_room_y, nb_rooms):
    rnd = randrange(3)
    if nb_rooms<0:
        nb_rooms = -nb_rooms
    else:
        nb_rooms += rnd
    rooms_ok = [(x<nb_rooms) for x in range(256)]
    max_rooms = max_nb_room_x*max_nb_room_y
    for x in range(0x40):
        a = randrange(max_rooms)
        b = randrange(max_rooms)
        tmp = rooms_ok[a]
        rooms_ok[a] = rooms_ok[b]
        rooms_ok[b] = tmp
    StatusData.nb_rooms = 0
    odd_x = (max_nb_room_x%2)
    counter = 0
    for x in range(max_nb_room_x):
        for y in range(max_nb_room_y):
            if grid[x][y][8]==0:
                if StatusData.nb_rooms>=0x20:
                    grid[x][y][10]=0
                if rooms_ok[counter]:
                    grid[x][y][10]=1
                    StatusData.nb_rooms += 1
                    if odd_x and y==1 and x==(max_nb_room_x-1)//2:
                        grid[x][y][10]=0
                else:
                    grid[x][y][10]=0
                counter += 1
    if StatusData.nb_rooms>=2:
        return

    attempts = 0
    ok = False
    while attempts<200 and not ok:
        for x in range(max_nb_room_x):
            for y in range(max_nb_room_y):
                if grid[x][y][8]==0:
                    if randrange(100)<60:
                        grid[x][y][10]=1
                        ok = True
                        break
            if ok:
                break
        attempts += 1
    StatusData.second_spawn = 0

#US: 0233D318
def create_rooms(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, flags):
    imperfect = flags & 0x4
    room_number = 0
    for y in range(max_nb_room_y):
        cur_val_y = list_y[y]
        next_val_y = list_y[y+1]
        for x in range(max_nb_room_x):
            cur_val_x = list_x[x]
            next_val_x = list_x[x+1]
            range_x = next_val_x-cur_val_x-4
            range_y = next_val_y-cur_val_y-3
            if grid[x][y][8]==0:
                if grid[x][y][10]==0:
                    unk_x1 = 2
                    unk_x2 = 4
                    if x==0:
                        unk_x1 = 1
                    if x==max_nb_room_x-1:
                        unk_x2 = 2
                    unk_y1 = 2
                    unk_y2 = 4
                    if y==0:
                        unk_y1 = 1
                    if y==max_nb_room_y-1:
                        unk_y2 = 2
                    pt_x = randrangeswap(cur_val_x+2+unk_x1, cur_val_x+2+range_x-unk_x2)
                    pt_y = randrangeswap(cur_val_y+2+unk_y1, cur_val_y+2+range_y-unk_y2)
                    grid[x][y][0] = pt_x
                    grid[x][y][2] = pt_y
                    grid[x][y][4] = pt_x+1
                    grid[x][y][6] = pt_y+1
                    DungeonData.list_tiles[pt_x][pt_y][0] &= ~0x3
                    DungeonData.list_tiles[pt_x][pt_y][0] |= 0x1
                    DungeonData.list_tiles[pt_x][pt_y][7] = 0xFE
                else:
                    size_x = randrangeswap(5,range_x)
                    size_y = randrangeswap(4,range_y)
                    if size_x | 1 < range_x:
                        size_x |= 1
                    if size_y | 1 < range_y:
                        size_y |= 1
                    if size_x>size_y*3//2:
                        size_x = size_y*3//2
                    if size_y>size_x*3//2:
                        size_y = size_x*3//2
                    start_x = randrangeforce(range_x-size_x)+cur_val_x+2
                    end_x = start_x+size_x
                    start_y = randrangeforce(range_y-size_y)+cur_val_y+2
                    end_y = start_y+size_y
                    grid[x][y][0] = start_x
                    grid[x][y][2] = start_y
                    grid[x][y][4] = end_x
                    grid[x][y][6] = end_y
                    for room_x in range(start_x, end_x):
                        for room_y in range(start_y, end_y):
                            DungeonData.list_tiles[room_x][room_y][0] &= ~0x3
                            DungeonData.list_tiles[room_x][room_y][0] |= 0x1
                            DungeonData.list_tiles[room_x][room_y][7] = room_number
                    flag_secondary = (randrange(100)<StaticParam.SECONDARY_CHANCE)
                    if StatusData.middle_room_secondary==0:
                        flag_secondary = 0
                    flag_imp = imperfect
                    if flag_secondary and flag_imp:
                        if randrange(100)<50:
                            flag_imp = 0
                        else:
                            flag_secondary = 0
                    if flag_imp:
                        grid[x][y][0x1C] = 1
                    if flag_secondary:
                        grid[x][y][0x1D] = 1
                    room_number += 1

#US: 0233E05C
def create_connections(grid, max_nb_room_x, max_nb_room_y, pt_x, pt_y, prop):
    rnd_num = randrange(4)
    for i in range(prop.floor_connectivity):
        test = randrange(8)
        current_num = randrange(4)
        if test<4:
            rnd_num = current_num
        ok = False
        while not ok:
            if rnd_num&0x3==0 and pt_x<max_nb_room_x-1:
                ok = True
            elif rnd_num&0x3==1 and pt_y>0:
                ok = True
            elif rnd_num&0x3==2 and pt_x>0:
                ok = True
            elif rnd_num&0x3==3 and pt_y<max_nb_room_y-1:
                ok = True
            else:
                rnd_num+=1
        rnd_num &= 3
        if rnd_num==0 and grid[pt_x+1][pt_y][8]==0:
            grid[pt_x][pt_y][0x16] = 1
            grid[pt_x+1][pt_y][0x15] = 1
            pt_x += 1
        elif rnd_num==1 and grid[pt_x][pt_y-1][8]==0:
            grid[pt_x][pt_y][0x13] = 1
            grid[pt_x][pt_y-1][0x14] = 1
            pt_y -= 1
        elif rnd_num==2 and grid[pt_x-1][pt_y][8]==0:
            grid[pt_x][pt_y][0x15] = 1
            grid[pt_x-1][pt_y][0x16] = 1
            pt_x -= 1
        elif rnd_num==3 and grid[pt_x][pt_y+1][8]==0:
            grid[pt_x][pt_y][0x14] = 1
            grid[pt_x][pt_y+1][0x13] = 1
            pt_y += 1
    if prop.dead_end==0:
        more = True
        while more:
            more = False
            for y in range(max_nb_room_y):
                for x in range(max_nb_room_x):
                    if grid[x][y][8]==0 and grid[x][y][10]==0:
                        count_connect = 0
                        for v in range(0x13,0x17):
                            if grid[x][y][v]!=0:
                                count_connect += 1
                        if count_connect == 1:
                            rnd_num = randrange(4)
                            ok = False
                            for v in range(8):
                                if rnd_num&0x3==0 and pt_x<max_nb_room_x-1 and grid[x][y][0x16]==0:
                                    ok = True
                                elif rnd_num&0x3==1 and pt_y>0 and grid[x][y][0x13]==0:
                                    ok = True
                                elif rnd_num&0x3==2 and pt_x>0 and grid[x][y][0x15]==0:
                                    ok = True
                                elif rnd_num&0x3==3 and pt_y<max_nb_room_y-1 and grid[x][y][0x14]==0:
                                    ok = True
                                else:
                                    rnd_num+=1
                                if ok:
                                    break
                            rnd_num &= 3
                            ### WARNING! Not consistent with the original code!
                            ### That part is bugged in the actual version
                            if StaticParam.FIX_DEAD_END_ERROR:
                                if rnd_num==0 and grid[x+1][y][8]==0:
                                    grid[x][y][0x16] = 1
                                    grid[x+1][y][0x15] = 1
                                    more = True
                                    x += 1
                                elif rnd_num==1 and grid[x][y-1][8]==0:
                                    grid[x][y][0x13] = 1
                                    grid[x][y-1][0x14] = 1
                                    more = True
                                    y -= 1
                                elif rnd_num==2 and grid[x-1][y][8]==0:
                                    grid[x][y][0x15] = 1
                                    grid[x-1][y][0x16] = 1
                                    more = True
                                    x -= 1
                                elif rnd_num==3 and grid[x][y+1][8]==0:
                                    grid[x][y][0x14] = 1
                                    grid[x][y+1][0x13] = 1
                                    more = True
                                    y += 1
                            else:
                                if rnd_num==0 and grid[x+1][y][8]==0:
                                    grid[x][y][0x16] = 1
                                    grid[x+1][y][0x15] = 1
                                    more = True
                                    x += 1
                                elif rnd_num==1 and grid[x+1][y][8]==0:
                                    grid[x][y][0x13] = 1
                                    grid[x][y-1][0x14] = 1
                                    more = True
                                    y -= 1
                                elif rnd_num==2 and grid[x+1][y][8]==0:
                                    grid[x][y][0x15] = 1
                                    grid[x-1][y][0x16] = 1
                                    more = True
                                    x -= 1
                                elif rnd_num==3 and grid[x+1][y][8]==0:
                                    grid[x][y][0x14] = 1
                                    grid[x][y+1][0x13] = 1
                                    more = True
                                    y += 1

#US: 0233F120
def process_hallway(pt_x, pt_y, pt2_x, pt2_y, vertical, list_val_x, list_val_y):
    dep_pt_x = pt_x
    dep_pt_y = pt_y
    if vertical==0:
        counter = 0
        while pt_x!=list_val_x:
            if counter>=56:
                return
            counter += 1
            if DungeonData.list_tiles[pt_x][pt_y][0]&0x3==1:
                if dep_pt_x!=pt_x:
                    return
            else:
                DungeonData.list_tiles[pt_x][pt_y][0] &= ~0x3
                DungeonData.list_tiles[pt_x][pt_y][0] |= 0x1
            if pt_x>=list_val_x:
                pt_x-=1
            else:
                pt_x+=1
        counter = 0
        while pt_y!=pt2_y:
            if counter>=56:
                return
            counter += 1
            if DungeonData.list_tiles[pt_x][pt_y][0]&0x3==1:
                if dep_pt_x!=pt_x or dep_pt_y!=pt_y:
                    return
            else:
                DungeonData.list_tiles[pt_x][pt_y][0] &= ~0x3
                DungeonData.list_tiles[pt_x][pt_y][0] |= 0x1
            if pt_y>=pt2_y:
                pt_y-=1
            else:
                pt_y+=1
        counter = 0
        while pt_x!=pt2_x:
            if counter>=56:
                return
            counter += 1
            if DungeonData.list_tiles[pt_x][pt_y][0]&0x3==1:
                if dep_pt_x!=pt_x or dep_pt_y!=pt_y:
                    return
            else:
                DungeonData.list_tiles[pt_x][pt_y][0] &= ~0x3
                DungeonData.list_tiles[pt_x][pt_y][0] |= 0x1
            if pt_x>=pt2_x:
                pt_x-=1
            else:
                pt_x+=1
    else:
        counter = 0
        while pt_y!=list_val_y:
            if counter>=56:
                return
            counter += 1
            if DungeonData.list_tiles[pt_x][pt_y][0]&0x3==1:
                if dep_pt_y!=pt_y:
                    return
            else:
                DungeonData.list_tiles[pt_x][pt_y][0] &= ~0x3
                DungeonData.list_tiles[pt_x][pt_y][0] |= 0x1
            if pt_y>=list_val_y:
                pt_y-=1
            else:
                pt_y+=1
        counter = 0
        while pt_x!=pt2_x:
            if counter>=56:
                return
            counter += 1
            if DungeonData.list_tiles[pt_x][pt_y][0]&0x3==1:
                if dep_pt_x!=pt_x or dep_pt_y!=pt_y:
                    return
            else:
                DungeonData.list_tiles[pt_x][pt_y][0] &= ~0x3
                DungeonData.list_tiles[pt_x][pt_y][0] |= 0x1
            if pt_x>=pt2_x:
                pt_x-=1
            else:
                pt_x+=1
        counter = 0
        while pt_y!=pt2_y:
            if counter>=56:
                return
            counter += 1
            if DungeonData.list_tiles[pt_x][pt_y][0]&0x3==1:
                if dep_pt_x!=pt_x or dep_pt_y!=pt_y:
                    return
            else:
                DungeonData.list_tiles[pt_x][pt_y][0] &= ~0x3
                DungeonData.list_tiles[pt_x][pt_y][0] |= 0x1
            if pt_y>=pt2_y:
                pt_y-=1
            else:
                pt_y+=1

# US: 0233E43C
def create_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, no_merge_rooms):
    for y in range(max_nb_room_y):
        for x in range(max_nb_room_x):
            if grid[x][y][8]!=0:
                grid[x][y][0x17] = 0
                grid[x][y][0x18] = 0
                grid[x][y][0x19] = 0
                grid[x][y][0x1A] = 0
            else:
                if x==0:
                    grid[x][y][0x15] = 0
                if y==0:
                    grid[x][y][0x13] = 0
                if x==max_nb_room_x-1:
                    grid[x][y][0x16] = 0
                if y==max_nb_room_y-1:
                    grid[x][y][0x14] = 0
                for v in range(0x13,0x17):
                    grid[x][y][v+4] = grid[x][y][v]
    for x in range(max_nb_room_x):
        for y in range(max_nb_room_y):
            if grid[x][y][8]==0:
                if grid[x][y][10]==0:
                    pt_x = grid[x][y][0]
                    pt_y = grid[x][y][2]
                else:
                    pt_x = randrange(grid[x][y][0]+1, grid[x][y][4]-1)
                    pt_y = randrange(grid[x][y][2]+1, grid[x][y][6]-1)
                if grid[x][y][0x17]:
                    if grid[x][y-1][8]==0:
                        if grid[x][y-1][10]==0:
                            pt2_x = grid[x][y-1][0]
                        else:
                            pt2_x = randrange(grid[x][y-1][0]+1, grid[x][y-1][4]-1)
                        process_hallway(pt_x, grid[x][y][2], pt2_x, grid[x][y-1][6]-1, 1, list_x[x], list_y[y])
                    grid[x][y][0x17] = 0
                    grid[x][y-1][0x18] = 0
                    grid[x][y][0xb] = 1
                    grid[x][y-1][0xb] = 1
                if grid[x][y][0x18]:
                    if grid[x][y+1][8]==0:
                        if grid[x][y+1][10]==0:
                            pt2_x = grid[x][y+1][0]
                        else:
                            pt2_x = randrange(grid[x][y+1][0]+1, grid[x][y+1][4]-1)
                        process_hallway(pt_x, grid[x][y][6]-1, pt2_x, grid[x][y+1][2], 1, list_x[x], list_y[y+1]-1)
                    grid[x][y][0x18] = 0
                    grid[x][y+1][0x17] = 0
                    grid[x][y][0xb] = 1
                    grid[x][y+1][0xb] = 1
                if grid[x][y][0x19]:
                    if grid[x-1][y][8]==0:
                        if grid[x-1][y][10]==0:
                            pt2_y = grid[x-1][y][2]
                        else:
                            pt2_y = randrange(grid[x-1][y][2]+1, grid[x-1][y][6]-1)
                        # This is weird, it should be grid[x][y-1][4]-1
                        process_hallway(grid[x][y][0], pt_y, grid[x-1][y][0]-1, pt2_y, 0, list_x[x], list_y[y])
                    grid[x][y][0x19] = 0
                    grid[x-1][y][0x1a] = 0
                    grid[x][y][0xb] = 1
                    grid[x-1][y][0xb] = 1
                if grid[x][y][0x1a]:
                    if grid[x+1][y][8]==0:
                        if grid[x+1][y][10]==0:
                            pt2_y = grid[x+1][y][2]
                        else:
                            pt2_y = randrange(grid[x+1][y][2]+1, grid[x+1][y][6]-1)
                        process_hallway(grid[x][y][4]-1, pt_y, grid[x+1][y][0], pt2_y, 0, list_x[x+1]-1, list_y[y])
                    grid[x][y][0x1a] = 0
                    grid[x+1][y][0x19] = 0
                    grid[x][y][0xb] = 1
                    grid[x+1][y][0xb] = 1
    if no_merge_rooms==0:
        for x in range(max_nb_room_x):
            for y in range(max_nb_room_y):
                chance = randrange(100)
                if chance<StaticParam.MERGE_CHANCE and grid[x][y][8]==0 and grid[x][y][0xb]!=0 \
                   and grid[x][y][0x12]==0 and grid[x][y][0x9]==0 and grid[x][y][10]!=0:
                    rnd_num = randrange(4)
                    if rnd_num==0 and x>=1 and grid[x-1][y][8]==0 and grid[x-1][y][0xb]!=0 \
                   and grid[x-1][y][0x12]==0 and grid[x-1][y][0x9]==0 and grid[x-1][y][10]!=0:
                        src_y = min(grid[x-1][y][2], grid[x][y][2])
                        dst_y = max(grid[x-1][y][6], grid[x][y][6])
                        src_x = grid[x-1][y][0]
                        dst_x = grid[x][y][4]
                        room = DungeonData.list_tiles[grid[x][y][0]][grid[x][y][2]][7]
                        for cur_x in range(src_x, dst_x):
                            for cur_y in range(src_y, dst_y):
                                DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                                DungeonData.list_tiles[cur_x][cur_y][0] |= 0x1
                                DungeonData.list_tiles[cur_x][cur_y][7] = room
                        grid[x-1][y][0] = src_x
                        grid[x-1][y][2] = src_y
                        grid[x-1][y][4] = dst_x
                        grid[x-1][y][6] = dst_y
                        grid[x-1][y][0x12] = 1
                        grid[x][y][0x12] = 1
                        grid[x][y][0xb] = 0
                        grid[x][y][0x11] = 1
                    elif rnd_num==1 and y>=1 and grid[x][y-1][8]==0 and grid[x][y-1][0xb]!=0 \
                   and grid[x][y-1][0x12]==0 and grid[x][y-1][0x9]==0 and grid[x][y-1][10]!=0:
                        src_x = min(grid[x][y-1][0], grid[x][y][0])
                        dst_x = max(grid[x][y-1][4], grid[x][y][4])
                        src_y = grid[x][y-1][2]
                        dst_y = grid[x][y][6]
                        room = DungeonData.list_tiles[grid[x][y][0]][grid[x][y][2]][7]
                        for cur_x in range(src_x, dst_x):
                            for cur_y in range(src_y, dst_y):
                                DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                                DungeonData.list_tiles[cur_x][cur_y][0] |= 0x1
                                DungeonData.list_tiles[cur_x][cur_y][7] = room
                        grid[x][y-1][0] = src_x
                        grid[x][y-1][2] = src_y
                        grid[x][y-1][4] = dst_x
                        grid[x][y-1][6] = dst_y
                        grid[x][y-1][0x12] = 1
                        grid[x][y][0x12] = 1
                        grid[x][y][0xb] = 0
                        grid[x][y][0x11] = 1
                    elif rnd_num==2 and x<=max_nb_room_x-2 and grid[x+1][y][8]==0 and grid[x+1][y][0xb]!=0 \
                   and grid[x+1][y][0x12]==0 and grid[x+1][y][0x9]==0 and grid[x+1][y][10]!=0:
                        src_y = min(grid[x+1][y][2], grid[x][y][2])
                        dst_y = max(grid[x+1][y][6], grid[x][y][6])
                        src_x = grid[x][y][0]
                        dst_x = grid[x+1][y][4]
                        room = DungeonData.list_tiles[grid[x][y][0]][grid[x][y][2]][7]
                        for cur_x in range(src_x, dst_x):
                            for cur_y in range(src_y, dst_y):
                                DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                                DungeonData.list_tiles[cur_x][cur_y][0] |= 0x1
                                DungeonData.list_tiles[cur_x][cur_y][7] = room
                        grid[x+1][y][0] = src_x
                        grid[x+1][y][2] = src_y
                        grid[x+1][y][4] = dst_x
                        grid[x+1][y][6] = dst_y
                        grid[x+1][y][0x12] = 1
                        grid[x][y][0x12] = 1
                        grid[x][y][0xb] = 0
                        grid[x][y][0x11] = 1
                    elif rnd_num==3 and y<=max_nb_room_y-2 and grid[x][y+1][8]==0 and grid[x][y+1][0xb]!=0 \
                   and grid[x][y+1][0x12]==0 and grid[x][y+1][0x9]==0 and grid[x][y+1][10]!=0:
                        src_x = min(grid[x][y+1][0], grid[x][y][0])
                        dst_x = max(grid[x][y+1][4], grid[x][y][4])
                        src_y = grid[x][y][2]
                        dst_y = grid[x][y+1][6]
                        room = DungeonData.list_tiles[grid[x][y][0]][grid[x][y][2]][7]
                        for cur_x in range(src_x, dst_x):
                            for cur_y in range(src_y, dst_y):
                                DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                                DungeonData.list_tiles[cur_x][cur_y][0] |= 0x1
                                DungeonData.list_tiles[cur_x][cur_y][7] = room
                        grid[x][y+1][0] = src_x
                        grid[x][y+1][2] = src_y
                        grid[x][y+1][4] = dst_x
                        grid[x][y+1][6] = dst_y
                        grid[x][y+1][0x12] = 1
                        grid[x][y][0x12] = 1
                        grid[x][y][0xb] = 0
                        grid[x][y][0x11] = 1

#US: 0233F424
def add_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y):
    for x in range(max_nb_room_x):
        for y in range(max_nb_room_y):
            if grid[x][y][8]==0 and grid[x][y][0xb]==0 and grid[x][y][0x11]==0:
                if grid[x][y][10]!=0 and grid[x][y][9]==0:
                    rnd_x = randrange(grid[x][y][0]+1, grid[x][y][4]-1)
                    rnd_y = randrange(grid[x][y][2]+1, grid[x][y][6]-1)
                    if y>0 and grid[x][y-1][8]==0 and grid[x][y-1][0x12]==0 and grid[x][y-1][0xb]!=0:
                        if grid[x][y-1][10]==0:
                            pt_x = grid[x][y-1][0]
                        else:
                            pt_x = randrange(grid[x][y-1][0]+1,grid[x][y-1][4]-1)
                            pt_y = randrange(grid[x][y-1][2]+1,grid[x][y-1][6]-1)
                        process_hallway(rnd_x, grid[x][y][2], pt_x, grid[x][y-1][6]-1, 1, list_x[x], list_y[y])
                        grid[x][y][0xb] = 1
                        grid[x][y][0x13] = 1
                        grid[x][y-1][0x14] = 1
                    elif y<max_nb_room_y-1 and grid[x][y+1][8]==0 and grid[x][y+1][0x12]==0 and grid[x][y+1][0xb]!=0:
                        if grid[x][y+1][10]==0:
                            pt_x = grid[x][y+1][0]
                        else:
                            pt_x = randrange(grid[x][y+1][0]+1,grid[x][y+1][4]-1)
                            pt_y = randrange(grid[x][y+1][2]+1,grid[x][y+1][6]-1)
                        process_hallway(rnd_x, grid[x][y][6]-1, pt_x, grid[x][y+1][2], 1, list_x[x], list_y[y+1]-1)
                        grid[x][y][0xb] = 1
                        grid[x][y][0x14] = 1
                        grid[x][y+1][0x13] = 1
                    elif x>0 and grid[x-1][y][8]==0 and grid[x-1][y][0x12]==0 and grid[x-1][y][0xb]!=0:
                        if grid[x-1][y][10]==0:
                            pt_y = grid[x-1][y][2]
                        else:
                            pt_x = randrange(grid[x-1][y][0]+1,grid[x-1][y][4]-1)
                            pt_y = randrange(grid[x-1][y][2]+1,grid[x-1][y][6]-1)
                        # This is weird, it should be grid[x][y-1][4]-1
                        process_hallway(grid[x][y][0], rnd_y, grid[x-1][y][0]-1, pt_y, 0, list_x[x], list_y[y])
                        grid[x][y][0xb] = 1
                        grid[x][y][0x15] = 1
                        grid[x-1][y][0x16] = 1
                    elif x<max_nb_room_x-1 and grid[x+1][y][8]==0 and grid[x+1][y][0x12]==0 and grid[x+1][y][0xb]!=0:
                        if grid[x+1][y][10]==0:
                            pt_y = grid[x+1][y][2]
                        else:
                            pt_x = randrange(grid[x+1][y][0]+1,grid[x+1][y][4]-1)
                            pt_y = randrange(grid[x+1][y][2]+1,grid[x+1][y][6]-1)
                        process_hallway(grid[x][y][4]-1, rnd_y, grid[x+1][y][0], pt_y, 0, list_x[x+1]-1, list_y[y])
                        grid[x][y][0xb] = 1
                        grid[x][y][0x16] = 1
                        grid[x-1][y][0x15] = 1
                else:
                    DungeonData.list_tiles[grid[x][y][0]][grid[x][y][2]][0] &= ~0x3
                    DungeonData.list_tiles[grid[x][y][0]][grid[x][y][2]][2] &= ~0x7
    for y in range(max_nb_room_y):
        for x in range(max_nb_room_x):
            if grid[x][y][8]==0 and grid[x][y][0x11]==0 and grid[x][y][0xb]==0 and grid[x][y][0xf]==0:
                for cur_x in range(grid[x][y][0], grid[x][y][4]):
                    for cur_y in range(grid[x][y][2], grid[x][y][6]):
                        DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                        DungeonData.list_tiles[cur_x][cur_y][2] &= ~0x7
                        DungeonData.list_tiles[cur_x][cur_y][7] = 0xFF

#US: 0233F900
def store_check_tile(tile_dat, secondary, room):
    tile_dat[0] &= ~0x3
    if secondary!=0 and tile_dat[7]==room:
        tile_dat[0] |= 0x2

#US: 023406D4
def line_maze(pt_x, pt_y, pt2_x, pt2_y, pt3_x, pt3_y, secondary, room):
    ok = True
    while ok:
        rnd_val = randrange(4)
        store_check_tile(DungeonData.list_tiles[pt_x][pt_y], secondary, room)
        ok = False
        for i in range(4):
            rnd_val&=0x3
            if rnd_val==0:
                val_x = 2
                val_y = 0
            elif rnd_val==1:
                val_x = 0
                val_y = -2
            elif rnd_val==2:
                val_x = -2
                val_y = 0
            elif rnd_val==3:
                val_x = 0
                val_y = 2
            if pt2_x<=pt_x+val_x<pt3_x and pt2_y<=pt_y+val_y<pt3_y:
                if DungeonData.list_tiles[pt_x+val_x][pt_y+val_y][0]&0x3==1:
                    ok = True
                    break
            rnd_val += 1
        if ok:
            if rnd_val==0:
                store_check_tile(DungeonData.list_tiles[pt_x+1][pt_y], secondary, room)
                pt_x += 2
            elif rnd_val==1:
                store_check_tile(DungeonData.list_tiles[pt_x][pt_y-1], secondary, room)
                pt_y -= 2
            elif rnd_val==2:
                store_check_tile(DungeonData.list_tiles[pt_x-1][pt_y], secondary, room)
                pt_x -= 2
            elif rnd_val==3:
                store_check_tile(DungeonData.list_tiles[pt_x][pt_y+1], secondary, room)
                pt_y += 2

#US: 02340458
def create_maze(grid_cell, secondary):
    grid_cell[0x10]=1
    StatusData.has_maze = 1
    room = DungeonData.list_tiles[grid_cell[0]][grid_cell[2]][7]
    for cur_x in range(grid_cell[0]+1, grid_cell[4]-1, 2):
        if DungeonData.list_tiles[cur_x][grid_cell[2]-1][0]&0x3!=1:
            line_maze(cur_x, grid_cell[2]-1, grid_cell[0], grid_cell[2], grid_cell[4], grid_cell[6], secondary, room)
    
    for cur_y in range(grid_cell[2]+1, grid_cell[6]-1, 2):
        if DungeonData.list_tiles[grid_cell[4]][cur_y][0]&0x3!=1:
            line_maze(grid_cell[4], cur_y, grid_cell[0], grid_cell[2], grid_cell[4], grid_cell[6], secondary, room)
    
    for cur_x in range(grid_cell[0]+1, grid_cell[4]-1, 2):
        if DungeonData.list_tiles[cur_x][grid_cell[6]][0]&0x3!=1:
            line_maze(cur_x, grid_cell[6], grid_cell[0], grid_cell[2], grid_cell[4], grid_cell[6], secondary, room)

    for cur_y in range(grid_cell[2]+1, grid_cell[6]-1, 2):
        if DungeonData.list_tiles[grid_cell[0]-1][cur_y][0]&0x3!=1:
            line_maze(grid_cell[0]-1, cur_y, grid_cell[0], grid_cell[2], grid_cell[4], grid_cell[6], secondary, room)
    for cur_x in range(grid_cell[0]+3, grid_cell[4]-3, 2):
        for cur_y in range(grid_cell[2]+3, grid_cell[6]-3, 2):
            if DungeonData.list_tiles[cur_x][cur_y][0]&0x3==1:
                if secondary:
                    DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                    DungeonData.list_tiles[cur_x][cur_y][0] |= 0x2
                else:
                    DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                line_maze(cur_x, cur_y, grid_cell[0], grid_cell[2], grid_cell[4], grid_cell[6], secondary, room)

#US: 02340224
def mazify(grid, max_nb_room_x, max_nb_room_y, maze_chance):
    if maze_chance>0:
        if randrange(100)<maze_chance:
            if StaticParam.PATCH_APPLIED or DungeonData.maze_value<0:
                nb_valid = 0
                for y in range(max_nb_room_y):
                    for x in range(max_nb_room_x):
                        if grid[x][y][8]==0 and grid[x][y][0x11]==0 and grid[x][y][0xb]!=0 and grid[x][y][10]!=0 and \
                           grid[x][y][9]==0 and grid[x][y][0xc]==0 and grid[x][y][0xe]==0 and grid[x][y][0xf]==0:
                            if (grid[x][y][4]-grid[x][y][0])&1 and (grid[x][y][6]-grid[x][y][2])&1:
                                nb_valid += 1
                if nb_valid>0:
                    values = [i==0 for i in range(100)]
                    for x in range(0x40):
                        a = randrange(nb_valid)
                        b = randrange(nb_valid)
                        tmp = values[a]
                        values[a] = values[b]
                        values[b] = tmp
                    counter = 0
                    for y in range(max_nb_room_y):
                        for x in range(max_nb_room_x):
                            if grid[x][y][8]==0 and grid[x][y][0x11]==0 and grid[x][y][0xb]!=0 and grid[x][y][10]!=0 and \
                               grid[x][y][9]==0 and grid[x][y][0xc]==0 and grid[x][y][0xe]==0 and grid[x][y][0xf]==0:
                                if (grid[x][y][4]-grid[x][y][0])&1 and (grid[x][y][6]-grid[x][y][2])&1:
                                    if values[counter]:
                                        create_maze(grid[x][y], 0)
                                    counter += 1

#US: 022E03B0
def get_floor_type():
    if DungeonData.unknown_798==2 and DungeonData.floor_dungeon_number==DungeonData.unknown_751:
        return 2
    if DungeonData.fixed_floor_number>0 and DungeonData.fixed_floor_number<=0x6E:
        return 1
    return 0

#US: 0233FBE8
def generate_kecleon_shop(grid, max_nb_room_x, max_nb_room_y, kecleon_chance):
    if StatusData.has_monster_house==0 and get_floor_type()!=2 and kecleon_chance!=0:
        if randrange(100)<kecleon_chance:
            list_x = [i for i in range(0xF)]
            list_y = [i for i in range(0xF)]
            for x in range(200):
                a = randrange(0xF)
                b = randrange(0xF)
                tmp = list_x[a]
                list_x[a] = list_x[b]
                list_x[b] = tmp
            for x in range(200):
                a = randrange(0xF)
                b = randrange(0xF)
                tmp = list_y[a]
                list_y[a] = list_y[b]
                list_y[b] = tmp
            for i in range(0xF):
                if list_x[i]<max_nb_room_x:
                    x = list_x[i]
                    for j in range(0xF):
                        if list_y[j]<max_nb_room_y:
                            y = list_y[j]
                            if grid[x][y][8]==0 and grid[x][y][0x11]==0 and grid[x][y][0x12]==0 and \
                               grid[x][y][10]!=0 and grid[x][y][0xb]!=0 and grid[x][y][9]==0 and grid[x][y][0x10]==0 and grid[x][y][0x1D]==0:
                                if abs(grid[x][y][0]-grid[x][y][4])>=5 and abs(grid[x][y][2]-grid[x][y][6])>=4:
                                    StatusData.has_kecleon_shop = 1
                                    StatusData.kecleon_shop_min_x = grid[x][y][0]
                                    StatusData.kecleon_shop_min_y = grid[x][y][2]
                                    StatusData.kecleon_shop_max_x = grid[x][y][4]
                                    StatusData.kecleon_shop_max_y = grid[x][y][6]
                                    if grid[x][y][6]-grid[x][y][2]<3:
                                        StatusData.kecleon_shop_max_y = grid[x][y][6] + 1
                                    DungeonData.kecleon_shop_min_x = 9999
                                    DungeonData.kecleon_shop_min_y = 9999
                                    DungeonData.kecleon_shop_max_x = -9999
                                    DungeonData.kecleon_shop_max_y = -9999
                                    for cur_x in range(StatusData.kecleon_shop_min_x+1, StatusData.kecleon_shop_max_x-1):
                                        for cur_y in range(StatusData.kecleon_shop_min_y+1, StatusData.kecleon_shop_max_y-1):
                                            DungeonData.list_tiles[cur_x][cur_y][0] |= 0x20
                                            DungeonData.list_tiles[cur_x][cur_y][2] &= ~0x9
                                            if cur_x<=DungeonData.kecleon_shop_min_x:
                                                DungeonData.kecleon_shop_min_x = cur_x
                                            if cur_y<=DungeonData.kecleon_shop_min_y:
                                                DungeonData.kecleon_shop_min_y = cur_y
                                            if cur_x>=DungeonData.kecleon_shop_max_x:
                                                DungeonData.kecleon_shop_max_x = cur_x
                                            if cur_y>=DungeonData.kecleon_shop_max_y:
                                                DungeonData.kecleon_shop_max_y = cur_y
                                    for cur_x in range(grid[x][y][0], grid[x][y][4]):
                                        for cur_y in range(grid[x][y][2], grid[x][y][6]):
                                            DungeonData.list_tiles[cur_x][cur_y][2] |= 0x10
                                    StatusData.kecleon_shop_middle_x = (StatusData.kecleon_shop_min_x+StatusData.kecleon_shop_max_x)//2
                                    StatusData.kecleon_shop_middle_y = (StatusData.kecleon_shop_min_y+StatusData.kecleon_shop_max_y)//2
                                    return

#US: 02349250
def is_current_mission_type(a,b):
    if DungeonData.mission_flag!=0 and DungeonData.mission_type_1==a and DungeonData.mission_type_2==b:
        return True
    return False

#US: 02349250
def is_current_mission_special_type():
    if DungeonData.mission_flag!=0:
        if DungeonData.mission_type_1 in [0,1,2,7,8,9,10]:
            return True
    return False

#US: 0233FF9C
def generate_monster_house(grid, max_nb_room_x, max_nb_room_y, mh_chance):
    if mh_chance!=0:
        if randrange(100)<mh_chance:
            if StatusData.has_kecleon_shop==0:
                if (is_current_mission_type(10,7) or not is_current_mission_special_type()) and get_floor_type()==0:
                    nb_valid = 0
                    for x in range(max_nb_room_x):
                        for y in range(max_nb_room_y):
                            if grid[x][y][8]==0 and grid[x][y][0x11]==0 and grid[x][y][0xc]==0 and \
                               grid[x][y][10]!=0 and grid[x][y][0xb]!=0 and grid[x][y][9]==0 and grid[x][y][0xf]==0 and grid[x][y][0x10]==0:
                                nb_valid += 1
                    if nb_valid>0:
                        values = [i==0 for i in range(0x100)]
                        for x in range(0x40):
                            a = randrange(nb_valid)
                            b = randrange(nb_valid)
                            tmp = values[a]
                            values[a] = values[b]
                            values[b] = tmp
                        counter = 0
                        for x in range(max_nb_room_x):
                            for y in range(max_nb_room_y):
                                if grid[x][y][8]==0 and grid[x][y][0x11]==0 and grid[x][y][0xc]==0 and \
                                   grid[x][y][10]!=0 and grid[x][y][0xb]!=0 and grid[x][y][9]==0 and grid[x][y][0xf]==0 and grid[x][y][0x10]==0:
                                    if values[counter]:
                                        StatusData.has_monster_house = 1
                                        grid[x][y][0xe] = 1
                                        for cur_x in range(grid[x][y][0], grid[x][y][4]):
                                            for cur_y in range(grid[x][y][2], grid[x][y][6]):
                                                DungeonData.list_tiles[cur_x][cur_y][0] |= 0x40
                                                DungeonData.mh_room = DungeonData.list_tiles[cur_x][cur_y][7]
                                        return
                                    counter += 1

#US: 0233C9E8
def generate_extra_hallways(grid, max_nb_room_x, max_nb_room_y, extra_hallways):
    for i in range(extra_hallways):
        x = randrange(max_nb_room_x)
        y = randrange(max_nb_room_y)
        if grid[x][y][10]!=0 and grid[x][y][0xb]!=0 and grid[x][y][8]==0 and grid[x][y][0x10]==0:
            cur_x = randrange(grid[x][y][0], grid[x][y][4])
            cur_y = randrange(grid[x][y][2], grid[x][y][6])
            rnd_val = randrange(4)*2
            for j in range(3):
                if rnd_val==0 and y>=max_nb_room_y-1:
                    rnd_val = 2
                if rnd_val==2 and x>=max_nb_room_x-1:
                    rnd_val = 4
                if rnd_val==4 and y<=0:
                    rnd_val = 6
                if rnd_val==6 and x<=0:
                    rnd_val = 0
            room = DungeonData.list_tiles[cur_x][cur_y][7]
            ok = True
            while ok:
                if DungeonData.list_tiles[cur_x][cur_y][7]==room:
                    cur_x += StaticParam.LIST_DIRECTIONS[rnd_val*4]
                    cur_y += StaticParam.LIST_DIRECTIONS[rnd_val*4+2]
                else:
                    ok = False
            ok = True
            while ok:
                if DungeonData.list_tiles[cur_x][cur_y][0]&0x3==1:
                    cur_x += StaticParam.LIST_DIRECTIONS[rnd_val*4]
                    cur_y += StaticParam.LIST_DIRECTIONS[rnd_val*4+2]
                else:
                    ok = False
            if DungeonData.list_tiles[cur_x][cur_y][0]!=2:
                valid = True
                for x in range(cur_x-2, cur_x+2):
                    for y in range(cur_y-2, cur_y+2):
                        if x<0 or x>=56 or y<0 or y>=32:
                            valid = False
                            break
                    if not valid:
                        break
                if valid:
                    d = (rnd_val+2) & 0x6
                    if DungeonData.list_tiles[cur_x+StaticParam.LIST_DIRECTIONS[d*4]][cur_y+StaticParam.LIST_DIRECTIONS[d*4+2]][0]&0x3!=1:
                        d2 = (rnd_val-2) & 0x6
                        if DungeonData.list_tiles[cur_x+StaticParam.LIST_DIRECTIONS[d2*4]][cur_y+StaticParam.LIST_DIRECTIONS[d2*4+2]][0]&0x3!=1:
                            rnd = randrange(3)+3
                            while True:
                                if cur_x<=1 or cur_y<=1 or cur_x>=55 or cur_y>=31:
                                    break
                                if DungeonData.list_tiles[cur_x][cur_y][0]&0x3==1:
                                    break
                                if DungeonData.list_tiles[cur_x][cur_y][0]&0x10:
                                    break
                                flag = 1
                                passed = False
                                for v in [(1,0), (1,1), (0,1)]:
                                    if DungeonData.list_tiles[cur_x+v[0]][cur_y+v[1]][0]&0x3!=1:
                                        passed = True
                                        break
                                if not passed:
                                    flag = 0
                                passed = False
                                for v in [(1,0), (1,-1), (0,-1)]:
                                    if DungeonData.list_tiles[cur_x+v[0]][cur_y+v[1]][0]&0x3!=1:
                                        passed = True
                                        break
                                if not passed:
                                    flag = 0
                                passed = False
                                for v in [(-1,0), (-1,1), (0,1)]:
                                    if DungeonData.list_tiles[cur_x+v[0]][cur_y+v[1]][0]&0x3!=1:
                                        passed = True
                                        break
                                if not passed:
                                    flag = 0
                                passed = False
                                for v in [(-1,0), (-1,-1), (0,-1)]:
                                    if DungeonData.list_tiles[cur_x+v[0]][cur_y+v[1]][0]&0x3!=1:
                                        passed = True
                                        break
                                if not passed:
                                    flag = 0
                                if flag:
                                    DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                                    DungeonData.list_tiles[cur_x][cur_y][0] |= 0x1
                                d = (rnd_val+2) & 0x6
                                d2 = (rnd_val-2) & 0x6
                                if DungeonData.list_tiles[cur_x+StaticParam.LIST_DIRECTIONS[d*4]][cur_y+StaticParam.LIST_DIRECTIONS[d*4+2]][0]&0x3==1:
                                    break
                                if DungeonData.list_tiles[cur_x+StaticParam.LIST_DIRECTIONS[d2*4]][cur_y+StaticParam.LIST_DIRECTIONS[d2*4+2]][0]&0x3==1:
                                    break
                                rnd -= 1
                                if rnd==0:
                                    rnd = randrange(3)+3
                                    sel = randrange(100)
                                    if sel<50:
                                        rnd_val += 2
                                    else:
                                        rnd_val -= 2
                                    rnd_val &= 6
                                    if cur_x>=32 and StatusData.floor_size==1 and rnd_val==0x2:
                                        break
                                    if cur_x>=48 and StatusData.floor_size==2 and rnd_val==0x2:
                                        break
                                cur_x+=StaticParam.LIST_DIRECTIONS[rnd_val*4]
                                cur_y+=StaticParam.LIST_DIRECTIONS[rnd_val*4+2]

#US: 0233ED34
def generate_room_imperfections(grid, max_nb_room_x, max_nb_room_y):
    for x in range(max_nb_room_x):
        for y in range(max_nb_room_y):
            if grid[x][y][8]==0 and grid[x][y][0x11]==0 and grid[x][y][0x12]==0 and \
               grid[x][y][10]!=0 and grid[x][y][0xb]!=0 and grid[x][y][9]==0 and grid[x][y][0x10]==0 and grid[x][y][0x1C]!=0:
                if randrange(100)>=StaticParam.IMPERFECT_CHANCE:
                    length = (grid[x][y][4]-grid[x][y][0])+(grid[x][y][6]-grid[x][y][2])
                    length = max(length//4, 1)
                    for counter in range(length):
                        for i in range(2):
                            rnd_val = randrange(4)
                            if rnd_val==0:
                                pt_x = grid[x][y][0]
                                pt_y = grid[x][y][2]
                                if i==0:
                                    move_y = 1 #r5
                                    move_x = 0 #r13+0x28
                                else:
                                    move_y = 0
                                    move_x = 1
                            elif rnd_val==1:
                                pt_x = grid[x][y][4]-1
                                pt_y = grid[x][y][2]
                                if i==0:
                                    move_y = 0
                                    move_x = -1
                                else:
                                    move_y = 1
                                    move_x = 0
                            elif rnd_val==2:
                                pt_x = grid[x][y][4]-1
                                pt_y = grid[x][y][6]-1
                                if i==0:
                                    move_y = -1
                                    move_x = 0
                                else:
                                    move_y = 0
                                    move_x = -1
                            elif rnd_val==3:
                                pt_x = grid[x][y][0]
                                pt_y = grid[x][y][6]-1
                                if i==0:
                                    move_y = 0
                                    move_x = 1
                                else:
                                    move_y = -1
                                    move_x = 0
                            for v in range(10):
                                if pt_x>=grid[x][y][0] and pt_x<grid[x][y][4] and pt_y>=grid[x][y][2] and pt_y<grid[x][y][6]:
                                    if DungeonData.list_tiles[pt_x][pt_y][0]&0x3==1:
                                        c = 0
                                        while c<8:
                                            next_x = pt_x+StaticParam.LIST_DIRECTIONS[c*4]
                                            next_y = pt_y+StaticParam.LIST_DIRECTIONS[c*4+2]
                                            found = False
                                            for dx in [-1,0,1]:
                                                for dy in [-1,0,1]:
                                                    if DungeonData.list_tiles[next_x+dx][next_y+dy][0]&0x3==1:
                                                        if DungeonData.list_tiles[next_x+dx][next_y+dy][7]==0xFF:
                                                            found = True
                                                            break
                                                if found:
                                                    break
                                            if found:
                                                break
                                            c+=1
                                        if c==8:
                                            base = rnd_val*8
                                            c = 0
                                            while c<8:
                                                next_x = pt_x+StaticParam.LIST_DIRECTIONS[c*4]
                                                next_y = pt_y+StaticParam.LIST_DIRECTIONS[c*4+2]
                                                if DungeonData.list_tiles[next_x][next_y][0]&0x3==1:
                                                    val = 1
                                                else:
                                                    val = 0
                                                if StaticParam.LIST_CHECKS[base+c]!=val:
                                                    break
                                                c+=2
                                            if c==8:
                                                DungeonData.list_tiles[pt_x][pt_y][0] &= ~0x3
                                        break
                                    else:
                                        pt_x += move_x
                                        pt_y += move_y
                                else:
                                    break

#US: 0234087C
def set_unk_20(grid_cell):
    for cur_x in range(grid_cell[0], grid_cell[4]):
        for cur_y in range(grid_cell[2], grid_cell[6]):
            DungeonData.list_tiles[cur_x][cur_y][2] |= 0x20

#US: 023408D0
def test_room(cur_x, cur_y):
    for dx in [-1,0,1]:
        if cur_x+dx<0:
            continue
        if cur_x+dx>=56:
            break
        for dy in [-1,0,1]:
            if cur_y+dy<0:
                continue
            if cur_y+dy>=32:
                break
            if dx!=0 and dy!=0:
                continue
            if DungeonData.list_tiles[cur_x+dx][cur_y+dy][0]&3==1 and \
               DungeonData.list_tiles[cur_x+dx][cur_y+dy][7]==0xFF:
                return True
    return False

#US: 0233D674
def generate_room_middle_secondary(grid, max_nb_room_x, max_nb_room_y):
    for y in range(max_nb_room_y):
        for x in range(max_nb_room_x):
            if grid[x][y][8]==0 and grid[x][y][0xe]==0 and grid[x][y][0x12]==0 and \
               grid[x][y][10]!=0 and grid[x][y][0x1D]!=0 and grid[x][y][0x1C]==0:
                rnd_val = randrange(6)
                if rnd_val==1 and StatusData.middle_room_secondary>0:
                    StatusData.middle_room_secondary -= 1
                    if (grid[x][y][4]-grid[x][y][0])&1 and (grid[x][y][6]-grid[x][y][2])&1:
                        set_unk_20(grid[x][y])
                        create_maze(grid[x][y], 1)
                    else:
                        middle_x = (grid[x][y][4]+grid[x][y][0])//2
                        middle_y = (grid[x][y][6]+grid[x][y][2])//2
                        if grid[x][y][4]-grid[x][y][0]>=5 and grid[x][y][6]-grid[x][y][2]>=5:
                            DungeonData.list_tiles[middle_x][middle_y][0] &= ~0x3
                            DungeonData.list_tiles[middle_x][middle_y][0] |= 0x2
                            DungeonData.list_tiles[middle_x][middle_y-1][0] &= ~0x3
                            DungeonData.list_tiles[middle_x][middle_y-1][0] |= 0x2
                            DungeonData.list_tiles[middle_x-1][middle_y][0] &= ~0x3
                            DungeonData.list_tiles[middle_x-1][middle_y][0] |= 0x2
                            DungeonData.list_tiles[middle_x+1][middle_y][0] &= ~0x3
                            DungeonData.list_tiles[middle_x+1][middle_y][0] |= 0x2
                            DungeonData.list_tiles[middle_x][middle_y+1][0] &= ~0x3
                            DungeonData.list_tiles[middle_x][middle_y+1][0] |= 0x2
                        else:
                            DungeonData.list_tiles[middle_x][middle_y][0] &= ~0x3
                            DungeonData.list_tiles[middle_x][middle_y][0] |= 0x2
                    grid[x][y][9] = 1
                elif rnd_val==2 and StatusData.middle_room_secondary>0:
                    if (grid[x][y][4]-grid[x][y][0])&1 and (grid[x][y][6]-grid[x][y][2])&1:
                        StatusData.middle_room_secondary -= 1
                        set_unk_20(grid[x][y])
                        for i in range(0x40):
                            rnd_x = randrange(grid[x][y][4]-grid[x][y][0])
                            rnd_y = randrange(grid[x][y][6]-grid[x][y][2])
                            if (rnd_x+rnd_y)&1:
                                DungeonData.list_tiles[grid[x][y][0]+rnd_x][grid[x][y][2]+rnd_y][0] &= ~0x3
                                DungeonData.list_tiles[grid[x][y][0]+rnd_x][grid[x][y][2]+rnd_y][0] |= 0x2
                        grid[x][y][9] = 1
                elif rnd_val==3:
                    if grid[x][y][4]-grid[x][y][0]>=5 and grid[x][y][6]-grid[x][y][2]>=5:
                        rnd_x1 = randrangeswap(grid[x][y][0]+2, grid[x][y][4]-3)
                        rnd_y1 = randrangeswap(grid[x][y][2]+2, grid[x][y][6]-3)
                        rnd_x2 = randrangeswap(grid[x][y][0]+2, grid[x][y][4]-3)
                        rnd_y2 = randrangeswap(grid[x][y][2]+2, grid[x][y][6]-3)
                        if StatusData.middle_room_secondary>0:
                            StatusData.middle_room_secondary -= 1
                            set_unk_20(grid[x][y])
                            if rnd_x1>rnd_x2:
                                tmp=rnd_x1
                                rnd_x1=rnd_x2
                                rnd_x2=tmp
                            if rnd_y1>rnd_y2:
                                tmp=rnd_y1
                                rnd_y1=rnd_y2
                                rnd_y2=tmp
                            for cur_x in range(rnd_x1,rnd_x2+1):
                                for cur_y in range(rnd_y1,rnd_y2+1):
                                    DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                                    DungeonData.list_tiles[cur_x][cur_y][0] |= 0x2
                            grid[x][y][9] = 1
                elif rnd_val==4:
                    if grid[x][y][4]-grid[x][y][0]>=6 and grid[x][y][6]-grid[x][y][2]>=6:
                        middle_x = (grid[x][y][4]+grid[x][y][0])//2
                        middle_y = (grid[x][y][6]+grid[x][y][2])//2
                        if StatusData.middle_room_secondary>0:
                            StatusData.middle_room_secondary -= 1
                            set_unk_20(grid[x][y])
                            for t in [(-2,-2), (-1,-2), (0,-2), (1,-2), (-2,-1), (-2,0), (-2,1), (-2,1), (-1,1), (0,1), (1,-2), (1,-1), (1,0), (1,1)]:
                                DungeonData.list_tiles[middle_x+t[0]][middle_y+t[1]][0] &= ~0x3
                                DungeonData.list_tiles[middle_x+t[0]][middle_y+t[1]][0] |= 0x6
                            DungeonData.list_tiles[middle_x-1][middle_y-1][2] |= 0x54
                            DungeonData.list_tiles[middle_x][middle_y-1][2] |= 0x12
                            DungeonData.list_tiles[middle_x-1][middle_y][2] |= 0x12
                            DungeonData.list_tiles[middle_x][middle_y][2] |= 0x12
                            grid[x][y][9] = 1
                elif rnd_val==5 and StatusData.middle_room_secondary>0:
                    StatusData.middle_room_secondary -= 1
                    set_unk_20(grid[x][y])
                    if randrange(2)==0:
                        middle_y = (grid[x][y][6]+grid[x][y][2])//2
                        valid = True
                        for i in range(grid[x][y][0], grid[x][y][4]):
                            if test_room(i,middle_y):
                                valid = False
                                break
                        if valid:
                            for i in range(grid[x][y][0], grid[x][y][4]):
                                DungeonData.list_tiles[i][middle_y][0] &= ~0x3
                                DungeonData.list_tiles[i][middle_y][0] |= 0x2
                            for cur_x in range(grid[x][y][0], grid[x][y][4]):
                                for cur_y in range(grid[x][y][2], grid[x][y][6]):
                                    DungeonData.list_tiles[cur_x][cur_y][2] |= 0x80
                            grid[x][y][9] = 1
                    else:
                        middle_x = (grid[x][y][4]+grid[x][y][0])//2
                        valid = True
                        for i in range(grid[x][y][2], grid[x][y][6]):
                            if test_room(middle_x,i):
                                valid = False
                                break
                        if valid:
                            for i in range(grid[x][y][2], grid[x][y][6]):
                                DungeonData.list_tiles[middle_x][i][0] &= ~0x3
                                DungeonData.list_tiles[middle_x][i][0] |= 0x2
                            for cur_x in range(grid[x][y][0], grid[x][y][4]):
                                for cur_y in range(grid[x][y][2], grid[x][y][6]):
                                    DungeonData.list_tiles[cur_x][cur_y][2] |= 0x80
                            grid[x][y][9] = 1

#US: 0233B028
def generate_normal_floor(max_nb_room_x, max_nb_room_y, prop):
    list_x, list_y = generate_grid_positions(max_nb_room_x, max_nb_room_y)
    grid = init_grid(max_nb_room_x, max_nb_room_y)
    place_rooms(grid, max_nb_room_x, max_nb_room_y, prop.nb_rooms)
    #RandomGenerator.print()
    create_rooms(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, prop.bit_flags)
    #RandomGenerator.print()
    rnd_x = randrange(max_nb_room_x)
    rnd_y = randrange(max_nb_room_y)
    create_connections(grid, max_nb_room_x, max_nb_room_y, rnd_x, rnd_y, prop)
    #RandomGenerator.print()
    create_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, 0)
    #RandomGenerator.print()
    """
    print("-----------------------------")
    print("%08X" % max_nb_room_x)
    print("%08X" % max_nb_room_y)
    print("-----------------------------")
    for x in range(15):
        for y in range(15):
            c = grid[x][y]
            print("%04X" % c[0])
            print("%04X" % c[2])
            print("%04X" % c[4])
            print("%04X" % c[6])
            print("-----------------------------")
    """
    add_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y)
    #RandomGenerator.print()
    mazify(grid, max_nb_room_x, max_nb_room_y, prop.maze_chance)
    generate_kecleon_shop(grid, max_nb_room_x, max_nb_room_y, StatusData.kecleon_chance)
    generate_monster_house(grid, max_nb_room_x, max_nb_room_y, StatusData.mh_chance)
    #RandomGenerator.print()
    generate_extra_hallways(grid, max_nb_room_x, max_nb_room_y, prop.extra_hallways)
    #RandomGenerator.print()
    generate_room_imperfections(grid, max_nb_room_x, max_nb_room_y)
    #RandomGenerator.print()
    generate_room_middle_secondary(grid, max_nb_room_x, max_nb_room_y)
    #RandomGenerator.print()

#US: 02342B7C
def reset_y_borders():
    for x in range(56):
        DungeonData.list_tiles[x][1]=TileData()
        if x==0 or x==55:
            DungeonData.list_tiles[x][1][0]|=0x10
        DungeonData.list_tiles[x][0x1E]=TileData()
        if x==0 or x==55:
            DungeonData.list_tiles[x][0x1E][0]|=0x10

#US: 02340A78
def delete_status_10():
    for x in range(56):
        for y in range(32):
            if DungeonData.list_tiles[x][y][0]&0x10:
                DungeonData.list_tiles[x][y][0] &= ~0x3
#US: 0233F93C
def generate_junctions():
    for x in range(56):
        for y in range(32):
            if DungeonData.list_tiles[x][y][0]&3==1:
                if DungeonData.list_tiles[x][y][7]==0xFF:
                    if x>0 and DungeonData.list_tiles[x-1][y][7]!=0xFF:
                        DungeonData.list_tiles[x-1][y][0] |= 8
                        if DungeonData.list_tiles[x-1][y][0]&3==2:
                            DungeonData.list_tiles[x-1][y][0] &= ~0x3
                            DungeonData.list_tiles[x-1][y][0] |= 1
                    if y>0 and DungeonData.list_tiles[x][y-1][7]!=0xFF:
                        DungeonData.list_tiles[x][y-1][0] |= 8
                        if DungeonData.list_tiles[x][y-1][0]&3==2:
                            DungeonData.list_tiles[x][y-1][0] &= ~0x3
                            DungeonData.list_tiles[x][y-1][0] |= 1
                    if y<31 and DungeonData.list_tiles[x][y+1][7]!=0xFF:
                        DungeonData.list_tiles[x][y+1][0] |= 8
                        if DungeonData.list_tiles[x][y+1][0]&3==2:
                            DungeonData.list_tiles[x][y+1][0] &= ~0x3
                            DungeonData.list_tiles[x][y+1][0] |= 1
                    if x<55 and DungeonData.list_tiles[x+1][y][7]!=0xFF:
                        DungeonData.list_tiles[x+1][y][0] |= 8
                        if DungeonData.list_tiles[x+1][y][0]&3==2:
                            DungeonData.list_tiles[x+1][y][0] &= ~0x3
                            DungeonData.list_tiles[x+1][y][0] |= 1
                elif DungeonData.list_tiles[x][y][7]==0xFE:
                    DungeonData.list_tiles[x][y][7] = 0xFF

#US: 02340CAC
def is_out_of_bounds(x,y):
    return (x<0 or x>=56 or y<0 or y>=32)

#US: 0234176C
def store_secondary_check(tile):
    if not tile[0]&0x13:
        tile[0] &= ~0x3
        tile[0] |= 2

#US: 023417AC
def generate_secondary(test_attrib, prop):
    if prop.bit_flags&test_attrib:
        nb_gen = [1,1,1,2,2,2,3,3][randrange(8)]
        for i in range(nb_gen):
            if randrange(100)<50:
                pt_y = 31
                dir_y = -1
                test = True
            else:
                pt_y = 0
                dir_y = 1
                test = False
            rnd_val = randrange(50)+10
            pt_x = randrange(2,54)
            dir_x = 0
            ok = False
            while not ok:
                for v in range(randrange(6)+2):
                    if 0<=pt_x<56:
                        if 0<=pt_y<32:
                            tile = DungeonData.list_tiles[pt_x][pt_y]
                        else:
                            tile = StaticParam.DEFAULT_TILE
                        if tile[0]&3==2:
                            ok = True
                            break
                        if not is_out_of_bounds(pt_x, pt_y):
                            store_secondary_check(DungeonData.list_tiles[pt_x][pt_y])
                    pt_x += dir_x
                    pt_y += dir_y
                    if pt_y<0 or pt_y>=32:
                        break
                    rnd_val -= 1
                    if rnd_val==0:
                        for j in range(0x40):
                            off_x = randrange(7)-3
                            off_y = randrange(7)-3
                            if 2<=pt_x+off_x<54 and 2<=pt_y+off_y<30:
                                second_near = False
                                for x in range(-1,2):
                                    for y in range(-1,2):
                                        if x!=0 or y!=0:
                                            if DungeonData.list_tiles[pt_x+off_x+x][pt_y+off_y+y][0]&3==2:
                                                second_near = True
                                                break
                                    if second_near:
                                        break
                                if second_near:
                                    if not is_out_of_bounds(pt_x+off_x, pt_y+off_y):
                                        store_secondary_check(DungeonData.list_tiles[pt_x+off_x][pt_y+off_y])
                        for off_x in range(-3,4):
                            for off_y in range(-3,4):
                                counter = 0
                                if 2<=pt_x+off_x<54 and 2<=pt_y+off_y<30:
                                    for x in range(-1,2):
                                        for y in range(-1,2):
                                            if x!=0 or y!=0:
                                                if DungeonData.list_tiles[pt_x+off_x+x][pt_y+off_y+y][0]&3==2:
                                                    counter += 1
                                    if counter>=4:
                                        if not is_out_of_bounds(pt_x+off_x, pt_y+off_y):
                                            store_secondary_check(DungeonData.list_tiles[pt_x+off_x][pt_y+off_y])
                if not ok:
                    if dir_x!=0:
                        if test:
                            dir_y = -1
                        else:
                            dir_y = 1
                        dir_x = 0
                    else:
                        if randrange(100)<50:
                            dir_x = -1
                        else:
                            dir_x = 1
                        dir_y = 0
                if pt_y<0 or pt_y>=32:
                    ok = True
        #RandomGenerator.print()
        for i in range(prop.secondary_density):
            attempts = 0
            while attempts<200:
                rnd_x = randrange(56)
                rnd_y = randrange(32)
                if 1<=rnd_x<55 and 1<=rnd_y<31:
                    break
                attempts += 1
            if attempts!=200:
                table = [[(x==0 or y==0 or x==9 or y==9) for x in range(10)] for y in range(10)]
                for v in range(0x50):
                    x = randrange(8)+1
                    y = randrange(8)+1
                    if table[x-1][y] or table[x+1][y] or table[x][y+1] or table[x][y-1]:
                        table[x][y] = True
                for x in range(10):
                    for y in range(10):
                        if not table[x][y]:
                            if not is_out_of_bounds(rnd_x+x-5,rnd_y+y-5):
                                store_secondary_check(DungeonData.list_tiles[rnd_x+x-5][rnd_y+y-5])
                            else:
                                store_secondary_check(StaticParam.DEFAULT_TILE)
        for x in range(56):
            for y in range(32):
                if DungeonData.list_tiles[x][y][0]&0x3==2:
                    if DungeonData.list_tiles[x][y][0]&0x160 or DungeonData.list_tiles[x][y][2]&0x1:
                        DungeonData.list_tiles[x][y][0] &= ~0x3
                        DungeonData.list_tiles[x][y][0] |= 1
                    else:
                        if x<=1 or x>=55 or y<=1 or y>=31:
                            DungeonData.list_tiles[x][y][0] &= ~0x3

#US: 0233C774
def generate_one_mh_room():
    grid = init_grid(1,1)
    grid[0][0][0] = 2
    grid[0][0][2] = 2
    grid[0][0][4] = 54
    grid[0][0][6] = 30
    grid[0][0][10] = 1
    grid[0][0][0xb] = 1
    grid[0][0][8] = 0
    for x in range(grid[0][0][0], grid[0][0][4]):
            for y in range(grid[0][0][2], grid[0][0][6]):
                DungeonData.list_tiles[x][y][0] &= ~0x3
                DungeonData.list_tiles[x][y][0] |= 1
                DungeonData.list_tiles[x][y][7] = 0
    generate_monster_house(grid, 1, 1, 999)

#US: 0233B190
def generate_ring(prop):
    max_nb_room_x = 6
    max_nb_room_y = 4
    list_x = [0,5,0x10,0x1C,0x27,0x33,0x38]
    list_y = [2,7,0x10,0x19,0x1E]
    grid = init_grid(max_nb_room_x, max_nb_room_y)
    
    for i in range(6):
        grid[i][0][10]=0
        grid[i][3][10]=0
    
    for i in range(4):
        grid[0][i][10]=0
        grid[5][i][10]=0
    
    for x in range(1,5):
        for y in range(1,3):
            grid[x][y][10]=1
    room_nb = 0
    for y in range(4):
        for x in range(6):
            if grid[x][y][10]:
                range_x = list_x[x+1]-list_x[x]-3
                range_y = list_y[y+1]-list_y[y]-3
                size_x = randrangeswap(5, range_x)
                size_y = randrangeswap(4, range_y)
                start_x = randrangeforce(range_x-size_x)+list_x[x]+2
                start_y = randrangeforce(range_y-size_y)+list_y[y]+2
                grid[x][y][0]=start_x
                grid[x][y][2]=start_y
                grid[x][y][4]=start_x+size_x
                grid[x][y][6]=start_y+size_y
                for cur_x in range(start_x, start_x+size_x):
                    for cur_y in range(start_y, start_y+size_y):
                        DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                        DungeonData.list_tiles[cur_x][cur_y][0] |= 1
                        DungeonData.list_tiles[cur_x][cur_y][7] = room_nb
                room_nb += 1
            else:
                start_x = randrangeswap(list_x[x]+1, list_x[x+1]-2)
                start_y = randrangeswap(list_y[y]+1, list_y[y+1]-2)
                grid[x][y][0]=start_x
                grid[x][y][2]=start_y
                grid[x][y][4]=start_x+1
                grid[x][y][6]=start_y+1
                DungeonData.list_tiles[start_x][start_y][0] &= ~0x3
                DungeonData.list_tiles[start_x][start_y][0] |= 1
                DungeonData.list_tiles[start_x][start_y][7] = 0xFF
    grid[0][0][0x16]=1
    grid[1][0][0x15]=1
    grid[1][0][0x16]=1
    grid[2][0][0x15]=1
    grid[2][0][0x16]=1
    grid[3][0][0x15]=1
    grid[3][0][0x16]=1
    grid[4][0][0x15]=1
    grid[4][0][0x16]=1
    grid[5][0][0x15]=1
    grid[0][0][0x14]=1
    grid[0][1][0x13]=1
    grid[0][1][0x14]=1
    grid[0][2][0x13]=1
    grid[0][2][0x14]=1
    grid[0][3][0x13]=1
    grid[0][3][0x16]=1
    grid[1][3][0x15]=1
    grid[1][3][0x16]=1
    grid[2][3][0x15]=1
    grid[2][3][0x16]=1
    grid[3][3][0x15]=1
    grid[3][3][0x16]=1
    grid[4][3][0x15]=1
    grid[4][3][0x16]=1
    grid[5][3][0x15]=1
    grid[5][0][0x14]=1
    grid[5][1][0x13]=1
    grid[5][1][0x14]=1
    grid[5][2][0x13]=1
    grid[5][2][0x14]=1
    grid[5][3][0x13]=1
    rnd_x = randrange(max_nb_room_x)
    rnd_y = randrange(max_nb_room_y)
    create_connections(grid, max_nb_room_x, max_nb_room_y, rnd_x, rnd_y, prop)
    create_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, 0)
    add_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y)
    generate_kecleon_shop(grid, max_nb_room_x, max_nb_room_y, StatusData.kecleon_chance)
    generate_monster_house(grid, max_nb_room_x, max_nb_room_y, StatusData.mh_chance)
    generate_extra_hallways(grid, max_nb_room_x, max_nb_room_y, prop.extra_hallways)
    generate_room_imperfections(grid, max_nb_room_x, max_nb_room_y)

#US: 0233B61C
def generate_crossroads(prop):
    max_nb_room_x = 5
    max_nb_room_y = 4
    list_x = [0,0xB,0x16,0x21,0x2C,0x38]
    list_y = [1,9,0x10,0x17,0x1F]
    grid = init_grid(max_nb_room_x, max_nb_room_y)
    for i in range(5):
        grid[i][0][10]=1
        grid[i][3][10]=1
    for i in range(4):
        grid[0][i][10]=1
        grid[5][i][10]=1

    for x in range(1,4):
        for y in range(1,3):
            grid[x][y][10]=0

    grid[0][0][8]=1
    grid[0][3][8]=1
    grid[4][0][8]=1
    grid[4][3][8]=1
    
    room_nb = 0
    for y in range(4):
        for x in range(5):
            if grid[x][y][8]==0:
                if grid[x][y][10]:
                    range_x = list_x[x+1]-list_x[x]-3
                    range_y = list_y[y+1]-list_y[y]-3
                    size_x = randrangeswap(5, range_x)
                    size_y = randrangeswap(4, range_y)
                    start_x = randrangeforce(range_x-size_x)+list_x[x]+2
                    start_y = randrangeforce(range_y-size_y)+list_y[y]+2
                    grid[x][y][0]=start_x
                    grid[x][y][2]=start_y
                    grid[x][y][4]=start_x+size_x
                    grid[x][y][6]=start_y+size_y
                    for cur_x in range(start_x, start_x+size_x):
                        for cur_y in range(start_y, start_y+size_y):
                            DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                            DungeonData.list_tiles[cur_x][cur_y][0] |= 1
                            DungeonData.list_tiles[cur_x][cur_y][7] = room_nb
                    room_nb += 1
                else:
                    start_x = randrangeswap(list_x[x]+1, list_x[x+1]-2)
                    start_y = randrangeswap(list_y[y]+1, list_y[y+1]-2)
                    grid[x][y][0]=start_x
                    grid[x][y][2]=start_y
                    grid[x][y][4]=start_x+1
                    grid[x][y][6]=start_y+1
                    DungeonData.list_tiles[start_x][start_y][0] &= ~0x3
                    DungeonData.list_tiles[start_x][start_y][0] |= 1
                    DungeonData.list_tiles[start_x][start_y][7] = 0xFF
    for x in range(1,4):
        for y in range(3):
            grid[x][y][0x14]=1
            grid[x][y+1][0x13]=1
    for x in range(4):
        for y in range(1,3):
            grid[x][y][0x16]=1
            grid[x+1][y][0x15]=1
    create_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, 1)
    add_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y)
    generate_kecleon_shop(grid, max_nb_room_x, max_nb_room_y, StatusData.kecleon_chance)
    generate_monster_house(grid, max_nb_room_x, max_nb_room_y, StatusData.mh_chance)
    generate_extra_hallways(grid, max_nb_room_x, max_nb_room_y, prop.extra_hallways)
    generate_room_imperfections(grid, max_nb_room_x, max_nb_room_y)

#US: 0233C844
def generate_2_rooms_mh():
    max_nb_room_x = 2
    max_nb_room_y = 1
    list_x = [2,0x1C,0x36]
    list_y = [2,0x1E]
    grid = init_grid(max_nb_room_x, max_nb_room_y)
    room_nb = 0
    y = 0
    for x in range(2):
        range_x = list_x[x+1]-list_x[x]-3
        range_y = list_y[y+1]-list_y[y]-3
        size_x = randrangeswap(10, range_x)
        size_y = randrangeswap(16, range_y)
        start_x = randrangeforce(range_x-size_x)+list_x[x]+1
        start_y = randrangeforce(range_y-size_y)+list_y[y]+1
        grid[x][y][0]=start_x
        grid[x][y][2]=start_y
        grid[x][y][4]=start_x+size_x
        grid[x][y][6]=start_y+size_y
        for cur_x in range(start_x, start_x+size_x):
            for cur_y in range(start_y, start_y+size_y):
                DungeonData.list_tiles[cur_x][cur_y][0] &= ~0x3
                DungeonData.list_tiles[cur_x][cur_y][0] |= 1
                DungeonData.list_tiles[cur_x][cur_y][7] = room_nb
        room_nb += 1
    grid[0][0][0x16] = 1
    grid[1][0][0x15] = 1
    create_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, 0)
    generate_monster_house(grid, max_nb_room_x, max_nb_room_y, 999)

#US: 0233BA7C
def generate_room_line(prop):
    max_nb_room_x = 5
    max_nb_room_y = 1
    list_x = [0,0xB,0x16,0x21,0x2C,0x38]
    list_y = [4,0xF]
    grid = init_grid(max_nb_room_x, max_nb_room_y)
    place_rooms(grid, max_nb_room_x, max_nb_room_y, prop.nb_rooms)
    create_rooms(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, prop.bit_flags)
    rnd_x = randrange(max_nb_room_x)
    rnd_y = randrange(max_nb_room_y)
    create_connections(grid, max_nb_room_x, max_nb_room_y, rnd_x, rnd_y, prop)
    create_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, 1)
    add_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y)
    generate_kecleon_shop(grid, max_nb_room_x, max_nb_room_y, StatusData.kecleon_chance)
    generate_monster_house(grid, max_nb_room_x, max_nb_room_y, StatusData.mh_chance)
    generate_extra_hallways(grid, max_nb_room_x, max_nb_room_y, prop.extra_hallways)
    generate_room_imperfections(grid, max_nb_room_x, max_nb_room_y)

#US: 0233BBDC
def generate_cross(prop):
    max_nb_room_x = 3
    max_nb_room_y = 3
    list_x = [0xB,0x16,0x21,0x2C]
    list_y = [2,0xB,0x14,0x1E]
    grid = init_grid(max_nb_room_x, max_nb_room_y)
    for x in range(3):
        for y in range(3):
            grid[x][y][10]=1
    grid[0][0][8]=1
    grid[0][2][8]=1
    grid[2][0][8]=1
    grid[2][2][8]=1
    create_rooms(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, prop.bit_flags)
    grid[1][0][0x14]=1
    grid[1][1][0x13]=1
    grid[1][1][0x14]=1
    grid[1][2][0x13]=1
    grid[0][1][0x16]=1
    grid[1][1][0x15]=1
    grid[1][1][0x16]=1
    grid[2][1][0x15]=1
    create_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, 1)
    add_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y)
    generate_kecleon_shop(grid, max_nb_room_x, max_nb_room_y, StatusData.kecleon_chance)
    generate_monster_house(grid, max_nb_room_x, max_nb_room_y, StatusData.mh_chance)
    generate_extra_hallways(grid, max_nb_room_x, max_nb_room_y, prop.extra_hallways)
    generate_room_imperfections(grid, max_nb_room_x, max_nb_room_y)

#US: 0233BF30
def merge_rooms(room_x, room_y1, room_y2, grid):
    room_y2 += room_y1
    src_x = min(grid[room_x][room_y1][0], grid[room_x][room_y2][0])
    dst_x = max(grid[room_x][room_y1][4], grid[room_x][room_y2][4])
    src_y = grid[room_x][room_y1][2]
    dst_y = grid[room_x][room_y2][6]
    room = DungeonData.list_tiles[grid[room_x][room_y1][0]][grid[room_x][room_y1][2]][7]
    for x in range(src_x, dst_x):
        for y in range(src_y, dst_y):
            DungeonData.list_tiles[x][y][0] &= ~0x3
            DungeonData.list_tiles[x][y][0] |= 0x1
            DungeonData.list_tiles[x][y][7] = room
    grid[room_x][room_y1][0] = src_x
    grid[room_x][room_y1][2] = src_y
    grid[room_x][room_y1][4] = dst_x
    grid[room_x][room_y1][6] = dst_y
    grid[room_x][room_y1][0x12] = 1
    grid[room_x][room_y2][0x12] = 1
    grid[room_x][room_y2][0xb] = 0
    grid[room_x][room_y2][0x11] = 1
    
#US: 0233BD74
def generate_beetle(prop):
    max_nb_room_x = 3
    max_nb_room_y = 3
    list_x = [0x5,0xF,0x23,0x32]
    list_y = [2,0xB,0x14,0x1E]
    grid = init_grid(max_nb_room_x, max_nb_room_y)
    for x in range(3):
        for y in range(3):
            grid[x][y][10]=1
    create_rooms(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, prop.bit_flags)
    for y in range(3):
        grid[0][y][0x16]=1
        grid[1][y][0x15]=1
        grid[1][y][0x16]=1
        grid[2][y][0x15]=1
    create_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, 1)
    merge_rooms(1,0,1,grid)
    merge_rooms(1,0,2,grid)
    add_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y)
    generate_kecleon_shop(grid, max_nb_room_x, max_nb_room_y, StatusData.kecleon_chance)
    generate_monster_house(grid, max_nb_room_x, max_nb_room_y, StatusData.mh_chance)
    generate_extra_hallways(grid, max_nb_room_x, max_nb_room_y, prop.extra_hallways)
    generate_room_imperfections(grid, max_nb_room_x, max_nb_room_y)

#US: 0233C07C
def generate_outer_room_floor(max_nb_room_x, max_nb_room_y, prop):
    list_x, list_y = generate_grid_positions(max_nb_room_x, max_nb_room_y)
    grid = init_grid(max_nb_room_x, max_nb_room_y)
    for x in range(max_nb_room_x):
        for y in range(max_nb_room_y):
            grid[x][y][10] = 1
    for x in range(1,max_nb_room_x-1):
        for y in range(1,max_nb_room_y-1):
            grid[x][y][8] = 1
    create_rooms(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, prop.bit_flags)
    if StaticParam.FIX_OUTER_ROOM_ERROR:
        for x in range(max_nb_room_x):
            if x>0:
                grid[x][0][0x16] = 1
                grid[x][max_nb_room_y-1][0x16] = 1
            if x<max_nb_room_x-1:
                grid[x+1][0][0x15] = 1
                grid[x+1][max_nb_room_y-1][0x15] = 1
        for y in range(max_nb_room_y):
            if y>0:
                grid[0][y][0x13] = 1
                grid[max_nb_room_x-1][y][0x13] = 1
            if y<max_nb_room_y-1:
                grid[0][y+1][0x14] = 1
                grid[max_nb_room_x-1][y+1][0x14] = 1
    else:
        # Normal algorithm has weird conditions
        for x in range(max_nb_room_x-1):
            if x>0:
                grid[x][0][0x16] = 1
                grid[x][max_nb_room_y-1][0x16] = 1
            if x<max_nb_room_x-2:
                grid[x+1][0][0x15] = 1
                grid[x+1][max_nb_room_y-1][0x15] = 1
        for y in range(max_nb_room_y-1):
            if y>0:
                grid[0][y][0x13] = 1
                grid[max_nb_room_x-1][y][0x13] = 1
            # Glitch on normal algorithm: connections are not made with the last row
            if y<max_nb_room_y-2:
                grid[0][y][0x14] = 1
                grid[max_nb_room_x-1][y][0x14] = 1
    create_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y, 0)
    add_hallways(grid, max_nb_room_x, max_nb_room_y, list_x, list_y)
    mazify(grid, max_nb_room_x, max_nb_room_y, prop.maze_chance)
    generate_kecleon_shop(grid, max_nb_room_x, max_nb_room_y, StatusData.kecleon_chance)
    generate_monster_house(grid, max_nb_room_x, max_nb_room_y, StatusData.mh_chance)
    generate_extra_hallways(grid, max_nb_room_x, max_nb_room_y, prop.extra_hallways)
    generate_room_imperfections(grid, max_nb_room_x, max_nb_room_y)
    generate_room_middle_secondary(grid, max_nb_room_x, max_nb_room_y)

#SPECIAL
def generate_maze():
    grid = init_grid(1,1)
    grid[0][0][0] = 2
    grid[0][0][2] = 2
    grid[0][0][4] = 53
    grid[0][0][6] = 29
    grid[0][0][10] = 1
    grid[0][0][0xb] = 1
    grid[0][0][8] = 0
    for x in range(grid[0][0][0], grid[0][0][4]):
            for y in range(grid[0][0][2], grid[0][0][6]):
                DungeonData.list_tiles[x][y][0] &= ~0x3
                DungeonData.list_tiles[x][y][0] |= 1
    create_maze(grid[0][0], 0)
    for x in range(2, 5):
            for y in range(2, 5):
                DungeonData.list_tiles[x][y][0] &= ~0x3
                DungeonData.list_tiles[x][y][0] |= 1
                DungeonData.list_tiles[x][y][7] = 0x0
    for x in range(2, 5):
            for y in range(26, 29):
                DungeonData.list_tiles[x][y][0] &= ~0x3
                DungeonData.list_tiles[x][y][0] |= 1
                DungeonData.list_tiles[x][y][7] = 0x1
    for x in range(50, 53):
            for y in range(2, 5):
                DungeonData.list_tiles[x][y][0] &= ~0x3
                DungeonData.list_tiles[x][y][0] |= 1
                DungeonData.list_tiles[x][y][7] = 0x2
    for x in range(50, 53):
            for y in range(26, 29):
                DungeonData.list_tiles[x][y][0] &= ~0x3
                DungeonData.list_tiles[x][y][0] |= 1
                DungeonData.list_tiles[x][y][7] = 0x3
    for x in range(26, 29):
            for y in range(14, 17):
                DungeonData.list_tiles[x][y][0] &= ~0x3
                DungeonData.list_tiles[x][y][0] |= 1
                DungeonData.list_tiles[x][y][7] = 0x4

#US: 02342C8C
def generate_stairs(spawn, hidden_stairs):
    x = spawn[0]
    y = spawn[1]
    DungeonData.list_tiles[x][y][2]|=0x1
    DungeonData.list_tiles[x][y][2]&=~0x2
    if not hidden_stairs:
        DungeonData.stairs_spawn_x = x
        DungeonData.stairs_spawn_y = y
        StatusData.stairs_room = DungeonData.list_tiles[x][y][7]
    else:
        if StatusData.second_spawn:
            StatusData.hidden_stairs_spawn_x = x
            StatusData.hidden_stairs_spawn_y = y
        else:
            DungeonData.hidden_stairs_spawn_x = x
            DungeonData.hidden_stairs_spawn_y = y
            DungeonData.hidden_stairs_type = hidden_stairs
    if not hidden_stairs and get_floor_type()==2:
        room = DungeonData.list_tiles[x][y][7]
        for x in range(56):
            for y in range(32):
                if DungeonData.list_tiles[x][y][0]&3==1 and DungeonData.list_tiles[x][y][7]==room:
                    DungeonData.list_tiles[x][y][0]|=0x40
                    DungeonData.mh_room = DungeonData.list_tiles[x][y][7]

#US: 02340CE4
def shuffle_spawns(valid_spawns):
    for i in range(len(valid_spawns)*2):
        a = randrange(len(valid_spawns))
        b = randrange(len(valid_spawns))
        tmp = valid_spawns[a]
        valid_spawns[a] = valid_spawns[b]
        valid_spawns[b] = tmp

#US: 02340D4C
def generate_item_spawns(prop, empty):
    if DungeonData.stairs_spawn_x==-1 or DungeonData.stairs_spawn_y==-1:
        valid_spawns = []
        for x in range(56):
            for y in range(32):
                if DungeonData.list_tiles[x][y][0]&0x3==1 and DungeonData.list_tiles[x][y][7]!=0xFF and DungeonData.list_tiles[x][y][0]&0x20==0 \
                    and DungeonData.list_tiles[x][y][2]&0x8==0 and DungeonData.list_tiles[x][y][2]&0x10==0 and DungeonData.list_tiles[x][y][0]&0x8==0 \
                     and DungeonData.list_tiles[x][y][0]&0x100==0:
                    valid_spawns.append((x, y))
        if len(valid_spawns)>0:
            stairs = randrange(len(valid_spawns))
            generate_stairs(valid_spawns[stairs], 0)
            if StatusData.hidden_stairs_type:
                del valid_spawns[stairs]
                if DungeonData.floor_dungeon_number+1<DungeonData.floor_dungeon_max:
                    use_gen_1(3)
                    stairs = randrange(len(valid_spawns))
                    generate_stairs(valid_spawns[stairs], StatusData.hidden_stairs_type)
                    use_gen_0()
    #RandomGenerator.print()
    valid_spawns = []
    for x in range(56):
        for y in range(32):
            if DungeonData.list_tiles[x][y][0]&0x3==1 and DungeonData.list_tiles[x][y][7]!=0xFF and DungeonData.list_tiles[x][y][0]&0x20==0 \
                and DungeonData.list_tiles[x][y][0]&0x40==0 and DungeonData.list_tiles[x][y][0]&0x8==0 \
                 and DungeonData.list_tiles[x][y][0]&0x100==0:
                valid_spawns.append((x, y))
    if len(valid_spawns)>0:
        nb_items = prop.item_density
        if nb_items!=0:
            nb_items = max(randrange(nb_items-2,nb_items+2), 1)
        if DungeonData.guaranteed_item_id!=0:
            nb_items += 1
        DungeonData.nb_items = nb_items+1
        if nb_items+1>0:
            shuffle_spawns(valid_spawns)
            start = randrange(len(valid_spawns))
            nb_items += 1
            for i in range(nb_items):
                c = valid_spawns[start]
                start += 1
                if start==len(valid_spawns):
                    start = 0
                DungeonData.list_tiles[c[0]][c[1]][2]|=0x2
    #RandomGenerator.print()
    valid_spawns = []
    for x in range(56):
        for y in range(32):
            if DungeonData.list_tiles[x][y][0]&0x3==0:
                valid_spawns.append((x, y))
    if len(valid_spawns)>0:
        nb_items = prop.buried_item_density
        if nb_items!=0:
            nb_items = randrange(nb_items-2,nb_items+2)
        if nb_items>0:
            shuffle_spawns(valid_spawns)
            start = randrange(len(valid_spawns))
            for i in range(nb_items):
                c = valid_spawns[start]
                start += 1
                if start==len(valid_spawns):
                    start = 0
                DungeonData.list_tiles[c[0]][c[1]][2]|=0x2
    valid_spawns = []
    if not empty:
        for x in range(56):
            for y in range(32):
                if DungeonData.list_tiles[x][y][0]&0x20==0 and DungeonData.list_tiles[x][y][0]&0x40 \
                    and DungeonData.list_tiles[x][y][0]&0x8==0:
                    valid_spawns.append((x, y))
    if len(valid_spawns)>0:
        nb_items = max(6, randrangeswap((5*len(valid_spawns))//10, (8*len(valid_spawns))//10))
        if nb_items>=StaticParam.MH_NORMAL_SPAWN_ITEM:
            nb_items = StaticParam.MH_NORMAL_SPAWN_ITEM
        shuffle_spawns(valid_spawns)
        start = randrange(len(valid_spawns))
        for i in range(nb_items):
            c = valid_spawns[start]
            start += 1
            if start==len(valid_spawns):
                start = 0
            if randrange(2)==1:
                DungeonData.list_tiles[c[0]][c[1]][2]|=0x2
            elif DungeonData.free_mode or DungeonData.dungeon_number>=StaticParam.MH_MIN_TRAP_DUNGEON:
                DungeonData.list_tiles[c[0]][c[1]][2]|=0x4
    #RandomGenerator.print()
    valid_spawns = []
    for x in range(56):
        for y in range(32):
            if DungeonData.list_tiles[x][y][0]&0x3==1 and DungeonData.list_tiles[x][y][7]!=0xFF and DungeonData.list_tiles[x][y][0]&0x20==0 \
                and DungeonData.list_tiles[x][y][2]&0x2==0 and DungeonData.list_tiles[x][y][0]&0x8==0 \
                 and DungeonData.list_tiles[x][y][0]&0x100==0:
                valid_spawns.append((x, y))
    if len(valid_spawns)>0:
        nb_traps = randrangeswap(prop.trap_density//2, prop.trap_density)
        if nb_traps>0:
            if nb_traps >= 56:
                nb_traps = 56
            shuffle_spawns(valid_spawns)
            start = randrange(len(valid_spawns))
            for i in range(nb_traps):
                c = valid_spawns[start]
                start += 1
                if start==len(valid_spawns):
                    start = 0
                DungeonData.list_tiles[c[0]][c[1]][2]|=0x4
    if get_floor_type()==2:
        flag = True
    else:
        flag = False
    valid_spawns = []
    if DungeonData.player_spawn_x==-1 or DungeonData.player_spawn_y==-1:
        for x in range(56):
            for y in range(32):
                if DungeonData.list_tiles[x][y][0]&0x3==1 and DungeonData.list_tiles[x][y][7]!=0xFF and DungeonData.list_tiles[x][y][0]&0x20==0 \
                    and DungeonData.list_tiles[x][y][0]&0x8==0 and DungeonData.list_tiles[x][y][0]&0x100==0 \
                    and DungeonData.list_tiles[x][y][2]&0x2==0 and DungeonData.list_tiles[x][y][2]&0x8==0 and DungeonData.list_tiles[x][y][2]&0x4==0:
                    if not flag or DungeonData.list_tiles[x][y][2]&0x1==0:
                        valid_spawns.append((x, y))
        if len(valid_spawns)>0:
            spawn = valid_spawns[randrange(len(valid_spawns))]
            DungeonData.player_spawn_x = spawn[0]
            DungeonData.player_spawn_y = spawn[1]

#US: 02341470
def generate_monster_spawns(prop, empty):
    valid_spawns = []
    if prop.enemy_density<1:
        enemies = abs(prop.enemy_density)
    else:
        enemies = randrange(prop.enemy_density//2, prop.enemy_density)
        if enemies<1:
            enemies = 1
    for x in range(56):
        for y in range(32):
            if DungeonData.list_tiles[x][y][0]&0x3==1 and DungeonData.list_tiles[x][y][7]!=0xFF and DungeonData.list_tiles[x][y][0]&0x20==0 \
                and DungeonData.list_tiles[x][y][2]&0x2==0 and DungeonData.list_tiles[x][y][2]&0x1==0 and DungeonData.list_tiles[x][y][0]&0x8==0 \
                 and DungeonData.list_tiles[x][y][0]&0x100==0:
                if DungeonData.player_spawn_x!=x or DungeonData.player_spawn_y!=y:
                    if StatusData.no_enemy_spawn==0 or DungeonData.mh_room!=DungeonData.list_tiles[x][y][7]:
                        valid_spawns.append((x, y))
    if len(valid_spawns)>0 and enemies+1>0:
        shuffle_spawns(valid_spawns)
        enemies += 1
        start = randrange(len(valid_spawns))
        for i in range(enemies):
            c = valid_spawns[start]
            start += 1
            if start==len(valid_spawns):
                start = 0
            DungeonData.list_tiles[c[0]][c[1]][2]|=0x8
    if DungeonData.create_mh:
        valid_spawns = []
        mh_spawn = StaticParam.MH_NORMAL_SPAWN_ENM
        if empty:
            mh_spawn = 3
        if DungeonData.create_mh:
            mh_spawn = (mh_spawn*3)//2
        for x in range(56):
            for y in range(32):
                if DungeonData.list_tiles[x][y][0]&0x3==1 and DungeonData.list_tiles[x][y][7]!=0xFF and DungeonData.list_tiles[x][y][0]&0x20==0 \
                   and DungeonData.list_tiles[x][y][0]&0x100==0 and DungeonData.list_tiles[x][y][0]&0x40:
                    if DungeonData.player_spawn_x!=x or DungeonData.player_spawn_y!=y:
                        valid_spawns.append((x, y))
        if len(valid_spawns)>0:
            enemies = max(1, randrange((7*len(valid_spawns))//10, (8*len(valid_spawns))//10))
            if enemies>=mh_spawn:
                enemies = mh_spawn
            shuffle_spawns(valid_spawns)
            start = randrange(len(valid_spawns))
            for i in range(enemies):
                c = valid_spawns[start]
                start += 1
                if start==len(valid_spawns):
                    start = 0
                DungeonData.list_tiles[c[0]][c[1]][2]|=0x8

#US: 02340974
def clear_safe():
    for x in range(56):
        for y in range(32):
            if DungeonData.list_tiles[x][y][0]&0x3!=1:
                if DungeonData.list_tiles[x][y][0]&0x110:
                    DungeonData.list_tiles[x][y][2]&=~0x2
                DungeonData.list_tiles[x][y][2]&=~0x4
            if DungeonData.list_tiles[x][y][2]&0x1:
                DungeonData.list_tiles[x][y][0]|=0x200
                DungeonData.list_tiles[x][y][2]&=~0x4
            if DungeonData.list_tiles[x][y][2]&0x2:
                DungeonData.list_tiles[x][y][2]&=~0x4
            
#US: 02341E6C
def test_reachable(xpos,ypos,mark_invalid):
    tst = [[0 for y in range(32)] for x in range(56)]
    for x in range(56):
        for y in range(32):
            if mark_invalid:
                DungeonData.list_tiles[x][y][0]&=~0x8000
            if DungeonData.list_tiles[x][y][0]&0x3!=1:
                if DungeonData.list_tiles[x][y][0]&0x4==0:
                    tst[x][y]|=0x1
            if DungeonData.list_tiles[x][y][0]&0x3==2:
                if DungeonData.list_tiles[x][y][0]&0x4==0:
                    tst[x][y]|=0x2
    tst[xpos][ypos]|=0x50
    if DungeonData.stairs_spawn_x!=xpos and DungeonData.stairs_spawn_y!=ypos:
        return False
    StatusData.unk_val_24 = 0
    count = 0
    checked = 1
    while checked:
        count += 1
        checked = 0
        for x in range(56):
            for y in range(32):
                if tst[x][y]&0x80==0 and tst[x][y]&0x40:
                    tst[x][y]&=~0x40
                    tst[x][y]|=0x80
                    checked += 1
                    if x>0 and tst[x-1][y]&0x83==0:
                        tst[x-1][y]|=0x40
                    if y>0 and tst[x][y-1]&0x83==0:
                        tst[x][y-1]|=0x40
                    if x<55 and tst[x+1][y]&0x83==0:
                        tst[x+1][y]|=0x40
                    if y<31 and tst[x][y+1]&0x83==0:
                        tst[x][y+1]|=0x40
                    if x>0 and y>0 and tst[x-1][y-1]&0x87==0 and tst[x][y-1]&0x1==0 and tst[x-1][y]&0x1==0:
                        tst[x-1][y-1]|=0x40
                    if x<55 and y>0 and tst[x+1][y-1]&0x87==0 and tst[x][y-1]&0x1==0 and tst[x+1][y]&0x1==0:
                        tst[x+1][y-1]|=0x40
                    if x>0 and y<31 and tst[x-1][y+1]&0x87==0 and tst[x][y+1]&0x1==0 and tst[x-1][y]&0x1==0:
                        tst[x-1][y+1]|=0x40
                    if x<55 and y<31 and tst[x+1][y+1]&0x87==0 and tst[x][y+1]&0x1==0 and tst[x+1][y]&0x1==0:
                        tst[x+1][y+1]|=0x40
    StatusData.unk_val_24 = count
    for x in range(56):
        for y in range(32):
            if tst[x][y]&0x87==0:
                if mark_invalid:
                    DungeonData.list_tiles[x][y][0]|=0x8000
                else:
                    if DungeonData.list_tiles[x][y][0]&0x100==0:
                        return False
    return True

#US: 02340B0C
def reinit_tiles():
    DungeonData.clear_tiles()
    for x in range(56):
        for y in range(32):
            if is_out_of_bounds(x-1,y) or is_out_of_bounds(x,y-1) \
                or is_out_of_bounds(x+1,y) or is_out_of_bounds(x,y+1) \
                or is_out_of_bounds(x-1,y-1) or is_out_of_bounds(x-1,y+1) \
                or is_out_of_bounds(x+1,y-1) or is_out_of_bounds(x+1,y+1):
                DungeonData.list_tiles[x][y][0] |= 0x10
    DungeonData.stairs_spawn_x = -1
    DungeonData.stairs_spawn_y = -1
    DungeonData.clear_fixed_room()
    DungeonData.nb_active_items = 0
    DungeonData.clear_active_traps()

#US: ???
def process_fixed_room(fixed_floor_number, prop):
    return True # TODO

#US: 0233A6D8
def generate_floor():
    StatusData.floor_size = 0
    prop = Properties
    DungeonData.fixed_floor_number = Properties.fixed_floor_number
    StatusData.mh_chance = Properties.mh_chance
    StatusData.kecleon_chance = Properties.kecleon_chance
    StatusData.middle_room_secondary = Properties.middle_room_secondary
    StatusData.hidden_stairs_type = Properties.hidden_stairs_type+1
    gen_attempts2 = 0
    while gen_attempts2<10:
        DungeonData.player_spawn_x = -1
        DungeonData.player_spawn_y = -1
        DungeonData.stairs_spawn_x = -1
        DungeonData.stairs_spawn_y = -1
        DungeonData.hidden_stairs_spawn_x = -1
        DungeonData.hidden_stairs_spawn_y = -1
        
        gen_attempts = 0

        fixed_room = 0
        while gen_attempts<10:
            #RandomGenerator.print()
            ReturnData.invalid_generation = False
            if fixed_room==0:
                if 0<DungeonData.fixed_floor_number<0xA5:
                    break
                fixed_room = 0
            DungeonData.attempts = gen_attempts

            if gen_attempts>=1:
                StatusData.middle_room_secondary = 0
            
            StatusData.is_not_valid = 0
            StatusData.kecleon_shop_middle_x = -1
            StatusData.kecleon_shop_middle_y = -1

            reinit_tiles()

            DungeonData.player_spawn_x = -1
            DungeonData.player_spawn_y = -1

            if DungeonData.fixed_floor_number!=0:
                if not process_fixed_room(DungeonData.fixed_floor_number, prop):
                    fixed_room = 1
            
            max_nb_room_x = 2 # [r13,#+0x8]
            max_nb_room_y = 2 # [r13,#+0x4]
            attempts = 0x20
            while attempts>0:
                if prop.layout==8:
                    max_x = 5
                    max_y = 4
                else:
                    max_x = 9
                    max_y = 8
                max_nb_room_x = randrange(2, max_x)
                max_nb_room_y = randrange(2, max_y)

                if max_nb_room_x<=6 and max_nb_room_y<=4:
                    break
                attempts -= 1

            if attempts==0:
                max_nb_room_x = max_nb_room_y = 4

            if 0x38//max_nb_room_x<=7:
                max_nb_room_x = 1
            if 0x20//max_nb_room_y<=7:
                max_nb_room_y = 1
            secondary_gen = 0
            if prop.layout==1:
                max_nb_room_x = 4
                max_nb_room_y = randrange(2)+2
                StatusData.floor_size = 1
                generate_normal_floor(max_nb_room_x, max_nb_room_y, prop)
                secondary_gen = 1
            elif prop.layout==2:
                generate_one_mh_room()
                DungeonData.create_mh = 1
            elif prop.layout==3:
                generate_ring(prop)
                secondary_gen = 1
            elif prop.layout==4:
                generate_crossroads(prop)
                secondary_gen = 1
            elif prop.layout==5:
                generate_2_rooms_mh()
                DungeonData.create_mh = 1
            elif prop.layout==6:
                generate_room_line(prop)
                secondary_gen = 1
            elif prop.layout==7:
                generate_cross(prop)
            elif prop.layout==9:
                generate_beetle(prop)
            elif prop.layout==10:
                generate_outer_room_floor(max_nb_room_x, max_nb_room_y, prop)
                secondary_gen = 1
            elif prop.layout==11:
                max_nb_room_x = 4
                max_nb_room_y = randrange(2)+2
                StatusData.floor_size = 2
                generate_normal_floor(max_nb_room_x, max_nb_room_y, prop)
                secondary_gen = 1
    ##        elif prop.layout==12:
    ##            generate_maze()
    ##            secondary_gen = 1
            else:
                generate_normal_floor(max_nb_room_x, max_nb_room_y, prop)
                secondary_gen = 1
            reset_y_borders()
            delete_status_10()
            if not StatusData.is_not_valid:
                room = [False for i in range(0x40)]
                room_tiles = 0
                for x in range(56):
                    for y in range(32):
                        if DungeonData.list_tiles[x][y][0]&0x3==1:
                            if DungeonData.list_tiles[x][y][7]<0xF0:
                                room_tiles += 1
                                if DungeonData.list_tiles[x][y][7]<0x40:
                                    room[DungeonData.list_tiles[x][y][7]] = True
                nb_rooms = room.count(True)
                if nb_rooms>=2 and room_tiles>=20:
                    break
            gen_attempts += 1
            if StaticParam.SHOW_ERROR:
                ReturnData.invalid_generation = True
                break
        if gen_attempts==10:
            ReturnData.invalid_generation = True
            StatusData.kecleon_shop_middle_x = -1
            StatusData.kecleon_shop_middle_y = -1
            generate_one_mh_room()
            DungeonData.create_mh = 1
        generate_junctions()
        if secondary_gen:
            #RandomGenerator.print()
            generate_secondary(1, prop)
        
        if randrange(100)<prop.empty_mh_chance:
            empty = True
        else:
            empty = False

        #RandomGenerator.print()
        generate_item_spawns(prop,empty)
        #RandomGenerator.print()
        generate_monster_spawns(prop,empty)
        #RandomGenerator.print()
        clear_safe()

        if DungeonData.player_spawn_x!=-1 and DungeonData.player_spawn_y!=-1:
            if get_floor_type()==1:
                break
            else:
                if DungeonData.stairs_spawn_x!=-1 and DungeonData.stairs_spawn_y!=-1:
                    if test_reachable(DungeonData.stairs_spawn_x,DungeonData.stairs_spawn_y,False):
                        break
        gen_attempts2 += 1
        if StaticParam.SHOW_ERROR:
            ReturnData.invalid_generation = True
            break
    if gen_attempts2==10:
        ReturnData.invalid_generation = True
        StatusData.kecleon_shop_middle_x = -1
        StatusData.kecleon_shop_middle_y = -1
        reinit_tiles()
        generate_one_mh_room()
        DungeonData.create_mh = 1
        generate_junctions()
        generate_item_spawns(prop,0)
        generate_monster_spawns(prop,0)
        clear_safe()
    # Don't mind the rest of floor generation
