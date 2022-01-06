# Projet de l'UE Cryptographie Avancée

**<u>Subject :</u>** Cryptosystem Conversion, Packing and Matrix Processing of Homomorphically Encrypted Data: Application to IOT Devices

## Implementation

  -Damgard-Jurik cryptosystem (D-J) 
  
  -Combined Linear Congruential Generator (CLCG)
  
  -Secure Combined Linear Congruential Generator Cryptosystem ( SCLCG)
  
  -Data packing and filtering operations
  
## Damgard-Jurik cryptosystem (D-J)

This algorithm is the cryptosystem of Damgard-Jurik implementation.  Can cipher either a str message or a great int.

Mains methods used:

```python
 def ciphering(self):
        """Cipher the `msg` argument with the Damgard-Jurik Cryptosystem"""
```

```python
 def __F__(self, a):
        """Private method: The F procedure Damgard-Jurik method to decipher a message"""
```

```python
 def deciphering(self):
        """Decipher the `ciphered_msg` argument with the Damgard-Jurik Cryptosystem"""
```


## Combined Linear Congruential Generator (CLCG)

 This algorithm represents the Combined Linear Congruential Generator encryption.
 
 Main methods used:
 
 ```python
 def __lcgX__(self, Xi:mpz):
        """Private method: Compute the X's LCG"""
 ```

 ```python
 def __lcgY__(self, Yi:mpz):
        """Private method: Compute the Y's LCG"""
 ```

 ```python
 def clcgEncryption(self):
       """Cipher the `msg` argument with the CLCG Cryptosystem"""
 ```
  
 
## Secure Combined Linear Congruential Generator Cryptosystem (SCLCG)

This algorithm represents the Secure Combined Linear Congruential Generator Cryptosystem.

It allows us to convert a CLCG encrypted message into a D-J encrypted message without deciphering it.

We encountered a gmp:overflow in mpz error when implementing this algorithm.

## Data packing and filtering operations

This algorithm represents all the operation used to pack the data and to unpack it as well. It concerns the simple Packing of the data, the packing and filtering of the values, the Damgard-Jurik encryption of the packed data and finaly the Unpacking with a simple algorithm and a generalized version of the later. 

During the implementation, we noticed that the Unpacking likely is not functionning. The result returned by the unpacking following the first algorithm and the one returned by the generalized version are not the same. Since we cannot tell which one is wrong, we didn't manage to solve the issue. 

Main methods used:

```python
def packingData(self, i:int):
        """This method packs the data from the ith Sensor into a single value"""
```

```python
def computeFilters(self):
        """Compute the packed data with the filters through the Damgard-Jurik crypto-system"""
```

```python
def unpackingData(self, j:int):
        """Unpack the data and generate the aj value"""
```

```python
def generalisedUnpacking(self): # FIXME: Error in the computation, the values aren't the same with unpackingData. Could be a typo in the equation
        """Generalised algorithm for data unpacking"""
```
