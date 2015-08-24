#!/usr/bin/python3

import socket
import time
import select
import os

HOST = '192.168.0.179'
PORT = 21000
TestLen = 512            #total testing times
ReceiveMsgTimeout = 20

#Create Socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 21000))
#s.listen(1)
#conn, addr = s.accept()

#Create LOG
FileName = time.strftime('%Y-%m-%d-%H%M%S_log')
f = open('log' + '/' + FileName, 'w')

#Display and logging address of connected
#f.write('Connected by' + str(addr) + '\n')
#print('Connected by', addr)

#Varible for counting Miss message
Variable = {}
#for Calculating receive interval
RInterval = []
#for Calcilat Average of reveive interval
AverageTime = []
#Dictionary of testing bytes
MessageDict = 'abcdefghijklmnopqrstuvwxyz'
#for sending message
message = ''
MsgCount = 0
MsgLen = 0

#waiting for welcome message and display it
while True:
    msg, (addr, port) = s.recvfrom(100)
    print (msg, (addr, port))
    s.sendto(b'hey!\n', ('', 21000))
    time.sleep(2)


