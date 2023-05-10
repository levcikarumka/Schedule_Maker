from tkinter import *
from tkinter import messagebox 

class ScheduleRegisterScreen():
    def __init__ (self, mainframe, client, scheduleloginframe, title_label):
        self.client = client
        self.scheduleloginframe = scheduleloginframe
        self.title_label = title_label
        self.scheduleRegisterframe = Frame(mainframe, width=1920, height=1080)
        self.scheduleRegister_contentframe = Frame(self.scheduleRegisterframe, padx=15, pady=15, highlightbackground='purple', highlightcolor='purple', highlightthickness=2, bg="#90EE90")

        self.title_label_reg = Label(self.scheduleRegister_contentframe, text="Title:", font=("Ariel", 14), bg="#90EE90")
        self.password_label_reg = Label(self.scheduleRegister_contentframe, text="Password:", font=("Ariel", 14), bg="#90EE90")
        self.confirm_password_label_reg = Label(self.scheduleRegister_contentframe, text="Repeat password:", font=("Ariel", 14), bg="#90EE90")

        self.title_entry_reg = Entry(self.scheduleRegister_contentframe, font=("Ariel", 14))
        self.password_entry_reg = Entry(self.scheduleRegister_contentframe, font=("Ariel", 14), show='*')
        self.confirm_password_entry_reg = Entry(self.scheduleRegister_contentframe, font=("Ariel", 14), show='*')

        self.see_password_button_reg = Button(self.scheduleRegister_contentframe, text="show", bg="#90EE90")

        register_button = Button(self.scheduleRegister_contentframe, text="Create", font=("Ariel", 16), bg="blue", fg="#fff", padx=25, pady=10, width=25)

        to_login_label = Label(self.scheduleRegister_contentframe, text="Have a schedule? Login now!", font=("Ariel", 14), bg="#90EE90", fg='red')
        self.scheduleRegister_contentframe.pack(fill="both", expand=1)

        self.title_label_reg.grid(row=0, column=0, pady=15, sticky='e')
        self.title_entry_reg.grid(row=0, column=1)

        self.password_label_reg.grid(row=1, column=0, pady=15, sticky='e')
        self.password_entry_reg.grid(row=1, column=1)

        self.confirm_password_label_reg.grid(row=2, column=0, pady=15, sticky='e')
        self.confirm_password_entry_reg.grid(row=2, column=1)

        self.see_password_button_reg.grid(row=1, column=2)

        register_button.grid(row=3, column=0, columnspan=2, padx=20, pady=50)

        to_login_label.grid(row=4, column=0, columnspan=2, padx=20, pady=30)

        self.see_password_button_reg['command'] = self.show_password_reg

        to_login_label.bind("<Button-1>", lambda page: self.to_schedulelogin())

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

    def to_schedulelogin(self):
        self.scheduleRegisterframe.forget()
        self.scheduleloginframe.pack(fill='both', expand=1)
        self.title_label['text'] = 'Schedule Login'
        self.title_label['bg'] = 'purple'

    # is title available?

    def title_check(self):
        title = self.title_entry_reg.get()
        if " " in title or "|" in title:
            return False
        else:
            return True

    # new account registration

    def register(self):
        title = self.title_entry_reg.get().strip()
        password = self.password_entry_reg.get().strip()
        passwordrep = self.confirm_password_entry_reg.get().strip()

        if len(title) > 0 and len(password) > 0 and len(passwordrep) and " " not in title and " " not in password:

            self.client.send(f"create {title} {password} {passwordrep}")
            msg = self.client.recv()
            if msg == 'online':
                messagebox.showinfo('Register', 'Your schedule was created successfully')
            else:
                messagebox.showwarning('Register', msg)
