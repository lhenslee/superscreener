import tkinter as tk
import tkhelper
from tkinter import ttk
from workoutstructs import *

LARGE_FONT = ('Verdana',12)
NORM_FONT = ('Arial',10)
SMALL_FONT = ('Calibri',8)

class LitLift(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self,default='rari.ico')
        tk.Tk.wm_title(self,"Lit Lift")
        
        container = tk.Frame(self)

        container.pack(side='top', fill='y',expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        for F in (StartPage):

            frame = F(container,self)

            self.frames[F] = frame

            frame.grid(row=0,column=0,sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text='Welcome to Lit Lift',font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        intvar = [x for x in range(6)]
        variables = chest, mback, lback, lats, quadriceps
        titles = ['Chest', 'Middle Back', 'Lower Back', 'Lats', 'Quadriceps']
        tkhelper.checks_afterbutton(intvar, variables, titles, 3)
        
app = LitLift()
app.mainloop()

























        
