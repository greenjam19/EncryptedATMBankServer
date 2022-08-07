from random import * 
def Hash(message):
    def XOR_4(word1, word2, word3, word4):
        xor_ = []
        for i in range(32):
            temp = ((((int(word1[i])+int(word2[i]))%2 + int(word3[i]))%2) + int(word4[i]))%2
            xor_.append(str(temp))
        return xor_

    def rotate(n, b):
            if type(n) == int:
                return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF
            return n[b:] + n[:b]

    """
    Takes in 16 32-bits chunks, and extends it to 80
    """
    def expand_block(block):
        
            for i in range (16,80):
                word1, word2, word3, word4 = block[i - 3], block[i - 8], block[i - 14], block[i - 16]
                newEntry = rotate(XOR_4(word1,word2,word3,word4),1)
                block.append(''.join(newEntry))

    """5 hex strings of length 8, must be constant"""
    H = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    a, b, c, d, e = H[0], H[1], H[2], H[3], H[4] 

    """Message padding stage"""
    len_in64 = bin(len(message))[2:]
    len_in64 = "0"*(64-len(len_in64)) + len_in64

    message += "1" 

    while(len(message)%512!=448):
        message+= '0'
    message+= len_in64

    """Split into chunks each of 512 "bits" """
    chunks_512 = [message[i:i+512] for i in range(0, len(message), 512)]

    """Split those chunks of 512 bits into chunks each of 32 "bits (16 for each subarray in chunks_32)" """
    chunks_32 = []
    for i in range(len(chunks_512)):
        chunks_32.append([chunks_512[i][j:j+32] for j in range(0, 512, 32)])

    for i in range(len(chunks_32)):
        expand_block(chunks_32[i])
        


    for i in range(len(chunks_32)):
        expand_block(chunks_32[i])
        a, b, c, d, e = H
        for j in range(0,80):
            if 0 <= j < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999

            elif 20 <= j < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1

            elif 40 <= j < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
                
            elif 60 <= j < 80:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            a, b,c,d,e = (rotate(a, 5) + f + e + k + int(chunks_32[i][j], 2) & 0xFFFFFFFF,
                        a, 
                        rotate(b, 30), 
                        c, 
                        d)

        H = [H[0] + a & 0xFFFFFFFF, H[1] + b & 0xFFFFFFFF, H[2] + c & 0xFFFFFFFF, 
                                        H[3] + d & 0xFFFFFFFF, H[4] + e & 0xFFFFFFFF]

    HASH_VALUE = "%08x%08x%08x%08x%08x" % tuple(H)

    return HASH_VALUE

def main():
    """Is currently encoding the string "A Test" """
    hash1 = Hash('010000010010000001010100011001010111001101110100')
    
    """Is currently encoding the string "RENSSELAER" """
    hash2 = Hash('01010010010001010100111001010011010100110100010101001100010000010100010101010010')
    
    # use link http://www.sha1-online.com/ to get expected values of different strings above
    exp1 = '8f0c0855915633e4a7de19468b3874c8901df043'
    exp2 = '09d3f3dd1acef4c83ea8bcbe56083b13b77abcb8'

    assert(hash1 == exp1)
    assert(hash2 == exp2)

if __name__ == "__main__":
    main()


    








