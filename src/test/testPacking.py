import os
import sys 
sys.path.append(os.getcwd() + "/src")

from packing import Packing

print("Test of the data packing")
pack = Packing()
print("Data = ", pack.getData()[18])

print("\nPacking...\n")
pack.packingData(18)
print("Packed data = ", pack.getPackedData())

print("\nFiltering values...\n")
pack.computeFilters()
print("Filtered values = ", pack.getFilteredData())
print("\nFiltered and encrypted values = ", pack.getFilteredEncryptedData())

print("\nUnpacking data...\n")
pack.unpackingData(18)
print("Unpacked value = ", pack.getUnpackedData())

print("\nUnpacking with generalized algorithm...\n")
pack.generalisedUnpacking()
print("Generalized unpacking = ", pack.getGeneralizedUnpack()[18])