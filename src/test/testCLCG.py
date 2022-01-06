import os
import sys 
sys.path.append(os.getcwd() + "/src")

from clcg import CLCG

print("Test of the CLCG cryptosystem")
crypto = CLCG()
print("Data = ", crypto.getData())
print("Encrypting data...")
crypto.clcgEncryption()
print("Encrypted data = ", crypto.getEncrypted())

print("Converting CLCG to DJ...")
crypto.clcgToDJ(2)
