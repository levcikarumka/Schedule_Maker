from tkinter import *
from Register_screen import RegisterScreen
from tkinter import messagebox
from ScheduleLogin_screen import ScheduleLoginScreen

class LoginScreen():
    def __init__ (self, mainframe, client, title_label):
        self.client = client
        self.title_label = title_label
        self.mainframe = mainframe
        self.loginframe = Frame(mainframe, width=1920, height=1080)
        self.login_contentframe = Frame(self.loginframe, padx=15, pady=100, highlightbackground='purple', highlightcolor='purple', highlightthickness=2, bg="cyan")

        self.username_label = Label(self.login_contentframe, text="Username:", font=("Ariel", 14), bg="cyan")
        self.password_label = Label(self.login_contentframe, text="Password:", font=("Ariel", 14), bg="cyan")

        self.username_entry = Entry(self.login_contentframe, font=("Ariel", 14))
        self.password_entry = Entry(self.login_contentframe, font=("Ariel", 14), show='*')

        self.see_password_button = Button(self.login_contentframe, text="show", bg='cyan')

        login_button = Button(self.login_contentframe, text="Login", font=("Ariel", 16), bg="green", fg="#fff", padx=25, pady=10, width=25)

        to_register_label = Label(self.login_contentframe, text="New here? Register now!", font=("Ariel", 14), bg="cyan", fg='red')

        mainframe.pack(fill="both", expand=1)
        self.loginframe.pack(fill="both", expand=1)
        self.login_contentframe.pack(fill="both", expand=1)

        self.username_label.grid(row=0, column=0, pady=15)
        self.username_entry.grid(row=0, column=1)

        self.password_label.grid(row=1, column=0, pady=15)
        self.password_entry.grid(row=1, column=1)

        self.see_password_button.grid(row=1, column=2)

        login_button.grid(row=2, column=0, columnspan=2, padx=20, pady=40)

        to_register_label.grid(row=3, column=0, columnspan=2, padx=20, pady=40)

        self.see_password_button['command'] = self.show_password

        to_register_label.bind("<Button-1>", lambda page: self.to_register())

        login_button['command'] = self.login



    def show_password(self):
        if self.password_entry['show'] == "*":
           self.password_entry['show'] = ""
           self.see_password_button['text'] = "hide"
        else:
            self.password_entry['show'] = "*"
            self.see_password_button['text'] = "show"

    #transfer to register page

    def to_register(self):
        self.loginframe.pack_forget()
        RegisterScreen(self.mainframe, self.client, self.loginframe, self.title_label).registerframe.pack()
        self.title_label['text'] = 'Register'
        self.title_label['bg'] = 'blue'


    # Account login

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if len(username) > 0 and len(password) > 0:

            self.client.send(f"login {username} {password}")

            msg = self.client.recv()

            if msg == 'online':
                self.loginframe.pack_forget()
                ScheduleLoginScreen(self.mainframe, self.client, self.loginframe, self.title_label).scheduleloginframe.pack()
                self.title_label['text'] = 'Schedule Login'
                self.title_label['bg'] = 'purple'
                self.title_label['width'] = '25'

            else:
                messagebox.showwarning('Login', msg)

#проверить на знаки особенные и пробелы
