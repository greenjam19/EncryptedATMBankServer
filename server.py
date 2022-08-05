#server module to act as the bank

#imports
import socket

def main():
	#static variables
	HOST = "127.0.0.1"
	PORT = 65432

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
				print("SERVER: Received", data)
				conn.sendall(data.encode('UTF-8'))

if __name__ == "__main__":
	main()