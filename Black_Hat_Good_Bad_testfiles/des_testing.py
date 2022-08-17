from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from des import *

def test_3des_block():
    for i in range(1000):
        key = BitArray(uint = randint(pow(2, 63), pow(2, 64) - 1), length=64) + BitArray(uint = randint(pow(2, 63), pow(2, 64) - 1), length=64) + BitArray(uint = randint(pow(2, 63), pow(2, 64) - 1), length=64)
        plaintext = BitArray(uint = randint(pow(2, 63), pow(2, 64) - 1), length=64)

        their_cipher = DES3.new(key.bytes, DES3.MODE_ECB)
        my_cipher = TripleDES(key)

        # Testing equality of outputs
        if BitArray(their_cipher.encrypt(plaintext.bytes)) == my_cipher.encrypt_block(plaintext):
            print("true")
        else:
            print("false")
            print("their ciphertext", BitArray(their_cipher.encrypt(plaintext.bytes)))
            print("my ciphertext", my_cipher.encrypt_block(plaintext))
            return

        # Testing their encrypt decrypt for sanity
        if their_cipher.decrypt(their_cipher.encrypt(plaintext.bytes)) == plaintext.bytes:
            print("true")
        else:
            print("false")
            print("plaintext", plaintext)
            print("deciphered text:", their_cipher.decrypt(their_cipher.encrypt(plaintext.bytes)))
            return

        # Testing full encrypt decrpyt
        if my_cipher.encrypt_block(my_cipher.decrypt_block(plaintext)) == plaintext:
            print("true")
        else:
            print("false")
            print("plaintext", plaintext)
            print("deciphered text:", my_cipher.encrypt_block(my_cipher.decrypt_block(plaintext)))
            return

        print("tests passed for plaintext:", plaintext)
        print()

        if (i % 100 == 0 and i != 0):
            print()
            print(i, "tests passed!")
            print()

if __name__ == "__main__":
    test_3des_block()