#Client module acting as the ATM

#imports
import socket
import math
import secrets

from RSA import *
from sha1 import *
from DES import *
def check_int(d_w):
	st = "How much would you like to " + d_w + "?\n"
	amount = input(st)
	try:
		amount_int = int(amount)
		is_int = True
	except ValueError:
		is_int = False
	return amount, is_int

def main():
	# static variables
	HOST = "127.0.0.1"
	PORT = 65432

	# non-static variables
	authenticated = False
	# key used for DES
	symmetric_key = 0

	#######
	#SETUP#
	#######
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

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Authentication steps
		s.connect((HOST, PORT))
		
		
		# Entering a loop where we will continually communicate
		# w/ the bank
		while(1):
			if not authenticated:

				###########
				#HANDSHAKE#
				###########

				# Client_hello
				# Usage <Hello/TLS/RSA/DES
				msg = "Hello TLS RSA 3DES"
				try:
					msg_encrypted = RSA_encrypt_sign(client_private, server_public, msg)
				except:
					print("CLIENT: ERROR: Message not understood. Exiting...")
					return 1
				s.sendall(msg_encrypted)

				# Server_hello
				data = s.recv(512)
				try:
					message = RSA_decrypt_sign(client_private, server_public, data)
				except:
					print("CLIENT: ERROR: Message not understood. Exiting...")
					return 1
				data = message.split()
				if len(data) != 1 or data[0] != "Success":
					print("ERROR: Incompatable securities. Exiting...")
					return 1
				print("CLIENT: Established security capabilities")

				# Client_nonce
				RNG = secrets.SystemRandom()
				nonce = RNG.randrange(2**100, 2**200)
				try:
					nonce_encrypted = RSA_encrypt_sign(client_private, server_public, str(nonce))
				except:
					print("CLIENT: ERROR: Message not understood. Exiting...")
					return 1
				s.sendall(nonce_encrypted)
				nonce_bounceback = s.recv(512)
				try:
					nonce_bounceback = RSA_decrypt_sign(client_private, server_public, nonce_bounceback)
				except:
					print("CLIENT: ERROR: Message not understood. Exiting...")
					return 1
				if nonce_bounceback != str(nonce):
					print("ERROR: Incorrect server authentication. Exiting...")
					return 1

				# Server_key_exchange
				data = s.recv(512)
				try:
					message = RSA_decrypt_sign(client_private, server_public, data)
				except:
					print("CLIENT: ERROR: Message not understood. Exiting...")
					return 1
				data = message.split()
				symmetric_key = int(data[0])

				# Client_key_auth
				try:
					msg_encrypted = RSA_encrypt_sign(client_private, server_public, data[0])
				except:
					print("CLIENT: ERROR: Message not understood. Exiting...")
					return 1
				s.sendall(msg_encrypted)

				# Server_Hmac_key_exchange
				data = s.recv(512)
				try:
					message = RSA_decrypt_sign(client_private, server_public, data)
				except:
					print("CLIENT: ERROR: Message not understood. Exiting...")
					return 1
				data = message.split()
				hmac_key = int(data[0])

				# Client_key_auth
				try:
					msg_encrypted = RSA_encrypt_sign(client_private, server_public, data[0])
				except:
					print("CLIENT: ERROR: Message not understood. Exiting...")
					return 1
				s.sendall(msg_encrypted)

				#Server_verify_goodbye
				data = s.recv(512)
				try:
					message = RSA_decrypt_sign(client_private, server_public, data)
				except:
					print("CLIENT: ERROR: Message not understood. Exiting...")
					return 1
				data = message.split()
				if len(data) != 1 or data[0] != "Success":
					print("ERROR: Fraudulent messaging detected. Exiting...")
					return 1
				print("CLIENT: Authenticated")
				authenticated = True

			else:

				###################
				#BAKING OPERATIONS#
				###################

				# Use sendall to send messages to server (bank)
				print("USAGE: <Withdraw/Deposit/Check/Quit>")
				print("")
				message = input("What would you like to do?\n").lower()
				transmission = ""
				if message == "check":
					print("CLIENT: Requested balance check")
					transmission += "check "
				elif message == "deposit":
					print("CLIENT: Requested money deposit")
					transmission += "deposit "
					amount, is_int = check_int("deposit")
					if not is_int:
						print("WARNING: Please enter an integer value")
						continue
					transmission += amount
				elif message == "withdraw":
					print("CLIENT: Requested money withdraw")
					transmission += "withdraw "
					amount, is_int = check_int("withdraw")
					if not is_int:
						print("WARNING: Please enter an integer value")
						continue
					transmission += amount
				elif message == "quit":
					print("CLIENT: Atm requested quit. Exiting...")
					transmission += "quit"
				else:
					print("WARNING: Unrecognized command")
					continue
				transmission+='.'

				# print("This is the transmission:", transmission.lower())
				# m = makeBlocks(transmission.lower(),1)
				# bit_m = ""
				# for i in range(len(m)):
				# 	bit_m += m[i].bin

				# #m = str(transmission.lower().encode('UTF-8', errors = "ignore"))
				
				# #m = bin(int(''.join(str(ord(c)) for c in m)))[2:]
			
				# message_hmac = HMAC(bit_m, hmac_key)
				# print("Hashing this value:", bit_m,"with this key:",hmac_key)
				# print("This is message_hmac:",message_hmac)
				# number = int(message_hmac,16)
				# length = math.ceil(number.bit_length() / 8)

				# # hmac_bytes = number.to_bytes(length, byteorder="little")
				# # mess = transmission.lower().encode('UTF-8', errors = "ignore") + hmac_bytes
                
	
                
				# encrypt_mess = encodeTripleDES(transmission + message_hmac, BitArray(uint = symmetric_key, length = 192))
				# print("Sending", blocksToString(encrypt_mess), encrypt_mess)
				# encrypt_mess_bytes = blocksToString(encrypt_mess).encode('UTF-8')
				s.sendall(create_packet(transmission, symmetric_key, hmac_key))
                
				# encrypt_mess = encodeTripleDES(message_hmac, BitArray(uint = symmetric_key, length = 192))
				# encrypt_mess_bytes = blocksToString(encrypt_mess).encode('UTF-8')
				# s.sendall(encrypt_mess_bytes)
                
				data = s.recv(512).decode('UTF-8', errors = "ignore")
				word, data = read_packet(data, symmetric_key, hmac_key)
				print("got back: ", data)
				if data[0] == "Quit":
					break
				elif data[0] == "Warning":
					print("Received", data[0])
					if(data[1] == "NEC"):
						print("Client has insifficient capital to complete this withdrawl")
				else:
					print("Received", data[0])
					print("Client has", data[1], "dollars remaining in account")

	return 0
if __name__ == "__main__":
	main()