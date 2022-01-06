from gmpy2 import random_state,mpz_urandomb
import random

def seedLCG():
    global rand_X
    global rand_Y
    seed_X = random_state(int(random.randint(0,10000)))
    seed_Y = random_state(int(random.randint(0,10000)))
    rand_X=mpz_urandomb(seed_X,24)
    rand_Y=mpz_urandomb(seed_Y,24)
def lcg_x():
    a_x = 1140671485
    c_x = 128201163
    m = 2**24
    global rand_X
    rand_X = (a_x*rand_X + c_x) % m
    return rand_X
def lcg_y():
    a_y = 1491770722
    c_y = 180119570
    m = 2**24
    global rand_Y
    rand_Y = (a_y*rand_Y + c_y) % m
    return rand_Y

def CLCG_enc(data):
    m=2**24
    enc=[]
    for i in range(len(data)):
        X=lcg_x()
        Y=lcg_y()
        Z=X+Y
        enc.append(( data[i]+Z ) % m)
    return enc

data=[180119570,109380217,162141564,189175109,168829998]
seedLCG()
print(CLCG_enc(data))

    