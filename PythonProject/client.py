import json
with open('cpnfig.JSON') as json_file:
    config = json.load(json_file)

template_reset = ''
with open('template.txt') as file:
    template_reset = file.read()

with open('chat.txt', 'w') as file:
    file.write(template_reset)

import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title('Chat')
root.geometry('450x450')
root.resizable(False, False)

root.option_add('*Font','{Calibri} 11')
root.option_add('*Background', 'white')

messages_frame = tk.Frame(root)
my_msg = tk.StringVar()
scrollbar = tk.Scrollbar(messages_frame)

msg_list = tk.Listbox(messages_frame, height=20,width=60, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(root,width=62, textvariable=my_msg)

entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tk.Button(root, text="Send", width=15, command=send)
send_button.pack()

from  socket import AF_INET, socket, SOCK_STREAM

def send(event=None):
    msg = my_msg.get()

    my_msg.get('')
    CLIENT.send(bytes(msg, 'utf8'))

root.protocol("WM_DELETE_WINDOW", on_closing)

def on_closing(event=None):
    if messagebox.askokcancel('Quit','Do you want to quit?'):
        my_msg.set('{quit}')
        send()
        CLIENT.close()
        root.quit()

HOST = config['ip']
PORT = config['port']
BUFSIZ = 1024
ADDR = (HOST, PORT)

CLIENT = socket(AF_INET, SOCK_STREAM)
CLIENT.connect(ADDR)

from threading import Thread

RECEIVE_THREAD = Thread(target=receive)
RECEIVE_THREAD.start()
root.mainloop()

def receive():
    while True:
        try:
            msg = CLIENT.recv(BUFSIZ).decode("utf8")
            n = 60
            for i in range(0, len(msg), n):
                msg_list.insert(tk.END, msg[i:(i + n)])

        except OSError:
            break