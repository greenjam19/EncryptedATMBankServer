#server module to act as the bank

#imports
import socket
import os
import random
import math
import secrets
from bitstring import BitArray
from sha1 import *
from DES import *
from RSA import *

def main():
	#static variables
	HOST = "127.0.0.1"
	PORT = 65432

	time = 0
	# non-static variables
	balance = 0
	authenticated = False
	# Key used for DES (setup)
	symmetric_key = secrets.randbits(192)
	# Key used for HMAC Encryption
	hmac_key = secrets.randbits(64)
	#######
	#SETUP#
	#######
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

	# No need to call s.close() here, as everything is done in a with
	# statement
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Using TCP                             ^^^^^^^^^
		#Binding to associate socket w/ localhost (127.0.0.1)
		s.bind((HOST, PORT))
		s.listen()

		print("SERVER: Blocked on accept")
		conn, addr = s.accept()
		with conn:
			print("SERVER: Connected to", addr, "(localhost)")
			while(1):
				if not authenticated:

					###########
					#HANDSHAKE#
					###########

					returnable = ""
					#Client_hello
					data = conn.recv(512)
					try:
						message = RSA_decrypt_sign(server_private, client_public, data)
					except:
						print("SERVER: ERROR: Message not understood. Exiting...")
						return 1
					data = message.split()
					if(len(data) != 4 or data[0] != "Hello" or data[1] != "TLS" or data[2] \
						!= "RSA" or data[3] != "3DES"):
						returnable += "Failure"
					else:
						returnable += "Success"
					#Server_hello
					try:
						msg_encrypted = RSA_encrypt_sign(server_private, client_public, returnable)
					except:
						print("SERVER: ERROR: Message not understood. Exiting...")
						return 1
					conn.sendall(msg_encrypted)
					if(returnable == "Failure"):
						print("SERVER: Detected incompatablie client. Exiting...")
						break

					# Client_nonce
					nonce = conn.recv(512)
					try:
						nonce_decrypted = RSA_decrypt_sign(server_private, client_public, nonce)
						nonce_encrypted = RSA_encrypt_sign(server_private, client_public, nonce_decrypted)
					except:
						print("SERVER: ERROR: Message not understood. Exiting...")
						return 1
					conn.sendall(nonce_encrypted)

					#Server_symmetric_key
					returnable = str(symmetric_key)
					try:
						msg_encrypted = RSA_encrypt_sign(server_private, client_public, returnable)
					except:
						print("SERVER: ERROR: Message not understood. Exiting...")
						return 1	
					conn.sendall(msg_encrypted)
					data = conn.recv(512)
					try:
						message = RSA_decrypt_sign(server_private, client_public, data)
					except:
						print("SERVER: ERROR: Message not understood. Exiting...")
						return 1
					data = message.split()
					if(len(data) != 1 or data[0] != returnable):
						returnable = "Failure"
					else:
						returnable = "Success"

					#Server_HMAC_key_exchange
					returnable = str(hmac_key)
					try:
						msg_encrypted = RSA_encrypt_sign(server_private, client_public, returnable)
					except:
						print("SERVER: ERROR: Message not understood. Exiting...")
						return 1	
					conn.sendall(msg_encrypted)
					data = conn.recv(512)
					try:
						message = RSA_decrypt_sign(server_private, client_public, data)
					except:
						print("SERVER: ERROR: Message not understood. Exiting...")
						return 1
					data = message.split()
					if(len(data) != 1 or data[0] != returnable):
						returnable = "Failure"
					else:
						returnable = "Success"

					#Server_verify_goodbye
					try:
						msg_encrypted = RSA_encrypt_sign(server_private, client_public, returnable)
					except:
						print("SERVER: ERROR: Message not understood. Exiting...")
						return 1
					conn.sendall(msg_encrypted)
					if(returnable == "Failure"):
						print("SERVER: Fraudulent Behavior. Exiting...")
						return 1
					else:
						print("SERVER: Authenticated.")
						authenticated = True

				else:

					####################
					#BANKING OPERATIONS#
					####################

					data = conn.recv(512)


					if not data:
						break
					data = data.decode('UTF-8', errors = "ignore")
					#print("This is the initially received message:",data)
					returnable = ""
					if not authenticated:
						print(data)
					else:
						
						worked, lis = read_packet(data, symmetric_key, hmac_key)
						if (not worked):
							print("SERVER: Failed to validate mac. Message corruption detected! Closing server...")
							return 0 
						#print(lis)
						if (int(lis[-1]) != time):
							print("SERVER: Repeated message detected, invalid time stamp! Closing server...")
							return 0
						time += 1
						#lis = lis[0].split()

						#print(lis)
						if(lis[0] == "deposit"):
							balance += int(lis[1])
							returnable += "Success "
							returnable += str(balance)
						elif(lis[0] == "withdraw"):
							if(balance - int(lis[1]) < 0):
								returnable += "Warning NEC"
							else:
								balance -= int(lis[1])
								returnable += "Success "
								returnable += str(balance)
						elif(lis[0] == "check"):
							returnable += "Success "
							returnable += str(balance)
						elif(lis[0] == "quit"):
							print("SERVER: Received quit request from ATM. Exiting...")
							returnable += "Quit"
					returnable += " " + str(time)
					returnable += "."
					#print("sending back:", returnable + ".")
					#conn.sendall(returnable.encode("UTF-8", errors = "ignore"))
					conn.sendall(create_packet(returnable, symmetric_key, hmac_key))

if __name__ == "__main__":
	main()