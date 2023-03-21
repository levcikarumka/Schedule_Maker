from tkinter import *
from tkinter import messagebox 

class TimetableScreen():
    def __init__ (self, mainframe, client, scheduleLoginframe, title_label):
        self.client = client
        self.title_label = title_label
        self.mainframe = mainframe
        self.ScheduleLoginframe = scheduleLoginframe
        self.timetableframe = Frame(mainframe, width=1920, height=1080)
        self.timetable_contentframe = Frame(self.timetableframe, padx=15, pady=100, highlightbackground='purple', highlightcolor='purple', highlightthickness=2, bg="cyan")

        self.timetableframe.pack(fill="both", expand=1)
        self.timetable_contentframe.pack(fill="both", expand=1)

