# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 20:45:26 2022

@author: wut6
"""

from bitstring import BitArray
import random
import time

#initial permutation 
IP = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
)

# E-box 32 to 48
E_BOX = (
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
)

# S box 48 to 32
S_BOX = (
    ((14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
     (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
     (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
     (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),),

    ((15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
     (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
     (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
     (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),),

    ((10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
     (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
     (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
     (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),),

    ((7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
     (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
     (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
     (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),),

    ((2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
     (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
     (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
     (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),),

    ((12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
     (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
     (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
     (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),),

    ((4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
     (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
     (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
     (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),),

    ((13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
     (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
     (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
     (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),)
)

P_BOX = (
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25,
)

#inverse permutation
IP_1 = (
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
)

'''Key generation'''

# Check code removal 64 to 56
CLEAR_CHECK_CODE = (
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
)

# 48bit final subcode 56 to 58
KEY_SELECT_BOX = (
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
)

#amount of left spin for each round
left_spin = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)


'''takes in a permutation and applys it to the bits
resulting string will the same length as the permutation
size of the bitArray should be equal to or greater than the largest
index in perm (note: the permutation specifies indicies starting from 1)'''
def applyPermutation(bits, perm):
    temp = BitArray(length = len(perm))
    for i in range(len(perm)):
        temp[i] = bits[perm[i] - 1]
    return temp

#applies the sbox 0 - 7 on bits
#bits is 6 bits long, output is 4 bits
def apply_sbox(bits, sbox):
    r0 = bits[::5]
    c0 = bits[1:5]
    
    r0 = 0 if not r0 else r0.uint
    c0 = 0 if not c0 else c0.uint
    
    return BitArray(uint = S_BOX[sbox][r0][c0], length = 4)

#returns a circular left shift
def left_shift(bits):
    first = bits[0]
    bits = bits << 1
    bits[-1] = first
    return bits

#shifts both halves of a key
def key_shift(key, n):
    first, second= key[:key.length // 2], key[key.length//2:]
    for i in range(n):
        first = left_shift(first)
        second = left_shift(second)
    return first + second

#generates the subkeys for each round
#64-bit key generated 
def generateSubkeys(key, rounds):
    keys = []
    temp = applyPermutation(key, CLEAR_CHECK_CODE)
    for i in range(rounds):
        temp = key_shift(temp, left_spin[i])
        keys.append(applyPermutation(temp, KEY_SELECT_BOX))
    return keys

#converts the string into n bit blocks
#pads the last block with zeros if it is not divisible by n
def makeBlocks(string, n):
    bits = BitArray(length = 0)
    blocks = []
    for i in string:
        #print(BitArray(uint = ord(i), length = 8).bin)
        bits += BitArray(uint = ord(i), length = 8)
    #print("allbits:", bits.bin, bits.length)
    last = 0
    for i in range(n,bits.length, n):
        blocks.append(bits[last:i])
        last = i
    #print(last, bits.length)
    if (last < bits.length):
        finalBlock = bits[last:]
        if n - finalBlock.length > 0:
           finalBlock += BitArray(uint = 0, length = n - finalBlock.length)
        blocks.append(finalBlock)
    
    #print(blocks[-1].bin)
    return blocks

def blocksToString(blocks):
    bits = BitArray(length = 0)
    plaintext = ""
    for i in blocks:
        bits += i
    last = 0
    for i in range(8,bits.length, 8):
        plaintext += chr(bits[last:i].uint)
        last = i
    return plaintext
    
#half block is 32 bits
#key is 48 bits
def F(half_block, key):
    expanded = applyPermutation(half_block, E_BOX)
    expanded ^= key
    
    output = BitArray()
    for i in range(8):
        bits = expanded[i*8: (i+1) * 8]
        output += apply_sbox(bits, i)
    return applyPermutation(output, P_BOX)

def around(block, key, last):
    first, second = block[:block.length//2], block[block.length//2:]
    out = F(second, key)
    first ^= out
    if not last:
        return second + first
    else:
        return first + second

#encodes a list of blocks using DES
def encodeDES(blocks, key, rounds):
    out = []
    keys = generateSubkeys(key, rounds)
    
    for block in blocks:
        #print("len:", block.length)
        block = applyPermutation(block, IP)
        for r in range(rounds):
            block = around(block, keys[r], r == rounds - 1)
        out.append(applyPermutation(block, IP_1))
    return out

#decodes a list of 8 bit blocks using S-DES
def decodeDES(ciphertext, key, rounds):
    plaintext = []
    keys = generateSubkeys(key, rounds)
    
    for block in ciphertext:
        block = applyPermutation(block, IP)
        for r in range(rounds):
            block = around(block, keys[rounds - 1 - r], r == rounds - 1)
        plaintext.append(applyPermutation(block, IP_1))
    return plaintext

#key is 192 bits long
def encodeTripleDES(plaintext, key):
    blocks = makeBlocks(plaintext, 64)
    key1 = key[:64]
    key2 = key[64:128]
    key3 = key[128:]
    
    blocks = encodeDES(blocks, key1, 16)
    blocks = decodeDES(blocks, key2, 16)
    blocks = encodeDES(blocks, key3, 16)
    
    return blocks

def decodeTripleDES(plaintext, key):
    key1 = key[:64]
    key2 = key[64:128]
    key3 = key[128:]
    
    blocks = plaintext
    
    blocks = decodeDES(blocks, key3, 16)
    blocks = encodeDES(blocks, key2, 16)
    blocks = decodeDES(blocks, key1, 16)
    
    return blocks

#generate an n-bit random key
def generateRandomKey(n):
    key = BitArray(uint = 0, length = n)
    random.seed(time.time_ns() % 100000)
    for i in range(n // 2):
        if (random.randint(0,1) == 1):
            key[i] = True
    random.seed(time.time_ns() % 100000)
    for i in range(n//2, n):
        if (random.randint(0,1) == 1):
            key[i] = True
    
    return key



