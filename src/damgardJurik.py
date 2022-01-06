#=============================================================================#
#===============    File: damgardJurik.py                   ==================#
#===============    Version: 0.1                            ==================#
#===============    Authors:                                ==================#
#=============================================================================#

# Imports
import time
from math import pow, factorial
from valuesGenerator import ValuesGenerator
from gmpy2 import powmod, mpz_random, random_state, mpz, invert
#-----------------------------------------------------------------------------#

class DamgardJurik:
    """
    This class is the cryptosystem of Damgard-Jurik implementation.
    Can cipher either a str message or a great int
    """

    # Attributes

    ## Public key
    Kp = mpz(0)
    g = mpz(0)

    ## Private key
    Ks = mpz(0)

    ## D-J exponent
    n = mpz(0)

    ## Message
    msg = 0 # Could be string or int/mpz
    deciphered_msg = ''
    ascii_msg = []

    isStr = False

    ## Encrypted message
    ciphered = []
    #-------------------------------------------------------------------------#

    # Constructor:
    def __init__(self, message=None, key_size=0):
        if key_size == 0:
            self.Kp, self.g, self.Ks = ValuesGenerator.generateDJKey(16) # TODO: Redefine the size of the key (2048bits ?)
        else:
            self.Kp, self.g, self.Ks = ValuesGenerator.generateDJKey(key_size)
        self.n = mpz(2) # TODO: Define this value better, 1 is the value used in Pailler Cryptosystem

        if message is None:
            self.msg = "Hello World"
        else:
            self.msg = message

        if isinstance(self.msg, str): 
            self.ascii_msg = [ord(c) for c in self.msg] # Convert each char to its ascii int value
            self.isStr = True
    #-------------------------------------------------------------------------#

    # Getters/Setters
    def getCiphered(self):
        """Getter for `ciphered` argument"""
        return self.ciphered

    def getMsg(self):
        """Getter for `Msg` argument"""
        return self.msg

    def getDeciphered(self):
        """Getter for `deciphered` argument"""
        return self.deciphered_msg

    def getKpn(self):
        """Returns the value of `Kp**n`"""
        return self.Kp ** self.n

    def msgIsStr(self):
        """Returns `True` if the msg to encrypt is of type string. `False` else"""
        return self.isStr
    #-------------------------------------------------------------------------#

    # Methods
    def ciphering(self):
        """Cipher the `msg` argument with the Damgard-Jurik Cryptosystem"""
        seed = random_state(time.time_ns())       

        if self.isStr:
            for c in self.ascii_msg:
                r = mpz_random(seed, 15) + mpz(1) # TODO: The range of r might need to be clarified 
                
                enc = powmod(self.g, c, self.Kp**(self.n +1)) * powmod(mpz(r), self.Kp**self.n, self.Kp**(self.n +1))
                self.ciphered.append(enc)
        else:
            r = mpz_random(seed, 15) + mpz(1) # TODO: The range of r might need to be clarified # NOTE: + mpz(1) to avoid null output
            enc = powmod(self.g, self.msg, self.Kp**(self.n +1)) * powmod(mpz(r), self.Kp**self.n, self.Kp**(self.n +1))
            self.ciphered.append(enc)

    def __F__(self, a):
        """Private method: The F procedure Damgard-Jurik method to decipher a message"""
        ## L function used in the F procedure to decipher a msg
        def L(b):
            return mpz((b-1) / self.Kp)

        m = mpz(0)
        for j in range(1, self.n+1):
            t1 = L(a % self.Kp ** (j+1))
            t2 = m

            for k in range(2, j+1):
                m = m - mpz(1)
                t2 = (t2*m) % self.Kp**j
                t1 = (t1 - mpz(((t2*self.Kp**(k-1))/factorial(k)) )) % self.Kp**j 
            m = t1
        return m % self.Kp**self.n

    def deciphering(self): # BUG: Issue in this method: Some char dosen't decipher correctly # CORRECTED: need to use mpz and avoid a r=0
        """Decipher the `ciphered_msg` argument with the Damgard-Jurik Cryptosystem"""
        for c in self.ciphered:
            m = ( self.__F__(c**self.Ks) * invert(self.Ks, self.Kp**self.n) ) % self.Kp**self.n
            print("In deciphering, m = ", chr(int(m)), " m = ", int(m))
            self.deciphered_msg += chr(m)
    
