from tkinter import *
from tkinter import messagebox 
from cryptography.fernet import Fernet

class RegisterScreen():
    def __init__ (self, root, mainframe, client, loginframe, title_label, f):
        self.f = f
        self.root = root
        self.client = client
        self.loginframe = loginframe
        self.title_label = title_label
        self.registerframe = Frame(mainframe, width=1920, height=1080)
        self.register_contentframe = Frame(self.registerframe, padx=15, pady=15, bg="white")

        self.username_label_reg = Label(self.register_contentframe, text="Username:", font=("Ariel", 14), bg="white")
        self.password_label_reg = Label(self.register_contentframe, text="Password:", font=("Ariel", 14), bg="white")
        self.confirm_password_label_reg = Label(self.register_contentframe, text="Repeat password:", font=("Ariel", 14), bg="white")

        self.username_entry_reg = Entry(self.register_contentframe, borderwidth=2, font=("Ariel", 14))
        self.password_entry_reg = Entry(self.register_contentframe, borderwidth=2, font=("Ariel", 14), show='*')
        self.confirm_password_entry_reg = Entry(self.register_contentframe, borderwidth=2, font=("Ariel", 14), show='*')

        self.see_password_button_reg = Button(self.register_contentframe, text="show", bg="white")

        register_button = Button(self.register_contentframe, text="Register", font=("Ariel", 16), bg="blue", fg="#fff", padx=25, pady=10, width=25)

        to_login_label = Label(self.register_contentframe, text="Have an account? Login now!", font=("Ariel", 14), bg="white", fg='red')
        self.register_contentframe.pack(fill="both", expand=1)

        self.username_label_reg.grid(row=0, column=0, pady=15, sticky='e')
        self.username_entry_reg.grid(row=0, column=1)

        self.password_label_reg.grid(row=1, column=0, pady=15, sticky='e')
        self.password_entry_reg.grid(row=1, column=1)

        self.confirm_password_label_reg.grid(row=2, column=0, pady=15, sticky='e')
        self.confirm_password_entry_reg.grid(row=2, column=1)

        self.see_password_button_reg.grid(row=1, column=2)

        register_button.grid(row=3, column=0, columnspan=2, padx=20, pady=50)

        to_login_label.grid(row=4, column=0, columnspan=2, padx=20, pady=30)

        self.see_password_button_reg['command'] = self.show_password_reg

        to_login_label.bind("<Button-1>", lambda page: self.to_login())

        register_button['command'] = self.register

    def show_password_reg(self):
        if self.password_entry_reg['show'] == "*":
            self.password_entry_reg['show'] = ""
            self.confirm_password_entry_reg['show'] = ""
            self.see_password_button_reg['text'] = "hide"
        else:
            self.password_entry_reg['show'] = "*"
            self.confirm_password_entry_reg['show'] = "*"
            self.see_password_button_reg['text'] = "show"

    #transfer to login page

    def to_login(self):
         self.registerframe.pack_forget()
         self.loginframe.pack()
         self.title_label['text'] = 'Login'
         self.title_label['bg'] = 'green'

    # is username available?

    def username_check(self):
        username = self.username_entry_reg.get()
        if " " in username or "|" in username:
            return False
        else:
            return True

    # new account registration

    def register(self):
        username = self.username_entry_reg.get().strip()
        password = self.password_entry_reg.get().strip()
        passwordrep = self.confirm_password_entry_reg.get().strip()

        if len(username) > 0 and len(password) > 0 and len(passwordrep) and " " not in username and " " not in password:
            
            try:
                self.client.send(f"reg {username} {password} {passwordrep}", self.f)
                msg = self.client.recv(self.f)
                if msg == 'online':
                    messagebox.showinfo('Register', 'Your registration went successfully')
                else:
                    messagebox.showwarning('Register', msg)
            except:
                messagebox.showwarning('Server', "Server connection lost.")
                self.root.destroy()
