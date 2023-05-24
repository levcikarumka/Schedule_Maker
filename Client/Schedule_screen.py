from tkinter import *
from tkinter import messagebox 
from cryptography.fernet import Fernet

class ScheduleScreen():
    def __init__ (self, mainframe, client, ScheduleLoginframe, title_label, tts_users, username, f):
        self.f = f
        self.client = client
        self.title_label = title_label
        self.mainframe = mainframe
        self.tts_users = tts_users
        self.scheduleLoginframe = ScheduleLoginframe
        self.scheduleframe = Frame(mainframe, width=1920, height=1080)
        self.schedule_contentframe = Frame(self.scheduleframe, padx=15, pady=100, highlightbackground='purple', highlightcolor='purple', highlightthickness=2, bg="#CC7722")

        self.scheduleframe.pack(fill="both", expand=1)
        self.schedule_contentframe.pack(fill="both", expand=1)

        monday_label = Label(self.schedule_contentframe, text="Monday", font=("Ariel", 14), bg="#90EE90", fg='red', width=20)
        tuesday_label = Label(self.schedule_contentframe, text="Tuesday", font=("Ariel", 14), bg="#90EE90", fg='red', width=20)
        wednesday_label = Label(self.schedule_contentframe, text="Wednesday", font=("Ariel", 14), bg="#90EE90", fg='red', width=20)
        thursday_label = Label(self.schedule_contentframe, text="Thursday", font=("Ariel", 14), bg="#90EE90", fg='red', width=20)
        friday_label = Label(self.schedule_contentframe, text="Friday", font=("Ariel", 14), bg="#90EE90", fg='red', width=20)
        saturday_label = Label(self.schedule_contentframe, text="Saturday", font=("Ariel", 14), bg="#90EE90", fg='red', width=20)
        sunday_label = Label(self.schedule_contentframe, text="Sunday", font=("Ariel", 14), bg="#90EE90", fg='red', width=20)

        log_out_label = Label(self.schedule_contentframe, text="Back to entering a schedule", font=("Ariel", 14), bg="#90EE90", fg='red', width=40)

        self.hover_available_label = Label(self.schedule_contentframe, text="Available:", font=("Ariel", 14), bg="#90EE90", fg='red', width=40)
        self.hover_notAvailable_label = Label(self.schedule_contentframe, text="Not available:", font=("Ariel", 14), bg="#90EE90", fg='red', width=40)

        monday_label.grid(row=0, column=0, columnspan=2)
        tuesday_label.grid(row=0, column=2, columnspan=2)        
        wednesday_label.grid(row=0, column=4, columnspan=2)
        thursday_label.grid(row=0, column=6, columnspan=2)
        friday_label.grid(row=0, column=8, columnspan=2)
        saturday_label.grid(row=0, column=10, columnspan=2)
        sunday_label.grid(row=0, column=12, columnspan=2)        

        log_out_label.grid(row=14, column = 4, columnspan=4, pady=50)

        self.hover_available_label.grid(row=15, column = 4, columnspan=4, pady=50)
        self.hover_notAvailable_label.grid(row=16, column = 4, columnspan=4, pady=20)

        log_out_label.bind("<Button-1>", lambda page: self.to_schedulelogin())

        users = []
        timetable = ['000000000000000000000000', '000000000000000000000000', '000000000000000000000000', '000000000000000000000000', '000000000000000000000000', '000000000000000000000000', '000000000000000000000000']
        num_users = len(tts_users)
        self.num_users = num_users

        for u in range(0, num_users):
            if str(tts_users[u][0]) == str(username):
                user_index = u
            users.append([u, tts_users[u][0]])

        self.users = users

        for i in range(0, num_users):
            for j in range(1, 8):
                for z in range(0, 24):
                    if tts_users[i][j][z] == '1':
                        timetable[j-1] = timetable[j-1][:z] + str(int(timetable[j-1][z]) + 1) + timetable[j-1][z+1:]
        
        print(users)
        print(timetable)
        print(user_index)


        self.labels = {}

        user_selected = False

        for d in range(1, 13):
            for t in range(0, 14):
                if t % 2 == 0:
                    label_text = str((d - 1)) + ":00-" + str((d - 1)) + ":59"
                else:
                    label_text = str((d + 11)) + ":00-" + str((d + 11)) + ":59"

                if tts_users[user_index][(t // 2) + 1][12 * (t % 2) + (d - 1)] == '1':
                    user_selected = True 
                else:
                    user_selected = False

                if timetable[t // 2][12 * (t % 2) + (d - 1)] == '0' or timetable[t // 2][12 * (t % 2) + (d - 1)] == '1' and user_selected == False:
                    self.labels[14 * (d - 1) + t] = Label(self.schedule_contentframe, width=9, font=('Arial',16,'bold'), bg='white', text=label_text)   
                elif timetable[t // 2][12 * (t % 2) + (d - 1)] == str(num_users):
                    self.labels[14 * (d - 1) + t] = Label(self.schedule_contentframe, width=9, font=('Arial',16,'bold'), bg='green', text=label_text)
                elif timetable[t // 2][12 * (t % 2) + (d - 1)] == '1' and user_selected == True: 
                    self.labels[14 * (d - 1) + t] = Label(self.schedule_contentframe, width=9, font=('Arial',16,'bold'), bg='yellow', text=label_text)
                elif (int(timetable[t // 2][12 * (t % 2) + (d - 1)]) / num_users) < 0.5 and user_selected == True: 
                    self.labels[14 * (d - 1) + t] = Label(self.schedule_contentframe, width=9, font=('Arial',16,'bold'), bg='#00008B', text=label_text)
                elif (int(timetable[t // 2][12 * (t % 2) + (d - 1)]) / num_users) >= 0.5 and user_selected == True: 
                    self.labels[14 * (d - 1) + t] = Label(self.schedule_contentframe, width=9, font=('Arial',16,'bold'), bg='#00FFFF', text=label_text)
                elif (int(timetable[t // 2][12 * (t % 2) + (d - 1)]) / num_users) >= 0.5 and user_selected == False: 
                    self.labels[14 * (d - 1) + t] = Label(self.schedule_contentframe, width=9, font=('Arial',16,'bold'), bg='red', text=label_text)
                elif int(timetable[t // 2][12 * (t % 2) + (d - 1)]) >= 2 and user_selected == False: 
                    self.labels[14 * (d - 1) + t] = Label(self.schedule_contentframe, width=9, font=('Arial',16,'bold'), bg='#AA336A', text=label_text)      

                self.labels[14 * (d - 1) + t].bind("<Enter>", lambda event, day=t, time=d: self.on_enter(event, time, day))
                self.labels[14 * (d - 1) + t].bind("<Leave>", self.on_leave)
                self.labels[14 * (d - 1) + t].grid(row=d, column=t)
        
    def to_schedulelogin(self):
        self.scheduleframe.forget()
        self.scheduleLoginframe.pack(fill='both', expand=1)
        self.title_label['text'] = 'Schedule Login'
        self.title_label['bg'] = 'purple'
    
    def on_enter(self, event, time, day):
        using = []
        not_using = []
        for i in range(0, self.num_users):
            if self.tts_users[i][day//2 + 1][12 * (day % 2) + (time - 1)] == '1':
                using.append(str(self.tts_users[i][0]))
            else:
                not_using.append(str(self.tts_users[i][0]))

        self.hover_available_label.configure(text="Available:" + ', '.join(using))
        self.hover_notAvailable_label.configure(text="Not available:" + ', '.join(not_using))

    def on_leave(self, enter):
        self.hover_available_label.configure(text="Available:")
        self.hover_notAvailable_label.configure(text="Not available:")
