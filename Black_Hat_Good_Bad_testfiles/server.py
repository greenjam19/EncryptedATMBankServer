import socket
from client import verify
from rsa import RSA, t_to_h, t_to_i, i_to_t, i_to_h, h_to_t
from bitstring import BitArray
from time import sleep
import des
from HMAC import HMAC
import os

with open("tally.txt", "a+") as file:
    num_lines = len(file.readlines())
    file.close()
unchanged_len = num_lines

# Encrypts a plaintext using des ecb, returns the message as a str
def encrypt(msg : str, key) -> str:
    print(msg)
    msg = msg +'0x'+HMAC(msg)+'.'
    ecb = des.ECB(key)
    msg = ecb.encrypt(msg)
    msg = str(msg.hex)

    return msg

# verify the hmac
def verify(msg):
    msg = msg.rstrip('\x00').strip().strip('.')
    plain, mac = msg.split("0x")
    return mac == HMAC(plain)

    
if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 1235
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    #generate server public key 
    rsa = RSA()
    server_public , server_private = rsa.key_generation()
    
    balance = 0
    while True:
        client, address = server.accept()
        print('Welcome', address)
        #generate server public key 
        msg = str(server_public[0]) + "," +str(server_public[1])
        client.send(msg.encode('ascii'))
        
        #getting public key
        msg = client.recv(1024).decode()
        client_public = msg.split(',')
        # print("Client Public Key: ", client_public)
        #getting this is alice
        msg = client.recv(1024).decode() 
        print(msg)

        #Starting key exchange
        msg = "Client this is server"
        client_public = tuple([int(x) for x in client_public])
        msg = msg+'0x'+HMAC(msg)+'.'
        msg = str(rsa.public(client_public, rsa.private(server_private, t_to_i(msg))))
        client.send(msg.encode('ASCII'))
        sleep(1)
        #get 3des key from client
        msg = client.recv(1024).decode()
        try:
            msg = rsa.public(client_public, rsa.private(server_private, int(msg)))
            verify(i_to_t(msg))
        except:
            with open("tally.txt", "a+") as file:
                if unchanged_len == len(file.readlines()):
                    file.write("BAD FINISH\n")
                file.close()
            os._exit(0)
        if verify(i_to_t(msg)):
            msg = i_to_t(msg)
            msg = msg.split("0x")[0]
            key = BitArray(hex(int(msg)))
            
            msg = "Welcome To The Bank\n 1. Deposit, 2. Withdraw, 3. Check Balance \n | Deposit format: deposit 100   | \n | Withdraw format: withdraw 100 | \n | Check Balance format: check   | \n | Quit: quit                    |"
            client.send(msg.encode('ascii'))
            while True:
                # Decrypting a message using 3des ecb
                msg = client.recv(1024).decode()
                msg = BitArray("0x"+msg)
                try:
                    ecb = des.ECB(key)
                except:
                    with open("tally.txt", "a+") as file:
                        if unchanged_len == len(file.readlines()):
                            file.write("BAD FINISH\n")
                        file.close()
                    os._exit(0)
                msg = ecb.decrypt(msg)

                # Verifying message is unaltered
                if not verify(msg):
                    print("Error: Message altered en route session closed")
                    quit()

                # Remove the checksum
                msg = msg.split("0x")[0]

                print(msg)

                split_msg = msg.split()
                if split_msg[1] == "deposit":
                    msg = "Server: Now you have"
                    if int(split_msg[2].rstrip('\x00')) <=0:
                        msg = "Server: Need to be greater than 0"
                        msg = encrypt(msg, key)
                        client.send(msg.encode('ascii'))
                    else:
                        balance += int(split_msg[2].rstrip('\x00'))
                        msg = "Server: Now you have "+ str(balance)+" in your account"
                        msg = encrypt(msg, key)
                        client.send(msg.encode('ascii'))
                elif split_msg[1] == "withdraw":
                    if balance >= int(split_msg[2].rstrip('\x00')):
                        if int(split_msg[2].rstrip('\x00')) <=0:
                            msg = "Server: Need to be greater than 0"
                            msg = encrypt(msg, key)
                            client.send(msg.encode('ascii'))
                        else:
                            balance -= int(split_msg[2].rstrip('\x00'))
                            msg = "Server: You just withdraw "+ str(split_msg[2].rstrip('\x00')) +" dollar. Now you have "+ str(balance)+" in your account."
                            msg = encrypt(msg, key)
                            client.send(msg.encode('ascii'))
                    else:
                        msg = "Server: You have insufficient amount of money"
                        msg = encrypt(msg, key)
                        client.send(msg.encode('ascii'))
                elif split_msg[1].rstrip('\x00') == "check":
                    msg = "Server: Now you have "+ str(balance)+" in your account"
                    msg = encrypt(msg, key)
                    client.send(msg.encode('ascii'))
                elif split_msg[1].rstrip('\x00') == "quit":
                    msg = "Server: quit"
                    msg = encrypt(msg, key)
                    client.send(msg.encode('ascii'))
                    quit()
                else:
                    msg = "Server: Please enter correct syntax"
                    msg = encrypt(msg, key)
                    client.send(msg.encode('ascii'))
                    quit()
                # msg = "Server: "
                # msg += input('Server: ')
                # client.send(msg.encode('ascii'))
        else:
            print("Error msg input")