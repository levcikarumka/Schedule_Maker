from tkinter import *
from tkinter import messagebox 
from ScheduleRegister_screen import ScheduleRegisterScreen
from Timetable_screen import TimetableScreen
from Schedule_screen import ScheduleScreen
from cryptography.fernet import Fernet

class ScheduleLoginScreen():
    def __init__ (self, root, mainframe, client, loginframe, title_label, f):
        self.f = f
        self.root = root
        self.client = client
        self.title_label = title_label
        self.mainframe = mainframe
        self.loginframe = loginframe
        self.scheduleloginframe = Frame(mainframe, width=1920, height=1080)
        self.scheduleLogin_contentframe = Frame(self.scheduleloginframe, padx=15, pady=100, bg="white")

        self.scheduleName_label = Label(self.scheduleLogin_contentframe, text="Title:", font=("Ariel", 14), bg="white")
        self.password_label = Label(self.scheduleLogin_contentframe, text="Password:", font=("Ariel", 14), bg="white")

        self.scheduleName_entry = Entry(self.scheduleLogin_contentframe, borderwidth=2, font=("Ariel", 14))
        self.password_entry = Entry(self.scheduleLogin_contentframe, borderwidth=2, font=("Ariel", 14), show='*')

        self.see_password_button = Button(self.scheduleLogin_contentframe, text="show", bg='white')

        login_button = Button(self.scheduleLogin_contentframe, text="Login", font=("Ariel", 16), bg="purple", fg="#fff", padx=25, pady=10, width=25)

        to_register_label = Label(self.scheduleLogin_contentframe, text="Want to create new schedule? Do it now!", font=("Ariel", 14), bg="white", fg='red')
        
        timetable_label = Label(self.scheduleLogin_contentframe, text="Edit your own timetable", font=("Ariel", 14), bg="white", fg='red')


        logout_label = Label(self.scheduleLogin_contentframe, text="Log out", font=("Ariel", 14), bg="white", fg='red')

       # mainframe.pack(fill="both", expand=1)
       # self.scheduleloginframe.pack(fill="both", expand=1)
        self.scheduleLogin_contentframe.pack(fill="both", expand=1)

        self.scheduleName_label.grid(row=0, column=0, pady=15)
        self.scheduleName_entry.grid(row=0, column=1)

        self.password_label.grid(row=1, column=0, pady=15)
        self.password_entry.grid(row=1, column=1)

        self.see_password_button.grid(row=1, column=2)

        login_button.grid(row=2, column=0, columnspan=2, padx=20, pady=40)

        to_register_label.grid(row=3, column=0, columnspan=2, padx=20, pady=40)

        timetable_label.grid(row=4, column=0, columnspan=2, padx=20, pady=40)

        logout_label.grid(row=5, column=0, columnspan=2, padx=20, pady=40)

        self.see_password_button['command'] = self.show_password

        to_register_label.bind("<Button-1>", lambda page: self.to_scheduleCreate())

        timetable_label.bind("<Button-1>", lambda page: self.to_timetableEdit())
        
        logout_label.bind("<Button-1>", lambda page: self.log_out())

        login_button['command'] = self.login



    def show_password(self):
        if self.password_entry['show'] == "*":
           self.password_entry['show'] = ""
           self.see_password_button['text'] = "hide"
        else:
            self.password_entry['show'] = "*"
            self.see_password_button['text'] = "show"

    #transfer to register page

    def to_scheduleCreate(self):
        self.scheduleloginframe.pack_forget()
        ScheduleRegisterScreen(self.root, self.mainframe, self.client, self.scheduleloginframe, self.title_label, self.f).scheduleRegisterframe.pack()
        self.title_label['text'] = 'Schedule Create'
        self.title_label['bg'] = 'pink'

    #transfer back to login

    def log_out(self):
        self.scheduleloginframe.pack_forget()
        self.loginframe.pack()
        self.title_label['text'] = 'Login'
        self.title_label['bg'] = 'green'

    #transfer to timetable edit

    def to_timetableEdit(self):
        self.scheduleloginframe.pack_forget()
        try:
            self.client.send(f"tt", self.f)
            self.array = self.client.recv(self.f).split('|')[:-1]

            print(self.array)
            TimetableScreen(self.root, self.mainframe, self.client, self.scheduleloginframe, self.title_label, self.array, self.f).timetableframe.pack()
            self.title_label['text'] = 'Edit your timetable'
            self.title_label['bg'] = 'orange'
        except:
            messagebox.showwarning('Server', "Server connection lost.")
            self.root.destroy()

    # schedule login

    def login(self):

        scheduleName = self.scheduleName_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if len(scheduleName) > 0 and len(password) > 0:


            try:
                self.client.send(f"sch_login {scheduleName} {password}", self.f)

                msg = self.client.recv(self.f)

                if msg == 'online':
                    allpeople = []
                    try:
                        self.client.send(f"sch", self.f)
                    except:
                        messagebox.showwarning('Server', "Server connection lost.")
                        self.root.destroy()
                    self.scheduleloginframe.pack_forget()
                    username = self.client.recv(self.f)
                    num = int(self.client.recv(self.f))
                    for i in range (0, num):
                        allpeople.append(str(self.client.recv(self.f)).split('|')[:-1])
                    print(allpeople)
                    ScheduleScreen(self.mainframe, self.client, self.scheduleloginframe, self.title_label, allpeople, username, self.f).scheduleframe.pack()
                    self.title_label['text'] = 'Schedule'
                    self.title_label['bg'] = 'grey'

                else:
                    messagebox.showwarning('Login', msg)
            except:
                messagebox.showwarning('Server', "Server connection lost.")
                self.root.destroy()


