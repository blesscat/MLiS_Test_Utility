#!/usr/bin/python3

import socket
import time
import sys

HOST = '192.168.0.179'   # The remote host
PORT = int(sys.argv[1])       # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((HOST, PORT))
s.sendall(b'Hi')
#while i < 5
while True:
    #s.sendall(b'Hello, world')
    #data = s.recv(1024)
    #print(data)
    print(s.recv(100))


    time.sleep(1)
    #Data = b'3123123123123123>' + data
    Data = b'123>this is a loop test'
    print(Data)
    s.sendall(Data)
    #i += 1
    #s.close()
    #print('Received', repr(data))
time.sleep(20)
