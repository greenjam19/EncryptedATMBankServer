#server module to act as the bank

#imports
import socket

def main():
	#static variables
	HOST = "127.0.0.1"
	PORT = 42069

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
			print("SERVER: Connected to {}", addr)
			while(1):
				data = conn.recv(512)
				if(!data):
					break
				print("SERVER: Received {}", data)
				conn.sendall(data)