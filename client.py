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

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Authentication steps
		s.connect((HOST, PORT))
		
		
		# Entering a loop where we will continually communicate
		# w/ the bank
		while(1):
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
			data = s.recv(512).decode()
			if(data == "Quit"):
				break
			print("Received", data)

if __name__ == "__main__":
	main()