import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox 
import mysql.connector
from Schedule_create import mainform
import socket
from time import sleep
from Login_screen import LoginScreen

class Client:
    def __init__(self):
        self.IP = "127.0.0.1"
        self.PORT = 8000
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

    def send(self, msg):
        msg = msg + "|"
        self.conn.send(msg.encode(self.FORMAT, errors= 'ignore'))
    
    def recv(self):
        msg = self.conn.recv(self.SIZE).decode(self.FORMAT, errors= 'ignore')
        return msg

client = Client()

root = Tk()
#connection = mysql.connector.connect(host='localhost', user='root', port='3306', password='', database='sm_login_password')
#c = connection.cursor()

# Window width and height
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.geometry(f'{w}x{h}+0+0') 

# close button function
def close_window():
    client.send('exit')
    root.destroy()

cei = '/Users/MrLeonidiy/Desktop/Cyber project/Schedule_Maker/Client/eye_closed.png'
oei = '/Users/MrLeonidiy/Desktop/Cyber project/Schedule_Maker/Client/eye_opened.png'
closed_eye_icon = PhotoImage(file=cei)
open_eye_icon = PhotoImage(file=oei)


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
login_frame = LoginScreen(mainframe, client).loginframe
login_frame.pack()



# Login Page
#loginframe = tk.Frame(mainframe, width=w, height=h)
#login_contentframe = tk.Frame(loginframe, padx=15, pady=100, highlightbackground='purple', highlightcolor='purple', highlightthickness=2, bg="cyan")
#
#username_label = tk.Label(login_contentframe, text="Username:", font=("Ariel", 14), bg="cyan")
#password_label = tk.Label(login_contentframe, text="Password:", font=("Ariel", 14), bg="cyan")
#
#username_entry = tk.Entry(login_contentframe, font=("Ariel", 14))
#password_entry = tk.Entry(login_contentframe, font=("Ariel", 14), show='*')
#
#see_password_button = tk.Button(login_contentframe, image=open_eye_icon, bg='cyan')
#
#login_button = tk.Button(login_contentframe, text="Login", font=("Ariel", 16), bg="green", fg="#fff", padx=25, pady=10, width=25)
#
#to_register_label = tk.Label(login_contentframe, text="New here? Register now!", font=("Ariel", 14), bg="cyan", fg='red')
#
#mainframe.pack(fill="both", expand=1)
#loginframe.pack(fill="both", expand=1)
#login_contentframe.pack(fill="both", expand=1)
#
#username_label.grid(row=0, column=0, pady=15, sticky='e')
#username_entry.grid(row=0, column=1)
#
#password_label.grid(row=1, column=0, pady=15, sticky='e')
#password_entry.grid(row=1, column=1)
#
#see_password_button.grid(row=1, column=2)
#
#login_button.grid(row=2, column=0, columnspan=2, padx=20, pady=40)
#
#to_register_label.grid(row=3, column=0, columnspan=2, padx=20, pady=40)
#
#def show_password():
#    if password_entry['show'] == "*":
#        password_entry['show'] = ""
#        see_password_button['image'] = closed_eye_icon
#    else:
#        password_entry['show'] = "*"
#        see_password_button['image'] = open_eye_icon
#
#see_password_button['command'] = show_password
#
##transfer to register page
#
#def to_register():
#    loginframe.forget()
#    registerframe.pack(fill='both', expand=1)
#    title_label['text'] = 'Register'
#    title_label['bg'] = 'blue'
#
#to_register_label.bind("<Button-1>", lambda page: to_register())
#
## Account login
#
#def login():
#    username = username_entry.get().strip()
#    password = password_entry.get().strip()
#
#    values = (username, password)
#    select_query = "SELECT * FROM `users` WHERE `username` = %s and `password` = %s"
#    c.execute(select_query, values)
#    user = c.fetchone()
#    try:
#        len(user)
#        #messagebox.showinfo('Login', "Login successfully")
#        mainformwindow = tk.Toplevel()
#        app = mainform(mainformwindow)
#        root.withdraw()
#        mainformwindow.protocol("WM_DELETE_WINDOW", close_window)
#
#    except:
#        messagebox.showwarning('Login', "Wrong username or password")
#
#login_button['command'] = login
#
## Register Page
#
#registerframe = tk.Frame(mainframe, width=w, height=h)
#register_contentframe = tk.Frame(registerframe, padx=15, pady=15, highlightbackground='purple', highlightcolor='purple', highlightthickness=2, bg="#90EE90")
#
#username_label_reg = tk.Label(register_contentframe, text="Username:", font=("Ariel", 14), bg="#90EE90")
#password_label_reg = tk.Label(register_contentframe, text="Password:", font=("Ariel", 14), bg="#90EE90")
#confirm_password_label_reg = tk.Label(register_contentframe, text="Repeat password:", font=("Ariel", 14), bg="#90EE90")
#
#username_entry_reg = tk.Entry(register_contentframe, font=("Ariel", 14))
#password_entry_reg = tk.Entry(register_contentframe, font=("Ariel", 14), show='*')
#confirm_password_entry_reg = tk.Entry(register_contentframe, font=("Ariel", 14), show='*')
#
#see_password_button_reg = tk.Button(register_contentframe, image=open_eye_icon, bg="#90EE90")
#
#register_button = tk.Button(register_contentframe, text="Register", font=("Ariel", 16), bg="blue", fg="#fff", padx=25, pady=10, width=25)
#
#to_login_label = tk.Label(register_contentframe, text="Have an account? Login now!", font=("Ariel", 14), bg="#90EE90", fg='red')
#
#register_contentframe.pack(fill="both", expand=1)
#
#username_label_reg.grid(row=0, column=0, pady=15, sticky='e')
#username_entry_reg.grid(row=0, column=1)
#
#password_label_reg.grid(row=1, column=0, pady=15, sticky='e')
#password_entry_reg.grid(row=1, column=1)
#
#confirm_password_label_reg.grid(row=2, column=0, pady=15, sticky='e')
#confirm_password_entry_reg.grid(row=2, column=1)
#
#see_password_button_reg.grid(row=1, column=2)
#
#register_button.grid(row=3, column=0, columnspan=2, padx=20, pady=50)
#
#to_login_label.grid(row=4, column=0, columnspan=2, padx=20, pady=30)
#
#def show_password_reg():
#    if password_entry_reg['show'] == "*":
#        password_entry_reg['show'] = ""
#        confirm_password_entry_reg['show'] = ""
#        see_password_button_reg['image'] = closed_eye_icon
#    else:
#        password_entry_reg['show'] = "*"
#        confirm_password_entry_reg['show'] = "*"
#        see_password_button_reg['image'] = open_eye_icon
#
#
#see_password_button_reg['command'] = show_password_reg
#
#
##transfer to login page
#
#def to_login():
#    registerframe.forget()
#    loginframe.pack(fill='both', expand=1)
#    title_label['text'] = 'Login'
#    title_label['bg'] = 'green'
#
#to_login_label.bind("<Button-1>", lambda page: to_login())
#
## is username taken?
#
#def username_check():
#    username = username_entry_reg.get().strip()
#    values = (username,)
#    select_query = "SELECT * FROM `users` WHERE `username` = %s"
#    c.execute(select_query, values)
#    user = c.fetchone()
#    if user is not None:
#        return False
#    else:
#        return True
#
## new account registration
#
#def register():
#    username = username_entry_reg.get().strip()
#    password = password_entry_reg.get().strip()
#
#    
#    if len(username) > 0 and len(password) > 0:
#        if username_check():
#            if password == confirm_password_entry_reg.get().strip():
#                values = (username, password)
#                insert_query = "INSERT INTO `users`(`username`, `password`) VALUES (%s,%s)"
#                c.execute(insert_query, values)
#                connection.commit()
#                messagebox.showinfo('Register', 'Your registration went successfully')
#                registerframe.forget()
#                loginframe.pack(fill='both', expand=1)
#                title_label['text'] = 'Login'
#                title_label['bg'] = 'green'
#            else:
#                messagebox.showwarning('Register', "Passwords don't match")
#        else:
#            messagebox.showwarning('Username', "This username already taken, use another one")
#    else:
#        messagebox.showwarning('Register', "Something went wrong, check information you've provided")
#
#register_button['command'] = register
#
## end
#
#
#root.protocol("WM_DELETE_WINDOW", close_window())
root.mainloop()