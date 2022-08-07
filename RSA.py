# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 18:15:37 2022

@author: wut6
"""
import math

def RSA_encrypt(public_key, message):
	message = int.from_bytes(message.encode(), byteorder = 'little')
	ciphertext = pow(message, public_key[0], public_key[1])
	len = math.ceil(ciphertext.bit_length() / 8)
	return ciphertext.to_bytes(len, byteorder = 'little')

def RSA_decrypt(private_key, msg):
	msg = int.from_bytes(msg, 'little', signed = False)
	message = pow(msg, private_key[0], private_key[1] * private_key[2])
	len = math.ceil(message.bit_length() / 8)
	message = message.to_bytes(len, byteorder = 'little').decode()
	return(message)