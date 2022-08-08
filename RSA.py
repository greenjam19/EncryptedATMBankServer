# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 18:15:37 2022

@author: wut6
"""
import math

def RSA_encrypt(public_key, private_key, message):
    if (type(message) == type("a")):
        message = int.from_bytes(message.encode('utf-8'), byteorder = 'little')
    # else:
    #     message = int.from_bytes(message, byteorder = 'little')
    #message = pow(message, private_key[0], private_key[1]*private_key[2])
    ciphertext = pow(message, public_key[0], public_key[1])
    len = math.ceil(ciphertext.bit_length() / 8)
    return ciphertext.to_bytes(len, byteorder = 'little')

def RSA_decrypt(pblic_key, private_key, msg):
	msg = int.from_bytes(msg, 'little', signed = False)
	message = pow(msg, private_key[0], private_key[1] * private_key[2])
	#message = pow(message, public_key[0], public_key[1])
	len = math.ceil(message.bit_length() / 8)
	message = message.to_bytes(len, byteorder = 'little').decode('utf-8')
	return(message)

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
        
#message = "hello there"

#x = RSA_decrypt(client_private, message.encode('utf-8'))
#xp = RSA_encrypt(server_public, x)

#y = RSA_decrypt(server_private, xp)
#yp = RSA_encrypt(client_public, y)
#print(yp.decode())