#=============================================================================#
#===============    File: clcg.py                           ==================#
#===============    Version: 0.1                            ==================#
#===============    Authors:                                ==================#
#=============================================================================#

# Imports
from gmpy2 import random_state,mpz_urandomb, mpz, powmod, invert
import random
from valuesGenerator import ValuesGenerator
from damgardJurik import DamgardJurik
#-----------------------------------------------------------------------------#

class CLCG:
    """
    This class represents the Combined Linear Congruential Generator encryption
    """

    # Attributes

    ## Keys for LCG X and Y
    a_x = mpz(0)
    a_y = mpz(0)
    c_x = mpz(0)
    c_y = mpz(0)
    m = mpz(0)

    X0 = mpz(0)
    Y0 = mpz(0) 

    ## Damgard-Jurik instance
    DJ = None # Class: DamgardJurik

    ## Data / encrypted
    data = []
    encrypted = []
    #-------------------------------------------------------------------------#

    # Constructor
    def __init__(self, data = [], key_size = 0):
        if len(data) == 0 and key_size == 0:
            self.data = [ValuesGenerator.generateRandom() for i in range(10)]
        elif len(data) == 0 and key_size != 0:
            self.data = [ValuesGenerator.generateRandom(key_size)]
        elif len(data) != 0:
            self.data = data

        self.X0, self.a_x, self.c_x = ValuesGenerator.generateCLCG()
        self.Y0, self.a_y, self.c_y = ValuesGenerator.generateCLCG()
        self.m = ValuesGenerator.generateRandom()
    #-------------------------------------------------------------------------#

    # Getters / Setters
    def getData(self):
        """Getter for `data` attribute"""
        return self.data

    def getEncrypted(self):
        """Getter for `encrypted` attribute"""
        return self.encrypted
    def setM(self, m:mpz):
        """Setter for `M` attribute"""
        self.m= m
    #-------------------------------------------------------------------------#

    # Methods
    def __lcgX__(self, Xi:mpz):
        """Private method: Compute the X's LCG"""
        return (self.a_x*Xi + self.c_x) % self.m 

    def __lcgY__(self, Yi:mpz):
        """Private method: Compute the Y's LCG"""
        return (self.a_y*Yi + self.c_y) % self.m 

    def clcgEncryption(self):
        Xi = self.X0
        Yi = self.Y0

        for i in range(len(self.data)):
            Xi = self.__lcgX__(Xi)
            Yi = self.__lcgY__(Yi)
            Z = Xi + Yi

            self.encrypted.append((self.data[i]+Z) % self.m)

    def clcgToDJ(self,i:int):
        self.DJ = DamgardJurik(message=self.X0)
        self.DJ.ciphering()
        X0_rX0 = self.DJ.getCiphered()[0]
        self.DJ = DamgardJurik(message=self.Y0)
        self.DJ.ciphering()
        Y0_rY0 = self.DJ.getCiphered()[0]
        self.DJ = DamgardJurik(message=self.c_x)
        self.DJ.ciphering()
        cX_rcX = self.DJ.getCiphered()[0]
        self.DJ = DamgardJurik(message=self.c_y)
        self.DJ.ciphering()
        cY_rcY = self.DJ.getCiphered()[0]
        secret_key = [X0_rX0,Y0_rY0,cX_rcX,cY_rcY]
        self.DJ = DamgardJurik(message=self.encrypted[i])
        DJ_g = self.DJ.g
        DJ_Kp = self.DJ.Kp
        DJ_n = self.DJ.n
        Kp_n = DJ_Kp**DJ_n
        DJ_enc_CLCG = powmod(DJ_g,self.encrypted[i],Kp_n+1)
        i = mpz(i)

        Zi_rZi = (X0_rX0**(self.a_x*i)) * (cX_rcX**i) * (Y0_rY0**(self.a_y*i)) * (cY_rcY**i) ##gmp:overflow in mpz type
        
        DJ_data = DJ_enc_CLCG*invert(Zi_rZi,Kp_n+1)
        return DJ_data
