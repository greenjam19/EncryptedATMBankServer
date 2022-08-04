#server module to act as the bank

#imports
import socket

def main():
	#static variables
	HOST = "127.0.0.1"
	PORT = 65432

	with socket.socket