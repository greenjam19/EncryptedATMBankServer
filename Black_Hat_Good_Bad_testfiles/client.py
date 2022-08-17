import socket
from rsa import RSA, t_to_i, i_to_t
from bitstring import BitArray
from random import randint
from time import sleep
import des
from HMAC import HMAC
import os

with open("tally.txt", "a+") as file:
    num_lines = len(file.readlines())
    file.close()
unchanged_len = num_lines
# verify the hmac
def verify(msg):
    msg = msg.rstrip('\x00').strip().strip('.')
    plain, mac = msg.split("0x")
    return mac == HMAC(plain)

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 1235
    client = socket.socket()
    client.connect((host,port))
    server_public = str(client.recv(1024).decode())
    server_public = server_public.split(',')
    # print("Server Public Key: ",server_public)
    rsa = RSA()
    client_public , client_private = rsa.key_generation()
    msg = str(client_public[0]) + "," +str(client_public[1])
    client.send(msg.encode('ascii'))
    sleep(1)
    # msg = str(client.recv(1024).decode())
    # print("Server encrypt: ", msg)
    while(True):
        msg = "Client: Hi Bob, This is Alice"
        client.send(msg.encode('ascii'))
        sleep(1)
        msg = str(client.recv(1024).decode())
        # print("Msg from server ", msg)
        server_public = tuple([int(x) for x in server_public])
        msg = rsa.public(server_public, rsa.private(client_private, int(msg)))
        try:
            verify(i_to_t(msg))
        except:
            with open("tally.txt", "a+") as file:
                if unchanged_len == len(file.readlines()):
                    file.write("BAD FINISH\n")
                file.close()
            os._exit(0)
        if verify(i_to_t(msg)):
            a = randint(0, 2 ** 192 - 1)
            key = BitArray(uint = a, length=192) # Generating a random key
            msg = str(key.uint)
            msg = msg + '0x' +HMAC(msg) + '.'
            msg = str(rsa.public(server_public, rsa.private(client_private, t_to_i(msg))))
            client.send(msg.encode('ascii'))
            #welcome msg from the bank
            msg = str(client.recv(1024).decode())
            print(msg)
            while(True):
                # Wait on user input
                msg = "Client: "
                msg += "quit"
                #msg += input('Client: ')
                # Encode a message
                msg = msg +'0x'+HMAC(msg)+'.'
                ecb = des.ECB(key)
                msg = ecb.encrypt(msg)
                msg = str(msg.hex)

                client.send(msg.encode('ascii'))
            
                # Wait on response response from server
                msg = str(client.recv(1024).decode())
                last_line = ""
                with open("tally.txt", "a+") as file:
                    if unchanged_len == len(file.readlines()):
                        file.write("GOOD FINISH\n")
                    file.close()
                os._exit(0)
                # Decrypt message from server
                msg = BitArray("0x"+msg)
                ecb = des.ECB(key)
                msg = ecb.decrypt(msg)

                # Verifying message is unaltered
                if not verify(msg):
                    print("Error: Message altered en route session closed")
                    quit()

                # Removing the checksum
                msg = msg.split("0x")[0]

                # Decide what to do based on message
                if(msg == "Please enter correct syntax"):
                    print(msg)
                    quit()
                elif msg == "quit":
                    quit()
                else:
                    print(msg)
        client.close()