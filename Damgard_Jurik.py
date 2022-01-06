from gmpy2 import random_state, mpz_urandomb, bit_set, next_prime, bit_length, num_digits, mpz_random, gcd, invert, powmod, mpz,lcm
import time,random
import numpy

def get_prime(size):
    seed=random_state(int(random.randint(0,10000)))
    q=mpz_urandomb(seed,size)
    q=q.bit_set(size-1)
    p=next_prime(q)
    if p.bit_length()<213:
       return p
def get_DJ_keys(size,n):
    p,q=get_prime(size),get_prime(size)
    print('p:'+str(p))
    print('q:'+str(q))
    K_p=p*q
    g=1+K_p
    K_pu=[g,K_p]
    K_s=lcm(p-1,q-1)
    K_pr=K_s
    print('K_pr:'+str(K_pr))
    return K_pu,K_pr

def get_r(pub_key):
    while True:
        seed=random_state(time.time_ns())
        r=mpz_random(seed, pub_key[1])
        if gcd(r, pub_key[1])== 1:
             break
    return r

def DJ_encrypt(message, K_pu,n):
    print('m:'+str(message))
    print('K_p:'+str(K_pu[1]))
    print('g:'+str(K_pu[0]))
    print('n:'+str(n))
    r=get_r(K_pu)
    print('r:'+str(r))
    Kp_n1 = K_pu[1] ** (n+1)
    r=powmod(r,K_pu[1]**n,Kp_n1) 
    c=powmod(K_pu[0],message,Kp_n1)
    c=(c*r)%Kp_n1     
    print('c:'+str(c))
    return c
def fact(k):
    if k==0:
        return 1
    return k*fact(k-1)    
def L(b,n):
    assert (b-1) % n == 0
    return (b-1) // n
def F(a,K_pu,n):
    m=0
    Kp=K_pu[1]
    for j in range (1,n+1):
        Kp_j=K_pu[1]**j
        t1=L(a,Kp_j*Kp)
        print('t1:'+str(t1))
        t2=m
        print('t2:'+str(t2))
        for k in range (2,j+1):
            m=m-1
            t2=(t2*m) % Kp_j
            print('t2:'+str(t2))
            t1=(t1-(t2*(Kp**(k-1))*invert(fact(k),Kp_j))) % Kp_j
            print('t1:'+str(t1))
        m=t1
    return m % (Kp**n)
def DJ_decrypt(enc, K_pr, K_pu,n):
    Kp_n=K_pu[1]**n
    phiInv = invert(K_pr, Kp_n)
    print('inv:'+str(phiInv))
    c_Ks=numpy.power(enc,K_pr)
    print('c_Ks:'+str(c_Ks))
    print('Kp_n:'+ str(Kp_n))
    m=(F(c_Ks,K_pu[1],n)*phiInv) % Kp_n
    return m

K_pu,K_pr=get_DJ_keys(5,4)
c=DJ_encrypt(10,K_pu,4)
print('m:'+str(DJ_decrypt(c,K_pr,K_pu,4)))