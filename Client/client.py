#Client module acting as the ATM

#imports
import socket

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

	#######
	#SETUP#
	#######
	with open("publickey.txt", "r") as f:
		lines = f.readlines()
		e = int(lines[0])
		N = int(lines[1])
		# PUBLIC KEY: {e, N}
		server_public = (e, N)

	with open("privatekey.txt", "r") as f:
		lines = f.readlines()
		d = int(lines[0])
		p = int(lines[1])
		q = int(lines[2])
		# PRIVATE KEY: {d, p, q}
		client_private = (d, p, q)

	###################
	#BAKING OPERATIONS#
	###################

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Authentication steps
		s.connect((HOST, PORT))
		
		
		# Entering a loop where we will continually communicate
		# w/ the bank
		while(1):
			if not authenticated:
				# Client_hello
				# Usage <Hello/TLS/RSA/DES
				s.sendall(b"Hello TLS RSA DES")

				# Server_hello
				data = s.recv(512).decode().split()
				if(data[0] != "Success"):
					print("ERROR: Incompatable securities. Exiting...")
					return 1
				print("CLIENT: Established security capabilities")

				# Server_key_exchange
				data = s.recv(512).decode().split()
				print("CLIENT: Received symmetric key", data[0])

				# Client_key_auth
				s.sendall(data[0].encode("UTF-8"))

				#Server_verify_goodbye
				data = s.recv(512).decode().split()
				if(data[0] != "Success"):
					print("ERROR: Fraudulent messaging detected. Exiting...")
					return 1
				print("CLIENT: Authenticated")
				authenticated = True

			else:
				# Use sendall to send messages to server (bank)
				print("USAGE: <Withdraw/Deposit/Check/Quit>")
				print("")
				message = input("What would you like to do?\n").lower()
				transmission = ""
				if(message == "check"):
					print("CLIENT: Requested balance check")
					transmission += "check "
				elif(message == "deposit"):
					print("CLIENT: Requested money deposit")
					transmission += "deposit "
					amount, is_int = check_int("deposit")
					if not is_int:
						print("WARNING: Please enter an integer value")
						continue
					transmission += amount
				elif(message == "withdraw"):
					print("CLIENT: Requested money withdraw")
					transmission += "withdraw "
					amount, is_int = check_int("withdraw")
					if not is_int:
						print("WARNING: Please enter an integer value")
						continue
					transmission += amount
				elif(message == "quit"):
					print("CLIENT: Atm requested quit. Exiting...")
					transmission += "quit"
				else:
					print("WARNING: Unrecognized command")
					continue

				s.sendall(transmission.lower().encode('UTF-8'))
				data = s.recv(512).decode().split()
				if(data[0] == "Quit"):
					break
				elif(data[0] == "Warning"):
					print("Received", data[0])
					if(data[1] == "NEC"):
						print("Client has insifficient capital to complete this withdrawl")
				else:
					print("Received", data[0])
					print("Client has", data[1], "dollars remaining in account")

	return 0
if __name__ == "__main__":
	main()