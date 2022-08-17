# Cryptography Final Project

## Usage

To use the system you start by opening a terminal and typing ```python server.py```. You then start the client by running ```python client.py```. When stopping the client and server make sure you stop the client first otherwise there might be a message next time you start saying the port is in use. To avoid this simply change the port in the file.

On starting the application, the client and the server will initiate a handshake to exchange the session key. On certain runs you may encounter an error with an improperly decrypted key due to the use of the BitArray library. If this scenrio is enocountered simply start the server and client once more.

## File Structure

* client.py: The driver code for the TCP client
* server.py: The driver code for the TCP server
* des.py: Implementation of the des cipher as well as cipher modes
* des_testing.py: A script to test the accuracy of the 3des cipher
* rsa.py: A file containing the implementation of the rsa cipher
* sha1.py: A file containing the hashing algorithm
* HMAC.py: A file containing the HMAC algorithm

## Dependencies

Python 3.9.x

To run all parts of the project you must have the following libraries:
* bitstring
* pycryptodome

documentation for these can be found here:
* https://bitstring.readthedocs.io/en/latest/contents.html
* https://www.pycryptodome.org/src/api