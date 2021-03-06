#!/usr/bin/python3

import socket
import time
import select
import os
import threading
import builtins
from threading import Barrier
import random
import datetime

class terminal_test:
    def __init__(self):
        self.send_msg_flag = True
        builtins.FileName = time.strftime('%Y-%m-%d-%H%M%S_log')
        builtins.SendMsg_dic = [{} for i in range(number_of_servers)]
        builtins.received_flag = [False for i in range(number_of_servers)]
        builtins.AverageTime = ['' for i in range(number_of_servers)]
        builtins.MaxTime = ['' for i in range(number_of_servers)]
#        builtins.Send_Finished_flag = [False for i in range(number_of_servers)]
        builtins.F = ('log/' + FileName)
        self.B = Barrier(number_of_servers)
        self.received_B = Barrier(number_of_servers)
#        self.Send_B = Barrier(Send_Servers)

        self.main()

    def main(self):
        for i in range(number_of_servers):
            def callback():
                self.stability_test(WAIT, i)
            t = threading.Thread(target=callback)
            t.daemon = True
            t.start()
            builtins.PORT += 1
            time.sleep(0.1)

    def stability_test(self,wait,id_):
        port = PORT
        rece_dict =[set() for i in range(Send_Servers)]
        check_code =[0 for i in range(Send_Servers)]

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, port))
        s.listen(1)

        tempformat = 'Listening....{0}:{1}'.format(HOST, port)
        self.printlog(builtins.F, tempformat)

        conn, addr = s.accept()

        #Display and logging address of connected
        tempformat = '{0} Connected by {1}'.format(port, addr)
        self.printlog(builtins.F, tempformat)

        #Dictionary of testing bytes
        if id_< Send_Servers:
            MessageDict = [chr(i) for i in range(128)]
            del MessageDict[10]
            for i in range(5):
                MessageDict += MessageDict


        #waiting for welcome message and display it
        WaitingForSecond = select.select([conn], [], [], 30)
        if WaitingForSecond[0]:
            StartMsg = conn.recv(4096)
            self.printlog (builtins.F, str(StartMsg))


        #start testing
        self.B.wait()

        def receive_server():

            nonlocal rece_dict
            nonlocal check_code

            while not EXIT_flag:
                try:
                    data = b''
                    try:
                        WaitingForSecond = select.select([conn], [], [], 60)
                    except ValueError:
                        pass

                    try:
                        if WaitingForSecond[0]:
                            data = conn.recv(4096)
                    except OSError:
                        pass

                    if len(data) is 0:
                        break
                    try:
                        send_id = int(chr(data[-8]))
                    except ValueError:
                        send_id = 'unknow'
                    try:
                        loop=data[-7:-1]
                        loop = int(loop)
                    except ValueError:
                        loop = 'unknow'
                    try:
                        received_time = float(data[:6])
                    except ValueError:
                        received_time = 0
                        t = 0.000

                    try:
                        rece_dict[send_id].add(loop)
                        if check_code[send_id] is -1:
                            check_code[send_id] = loop
                    except TypeError:
                        pass

                    try:
                        while len(rece_dict[send_id]) >= 3:
                            time.sleep(0.2)
                            try:
                                rece_dict[send_id].remove(check_code[send_id])
                            except KeyError:
                                self.printlog(builtins.F,'{port}----------{0} {1} has been missed!!--------------------'\
                                              .format(send_id, check_code[send_id]+1, port=port))
                                builtins.Miss[id_] += 1
                            finally:
                                check_code[send_id] += 1

                    except TypeError:
                        pass

#=================================================================
                    if received_time is not 0:
                        t = float(str(time.time())[7:14]) - received_time
                        try:
                            builtins.MaxTime[id_] = max(AverageTime[id_],t)
                            builtins.AverageTime[id_] = (builtins.AverageTime[id_]+t)/2
                        except TypeError :
                            MaxTime[id_] = AverageTime[id_] = t

                    tempformat = "{port} Received {id_} {Loop}: {0}bytes_{1:.3}s".format(len(data),t , port=port, Loop = loop+1, id_=send_id)

                    self.printlog(builtins.F, tempformat)

                    if builtins.SendMsg_dic[send_id].get(loop) != data:
                        tempformat = "-------------------------ERROR-------------------------"
                        self.printlog(builtins.F, tempformat)
                        builtins.Miss[id_] += 1

                    if wait:
                        self.received_B.wait()

                    if send_id == id_:
                        builtins.received_flag[id_] = False

                except ValueError:
                    print('111')
#                    break

            try:
                for i in range(Send_Servers):
                    while len(rece_dict[i]) > 0:
                        try:
                            rece_dict[i].remove(check_code[i])
                        except KeyError:
                            self.printlog(builtins.F,'{port}----------{0} {1} has been missed!!--------------------'\
                                          .format(i, check_code[i]+1, port=port))
                            builtins.Miss[id_] += 1
                        finally:
                            check_code[i] += 1
            except TypeError:
                pass

        tr = threading.Thread(target=receive_server)
        tr.daemon = True
        tr.start()


        if builtins.Disconn:
            self.disconnect(conn, id_)


        if id_< Send_Servers:
            time.sleep(id_*3)

        #for i in range(Loop):
        i = 0
        while i < Loop:
            try:
                if wait:
                    if not tr.is_alive():
                       raise Exception('Thread is crushed')
                    self.B.wait()

                if id_< Send_Servers:

                    _=0
                    while builtins.received_flag[id_]:
                        _ += 1
                        time.sleep(0.1)
                        if _ > 150:
                            builtins.received_flag[id_] = False

                    if wait:
                        Waiting_time = random.randint(0,10)
                        self.printlog(builtins.F, str(i+1) + ' times,  ' + 'wait ' + str(Waiting_time) + 's')
                        time.sleep(Waiting_time)


                    random_bytes = random.randint(min_bytes-15,max_bytes-15)
                    message = random.sample(MessageDict, random_bytes)
                    SendMsg = (
                               (str(time.time())[7:14] +
                               ''.join(message)+ str(id_) +
                                '{0:0>6}'.format(i)+ chr(10))
                              )
                    SendMsg = (SendMsg[:10] + str(len(SendMsg)).zfill(4)+SendMsg[14:]).encode('ascii')
                    conn.sendall(SendMsg)

                    builtins.SendMsg_dic[id_][i] = SendMsg

                    if len(SendMsg_dic[id_]) > 3:
                        del SendMsg_dic[id_][i-3]

                    builtins.received_flag[id_] = True

                    tempformat = '{port} Sent {Loop}: {0}, {1}bytes'.\
                        format(SendMsg[:20], len(SendMsg), Loop = i+1, port=port)
                    self.printlog(builtins.F, tempformat)

                i += 1
                if builtins.EXIT_flag:
                    break
            except OSError:
                if builtins.EXIT_flag:
                    break
                conn.close()
                tempformat = 'Disconnected...{0}:{1}'.format(HOST, port)
                self.printlog(builtins.F, tempformat)
                rece_dict =[set() for i in range(Send_Servers)]
                tempformat = 'Listening....{0}:{1}'.format(HOST, port)
                self.printlog(builtins.F, tempformat)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((HOST, port))
                s.listen(1)
                conn, addr = s.accept()
                tempformat = '{0} Connected by {1}'.format(port, addr)
                self.printlog(builtins.F, tempformat)

                check_code = [-1 for i in range(Send_Servers)]
                time.sleep(1)
                tr = threading.Thread(target=receive_server)
                tr.daemon = True
                tr.start()
                if builtins.Disconn:
                    self.disconnect(conn, id_)

        builtins.Send_Finished_flag[id_] = True

#        if not wait and id_ >= Send_Servers:
        while not builtins.EXIT_flag:
            while tr.is_alive():
                time.sleep(0.1)

            if not builtins.EXIT_flag:
                conn.close()
                tempformat = 'Disconnected...{0}:{1}'.format(HOST, port)
                self.printlog(builtins.F, tempformat)
                tempformat = 'Listening....{0}:{1}'.format(HOST, port)
                self.printlog(builtins.F, tempformat)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((HOST, port))
                s.listen(1)
                conn, addr = s.accept()
                tempformat = '{0} Connected by {1}'.format(port, addr)
                self.printlog(builtins.F, tempformat)

                check_code = [-1 for i in range(Send_Servers)]
                time.sleep(1)
                tr = threading.Thread(target=receive_server)
                tr.daemon = True
                tr.start()

                if builtins.Disconn:
                    self.disconnect(conn,id_)

        time.sleep(5)
        conn.close()
#        if id_< Send_Servers:
#            self.Send_B.wait()
#        builtins.EXIT_flag = True
        self.B.wait()

        tempformat = "\n{Port}\nAverage : {Avg:.3}s\
                          \nMax : {Max:.3}s\
                          \n{Miss} message has been missed"\
                          .format(Avg = AverageTime[id_],\
                                  Max = MaxTime[id_],\
                                  Port=port,\
                                  Miss = Miss[id_])

        self.printlog(builtins.F, tempformat)
#        self.B.wait()
#        while tr.is_alive():
#            time.sleep(0.1)


    def disconnect(self, conn, id_):
        if disconn_field[id_].get().strip():
            def callback():
                discount = 0
                while discount <= int(builtins.disconn_field[id_].get()):
                    time.sleep(1)
                    discount += 1
                conn.close()
            t = threading.Thread(target=callback)
            t.daemon = True
            t.start()

    def printlog(self, filename, Print_format):
        d = datetime.datetime
        t = '[{0:.12}] '.format(d.strftime(d.now(), '%H:%M:%S.%f'))
        filename = open(filename, 'a')
        filename.write(t + Print_format + '\n')
        print(t + Print_format)
        filename.close()

if __name__ == '__main__':
    HOST = '192.168.0.185'
    builtins.PORT = 21000
    Loop = 50          #total testing times
    ReceiveMsgTimeout = 10
    number_of_servers = 5
    min_bytes = 800
    max_bytes = 1024
    terminal_test()

