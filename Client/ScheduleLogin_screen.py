from tkinter import *
from tkinter import messagebox 
from ScheduleRegister_screen import ScheduleRegisterScreen

class ScheduleLoginScreen():
    def __init__ (self, mainframe, client, loginframe, title_label):
        self.client = client
        self.title_label = title_label
        self.mainframe = mainframe
        self.loginframe = loginframe
        self.scheduleloginframe = Frame(mainframe, width=1920, height=1080)
        self.scheduleLogin_contentframe = Frame(self.scheduleloginframe, padx=15, pady=100, highlightbackground='purple', highlightcolor='purple', highlightthickness=2, bg="cyan")

        self.scheduleName_label = Label(self.scheduleLogin_contentframe, text="Title:", font=("Ariel", 14), bg="cyan")
        self.password_label = Label(self.scheduleLogin_contentframe, text="Password:", font=("Ariel", 14), bg="cyan")

        self.scheduleName_entry = Entry(self.scheduleLogin_contentframe, font=("Ariel", 14))
        self.password_entry = Entry(self.scheduleLogin_contentframe, font=("Ariel", 14), show='*')

        cei = '/Users/MrLeonidiy/Desktop/Cyber project/Schedule_Maker/Client/eye_closed.png'
        oei = '/Users/MrLeonidiy/Desktop/Cyber project/Schedule_Maker/Client/eye_opened.png'
        self.closed_eye_icon = PhotoImage(file=cei)
        self.open_eye_icon = PhotoImage(file=oei)

        self.see_password_button = Button(self.scheduleLogin_contentframe, image=self.open_eye_icon, bg='cyan')

        login_button = Button(self.scheduleLogin_contentframe, text="Login", font=("Ariel", 16), bg="green", fg="#fff", padx=25, pady=10, width=25)

        to_register_label = Label(self.scheduleLogin_contentframe, text="Want to create new schedule? Do it now!", font=("Ariel", 14), bg="cyan", fg='red')
        
        timetable_label = Label(self.scheduleLogin_contentframe, text="Edit your own timetable", font=("Ariel", 14), bg="cyan", fg='red')


        logout_label = Label(self.scheduleLogin_contentframe, text="Log out", font=("Ariel", 14), bg="cyan", fg='red')

       # mainframe.pack(fill="both", expand=1)
        self.scheduleloginframe.pack(fill="both", expand=1)
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
           self.see_password_button['image'] = self.closed_eye_icon
        else:
            self.password_entry['show'] = "*"
            self.see_password_button['image'] = self.open_eye_icon

    #transfer to register page

    def to_scheduleCreate(self):
        self.scheduleloginframe.pack_forget()
        ScheduleRegisterScreen(self.mainframe, self.client, self.scheduleloginframe, self.title_label).scheduleRegisterframe.pack()
        self.title_label['text'] = 'Schedule Create'
        self.title_label['bg'] = 'pink'

    #transfer back to login

    def log_out(self):
        self.scheduleloginframe.pack_forget()
        self.loginframe.pack(fill='both', expand=1)
        self.title_label['text'] = 'Login'
        self.title_label['bg'] = 'green'

    #transfer to timetable edit

    def to_timetableEdit(self):
        self.scheduleloginframe.pack_forget()
       # RegisterScreen(self.mainframe, self.client, self.loginframe, self.title_label).registerframe.pack()
        self.title_label['text'] = 'Edit your timetable'
        self.title_label['bg'] = 'orange'

    # schedule login

    def login(self):

        scheduleName = self.scheduleName_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if len(scheduleName) > 0 and len(password) > 0:

            self.client.send(f"sch_login {scheduleName} {password}")

            msg = self.client.recv()

            if msg == 'online':
                messagebox.showinfo('Login', 'Your login went successfully')
            else:
                messagebox.showwarning('Login', msg)


