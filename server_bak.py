#!/usr/bin/python3
#server

import socket
import time

#HOST = '192.168.0.179'    # Symbolic name meaning all available interfaces
#PORT = 21000              # Arbitrary non-privileged port
HOST = 'localhost'
PORT = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)


MessageDict = 'abcdefghijklmnopqrstuywxyz'
message = ''
MsgCount = 0
MsgLen = 0

time.sleep(10)
while MsgLen < 512:
    #time.sleep(0.3)
    message = message + MessageDict[MsgCount]
    SendMsg = (message.encode('ascii'))
    conn.sendall(SendMsg)
    data = conn.recv(1024)
    
    Data = data.find(d'>')
    data = data[Data:]
    #data = (data.encode('ascii'))
    print(data)

    #print(len(data))
    MsgCount += 1 
    MsgLen = len(SendMsg)

    if MsgCount == 26:
        MsgCount = 0
    if SendMsg != data:
        #raise NameError
        print ('received message is wrong!!')
        break
conn.close()
