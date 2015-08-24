#!/usr/bin/python3

import socket
import time


class main:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print('Listening....{0}: {1}'.format(HOST,PORT))
    conn, addr = s.accept()
    print('Connected by', addr)
    
    message_dict = 'abcdefghijklmnopqrstuywxyz'
    message = ''
    msg_count = 0
    #MsgLen = 0
    
    for loop in range(4096):
        #time.sleep(0.3)
        message = message + MessageDict[MsgCount]
        send_msg = (message.encode('ascii'))
        conn.sendall(send_msg)
        data = conn.recv(8192)
        #data = (data.encode('ascii'))
        print('Sent {1} bytes'.format(loop))
    
        #print(len(data))
        msg_count += 1 
        #MsgLen = len(send_msg)
    
        if msg_count == 26:
            msg_count = 0
        if send_msg != data:
            print ('received message is wrong!!')
    conn.close()
if __name__== '__main__':
    HOST = '192.168.0.104'
    PORT = 21500
