#=============================================================================#
#===============    File: packing.py                        ==================#
#===============    Version: 0.1                            ==================#
#===============    Authors:                                ==================#
#=============================================================================#

# Imports
from valuesGenerator import ValuesGenerator
from damgardJurik import DamgardJurik
from math import log2, floor
from gmpy2 import random_state,mpz_urandomb, mpz, f_mod

#-----------------------------------------------------------------------------#

class Packing:
    """
    This class handle the packing of the datas
    """

    # Attributes

    ## Sizes of the datas
    bw = mpz(0)        # We suppose here that all the filters have the same size
    key_size = mpz(0)  # The size of the Damgard-Jurik crypto-system
    data_size = mpz(0) # We suppose here that all di is encoded on the same ammount of bits
    M = 0            # 100 is an arbitrary value for the number of samples per sensors
    N = 0            # 100 is an arbitrary value for the number of sensors

    ## Filters value
    W = []

    ## Damgard-Jurik instance
    DJ = None # Class: DamgardJurik

    ## Data
    data = [[]]
    packed_data = mpz(0)
    unpacked_data = mpz(0)
    unpacked_generalized = [] # Unpacking the data with the generalized algorithm

    ## Computed Data
    filtered_encrypted_data = mpz(0) # The A matrix encrypted with Damgard_Jurik
    filtered_data = mpz(0) # The A matrix with the data filtered
    #-------------------------------------------------------------------------#

    #Constructor
    def __init__(self, data=[], bw=0, key_size=0, data_size=0, M=0, N=0, W=[]):
        if bw == 0:
            self.bw = 16
        else:
            self.bw = bw

        if key_size == 0:
            self.key_size = 1024
        else:
            self.key_size = key_size

        if data_size == 0:
            self.data_size = 32
        else:
            self.data_size = data_size

        if M == 0:
            self.M = 100
        else:
            self.M = M

        if N == 0:
            self.N = 100
        else:
            self.N = N

        if len(data) == 0:
            self.data = [[ValuesGenerator.generateRandom(32) for j in range(self.N)] for i in range(self.M)]
        else:
            self.data = data

        if len(W) == 0:
            self.W = [ValuesGenerator.generateRandom(self.bw) for i in range(self.M)]
        else:
            self.W = W
    #-------------------------------------------------------------------------#

    # Getters / Setters
    def getData(self):
        """Getter for the attribute `data`"""
        return self.data

    def getPackedData(self):
        """Getter for the attribute `packed_data`"""
        return self.packed_data

    def getFilteredEncryptedData(self):
        """getter for the attribute `filtered_encypted_data`"""
        return self.filtered_encrypted_data

    def getFilteredData(self):
        """"Getter for the attribute `filtered_data`"""
        return self.filtered_data
    
    def getUnpackedData(self):
        """Getter for the attribute `unpacked_data`"""
        return self.unpacked_data

    def getGeneralizedUnpack(self):
        """Getter for the `unpacked_generalized` argument"""
        return self.unpacked_generalized

    def getM(self):
        """Getter for the attribute `M`"""
        return self.M
    
    def getN(self):
        """Getter for the attribute `N`"""
        return self.N
    #-------------------------------------------------------------------------#

    # Methods
    def packingData(self, i:int):
        """This method packs the data from the ith Sensor into a single value"""
        Di = mpz(0)

        for j in range(self.N):
            bj = mpz(log2(self.M) + self.bw + self.data_size)
            Di += (mpz(2)**mpz(j*bj)) * self.data[i][j]
        
        self.packed_data = Di

    def computeFilters(self):
        """Compute the packed data with the filters through the Damgard-Jurik crypto-system"""
        A = mpz(0)
        bj = mpz(log2(self.M) + self.bw + self.data_size)

        for j in range(self.N):
            for i in range(self.M):
                A += (mpz(2)**mpz(j*bj)) * self.W[i] * self.data[i][j]

        self.filtered_data = A 

        self.DJ = DamgardJurik(message=A, key_size=self.key_size)
        self.DJ.ciphering()
        self.filtered_encrypted_data = self.DJ.getCiphered()[0]

    def unpackingData(self, j:int):
        """Unpack the data and generate the aj value"""
        bj = mpz(log2(self.M) + self.bw + self.data_size)
        self.unpacked_data = self.filtered_data // (mpz(2)**mpz(j*bj)) % mpz(2)**bj # FIX: Replacing the floor (or mpz()) function by an euclidian division 

    def generalisedUnpacking(self): # FIXME: Error in the computation, the values aren't the same with unpackingData. Could be a typo in the equation
        """Generalised algorithm for data unpacking"""
        Kpn = self.DJ.getKpn()
        save = mpz(0)
        bj = mpz(log2(self.M) + self.bw + self.data_size)
        self.unpacked_generalized = [mpz(0) for i in range(self.N)]

        if self.filtered_data > (Kpn-1) / 2:
            A = self.filtered_data - Kpn
        else:
            A = self.filtered_data

        for j in range(self.N-1, -1, -1):
            self.unpacked_generalized[j] = (A - save) // (mpz(2)**mpz(j*bj))
            save += self.unpacked_generalized[j] *  (mpz(2)**mpz(j*bj))



