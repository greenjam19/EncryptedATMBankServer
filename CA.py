#Authority module acting as the certificate distributor

#imports
import socket
import cert

def main():
	#static variables
	HOST = "127.0.0.1"
	PORT = 65433

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			# Using TCP                             ^^^^^^^^
			#Binding to associate socket w/ localhost (127.0.0.1)
			s.bind((HOST, PORT))
			s.listen()

			print("CA: Blocked on accept")
			conn, addr = s.accept()
			with conn:
				print("CA: Connected to", addr, "(localhost)")
				while(1):
					data = conn.recv(512)
					if not data:
						break
					data = data.decode()
					print("CA: Received", data)
					conn.sendall(data.encode("UTF-8"))

	PORT = 65434
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			# Using TCP                             ^^^^^^^^
			#Binding to associate socket w/ localhost (127.0.0.1)
			s.bind((HOST, PORT))
			s.listen()

			print("CA: Blocked on accept")
			conn, addr = s.accept()
			with conn:
				print("CA: Connected to", addr, "(localhost)")
				while(1):
					data = conn.recv(512)
					if not data:
						break
					data = data.decode()
					print("CA: Received", data)
					conn.sendall(data.encode("UTF-8"))

if __name__ == "__main__":
	main()