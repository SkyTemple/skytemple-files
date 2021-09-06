import random as sys_rnd

#US: 02353570
# Seeds are randomly generated using python's random module
# Then it uses the same algorithm as in EoS
class RandomGenerator:
    gen_type = 0 #0x0
    log = False
    
    mul = 0x5d588b65
    
    # Type 0
    count = 0 #0x4
    seed_old_t0 = sys_rnd.randrange(1<<32) #0x8
    seed_t0 = sys_rnd.randrange(1<<32) #0xC
    # Type 1
    add_t1 = 0x269ec3
    use_seed_t1 = 0 #0x10
    seeds_t1 = [sys_rnd.randrange(1<<32) for i in range(5)] #0x14-0x28
    def print():
        print("-------------")
        print("%08X"%RandomGenerator.gen_type)
        print("%08X"%RandomGenerator.count)
        print("%08X"%RandomGenerator.seed_old_t0)
        print("%08X"%RandomGenerator.seed_t0)
        print("%08X"%RandomGenerator.use_seed_t1)
        print("%08X"%RandomGenerator.seeds_t1[0])
        print("%08X"%RandomGenerator.seeds_t1[1])
        print("%08X"%RandomGenerator.seeds_t1[2])
        print("%08X"%RandomGenerator.seeds_t1[3])
        print("%08X"%RandomGenerator.seeds_t1[4])

def random():
    if RandomGenerator.gen_type==0:
        RandomGenerator.count += 1
        r = (RandomGenerator.seed_t0*RandomGenerator.mul+1)&0xFFFFFFFF
        RandomGenerator.seed_t0 = r
        r = (r>>0x10)&0xFFFF
    else:
        r = RandomGenerator.seeds_t1[RandomGenerator.use_seed_t1]
        r = (r*RandomGenerator.mul+RandomGenerator.add_t1)&0xFFFFFFFF
        RandomGenerator.seeds_t1[RandomGenerator.use_seed_t1] = r
        r&=0xFFFF
    return r
        

def randrange(a,b=None):
    if b==None:
        b = a
        a = 0
    r = (((b-a)*(random()&0xFFFF))>>0x10)&0xFFFF
    r += a
    if RandomGenerator.log:
        print("RN:",r)
    return r


def randrangeswap(a,b):
    if a==b:
        return a
    if a>b:
        return randrange(b,a)
    return randrange(a,b)


def randrangeforce(a):
    if a==0:
        random()
        return 0
    return randrange(a)

#US: 022EAC4C
def use_gen_1(use_seed):
    RandomGenerator.gen_type = 1
    RandomGenerator.use_seed_t1 = use_seed
#US: 022EAC4C
def use_gen_0():
    RandomGenerator.gen_type = 0
