# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 17:21:33 2022

@author: pardan
"""

import bitstring
from rsa import RSA, t_to_h, i_to_t, i_to_h

#The binary addition takes two lists of 0s and 1s and adds them together with carryIn and carryOut
#A BitArray that represents the sum is returned
def binary_addition(p1, p2):
        carryIn = 0
        arr = []
        #we will loop over the bit
        for i in range(len(p1.bin)-1, -1, -1):
            #If the bits are both 1, we have two scenarios
            if(int(p1.bin[i]) == 1 and int(p2.bin[i]) == 1):
                #If the carryIn is 0, the sum is 0 and the carryOut is 1
                if(carryIn == 0):
                    sums = 0
                    carryOut = 1
                #Else, the sums is 1 and the carryOut is 1
                else:
                    sums = 1
                    carryOut = 1
            #If one bit is 1 but the other isnt, we have two scenarios
            elif(int(p1.bin[i]) == 1 and int(p2.bin[i]) == 0):
                #If the carryIn is 0, the sum is 1 and the carryOut is 0
                if(carryIn == 0):
                    sums = 1
                    carryOut = 0
                #Else, the sum is 0 and the carryOut is 1
                else:
                    sums = 0
                    carryOut = 1
            #If one bit is 1 but the other isnt, we have two scenarios
            elif(int(p1.bin[i]) == 0 and int(p2.bin[i]) == 1):
                #If the carryIn is 0, the sum is 1 and the carry out is 0
                if(carryIn == 0):
                    sums = 1
                    carryOut = 0
                #Else, the sum is 0 and the carryOut is 1
                else:
                    sums = 0
                    carryOut = 1
            #If the bits are both 0, we have two scenarios
            else:
                #If the carry in is 0, the sum is 0 and there is no carryOut
                if(carryIn == 0):
                    sums = 0
                    carryOut = 0
                #Else, the sums is 1 and the carryOut is 0
                else:
                    sums = 1
                    carryOut = 0

            arr = [sums] + arr
            carryIn = carryOut
        
        ans = bitstring.BitArray(arr)
        return ans

class SHA:
    #The sha1 function is an implementation of the SHA-1 hashing function
    def sha1(bit_message):            
        #First, we will set the intial h values with the fixed hex values
        h0 = bitstring.BitArray(hex(0x67452301)) 
        h1 = bitstring.BitArray(hex(0xEFCDAB89))
        h2 = bitstring.BitArray(hex(0x98BADCFE))
        h3 = bitstring.BitArray(hex(0x10325476))
        h4 = bitstring.BitArray(hex(0xC3D2E1F0))

        #We will hold the original length of the binary representation of the message for later use
        og_length = len(bit_message.bin)

        #1 is added at the end of the bits
        bit_message.bin+='1'

        #We will save 64-bits of free sapce. If we have more space, we will simply add more 0 bits to the binary representation of the message
        while(len(bit_message.bin) % 512 != 448):
            bit_message.bin+='0'
        
        #We will use the original length of the binary representation of the message and represent it as 64-bits
        bit_length = bitstring.Bits(int=og_length, length=64)

        #We will then add the 64-bits to the binary representation of the message
        bit_message.bin+=bit_length.bin

        #Next, we will loop over the messages bits by 512 chunks
        words = []
        for i in range(0, len(bit_message.bin), 512):
            #We will take the 512 bit chunks and break it into 16 32-bit smaller chunks
            chunk = bit_message[i: i+512]
            w = []
            for j in range(0, len(chunk), 32):
                w.append(chunk[j:j+32])

            #For each of the 16 32-bit smaller chunks, we will turn them into 80 32-bit smaller chunks
            for j in range(16, 80):
                first = w[j - 3] ^ w[j - 8]
                second = first ^ w[j - 14]
                third = second ^ w[j - 16]
                third.rol(1)
                w.append(third)
            words.append(w)
        
        #The truncate ensures that we still in the range of 32-bits
        truncate = bitstring.BitArray(hex(0xffffffff))
        for i in range(len(words)):
            #We will set a0-e0 as the values of h0-h4 currently
            a0 = h0[:]
            b0 = h1[:]
            c0 = h2[:]
            d0 = h3[:]
            e0 = h4[:]
            
            #For each chunk, we will loop over the 80-bit smaller chunks and calculate for the next values of a0-e0
            for j in range(80):
                #The variables for the first 20 rounds
                if j >= 0 and j < 20:
                    f = (b0 & c0) | ((~b0) & d0)
                    k = bitstring.BitArray(hex(0x5A827999))
                
                #The variables for the second 20 rounds
                elif j >= 20 and j < 40:
                    f = b0 ^ c0 ^ d0
                    k = bitstring.BitArray(hex(0x6ED9EBA1))
                
                #The variables for the third 20 rounds
                elif j >= 40 and j < 60:
                    f = (b0 & c0) | (b0 & d0) | (c0 & d0)
                    k = bitstring.BitArray(hex(0x8F1BBCDC))
                    
                #The variable for the fourth 20 rounds
                elif j >= 60 and j < 80:
                    f = b0 ^ c0 ^ d0
                    k = bitstring.BitArray(hex(0xCA62C1D6))
                    
                #First, we set b as the original value of a
                b = a0[:]

                #Then we rotate the old values of a and b to the left, 5 bits for a and 30 bits for b
                a0.rol(5)
                b0.rol(30)
                
                #We then calculate for f + e0 + a0 + words[i][j] + k, which results in the new value of a
                temp = binary_addition(binary_addition(f, e0), a0)
                temp2 = binary_addition(temp, words[i][j])
                temp3 = binary_addition(temp2, k)
                a = temp3 & truncate

                #c is now the shifted left value of b
                c = b0

                #d is the old value of c
                d = c0

                #e is the old value of d
                e = d0
                
                #We then set a0-e0 as the new values of a-e for the next round
                a0 = a
                b0 = b
                c0 = c
                d0 = d
                e0 = e

            #After the 80 rounds, we then add a0 to h0, b0 to h1, c0 to h2, d0 to h3, and e0 to h4 
            h0 = binary_addition(h0, a0) & truncate
            h1 = binary_addition(h1, b0) & truncate
            h2 = binary_addition(h2, c0) & truncate
            h3 = binary_addition(h3, d0) & truncate
            h4 = binary_addition(h4, e0) & truncate

        #We will then combine the h values together and return the hex value as the hash value of the message
        return (h0+h1+h2+h3+h4).hex

#The main function is used to test one of the string messages
if __name__ == "__main__":
    mes = "wpwodvslgshlkhdshfkdhghkdhlkhgkhfhdskhfdhhghgldshgkhgkdshghdsghdkghdglhdkfhdskhdshfkshdkfhdskfhhfdfkhdfhdkhfkdshfkdshfkdhfkhf"
    aws = bitstring.BitArray(mes.encode())
    ans = SHA.sha1(aws)
    print(ans)
    assert(ans == "cb1497e482c4bedad70d59b8b5f12bf11c7b3b84")
      