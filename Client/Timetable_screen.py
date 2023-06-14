from tkinter import *
from tkinter import messagebox 
from cryptography.fernet import Fernet

class TimetableScreen():
    def __init__ (self, root, mainframe, client, scheduleLoginframe, title_label, tt_client, f):
        self.f = f
        self.root = root
        self.client = client
        self.title_label = title_label
        self.mainframe = mainframe
        self.scheduleLoginframe = scheduleLoginframe
        self.timetableframe = Frame(mainframe, width=1920, height=1080)
        self.timetable_contentframe = Frame(self.timetableframe, padx=15, pady=100, bg="white")

       #self.timetableframe.pack(fill="both", expand=1)
        self.timetable_contentframe.pack(fill="both", expand=1)

        monday_label = Label(self.timetable_contentframe, text="Monday", font=("Ariel", 14), bg="white", fg='red', width=20)
        tuesday_label = Label(self.timetable_contentframe, text="Tuesday", font=("Ariel", 14), bg="white", fg='red', width=20)
        wednesday_label = Label(self.timetable_contentframe, text="Wednesday", font=("Ariel", 14), bg="white", fg='red', width=20)
        thursday_label = Label(self.timetable_contentframe, text="Thursday", font=("Ariel", 14), bg="white", fg='red', width=20)
        friday_label = Label(self.timetable_contentframe, text="Friday", font=("Ariel", 14), bg="white", fg='red', width=20)
        saturday_label = Label(self.timetable_contentframe, text="Saturday", font=("Ariel", 14), bg="white", fg='red', width=20)
        sunday_label = Label(self.timetable_contentframe, text="Sunday", font=("Ariel", 14), bg="white", fg='red', width=20)

        to_login_label = Label(self.timetable_contentframe, text="Back to entering a schedule", font=("Ariel", 14), bg="white", fg='red', width=40)

        greencolorinfo_label = Label(self.timetable_contentframe, text="Green - you are free at this time", font=("Ariel", 14), bg="white")
        whitecolorinfo_label = Label(self.timetable_contentframe, text="White - you are busy at this time", font=("Ariel", 14), bg="white")

        monday_label.grid(row=0, column=0, columnspan=2)
        tuesday_label.grid(row=0, column=2, columnspan=2)        
        wednesday_label.grid(row=0, column=4, columnspan=2)
        thursday_label.grid(row=0, column=6, columnspan=2)
        friday_label.grid(row=0, column=8, columnspan=2)
        saturday_label.grid(row=0, column=10, columnspan=2)
        sunday_label.grid(row=0, column=12, columnspan=2)        

        greencolorinfo_label.grid(row=14, column=0, columnspan=4)
        whitecolorinfo_label.grid(row=14, column=8, columnspan=4)    
    

        to_login_label.grid(row=14, column = 4, columnspan=4, pady=50)

        to_login_label.bind("<Button-1>", lambda page: self.to_schedulelogin())

        self.buttons = {}

        for i in range(1, 13):
            for j in range(0, 14):
                if j % 2 == 0:
                    btn_text = str((i - 1)) + ":00-" + str((i)) + ":00"
                else:
                    btn_text = str((i + 11)) + ":00-" + str((i + 12)) + ":00"

                if tt_client[j // 2][12 * (j % 2) + (i-1)] == '0':
                    self.buttons[14 * (i - 1) + j] = Button(self.timetable_contentframe, width=9, fg='blue', font=('Arial',16,'bold'), bg='white', text=btn_text, command=lambda day=j, time=i-1: self.satus_change(day, time))   
                else:
                    self.buttons[14 * (i - 1) + j] = Button(self.timetable_contentframe, width=9, fg='blue', font=('Arial',16,'bold'), bg='green', text=btn_text, command=lambda day=j, time=i-1: self.satus_change(day, time))   
                self.buttons[14 * (i - 1) + j].grid(row=i, column=j)
                
    def satus_change(self, day, time):
        if self.buttons[14*(time) + day].cget('bg') == 'green':
            self.buttons[14*(time) + day].configure(bg="white")
        else:
            self.buttons[14*(time) + day].configure(bg="green")
        
        print(day, time)
        try:
            self.client.send(f"tt_st_ch {day} {time}", self.f)
        except:
            messagebox.showwarning('Server', "Server connection lost.")
            self.root.destroy()
        

    def to_schedulelogin(self):
        self.timetableframe.forget()
        self.scheduleLoginframe.pack()
        self.title_label['text'] = 'Schedule Login'
        self.title_label['bg'] = 'purple'


