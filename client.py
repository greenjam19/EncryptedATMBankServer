#Client module acting as the ATM

#imports
import socket

def main():
	# static variables
	HOST = "127.0.0.1"
	PORT = 65432

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		# Entering a loop where we will continually communicate
		# w/ the bank
		while(1):
			# Use sendall to send messages to server (bank)
			print("USAGE: <Withdraw/Deposit/Check/Quit>")
			print("")
			message = input("What would you like to do?\n")
			s.sendall(message.encode('UTF-8'))
			data = s.recv(512).decode()
			print("Received", data)

if __name__ == "__main__":
	main()