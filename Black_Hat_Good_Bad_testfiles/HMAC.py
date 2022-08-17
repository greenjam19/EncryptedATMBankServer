# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 18:16:29 2022

@author: pardan
"""

#HMAC
#MAC that will be added at the end of the message

import sha1
import bitstring


#The HMAC is the implementation of the HMAC function using SHA-1 hashing algorith,
def HMAC(message):
    #We will first set our key and outerpad and innerpad values
    key = bitstring.BitArray(int = 245, length = 10)
    outerPad = bitstring.BitArray(hex(0x012345673555555501234567355555550123456735555555012345673555555501234567355555550123456735555555012345673555555501234567355555555))
    innerPad = bitstring.BitArray(hex(0xabcdef12355555550123456735555555501234567355555555012345673555555550123456735555555501234567355555555012345673555555550123456735))

    #Since we are dealing with SHA-1, our block will be of 512-bits
    b = 512

    #We will all 0s to the front of the key bits until the length is 512-bits
    while(len(key.bin) < b):
        key.bin = '0' + key.bin
    
    #Next, we will XOR the new key value with the innerPad and outerPad
    arr = []
    for i in range(len(key.bin)):
        arr.append(int(key.bin[i]))
    
    k = bitstring.BitArray(arr)
    
    #We will hold the xor results
    xorInner = k ^ innerPad
    xorOuter = k ^ outerPad
    
    #We will then join the bits of the message binary representation with the xorInner result
    bin_message = bitstring.BitArray(bytes=message.encode())

    #The result will be stored in new_message
    new_message = xorInner+bin_message

    #Our first MAC value will be stored in MAC1
    MAC1 = sha1.SHA.sha1(new_message)
    
    #we will translate it into a bitstrig BitArray
    second_round = bitstring.BitArray(hex=MAC1)
    
    #Since the Hash values are always 512-bits in SHA-1, we will add 0s to the front until the length of the secound_round is 512-bits
    while(len(second_round.bin)!=512):
        second_round.bin = '0' + second_round.bin
        
    #We will then append the xorOuter result to the second_round variable
    new_message2 = xorOuter + second_round

    #Lastly, we have our final MAC value
    FINAL_MAC = sha1.SHA.sha1(new_message2)
    
    return FINAL_MAC
    