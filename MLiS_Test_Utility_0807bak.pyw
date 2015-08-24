#!/usr/bin/python3

import tkinter as tk
from tkinter import BooleanVar, StringVar, ttk
import sys
import threading
import builtins
import socket
import time
import datetime
import queue
import serial

class GUI_APP(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self, className=' MLiS_Test_Utility__201500807')
        self.q = queue.Queue(20)
#set sys.stdout and sys.stderr to function 'Textredirector'
        self.main()
#        sys.stdout = TextRedirector(self.text, "stdout")
        sys.stdout = put_queue(self.q,"stdout")
        sys.stderr = TextRedirector(self.text, "stderr")


    def main(self):
        self.frame_toolbar()
        self.text_frame()
        self.sydout_text()
        self.serial_output_frame()
        self.client_output_frame()

        def callback():
            while True:
                data=self.q.get()
                self.text.configure(state="normal")
                if self.scrl.get()[1] == 1.0:
                    self.text.insert("end", data)
                    self.text.see("end")
                else:
                    self.text.insert("end", data)
                self.text.configure(state="disabled")
        t = threading.Thread(target=callback)
        t.daemon = True
        t.start()


    def frame_toolbar(self):
#Create a toolbar and pack it to the TOP.
        toolbar = ttk.Labelframe(self)
        toolbar.pack(side="top", fill="x")

        self.memo_text = ttk.Entry(self, width = 20, justify='center')
        self.memo_text.pack(in_=toolbar, side='top', fill='x', pady = 10)

        self.radiobar = tk.Frame()
        self.radiobar.pack(in_=toolbar, side='bottom', fill = 'x')

#Create a Label 'HOST :'.
        host_text = ttk.Label(self, text="HOST :")

#Create a combox, and get IP from function 'get_ip'.
        self.host_box_value = StringVar()
        self.host_box = ttk.Combobox(self, textvariable=self.host_box_value)
        self.host_box['values'] = self.get_ip()
        self.host_box.current(0)

#Create a Label 'PORT :'.
        port_text = ttk.Label(self, text="PORT :")

#Create a Enter Field for 'port', and set default 21000.
        self.port_field = ttk.Entry(self, width=7)
        self.port_field.insert(0,21000)

#Creatr a Label 'Test Length :'.
        Loop_text = ttk.Label(self, text="Loop :")

#Create a Enter Field for 'port', and set default 512.
        self.Loop_field = ttk.Entry(self, width=7)
        self.Loop_field.insert(0,500)

#Create a Label 'Timeout(sec) :'.
        timeout_text = ttk.Label(self, text="TimeOut(sec) :")

#Create a Enter Field for 'timeout', and set default 3.
        self.timeout_field = ttk.Entry(self, width=4)
        self.timeout_field.insert(0,10)

        number_of_servers_text = ttk.Label(self, text="Number of Servers :")
        self.number_of_servers_field = ttk.Entry(self, width=3)
        self.number_of_servers_field.insert(0,5)

        Send_Servers_text = ttk.Label(self, text="Servers of send :")
        self.Send_Servers_field = ttk.Entry(self, width=3)
        self.Send_Servers_field.insert(0,1)

        min_bytes_text = ttk.Label(self, text="Min Bytes :")
        self.min_bytes_field = ttk.Entry(self, width=6)
        self.min_bytes_field.insert(0,500)

        max_bytes_text = ttk.Label(self, text="Max Bytes :")
        self.max_bytes_field = ttk.Entry(self, width=6)
        self.max_bytes_field.insert(0,1024)

        self.radio = BooleanVar(value='True')
        self.stability = ttk.Radiobutton(self, text='Stability Test', \
                                             variable=self.radio, \
                                             value='True')
        self.stress = ttk.Radiobutton(self, text='Stress Test', \
                                             variable=self.radio, \
                                             value='False')
        #self.stability.state(['selected'])
        self.disconn_var = BooleanVar()
        #self.send_var.set(False)
        self.disconn_checkbox = ttk.Checkbutton(self, text = "Disconnect  ", variable=self.disconn_var\
                                               , onvalue='True', offvalue='False', command=self.disconn_function)
        #nonsend_check_button.state(['selected'])

#Create 'Start' and 'clear' button.
        self.bstart = ttk.Button(self, text="START",width=10, command=self.bstart_test_button)
        bstop = ttk.Button(self, text="STOP",width=10, command=self.stop_button)
        bclear = ttk.Button(self, text="CLEAR",width=10, command=self.clear_button)
        btest = ttk.Button(self, text="TEST",width=10, command=self.test_button)

#pack all of component in the 'toolbar' field,begining from left.

        host_text.pack(in_=toolbar, side="left")
        self.host_box.pack(in_=toolbar, side="left")

        port_text.pack(in_=toolbar, side="left")
        self.port_field.pack(in_=toolbar, side="left")

        Loop_text.pack(in_=toolbar, side="left")
        self.Loop_field.pack(in_=toolbar, side="left")

#        timeout_text.pack(in_=toolbar, side="left")
#        self.timeout_field.pack(in_=toolbar, side="left")

        number_of_servers_text.pack(in_=toolbar, side="left")
        self.number_of_servers_field.pack(in_=toolbar, side="left")

        Send_Servers_text.pack(in_=toolbar, side="left")
        self.Send_Servers_field.pack(in_=toolbar, side="left")

        min_bytes_text.pack(in_=toolbar, side="left")
        self.min_bytes_field.pack(in_=toolbar, side="left")

        max_bytes_text.pack(in_=toolbar, side="left")
        self.max_bytes_field.pack(in_=toolbar, side="left")

        self.stability.pack(in_=self.radiobar, side="left",padx = 40, pady = 3)
        self.stress.pack(in_=self.radiobar, side="left",padx = 40, pady = 3)
        self.disconn_checkbox.pack(in_=self.radiobar, side='left')

#pack bottom in the 'toolbar' field, begining from right.
        btest.pack(in_=self.radiobar, side="right")
        bclear.pack(in_=self.radiobar, side="right")
        bstop.pack(in_=self.radiobar, side="right")
        self.bstart.pack(in_=self.radiobar, side="right")

    def text_frame(self):
        self.text_frame=tk.Frame()
        self.text_frame.pack(side='top', fill='both',expand=True)

    def sydout_text(self):
#Create a 'textpad' frame and scrollable text, and pack them.
        textpad=ttk.Labelframe(text='Output')
        textpad.pack(in_=self.text_frame, side='left', fill="both", expand=True)
        self.text = tk.Text(textpad, wrap="word",font='calibri', state='disabled', width = 60)#disabled')
        self.text.tag_configure("stderr", foreground="#b22222")
        self.scrl = ttk.Scrollbar(textpad, command=self.text.yview)
        self.text.config(yscrollcommand=self.scrl.set)
        self.scrl.pack(in_=textpad, side="right", fill="y")
        self.text.pack(in_=textpad, side="left", fill="both", expand=True)

    def serial_output_frame(self):
#Create a 'textpad' frame and scrollable text, and pack them.
        serial_pad=ttk.Labelframe(text='Serial Output')
        serial_pad.pack(in_=self.text_frame,anchor='ne', fill="both", expand=True)

        serial_textpad=tk.Frame()
        serial_textpad.pack(in_=serial_pad, side='top', fill="both", expand=True)
        self.serial_text = tk.Text(wrap="word", font='Calibri', state='normal', height=12, width=80)
        #self.serial_text.tag_configure("stderr", foreground="#b22222")
        self.serial_scrl = ttk.Scrollbar(command=self.serial_text.yview)
        self.serial_text.config(yscrollcommand=self.serial_scrl.set)
        self.serial_text.pack(in_=serial_textpad, side="left", fill="both", expand=True)
        self.serial_scrl.pack(in_=serial_textpad, side="right", fill="y")

        serial_toolbar = tk.Frame()
        serial_toolbar.pack(in_=serial_pad, side="bottom", fill="x", expand=True)

        serial_label = ttk.Label(self, text="Serial :")

        self.serial_label_field = ttk.Entry(self, width=7)
        self.serial_label_field.insert(0,'COM1')

        serial_baud_rate = ttk.Label(self, text="Baud Rate :")

        self.serial_baud_rate_field = ttk.Entry(self, width=7)
        self.serial_baud_rate_field.insert(0,115200)

        serial_label.pack(in_=serial_toolbar, side="left")
        self.serial_label_field.pack(in_=serial_toolbar, side="left")
        serial_baud_rate.pack(in_=serial_toolbar, side="left")
        self.serial_baud_rate_field.pack(in_=serial_toolbar, side="left")

        serial_bclear = ttk.Button(self, text="CLEAR",width=7, command=self.serial_output_clear)
        serial_bclear.pack(in_=serial_toolbar, side="right")

        serial_bclose = ttk.Button(self, text="CLOSE",width=7, command=self.serial_output_close)
        serial_bclose.pack(in_=serial_toolbar, side="right")

        serial_bopen = ttk.Button(self, text="OPEN",width=7, command=self.serial_output_open)
        serial_bopen.pack(in_=serial_toolbar, side="right")

#    def leftClick(self,event):
#        print("test")

    def client_output_frame(self):
#Create a 'textpad' frame and scrollable text, and pack them.
        client_pad=ttk.Labelframe(text='Client Output')
        client_pad.pack(in_=self.text_frame, anchor='se', fill="both", expand=True)

        client_textpad=tk.Frame()
        client_textpad.pack(in_=client_pad, side='top', fill="both", expand=True)
        self.client_text = tk.Text(wrap="word",font='Calibri', state='normal', height=12, width=80)
        #self.client_text.tag_configure("stderr", foreground="#b22222")
        self.client_scrl = ttk.Scrollbar(command=self.client_text.yview)
        self.client_text.config(yscrollcommand=self.client_scrl.set)
        self.client_text.pack(in_=client_textpad, side="left", fill="both", expand=True)
        self.client_scrl.pack(in_=client_textpad, side="right", fill="y")

#        self.client_text.bind("<Button-1>", self.leftClick)

        client_toolbar = tk.Frame()
        client_toolbar.pack(in_=client_pad, side="bottom", fill="x", expand=True)

        client_label = ttk.Label(self, text="Serial :")

        self.client_label_field = ttk.Entry(self, width=7)
        self.client_label_field.insert(0,'COM1')

        self.client_baud_rate = ttk.Label(self, text="Baud Rate :")

        self.client_baud_rate_field = ttk.Entry(self, width=7)
        self.client_baud_rate_field.insert(0,115200)

        client_label.pack(in_=client_toolbar, side="left")
        self.client_label_field.pack(in_=client_toolbar, side="left")
        self.client_baud_rate.pack(in_=client_toolbar, side="left")
        self.client_baud_rate_field.pack(in_=client_toolbar, side="left")

        client_bclear = ttk.Button(self, text="CLEAR",width=7, command=self.client_output_clear)
        client_bclear.pack(in_=client_toolbar, side="right")

        client_bclose = ttk.Button(self, text="CLOSE",width=7, command=self.client_output_close)
        client_bclose.pack(in_=client_toolbar, side="right")

        client_bopen = ttk.Button(self, text="OPEN",width=7, command=self.client_output_open)
        client_bopen.pack(in_=client_toolbar, side="right")

        self.send_var = BooleanVar()
        #self.send_var.set(False)
        send_check_button = ttk.Checkbutton(self, text = "Send Back", variable=self.send_var\
                                               , onvalue='True', offvalue='False')
        send_check_button.pack(in_=client_toolbar, side='left')
        #nonsend_check_button.state(['selected'])

    def bstart_test_button(self):
#set Variable to built in, let other module can use that.
        self.bstart.configure(state='disabled')
        builtins.HOST = self.host_box.get()
        builtins.PORT = int(self.port_field.get())
        builtins.Loop = int(self.Loop_field.get())
        builtins.ReceiveMsgTimeout = int(self.timeout_field.get())
        builtins.number_of_servers = int(self.number_of_servers_field.get())
        builtins.Send_Servers = int(self.Send_Servers_field.get())
        builtins.min_bytes = int(self.min_bytes_field.get())
        builtins.max_bytes = int(self.max_bytes_field.get())
        builtins.WAIT = self.radio.get()
        builtins.Disconn = self.disconn_var.get()
        if builtins.Disconn:
            builtins.disconn_field = self.disconn_field

        builtins.EXIT_flag = False
        builtins.Send_Finished_flag = [False for i in range(number_of_servers)]
        self.statusbar()
        def callback():
#import server.py
            import server
            s = server
            s.terminal_test()
#thrading server.py
        t = threading.Thread(target=callback)
#set daemon
        t.daemon = True
        t.start()

    def disconn_function(self):
        if self.disconn_var.get():
            self.disconn_text = []
            self.disconn_field = []
            self.disconn_frame = tk.Frame()
            self.disconn_frame.pack(in_=self.radiobar, side="left")
            for i in range(int(self.number_of_servers_field.get())):
                self.disconn_text.append(ttk.Label(self, text=str(i) +" :"))
                self.disconn_field.append(ttk.Entry(self, width=5))
                self.disconn_text[i].pack(in_=self.disconn_frame, side = 'left')
                self.disconn_field[i].pack(in_=self.disconn_frame, side = 'left')
        #        self.number_of_servers_field = ttk.Entry(self, width=3)
        #    self.top = tk.Toplevel()
        #    self.top.title('test')
        #    msg = tk.Message(self.top, text= 'about_message')
        #    msg.pack()

        #    button = tk.Button(self.top, text="Close", command=self.top.destroy)
        #    button.pack()
        else:
            self.disconn_frame.destroy()

    def test_button(self):
        print(builtins.SendMsg_dic)

#call function 'Textredirector.Clear'
    def stop_button(self):
        self.bstart.configure(state='enable')
        builtins.EXIT_flag = True
#        del builtins.SendMsg_dic

    def clear_button(self):
        self.text.configure(state="normal")
        self.text.delete('1.0', 'end')
        self.text.configure(state="disabled")
#        try:
#            for i in range(number_of_servers):
#                try:
#                    Connected[i].close()
#                    time.sleep(0.1)
#                except IndexError:
#                    pass
#                sys.stdout.clear()
#        except NameError:
#            sys.stdout.clear()

#use socket to get ip of all in this computer and return that.
    def get_ip(self):
        ip_list = socket.gethostbyname_ex(socket.gethostname())
        ip_list = ip_list[2]
        return ip_list

    def serial_output_open(self):
        try:
            com_port = self.serial_label_field.get()
            baud_rate = self.serial_baud_rate_field.get()
            filename = time.strftime('%Y-%m-%d-%H%M%S-log_' + com_port)
            #self.serial_text.insert("end", 'connected '+ com_port)
            com_port = int(com_port[3:]) - 1
            self.ser = serial.Serial(com_port, baud_rate)
            d = datetime.datetime
            self.serial_text.configure(state="normal")
            self.serial_text.insert("end", 'Opening {0} {1}\n'.\
                 format(self.serial_label_field.get(), self.serial_baud_rate_field.get()))
            self.serial_text.configure(state="disabled")

            def callback():
                try:
                    while True:
                        line = self.ser.readline()
                        t = '[{0:.12}] '.format(d.strftime(d.now(), '%H:%M:%S.%f'))
                        #t = t.encode('ascii')
                        temp_format = '{0} {1}\n'.format(t, str(line))

                        f = open('log/com/' + filename, 'a+')
                        f.write(temp_format)
                        f.close()

                        self.serial_text.configure(state="normal")
                        if self.serial_scrl.get()[1] == 1.0:
                            self.serial_text.insert("end", temp_format)
                            self.serial_text.see("end")
                        else:
                            self.serial_text.insert("end", temp_format)
                        self.serial_text.configure(state="disabled")
                except :
                    pass
            t = threading.Thread(target=callback)
            t.daemon = True
            t.start()

        except OSError:
            self.serial_text.configure(state="normal")
            self.serial_text.insert("end", '{0} IS NOT EXISTING OR HAS BEEN OPENED\n'.\
                              format(self.serial_label_field.get()))
            self.serial_text.configure(state="disabled")

    def serial_output_clear(self):
        self.serial_text.configure(state="normal")
        self.serial_text.delete('1.0', 'end')
        self.serial_text.configure(state="disabled")

    def serial_output_close(self):
        self.ser.close()
        self.serial_text.configure(state="normal")
        self.serial_text.insert('end', '{0} has been closed'.format(self.serial_label_field.get()))
        self.serial_text.configure(state="disabled")


    def client_output_open(self):
        try:
        #    self.client_close_flag = False
            com_port = self.client_label_field.get()
            baud_rate = self.client_baud_rate_field.get()
            filename = time.strftime('%Y-%m-%d-%H%M%S-log_' + com_port)
            #self.client_text.insert("end", 'connected '+ com_port)
            com_port = int(com_port[3:]) - 1
            self.ser2 = serial.Serial(com_port, baud_rate)
            d = datetime.datetime
            self.client_text.configure(state="normal")
            self.client_text.insert("end", 'Opening {0} {1}\n'.\
                 format(self.client_label_field.get(), self.client_baud_rate_field.get()))
            self.client_text.configure(state="disabled")

            def callback():
                try:
                    while True:
                        line = self.ser2.readline()
                        t = '[{0:.12}] '.format(d.strftime(d.now(), '%H:%M:%S.%f'))
                        if self.send_var.get():
                            def wait_send_back():
                                try:
                                    time.sleep(0.1)
                                    self.ser2.write(line)
                                except:
                                    pass
                            th_1 = threading.Thread(target=wait_send_back)
                            th_1.daemon = True
                            th_1.start()
                            #t = t.encode('ascii')
                            temp_format ='{0} {1}_{2}bytes\n'.format(t, str(line), len(line))
                        else:
                            temp_format ='{0} {1}\n'.format(t, str(line))

                        f = open('log/com/' + filename, 'a+')
                        f.write(temp_format)
                        f.close()

                        self.client_text.configure(state="normal")
                        if self.client_scrl.get()[1] == 1:
                            self.client_text.insert("end", temp_format)
                            self.client_text.see("end")
                        else:
                            self.client_text.insert("end", temp_format)
                        self.client_text.configure(state="disabled")
                except :
                    pass
            t = threading.Thread(target=callback)
            t.daemon = True
            t.start()

        except OSError:
            self.client_text.configure(state="normal")
            self.client_text.insert("end", '{0} IS NOT EXISTING OR HAS BEEN OPENED\n'.\
                              format(self.client_label_field.get()))
            self.client_text.configure(state="disabled")

    def client_output_clear(self):
        self.client_text.configure(state="normal")
        self.client_text.delete('1.0', 'end')
        self.client_text.configure(state="disabled")

    def client_output_close(self):
        #self.client_close_flag = True
        self.ser2.close()
        self.client_text.configure(state="normal")
        self.client_text.insert('end', '{0} has been closed'.format(self.client_label_field.get()))
        self.client_text.configure(state="disabled")

    def statusbar(self):
        builtins.Miss= [0 for i in range(5)]
        self.statusbar = ttk.Label(text='', relief='sunken' )
        self.statusbar.pack(side='bottom', fill = 'x')

        def callback():
            while True:
                time.sleep(0.1)
                self.statusbar.config(text='0: {0}     1: {1}     2: {2}     3: {3}     4: {4}'\
                         .format(builtins.Miss[0], builtins.Miss[1], builtins.Miss[2],\
                                 builtins.Miss[3], builtins.Miss[4]))
                if not False in builtins.Send_Finished_flag:
                    builtins.EXIT_flag = True

        t = threading.Thread(target=callback)
        t.daemon = True
        t.start()

#for set 'standard out' and 'standard error' to text of GUI.
class TextRedirector():
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag
    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
    def clear(self):
        self.widget.configure(state="normal")
        self.widget.delete('1.0', 'end')
        self.widget.configure(state="disabled")

class put_queue():
    def __init__(self, q, tag="stdout"):
        self.tag = tag
        self.q = q
    def write(self,str):
        self.q.put(str)

app = GUI_APP()
app.mainloop()
