from tkinter import *
from tkinter import messagebox 

class RegisterScreen():
    def __init__ (self, mainframe, client, loginframe, title_label):
        self.client = client
        self.loginframe = loginframe
        self.title_label = title_label
        self.registerframe = Frame(mainframe, width=1920, height=1080)
        self.register_contentframe = Frame(self.registerframe, padx=15, pady=15, highlightbackground='purple', highlightcolor='purple', highlightthickness=2, bg="#90EE90")

        self.username_label_reg = Label(self.register_contentframe, text="Username:", font=("Ariel", 14), bg="#90EE90")
        self.password_label_reg = Label(self.register_contentframe, text="Password:", font=("Ariel", 14), bg="#90EE90")
        self.confirm_password_label_reg = Label(self.register_contentframe, text="Repeat password:", font=("Ariel", 14), bg="#90EE90")

        self.username_entry_reg = Entry(self.register_contentframe, font=("Ariel", 14))
        self.password_entry_reg = Entry(self.register_contentframe, font=("Ariel", 14), show='*')
        self.confirm_password_entry_reg = Entry(self.register_contentframe, font=("Ariel", 14), show='*')

        cei = '/Users/MrLeonidiy/Desktop/Cyber project/Schedule_Maker/Client/eye_closed.png'
        oei = '/Users/MrLeonidiy/Desktop/Cyber project/Schedule_Maker/Client/eye_opened.png'
        self.closed_eye_icon = PhotoImage(file=cei)
        self.open_eye_icon = PhotoImage(file=oei)


        self.see_password_button_reg = Button(self.register_contentframe, image=self.open_eye_icon, bg="#90EE90")

        register_button = Button(self.register_contentframe, text="Register", font=("Ariel", 16), bg="blue", fg="#fff", padx=25, pady=10, width=25)

        to_login_label = Label(self.register_contentframe, text="Have an account? Login now!", font=("Ariel", 14), bg="#90EE90", fg='red')
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
            self.see_password_button_reg['image'] = self.closed_eye_icon
        else:
            self.password_entry_reg['show'] = "*"
            self.confirm_password_entry_reg['show'] = "*"
            self.see_password_button_reg['image'] = self.open_eye_icon

    #transfer to login page

    def to_login(self):
         self.registerframe.forget()
         self.loginframe.pack(fill='both', expand=1)
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

        if len(username) > 0 and len(password) > 0 and len(passwordrep):

            self.client.send(f"reg {username} {password} {passwordrep}")
            msg = self.client.recv()
            if msg == 'online':
                messagebox.showinfo('Register', 'Your registration went successfully')
            else:
                messagebox.showwarning('Register', msg)
