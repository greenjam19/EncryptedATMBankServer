#server module to act as the bank

#imports
import socket

def main():
	#static variables
	HOST = "127.0.0.1"
	PORT = 65432

	# non-static variables
	balance = 0

	# No need to call s.close() here, as everything is done in a with
	# statement
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Using TCP                             ^^^^^^^^
		#Binding to associate socket w/ localhost (127.0.0.1)
		s.bind((HOST, PORT))
		s.listen()

		print("SERVER: Blocked on accept")
		conn, addr = s.accept()
		with conn:
			print("SERVER: Connected to", addr, "(localhost)")
			while(1):
				data = conn.recv(512)
				if not data:
					break
				data = data.decode()
				lis = data.split()
				returnable = ""
				if(lis[0] == "quit"):
					print("SERVER: Received quit request from ATM. Exiting...")
					returnable += "Quit"
				else:
					print("SERVER: Received", data)
					if(lis[0] == "deposit"):
						balance += int(lis[1])
						returnable += "Success"
					elif(lis[0] == "withdraw"):
						if(balance - int(lis[1]) < 0):
							print("WARNING: Not enough capital in account to make withdrawl")
							returnable += "Warning"
						else:
							balance +- int(lis[1])
							returnable += "Success"
					elif(lis[0] == "check"):
						print("SERVER: Client has", balance, " dollars remaining in account")
						returnable += "Success"
				conn.sendall(returnable.encode("UTF-8"))

if __name__ == "__main__":
	main()