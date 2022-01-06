import os
import sys 
sys.path.append(os.getcwd() + "/src")

from valuesGenerator import ValuesGenerator
from damgardJurik import DamgardJurik

Kp,g,Ks = ValuesGenerator.generateDJKey(50)

print("Kp = ", Kp)
print("g = ", g)
print("Ks = ", Ks)


print("\n")
DJ = DamgardJurik()

print("DJ.msg = ", DJ.getMsg())
print("\nCiphering...\n")
DJ.ciphering()
print("Printing encrypted string...\n")
for c in DJ.getCiphered():
    print(c, " ", type(c))

print("Deciphering...\n")
DJ.deciphering()
print("Printing decrypted string...\n")
DJ.getDeciphered()
