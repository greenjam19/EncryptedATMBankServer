#server module to act as the bank

#imports
import socket
import os
import random

def main():
	#static variables
	HOST = "127.0.0.1"
	PORT = 65432


	# non-static variables
	balance = 0
	authenticated = False

	#######
	#SETUP#
	#######
	with open("privatekey.txt", "r") as f:
		lines = f.readlines()
		d = int(lines[0])
		p = int(lines[1])
		q = int(lines[2])
		# PRIVATE KEY: {d, p, q}
		server_private = (d, p, q)

	with open("publickey.txt", "r") as f:
		lines = f.readlines()
		e = int(lines[0])
		N = int(lines[1])
		# PUBLIC KEY: {e, N}
		client_public = (e, N)


	####################
	#BANKING OPERATIONS#
	####################

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
					returnable = ""
					#Client_hello
					data = conn.recv(512).decode().split()
					if(data[0] != "Hello" or data[1] != "TLS" or data[2] \
						!= "RSA" or data[3] != "DES"):
						returnable += "Failure"
					else:
						returnable += "Success"
					#Server_hello
					conn.sendall(returnable.encode("UTF-8"))

					#Server_symmetric_key
					returnable = str(random.getrandbits(192))
					conn.sendall(returnable.encode("UTF-8"))

					data = conn.recv(512).decode().split()
					if(data[0] != returnable):
						returnable = "Failure"

					else:
						returnable = "Success"
					#Server_verify_goodbye
					conn.sendall(returnable.encode("UTF-8"))
					if(returnable == "Failure"):
						print("SERVER: Fraudulent Behavior. Exiting...")
						return 1
					else:
						authenticated = True

				else:
					data = conn.recv(512)
					if not data:
						break
					data = data.decode()
					lis = data.split()
					returnable = ""
					if not authenticated:
						print(lis[0])
					else:
						if(lis[0] == "quit"):
							print("SERVER: Received quit request from ATM. Exiting...")
							returnable += "Quit"
						else:
							print("SERVER: Received", data)
							if(lis[0] == "deposit"):
								balance += int(lis[1])
								returnable += "Success "
								returnable += str(balance)
							elif(lis[0] == "withdraw"):
								if(balance - int(lis[1]) < 0):
									print("WARNING: Not enough capital in account to make withdrawl")
									returnable += "Warning NEC"
								else:
									balance -= int(lis[1])
									returnable += "Success "
									returnable += str(balance)
							elif(lis[0] == "check"):
								print("SERVER: Client has", balance, "dollars remaining in account")
								returnable += "Success "
								returnable += str(balance)
						conn.sendall(returnable.encode("UTF-8"))

if __name__ == "__main__":
	main()