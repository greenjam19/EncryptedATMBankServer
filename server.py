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
from RSA import RSA_encrypt_sign, RSA_decrypt_sign

def main():
	#static variables
	HOST = "127.0.0.1"
	PORT = 65432


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
					print("This is the initially received message:",data)
					lis = data.split()
					returnable = ""
					if not authenticated:
						print(lis[0])
					else:
						if(lis[0] == "quit"):
							print("SERVER: Received quit request from ATM. Exiting...")
							returnable += "Quit"
						else:
							decoded_mess = decodeTripleDES(makeBlocks(lis[0],64), BitArray(uint = symmetric_key, length = 192))
							ptext_mess = blocksToString(decoded_mess)
							print("SERVER: Received", ptext_mess)
							lis = ptext_mess.split('.')
							print("This is the transmission:", lis[0])
							m = makeBlocks(lis[0].lower() + '.',1)
							bit_m = ""
							for i in range(len(m)):
								bit_m += m[i].bin

							message_hmac = HMAC(bit_m, hmac_key)
							print("This is message_hmac:",message_hmac,"and this is lis[1]:", lis)
							print("Hashing this value:", bit_m,"with this key:",hmac_key)
							worked = True
							for i in range(len(message_hmac)):	
								if message_hmac[i] != lis[1][i]:
									print("SERVER: Received invalid MAC.")
									worked = False
									break
							if worked == False:
								continue
							lis = lis[0].split()
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
						conn.sendall(returnable.encode("UTF-8", errors = "ignore"))

if __name__ == "__main__":
	main()