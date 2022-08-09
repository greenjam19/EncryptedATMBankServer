# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 18:15:37 2022

@author: wut6
"""
import math

from sha1 import Hash
from bitstring import BitArray

from DES import *
from sha1 import *

def RSA_encrypt(public_key, message):
    if (type(message) == type("a")):
        message = int.from_bytes(message.encode('utf-8'), byteorder = 'little')
    # else:
    #     message = int.from_bytes(message, byteorder = 'little')
    #message = pow(message, private_key[0], private_key[1]*private_key[2])
    ciphertext = pow(message, public_key[0], public_key[1])
    len = math.ceil(ciphertext.bit_length() / 8)
    return ciphertext.to_bytes(len, byteorder = 'little')

def RSA_decrypt(private_key, msg):
    if (type(msg) == type("a".encode())):
        msg = int.from_bytes(msg, 'little', signed = False)
    message = pow(msg, private_key[0], private_key[1] * private_key[2])
	#message = pow(message, public_key[0], public_key[1])
	#len = math.ceil(message.bit_length() / 8)
	#message = message.to_bytes(len, byteorder = 'little').decode('utf-8')
    return(message)

def itoa(number):
    length = math.ceil(number.bit_length() / 8)
    message = number.to_bytes(length, byteorder="little").decode("utf-8")
    return message

def atoi(message):
    return int.from_bytes(message.encode('utf-8'), byteorder = 'little')

#takes a string message and a private key
#returns a signature (integer)
def RSA_sign(private_key, message):
    num = int.from_bytes(message.encode('utf-8'), byteorder = 'little')
    h = Hash(BitArray(uint = num, length = math.ceil(math.log(num) / math.log(2))).bin)
    signature = RSA_decrypt(private_key, int(h, 16));
    return signature

#takes the public key, message and signature
#returns true if the signature matches the message
def RSA_verify(public_key, message, signature):
    num = int.from_bytes(message.encode('utf-8'), byteorder = 'little')
    h = Hash(BitArray(uint = num, length = math.ceil(math.log(num) / math.log(2))).bin)
    h = int(h, 16)
    
    hprime = RSA_encrypt(public_key, signature)  
    hprime = int.from_bytes(hprime, byteorder = "little")
    #print("hprime", hprime)
    #print(h)
    return h == hprime

#encodes the message (string) with the private key of the sender
#and then the public key of the reciever
#return the ciphertext (bytes)
def RSA_encrypt_sign(private_key, public_key, message):
    #print(message.encode("utf-8"))
    x = RSA_decrypt(private_key, message.encode('utf-8'))
   # print("x", x)
    xp = RSA_encrypt(public_key, x)
    #print("xp", xp)
    return xp

#decryptes the ciphertext (bytes) using the public_key of the sender
#and the private_key of the reciever, return a string
def RSA_decrypt_sign(private_key, public_key, ciphertext):
    y = RSA_decrypt(private_key, ciphertext)
    #print("y", y)
    yp = RSA_encrypt(public_key, y)
    #print("yp", yp)
    tries = 0
    out = ""
    while True:
        try:
            out = yp.decode()
            break
        except:
            y+= private_key[1] * private_key[2]
            yp = RSA_encrypt(public_key, y)
        tries += 1
        if (tries == 20):
            break
            print("cannot decrypt")
    return out

def create_packet(transmission, symmetric_key, hmac_key):
    m = makeBlocks(transmission.lower(),1)
    bit_m = ""
    for i in range(len(m)):
        bit_m += m[i].bin

    message_hmac = HMAC(bit_m, hmac_key)
    number = int(message_hmac,16)

    encrypt_mess = encodeTripleDES(transmission + message_hmac, BitArray(uint = symmetric_key, length = 192))
    encrypt_mess_bytes = blocksToString(encrypt_mess).encode('UTF-8')

    return encrypt_mess_bytes

def read_packet(data, symmetric_key, hmac_key):
    decoded_mess = decodeTripleDES(makeBlocks(data,64), BitArray(uint = symmetric_key, length = 192))
    ptext_mess = blocksToString(decoded_mess)
    #print("SERVER: Received", ptext_mess)
    listOfData = ptext_mess.split('.')
    lis = ptext_mess.split(".")
    #print("decrypted:", lis)

    m = makeBlocks(lis[0].lower() + '.',1)
    bit_m = ""
    for i in range(len(m)):
        bit_m += m[i].bin

    message_hmac = HMAC(bit_m, hmac_key)

    worked = True
    for i in range(len(message_hmac)):  
        if message_hmac[i] != lis[1][i]:
            #print("SERVER: Received invalid MAC.")
            worked = False
            break
    return (worked, lis[0].split())

if __name__ == "__main__":
    with open("ServerPrivateKey.txt", "r") as f:
    		lines = f.readlines()
    		d = int(lines[0])
    		p = int(lines[1])
    		q = int(lines[2])
    		# PRIVATE KEY: {d, p, q}
    		server_private = (d, p, q)
    
    with open("ClientPublicKey.txt", "r") as f:
    		lines = f.readlines()
    		e = int(lines[0])
    		N = int(lines[1])
    		# PUBLIC KEY: {e, N}
    		client_public = (e, N)
    with open("ServerPublicKey.txt", "r") as f:
    		lines = f.readlines()
    		e = int(lines[0])
    		N = int(lines[1])
    		# PUBLIC KEY: {e, N}
    		server_public = (e, N)
    
    with open("ClientPrivateKey.txt", "r") as f:
    		lines = f.readlines()
    		d = int(lines[0])
    		p = int(lines[1])
    		q = int(lines[2])
    		# PRIVATE KEY: {d, p, q}
    		client_private = (d, p, q)
            
    message = "testing a very long strin"
    print(message.encode("utf-8"))
    x = RSA_decrypt(client_private, message.encode('utf-8'))
    print("x", x)
    xp = RSA_encrypt(server_public, x)
    print("xp", xp)
    
    
    y = RSA_decrypt(server_private, xp)
    print("y", y)
    yp = RSA_encrypt(client_public, y)
    print("yp", yp)
    while True:
        try:
            print(yp.decode())
            break
        except:
            y+= server_private[1] * server_private[2]
            yp = RSA_encrypt(client_public, y)
    #print(yp.decode("utf-8"))
    
    test = RSA_decrypt(client_private, message.encode("utf-8"))
    done = RSA_encrypt(client_public, test)
    
    test1 = RSA_encrypt(server_public, message)
    done1 = RSA_decrypt(server_private, test1)
    
    sig = RSA_sign(client_private, message)
    print("signature:", sig)
    
    print(RSA_verify(client_public, message, sig))