import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox 
import socket
from time import sleep
from Login_screen import LoginScreen
from Register_screen import RegisterScreen
from cryptography.fernet import Fernet

class Client:
    def __init__(self):
        self.IP = "192.168.1.107"
       # self.IP = IP
        #self.IP = input("input server ip ")
        self.PORT = 5050
        self.SIZE = 4096
        self.FORMAT = "utf-8"

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Waiting for a connection...")
        finished = False
        while not finished: 
            try:
                self.conn.connect((self.IP, self.PORT))
                print(f"Client connected to server at {self.IP}:{self.PORT}.")
                finished = True
                break
            except: 
                pass
            sleep(0.1)

    def send(self, msg, f):
        msg = msg + "|"
        self.conn.send(f.encrypt(msg.encode(self.FORMAT, errors= 'ignore')))
    
    def recv(self, f):
        msg = f.decrypt(self.conn.recv(self.SIZE)).decode(self.FORMAT, errors= 'ignore')
        return msg
    
    def recv_key(self):
        key = self.conn.recv(self.SIZE).decode(self.FORMAT, errors= 'ignore')
        return key

# close button function
def close_window():
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        try:
            client.send("exit", f)
            root.destroy()
        except:
            root.destroy()

client = Client()

root = Tk()

key = client.recv_key()
f = Fernet(key)

# Window width and height
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.geometry(f'{w}x{h}+0+0') 

headerframe = tk.Frame(root, highlightbackground='purple', highlightcolor='purple', highlightthickness=2, bg="black", width=w, height=70)
titleframe = tk.Frame(headerframe, bg='purple', padx=1, pady=1)
title_label = tk.Label(titleframe, text="Login", padx=20, pady=5, bg="green", fg="#fff", font=('Times New Roman', 24), width=8)
close_button = tk.Button(headerframe, text="x", borderwidth=1, relief='solid', font=("Ariel", 12), bg='red')

headerframe.pack()
titleframe.pack() 
title_label.pack()
close_button.pack()

titleframe.place(rely=0.5, relx=0.5, anchor=CENTER)
close_button.place(x=410, y=10)

close_button['command'] = close_window
mainframe = tk.Frame(root, width=w, height=h)
mainframe.pack()
login_frame = LoginScreen(root, mainframe, client, title_label, f).loginframe
login_frame.pack()

root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()
