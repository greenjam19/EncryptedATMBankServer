# Imports
import random

low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
              31, 37, 41, 43, 47, 53, 59, 61, 67, 
              71, 73, 79, 83, 89, 97, 101, 103, 
              107, 109, 113, 127, 131, 137, 139, 
              149, 151, 157, 163, 167, 173, 179, 
              181, 191, 193, 197, 199, 211, 223, 
              227, 229, 233, 239, 241, 251, 257, 
              263, 269, 271, 277, 281, 283, 293, 
              307, 311, 313, 317, 331, 337, 347, 
              349, 353, 359, 367, 373, 379, 383, 
              389, 397, 401, 409, 419, 421, 431, 
              433, 439, 443, 449, 457, 461, 463, 
              467, 479, 487, 491, 499]

# Using euclid to find GCD
def gcd(p, q):
    if(q == 0):
        return abs(p)
    else:
        return gcd(q, p % q)

def genLargeNum(n):
    # Picking random number in range (2^(n-1) + 1, 2^n - 1)
    randnum = random.randrange(2**(n-1)+1, 2**n-1)
    return randnum

def isProbablePrime(n):
    while(1):
        candidate = genLargeNum(n)
        for i in low_primes:
            if candidate % i == 0 and i**2 <= candidate:
                break
        else: 
            return candidate

def mrTrialBasic(candidate):
    #Using the miller-rabin algorithm to check if a number is probably prime
        #a^(p-1) mod p = 1 true if p is prime (Fermat's)
        # We will run 15 iterations of this test
        ec = candidate - 1
        divisions = 0
        while(ec % 2 == 0):
            ec >>= 1
            divisions += 1

        # Basic trial to test for composite number (note that this does not guarentee
        # a number IS prime if it returns True)
        def basicTrial(round_candidate):
            if(pow(round_candidate,ec,candidate) == 1):
                return False
            for i in range(divisions):
                if(pow(round_candidate,(2**i*ec), candidate) == candidate - 1):
                    return False
            return True
        
        # Because of this, we run trial 50 times so there is a very small change
        # the number is psuedo-prime
        for i in range(1):
            ro_candidate = random.randrange(2, candidate)
            if(basicTrial(ro_candidate)):
                return False
        return True


def generateNBitPrime(n):
    while(1):
        probable_prime = isProbablePrime(n)
        if not mrTrialBasic(probable_prime):
            continue
        #print(probable_prime, "is most likely prime")
        return probable_prime

def getEncryptionKey(phi_mod):
    #selecting (randomly) the encryption key e
    e = 0
    while(1):
        e = random.randrange(1, phi_mod)
        if(gcd(e, phi_mod) == 1):
            return e

def getDecryptionKey(e, phi_mod):
    d = pow(e, -1, phi_mod)
    assert((e*d) % phi_mod == 1)
    return d

# Function to generate public/private keys
def generateRSAkeys(n):
    # Generating 1024 bit p and q values
    prime1 = generateNBitPrime(n)
    #prime1_bin = bin(prime1)
    #print("Prime1 binary", prime1_bin)

    prime2 = generateNBitPrime(n)
    #prime2_bin = bin(prime2)
    #print("Prime2 binary", prime2_bin)

    modulus = prime1 * prime2
    phi_modulus = (prime1-1) * (prime2-2)

    e = getEncryptionKey(phi_modulus)
    d = getDecryptionKey(e, phi_modulus)

    f = open("Client/publickey.txt", "w")
    f.write(str(e))
    f.write('\n')
    f.write(str(modulus))
    f.close()

    f = open("Server/privatekey.txt", "w")
    f.write(str(d))
    f.write('\n')
    f.write(str(prime1))
    f.write('\n')
    f.write(str(prime2))
    f.close()

def main():
    generateRSAkeys(768)

if __name__ == "__main__":
    main();