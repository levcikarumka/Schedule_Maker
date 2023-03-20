#invite code
import tkinter as tk
from tkinter import *

w = 1200
h = 650

class mainform:
    def __init__(self, master):
        self.master = master
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws-w)/2
        y = (hs-h)/4
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

        self.master.config(bg="#2A2C2B")
        self.lbl = tk.Label(self.master, text='Main', font=('Arial', 50))
        self.lbl.place(rely=0.5, relx=0.5)
