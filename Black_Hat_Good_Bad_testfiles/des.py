from pydoc import plain
from bitstring import BitArray
from random import randint

# Initial and inverse permutations
InitialP = [
    58, 50, 42, 34, 26, 18, 10, 2, 
    60, 52, 44, 36, 28, 20, 12, 4, 
    62, 54, 46, 38, 30, 22, 14, 6, 
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

InverseP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# F box permutations
EP = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

P32 = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

# Sboxes 1 through 8
SBoxes = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Intial compression box in key schedule
P56 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Second compression permutation in key schedule
P48 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Number of left circular shifts
Shifts = [ 1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1 ]

# Utility function to make the inverse of a pbox
def make_inverse(InitialP):
    InverseP = [-1] * 64
    for i in range(64):
        InverseP[InitialP[i] - 1] = i + 1
    
    return InverseP

# Utilitiy function to reformat an array so there are no spaces
# Takes dimensions to reformat
def reformat_box(array, height, width):
    print("[")
    for i in range(height - 1):
        print(end="\t")
        for j in range(width - 1):
            print(array[i*width + j], end=", ")
        print(array[i*width + width - 1], end=",")
        print()
    print(end="\t")
    for j in range(width - 1):
        print(array[(height - 1)*width + j], end=", ")
    print(array[(height - 1)*width + width - 1])
    print("]")


# Function that allows for permutation or expansion given a permutation box
def permutation(original, PBox):
    output = BitArray(uint=0, length=len(PBox))

    i = 0
    for pos in PBox:
        output[i] = original[pos-1]
        i += 1
    
    return output

# Takes as input the round and the output from the previous round
def generate_round_key(i, initial):
    out1 = initial[:28]
    out2 = initial[28:]

    out1.rol(Shifts[i])
    out2.rol(Shifts[i])

    key = permutation(out1 + out2, P48)

    return (key, out1 + out2)

# Generation of round keys
def generate_keys(initial):
    keys = []

    # Initial permutation
    out = permutation(initial, P56)

    for i in range(16):
        result = generate_round_key(i, out)
        keys.append(result[0])
        out = result[1]

    return keys

# Function takes six bit inputs finds appropriate row, col in sbox
def SBox(bits, S_mat):
    row = bits[0] * 2 + bits[5]
    col = bits[1] * 8 + bits[2] * 4 + bits[3] * 2 + bits[4]
    return BitArray(uint=S_mat[row][col], length=4)

# All functionality for the f component
def FBox(bits, key):
    # expansion
    out = permutation(bits, EP)
    
    # xor
    out ^= key
    
    # Going through the 8 sboxes
    new_out = BitArray()
    for i in range(8):
        new_out += SBox(out[i*6:(i+1)*6], SBoxes[i]) 
    out = new_out
    
    # final permutation
    out = permutation(out, P32)
    
    return out

# A full round of DES
def Round(bits1, bits2, key):
    return (bits1 ^ FBox(bits2, key), bits2)

# The basic DES class
class DES():  
    def __init__(self, key):
        self.key = key
        self.keys = generate_keys(key)

    # Encrypts a 64 bit block
    def encrypt_block(self, bits):
        # Initial permuatation
        out = permutation(bits, InitialP)

        # Rounds
        bits1 = out[32:]
        bits2 = out[:32]
        for i in range(16):
            bits1, bits2 = Round(bits2, bits1, self.keys[i])
        
        # Inverse permutation
        out = permutation(bits1 + bits2, InverseP)
        
        return out
    
    # Decrypts a 64 bit block
    def decrypt_block(self, bits):
        # Initial permuatation
        out = permutation(bits, InitialP)

        # Rounds
        bits1 = out[32:]
        bits2 = out[:32]
        for i in range(15, -1, -1):
            bits1, bits2 = Round(bits2, bits1, self.keys[i])
        
        # Inverse permutation
        out = permutation(bits1 + bits2, InverseP)
        
        return out

# Class with implementation for triple des block cipher
class TripleDES():
    def __init__(self, key):
        self.des1 = DES(key[:64])
        self.des2 = DES(key[64:128])
        self.des3 = DES(key[128:])

    # Encrypts a 64 bit block
    def encrypt_block(self, bits):
        out = self.des1.encrypt_block(bits)
        out = self.des2.decrypt_block(out)
        out = self.des3.encrypt_block(out)

        return out
    
    def decrypt_block(self, bits):
        out = self.des3.decrypt_block(bits)
        out = self.des2.encrypt_block(out)
        out = self.des1.decrypt_block(out)

        return out

# Electronic codebook encryption mode for tripledes
class ECB(TripleDES):
    def encrypt(self, plaintext):
        # Padding with 0s based on block size of 8 bytes
        plaintext += "\0" * (8 - len(plaintext) % 8)
        plaintext = BitArray(bytes = bytes(plaintext, 'utf-8'))
        
        ciphertext = BitArray()

        # division happes twice 8 bits to a byte, 8 bytes to a block
        for i in range(((len(plaintext) // 8) // 8)):
            ciphertext += self.encrypt_block(plaintext[i*64:(i+1)*64])

        return ciphertext

    # expected that ciphertext is zero padded
    def decrypt(self, ciphertext):
        plaintext = BitArray()

        for i in range(((len(ciphertext) // 8) // 8)):
            plaintext += self.decrypt_block(ciphertext[i*64:(i+1)*64])
            
        return str(plaintext.bytes, 'utf-8')

# Must be used in the exact order of encrypt decrypt
class CBC(ECB):
    def __init__(self, key, IV):
        self.true_IV = IV
        self.IV = IV
        super().__init__(key)

    def encrypt(self, plaintext):
        self.IV = self.true_IV
        return super().encrypt(plaintext)

    def encrypt_block(self, bits):
        self.IV = super().encrypt_block(bits ^ self.IV)
        return self.IV

    def decrypt(self, ciphertext):
        self.IV = self.true_IV
        return super().decrypt(ciphertext)

    def decrypt_block(self, bits):
        ret = super().decrypt_block(bits) ^ self.IV
        self.IV = bits
        return ret

if __name__ == "__main__":
    # Sample run
    key = BitArray(uint = randint(pow(2, 63), pow(2, 64) - 1), length=64) + BitArray(uint = randint(pow(2, 63), pow(2, 64) - 1), length=64) + BitArray(uint = randint(pow(2, 63), pow(2, 64) - 1), length=64)
    plaintext = BitArray(uint = randint(0, pow(2, 64) - 1), length=64)

    des3 = TripleDES(key)

    print("plaintext:", plaintext)
    print("ciphertext:", des3.encrypt_block(plaintext))
    print("decrypted:", des3.decrypt_block(des3.encrypt_block(plaintext)))
    print()

    print("Running CBC 3des")

    IV = plaintext

    plaintext = "hi my name is bob"

    cbc= CBC(key, IV)

    print("plaintext:", plaintext)
    print("bytes:", bytes(plaintext, 'utf-8'))
    print("ciphertext:", cbc.encrypt(plaintext))
    print("decrypted:", cbc.decrypt(cbc.encrypt(plaintext)))
    print()

    print("Running ECB 3des")

    plaintext = "hi my name is bob"

    ecb = ECB(key)

    print("plaintext:", plaintext)
    print("bytes:", bytes(plaintext, 'utf-8'))
    print("ciphertext:", ecb.encrypt(plaintext))
    print("decrypted:", ecb.decrypt(ecb.encrypt(plaintext)))