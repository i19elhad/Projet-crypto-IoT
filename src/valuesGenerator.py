#=============================================================================#
#===============    File: valuesGenerator.py                ==================#
#===============    Version: 0.1                            ==================#
#===============    Authors:                                ==================#
#=============================================================================#

# Imports
import time
from gmpy2 import random_state, mpz_urandomb, bit_set, next_prime, bit_length, num_digits, mpz_random, gcd, invert, powmod, mpz

#-----------------------------------------------------------------------------#

class ValuesGenerator:
    """
    This class is a place holder for the methods used to generate the croptographic
    keys and other random values used in this project.
    """

    # Methodes
    @staticmethod
    def generatePrime(size):
        """Generate a prime number encoded on a certain `size` number of bits. Returns `p: mpz`"""
        seed = random_state(time.time_ns())
        p = mpz_urandomb(seed, size)
        p = p.bit_set(size-1) # Making sure that p is encoded on at least size-1 bits (next prime could set the last bit to 1)

        return next_prime(p)

    @staticmethod
    def generateDJKey(size=1024):
        """
        Generate the key couple {(g, Kp), Ks} used in Damgard-Jurik crypto-system.
        Returns three values: `Kp, g, Ks: mpz`
        """
        p,q = ValuesGenerator.generatePrime(size//2), ValuesGenerator.generatePrime(size//2)

        # Public key {Kp, g}
        Kp = p*q
        g = Kp + mpz(1)

        # Private key {Ks}
        Ks = mpz((p-1)*(q-1)) // gcd((p-1), (q-1)) # Computing the Least Common Multiple of p-1 and q-1

        return Kp, g, Ks

    @staticmethod
    def generateCLCG(size=32):
        """
        Generate the CLCG secret and multiplier/increment.
        Returns a result in the form of `X0, a_x, c: mpz`
        """
        seed = random_state(time.time_ns())

        X0 = mpz_urandomb(seed, size)
        a_x = mpz_urandomb(seed, size)
        c = mpz_urandomb(seed, size)

        return X0, a_x, c

    @staticmethod
    def generateRandom(size=32):
        """Generate a random `mpz` number between 0 and 2**size - 1"""
        seed = random_state(time.time_ns())

        return mpz_urandomb(seed, size)
