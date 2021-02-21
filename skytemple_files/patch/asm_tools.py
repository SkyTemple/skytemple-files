from typing import Dict, List, Set, Tuple

ALL = 0xFFFFFFFF

REG_SRC = 0x000F0000
REG_DEST = 0x0000F000
REG_NEG = 0x80000000

IMMEDIATE_FIELD = 0x00000FFF
IMM_REG_VAL = 0x00F
IMM_REG_SHIFT = 0xFF0
IMM_REG_SHIFT_TYPE = 0x06
IMM_REG_SHIFT_TYPE_LSL = 0x0
IMM_REG_SHIFT_TYPE_LSR = 0x1
IMM_REG_SHIFT_TYPE_ASR = 0x2
IMM_REG_SHIFT_TYPE_ROR = 0x3
IMM_REG_SHIFT_REG = 0xF0
IMM_REG_SHIFT_VAL = 0xF8
IMM_CONST_VAL = 0x0FF
IMM_CONST_SHIFT = 0xF00


BRANCH_MASK = 0x0E000000
BRANCH_CODE = 0x0A000000
BRANCH_ADDR = 0x00FFFFFF
BRANCH_NEG = 0x00800000
LDR_MASK = 0x0F7F0000
LDR_CODE = 0x051F0000
LDR_NEG = 0x00800000

AL_OP_MASK = 0x0C000000
AL_OP_CODE = 0x00000000
OPCODE_IMM = 0x02000000
OPCODE_MASK = 0x01E00000
OPCODE_SUB = 0x00400000
OPCODE_RSB = 0x00600000
OPCODE_ADD = 0x00800000
OPCODE_CMP = 0x01400000
OPCODE_MOV = 0x01A00000

COND_MASK = 0xF0000000
COND_EQ = 0x00000000
COND_NE = 0x10000000
COND_CS = 0x20000000
COND_CC = 0x30000000
COND_MI = 0x40000000
COND_PL = 0x50000000
COND_VS = 0x60000000
COND_VC = 0x70000000
COND_HI = 0x80000000
COND_LS = 0x90000000
COND_GE = 0xA0000000
COND_LT = 0xB0000000
COND_GT = 0xC0000000
COND_LE = 0xD0000000
COND_AL = 0xE0000000

def ror(val, rotate, nb_bits = 32):
    out = val % (1<<rotate)
    return (val>>rotate) + (out<<(nb_bits-rotate))

def get_imm_value(reg_list: int, imm_val: int, is_imm_const: int):
    if is_imm_const:
        const = imm_val&IMM_CONST_VAL
        rotate = (imm_val&IMM_CONST_SHIFT)>>7
        return ror(const, rotate)
    else:
        val = reg_list[imm_val&IMM_REG_VAL]
        shift = (imm_val&IMM_REG_SHIFT)>>4
        shift_type = (shift&IMM_REG_SHIFT_TYPE)>>1
        if shift%2:
            reg_shift = (shift&IMM_REG_SHIFT_REG)>>4
            val_shift = reg_list[reg_shift]
        else:
            val_shift = (shift&IMM_REG_SHIFT_VAL)>>3
        if shift_type==IMM_REG_SHIFT_TYPE_LSL:
            return val<<val_shift
        elif shift_type==IMM_REG_SHIFT_TYPE_LSR:
            return val>>val_shift
        elif shift_type==IMM_REG_SHIFT_TYPE_ASR:
            if val&REG_NEG:
                val |= ALL%(1<<rotate)
                return ror(val, val_shift)
            else:
                return val>>val_shift
        elif shift_type==IMM_REG_SHIFT_TYPE_ROR:
            return ror(val, val_shift)

def cond_pass(flags: List[int], test: int):
    # flags = [Z, C, N, V]
    if test==COND_EQ and flags[0]:return True
    elif test==COND_NE and not flags[0]:return True
    elif test==COND_CS and flags[1]:return True
    elif test==COND_CC and not flags[1]:return True
    elif test==COND_MI and flags[2]:return True
    elif test==COND_PL and not flags[2]:return True
    elif test==COND_VS and flags[3]:return True
    elif test==COND_VC and not flags[3]:return True
    elif test==COND_HI and flags[1] and not flags[0]:return True
    elif test==COND_LS and not (flags[1] and not flags[0]):return True
    elif test==COND_GE and flags[2]==flags[3]:return True
    elif test==COND_LT and flags[2]!=flags[3]:return True
    elif test==COND_GT and not flags[0] and flags[2]==flags[3]:return True
    elif test==COND_LE and (flags[0] or flags[2]!=flags[3]):return True
    elif test==COND_AL:return True
    return False

class AsmFunction:
    def __init__(self, data: bytes, old_start_address: int):
        self.data = data
        self.old_start_address = old_start_address
        self.external_calls = {}
    def _read_instr(self, i):
        code = 0
        for x in range(4):
            code += self.data[i*4+x]*(256**x)
        return code
    def process(self) -> Set[int]:
        calls = set()
        ext_data = set()
        for x in range(len(self.data)//4):
            offset = self.old_start_address+x*4
            code = self._read_instr(x)
            if code&BRANCH_MASK==BRANCH_CODE:
                baddr = code&BRANCH_ADDR
                if baddr>=BRANCH_NEG:
                    baddr -= 2*BRANCH_NEG
                baddr = baddr*0x4+offset+0x8
                if not (self.old_start_address<=baddr<self.old_start_address+len(self.data)):
                    self.external_calls[x] = (False, baddr, 'b')
                    calls.add(baddr)
            elif code&LDR_MASK==LDR_CODE:
                offset = code&IMMEDIATE_FIELD
                if not code&LDR_NEG:
                    offset = -offset
                offset += 0x8
                datapos = x+offset//4
                baddr = datapos*4+self.old_start_address
                if not (self.old_start_address<=datapos<self.old_start_address+len(self.data)):
                    self.external_calls[x] = (False, baddr, 'ldrdata')
                    ext_data.add(baddr)
                else:
                    self.external_calls[datapos] = (False, self._read_instr(datapos), 'ldr')
        return (calls, ext_data)
    def add_instructions(self, instr: bytes):
        self.data += instr
    def link_to_others(self, func_list: Dict[int, 'AsmFunction']) -> bool:
        has_links = False
        for c in self.external_calls.keys():
            v = self.external_calls[c]
            baddr = v[1]
            if baddr in func_list:
                if v[2] == 'ldr' or v[2] == 'b':
                    self.external_calls[c] = (True, func_list[baddr], v[2])
                    has_links = True
        return has_links
    def provide_data(self, data_list: Dict[int, int]) -> bool:
        has_links = False
        for c in self.external_calls.keys():
            v = self.external_calls[c]
            baddr = v[1]
            if baddr in data_list:
                if v[2] == 'ldrdata':
                    self.external_calls[c] = (True, data_list[baddr], v[2])
                    has_links = True
        return has_links
    def compile(self, new_start_address: int) -> bytes:
        new_data = bytearray(self.data)
        
        for c, v in self.external_calls.items():
            if v[0]:
                if v[2]=='ldrdata':
                    new_baddr = new_start_address+len(new_data)
                    new_data += bytearray([v[1]%256, (v[1]//256)%256, (v[1]//65536)%256, (v[1]//65536//256)%256])
                else:
                    if self==v[1]:
                        new_baddr = new_start_address
                    else:
                        new_baddr = new_start_address+len(new_data)
                        new_data += bytearray(v[1].compile(new_baddr))
            else:
                new_baddr = v[1]
            code = self._read_instr(c)
            if v[2]=='b':
                offset = new_start_address+c*4
                new_baddr = (new_baddr-offset-0x8)//4
                if new_baddr<0:
                    new_baddr += 2*BRANCH_NEG
                code = (code & (ALL ^ BRANCH_ADDR)) | (new_baddr & BRANCH_ADDR)
            elif v[2]=='ldr':
                code = new_baddr
            elif v[2]=='ldrdata':
                offset = new_start_address+c*4
                new_baddr = new_baddr-offset-0x8
                code = (code & (ALL ^ (IMMEDIATE_FIELD | LDR_NEG)))
                if new_baddr<0:
                    new_baddr -= new_baddr
                else:
                    code |= LDR_NEG
                if new_baddr>IMMEDIATE_FIELD:
                    raise Exception("Data too far from the current offset. ")
                code = (code | (new_baddr & IMMEDIATE_FIELD))
            new_data[c*4:c*4+4] = bytearray([code%256, (code//256)%256, (code//65536)%256, (code//65536//256)%256])
        return bytes(new_data)
    def exec(self, reg_list: List[int]):
        flags = [False, False, False, False]
        while self.old_start_address<=reg_list[15]-0x8<self.old_start_address+len(self.data):
            offset = reg_list[15]-0x8
            #print(hex(offset), flags)
            x = (offset-self.old_start_address)//0x4
            code = self._read_instr(x)
            if cond_pass(flags, code & COND_MASK):
                if code&BRANCH_MASK==BRANCH_CODE:
                    baddr = code&BRANCH_ADDR
                    if baddr>=BRANCH_NEG:
                        baddr -= 2*BRANCH_NEG
                    baddr = baddr*0x4+offset+0x8
                    reg_list[15] = baddr + 0x8
                elif code&LDR_MASK==LDR_CODE:
                    offset = code&IMMEDIATE_FIELD
                    if code&LDR_NEG:
                        offset = -offset
                    offset += 0x8
                    datapos = x+offset//4
                    if not (self.old_start_address<=datapos<self.old_start_address+len(self.data)):
                        if not self.external_calls[x][0]:
                            raise Exception("Data not found at "+hex(reg_list[15]-0x8))
                        reg_list[(code&REG_DEST)>>12] = self.external_calls[x][1]
                    else:
                        reg_list[(code&REG_DEST)>>12] = self.external_calls[datapos][1]
                    reg_list[15] += 0x4
                elif code&AL_OP_MASK==AL_OP_CODE:
                    opcode = code&OPCODE_MASK
                    op2 = get_imm_value(reg_list, code&IMMEDIATE_FIELD, code&OPCODE_IMM)
                    dest = (code&REG_DEST)>>12
                    reg_op = (code&REG_SRC)>>16
                    op1 = reg_list[reg_op]
                    if reg_op==15:
                        op1+=0x8
                    set_flags = False
                    if code&OPCODE_MASK==OPCODE_ADD:
                        res = op1+op2
                        reg_list[dest] = (res)&ALL
                    elif code&OPCODE_MASK==OPCODE_SUB:
                        op2 = ((-op2)&ALL)
                        res = op1+op2
                        reg_list[dest] = (res)&ALL
                    elif code&OPCODE_MASK==OPCODE_RSB:
                        op1 = ((-op1)&ALL)
                        res = op2+op1
                        reg_list[dest] = (res)&ALL
                    elif code&OPCODE_MASK==OPCODE_CMP:
                        op2 = ((-op2)&ALL)
                        res = op1+op2
                        set_flags = True
                    else:
                        raise Exception("Opcode not supported at "+hex(reg_list[15]-0x8))
                    if set_flags:
                        flags[0] = ((res)&ALL==0)
                        flags[1] = (res>=(2**32) or res<-(2**32))
                        flags[2] = (((res)&ALL)&REG_NEG==ALL&REG_NEG)
                        flags[3] = ((op1&REG_NEG)==(op2&REG_NEG) and (op1&REG_NEG)!=(res&REG_NEG))
                    if dest!=15:
                        reg_list[15] += 0x4
                else:
                    raise Exception("Instruction not supported at "+hex(reg_list[15]-0x8))
            else:
                reg_list[15] += 0x4
        return reg_list
    def process_switch(self, register_search: int, range_search: Tuple[int, int], init_values: Dict[int,int]={}) -> List[int]:
        ends = []
        for x in range(range_search[0], range_search[1]):
            reg_list = [None]*16
            reg_list[register_search]=x
            for k, v in init_values.items():
                reg_list[k]=v
            reg_list[15]=self.old_start_address+0x8
            reg_list = self.exec(reg_list)
            ends.append(reg_list[15]-0x8)
        return ends
