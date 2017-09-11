import csv
from decimal import *
import pandas as pd
import tkinter as tk
from tkinter import ttk
import os
from main import *
from functions import *


LARGE_FONT = ('Verdana',12)
NORM_FONT = ('Arial',10)
SMALL_FONT = ('Calibri',8)

class SuperScreener(tk.Tk):
    if not os.path.exists('Recent Screens/'):
        prev_screens = ''
    else:
        prev_screens = os.listdir('Recent Screens/')
    if not os.path.exists('stock_dfs/'):
        prev_dates = ''
    else:
        prev_dates = os.listdir('stock_dfs/')
    screen_folder = ''
    pickle_file = ''
    csv_folder = ''
    percent_folder = ''
    fscreener = ''
    fanalysis = ''
    bestscreens_file = ''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self,default='rari.ico')
        tk.Tk.wm_title(self,"Super Screener")
        
        container = tk.Frame(self)

        container.pack(side='top', fill='y',expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        for F in (StartPage, RecentScreens, NewScreen,TimeFrame,ScreenSettings,MegaScreen):

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
        label = tk.Label(self,text='Welcome to Super Screener!',font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self,text='Go to recent screens',
                            command = lambda: controller.show_frame(RecentScreens))
        button1.pack(pady=5)

        button2 = ttk.Button(self,text='Run a new screener',
                            command = lambda: controller.show_frame(NewScreen))
        button2.pack(pady=5)



class RecentScreens(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text='Recent Screens',font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        if not os.path.exists('recent_screens/'):
            self.prev_screens = ''
        else:
            self.prev_screens = os.listdir('recent_screens/')
        button2 = ttk.Button(self,text='Enter New Screener',
                             command = lambda : controller.show_frame(NewScreen))
        
        self.button = {}
        for i in (range(len(self.prev_screens))):
            self.button[i] = ttk.Button(self,text=self.prev_screens[i], command = lambda i=i : self.onclick(i))
            self.button[i].pack()
        button2.pack()
        

    def onclick(self,i):
        make_screener_files(self.prev_screens[i])
        self.controller.show_frame(TimeFrame)
        

class NewScreen(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text='Enter the URL from a Finviz Screener',font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.entry = tk.Entry(self,width = 50)
        self.entry.bind('<Return>',self.newEntry)
        self.entry.pack()

    def newEntry(self,event):
        new_ticker_list(self.entry.get())
        self.controller.show_frame(TimeFrame)


class TimeFrame(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        label = tk.Label(self,text='Enter or Select Your Time Frame',font=LARGE_FONT)
        label.grid(row=0,columnspan=4,pady=10,padx=10,sticky='ew')

        tk.Label(self,text='Start Year:',font=NORM_FONT).grid(row=1,column=0,sticky='e')
        tk.Label(self,text='Start Month:',font=NORM_FONT).grid(row=2,column=0,sticky='e')
        tk.Label(self,text='Start Day:',font=NORM_FONT).grid(row=3,column=0,sticky='e')
        tk.Label(self,text='End Year:',font=NORM_FONT).grid(row=1,column=2,pady=1,sticky='e')
        tk.Label(self,text='End Month:',font=NORM_FONT).grid(row=2,column=2,pady=1,sticky='e')
        tk.Label(self,text='End Day:',font=NORM_FONT).grid(row=3,column=2,pady=1,sticky='e')

        tk.Label(self).grid(row=1,rowspan=3,columnspan=3)
    
        self.esyear = ttk.Entry(self,width=5)
        self.esyear.grid(row=1,column=1)
        self.esmonth = ttk.Entry(self,width=5)
        self.esmonth.grid(row=2,column=1)
        self.esday = ttk.Entry(self,width=5)
        self.esday.grid(row=3,column=1)
        self.eeyear = ttk.Entry(self,width=5)
        self.eeyear.grid(row=1,column=3)
        self.eemonth = ttk.Entry(self,width=5)
        self.eemonth.grid(row=2,column=3)
        self.eeday = ttk.Entry(self,width=5)
        self.eeday.grid(row=3,column=3)

        ttk.Label(self,text='Recent Date Entries',font=NORM_FONT).grid(row=4,columnspan=4,pady=5)
        if not os.path.exists('stock_data/'):
            self.prev_dates = ''
        else:
            self.prev_dates = os.listdir('stock_data/')
        self.button = {}
        for i in (range(len(self.prev_dates))):
            self.button[i] = ttk.Button(self,text=self.prev_dates[i], command = lambda i=i : self.onclick(i))
            self.button[i].grid(row=5+i,column=0,columnspan=4)

        self.button1 = ttk.Button(self,text='Enter Dates',command = lambda : self.newEntry())
        self.button1.grid(row=1,rowspan=3,column=4)
        
    def onclick(self,i):
        set_dates_from_prev(self.prev_dates[i])
        store_stock_data()
        self.controller.show_frame(ScreenSettings)
        

    def newEntry(self):
        set_dates_from_entry(int(self.esyear.get()),int(self.esmonth.get()),int(self.esday.get()),
                             int(self.eeyear.get()),int(self.eemonth.get()),int(self.eeday.get()))
        store_stock_data()
        self.controller.show_frame(ScreenSettings)

class ScreenSettings(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        label = ttk.Label(self,text='Specify Your Screener Settings Below',font=LARGE_FONT)
        label.grid(row=0,columnspan=14,pady=10,padx=10)

        ttk.Label(self,text='1 Day Min:',font=NORM_FONT).grid(row=1,column=0,sticky='e')
        self.dayinc1 = ttk.Entry(self,width=5)
        self.dayinc1.grid(row=1,column=1)

        ttk.Label(self,text='1 Day Max:',font=NORM_FONT).grid(row=2,column=0,sticky='e')
        self.daymax1 = ttk.Entry(self,width=5)
        self.daymax1.grid(row=2,column=1)

        ttk.Label(self,text='2 Day Min:',font=NORM_FONT).grid(row=1,column=2,sticky='e')
        self.dayinc2 = ttk.Entry(self,width=5)
        self.dayinc2.grid(row=1,column=3)

        ttk.Label(self,text='2 Day Max:',font=NORM_FONT).grid(row=2,column=2,sticky='e')
        self.daymax2 = ttk.Entry(self,width=5)
        self.daymax2.grid(row=2,column=3)

        ttk.Label(self,text='3 Day Min:',font=NORM_FONT).grid(row=1,column=4,sticky='e')
        self.dayinc3 = ttk.Entry(self,width=5)
        self.dayinc3.grid(row=1,column=5)

        ttk.Label(self,text='3 Day Max:',font=NORM_FONT).grid(row=2,column=4,sticky='e')
        self.daymax3 = ttk.Entry(self,width=5)
        self.daymax3.grid(row=2,column=5)

        ttk.Label(self,text='Gap Min:',font=NORM_FONT).grid(row=1,column=6,sticky='e')
        self.gapup = ttk.Entry(self,width=5)
        self.gapup.grid(row=1,column=7)

        ttk.Label(self,text='Gap Max:',font=NORM_FONT).grid(row=2,column=6,sticky='e')
        self.gapdown = ttk.Entry(self,width=5)
        self.gapdown.grid(row=2,column=7)

        ttk.Label(self,text='Price Min:',font=NORM_FONT).grid(row=1,column=8,sticky='e')
        self.pricemin = ttk.Entry(self,width=5)
        self.pricemin.grid(row=1,column=9)

        ttk.Label(self,text='Price Max:',font=NORM_FONT).grid(row=2,column=8,sticky='e')
        self.pricemax = ttk.Entry(self,width=5)
        self.pricemax.grid(row=2,column=9)

        ttk.Label(self,text='Volume Min:',font=NORM_FONT).grid(row=1,column=10,sticky='e')
        self.volmin = ttk.Entry(self,width=5)
        self.volmin.grid(row=1,column=11)

        ttk.Label(self,text='Volume Max:',font=NORM_FONT).grid(row=2,column=10,sticky='e')
        self.volmax = ttk.Entry(self,width=5)
        self.volmax.grid(row=2,column=11)

        self.firstred_var = tk.IntVar()
        ttk.Label(self,text='Previous Green:',font=NORM_FONT).grid(row=3,column=4,sticky='e')
        self.firstred = ttk.Checkbutton(self,variable=self.firstred_var)
        self.firstred.grid(row=3,column=5)

        self.firstgreen_var = tk.IntVar()
        ttk.Label(self,text='Previous Red:',font=NORM_FONT).grid(row=3,column=6,sticky='e')
        self.firstgreen = ttk.Checkbutton(self,variable=self.firstgreen_var)
        self.firstgreen.grid(row=3,column=7)

        self.mscreen = ttk.Button(self,text='Mega Screener',command=lambda : controller.show_frame(MegaScreen))
        self.mscreen.grid(row=4,sticky='ew',pady=5,columnspan=14)

        ttk.Label(self,width=10).grid(row=1000,column=0)
        tk.Label(self,width=10).grid(row=1000,column=2)
        tk.Label(self,width=10).grid(row=1000,column=4)
        tk.Label(self,width=10).grid(row=1000,column=6)
        tk.Label(self,width=10).grid(row=1000,column=8)

        self.go_button = ttk.Button(self,text='Commence Screening', command=lambda : self.run()).grid(row=5,sticky='ew',pady=5,columnspan=14)

        

##        day3, day4, day5, green1, red1, min price, max price
        
        

    def run(self):
        mini = -1000000000
        maxi = 1000000000
        try:
            d1min = Decimal(self.dayinc1.get())
        except InvalidOperation:
            d1min = mini
        try:
            d1max = Decimal(self.daymax1.get())
        except InvalidOperation:
            d1max = maxi
        try:
            d2min = Decimal(self.dayinc2.get())
        except InvalidOperation:
            d2min = mini
        try:
            d2max = Decimal(self.daymax2.get())
        except InvalidOperation:
            d2max = maxi
        try:
            d3min = Decimal(self.dayinc3.get())
        except InvalidOperation:
            d3min = mini
        try:
            d3max = Decimal(self.daymax3.get())
        except InvalidOperation:
            d3max = maxi
        try:
            gmin = Decimal(self.gapup.get())
        except InvalidOperation:
            gmin = mini
        try:
            gmax = Decimal(self.gapdown.get())
        except InvalidOperation:
            gmax = maxi
        try:
            pmin = Decimal(self.pricemin.get())
        except InvalidOperation:
            pmin = mini
        try:
            pmax = Decimal(self.pricemax.get())
        except InvalidOperation:
            pmax = maxi
        try:
            vmin = Decimal(self.volmin.get())*100000
        except InvalidOperation:
            vmin = 100000
        try:
            vmax = Decimal(self.volmax.get())*100000
        except InvalidOperation:
            vmax = maxi
        gr = self.firstred_var.get()
        rg = self.firstgreen_var.get()
        set_entries(d1min,d1max,d2min,d2max,d3min,d3max,gmin,gmax,pmin,pmax,vmin,vmax)
        user_input_screener(gr,rg)
        with open(files.analysis_file, newline = "") as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
               c = 0
               for row in col:
                  label = tk.Label(self, width = 10, height = 2, \
                                        text = row, relief = 'groove')
                  label.grid(row = r+6, column = c)
                  c += 1
               r += 1

class MegaScreen(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self,text='Ideal Screeners:',font=LARGE_FONT)
        label.grid(pady=10,padx=10,columnspan=20)

        tk.Label(self,text='Stocks Passed:',font=NORM_FONT).grid(row=1,sticky='e')
        self.passed = ttk.Entry(self,width=5)
        self.passed.grid(row=1,column=1)

        tk.Label(self,text='Win Percent:',font=NORM_FONT).grid(row=2,sticky='e')
        self.win = ttk.Entry(self,width=5)
        self.win.grid(row=2,column=1)

        tk.Label(self,text='Loss Percent:',font=NORM_FONT).grid(row=3,sticky='e')
        self.loss = ttk.Entry(self,width=5)
        self.loss.grid(row=3,column=1)

        ttk.Label(self,text='Average:',font=NORM_FONT).grid(row=4,sticky='e')
        self.avg = ttk.Entry(self,width=5)
        self.avg.grid(row=4,column=1)

        self.daymin1 = tk.IntVar()
        tk.Label(self,text='1 Day Screens:',font=NORM_FONT).grid(row=1,column=2,sticky='e')
        self.firstred = ttk.Checkbutton(self,variable=self.daymin1)
        self.firstred.grid(row=1,column=3)

        self.daymin2 = tk.IntVar()
        tk.Label(self,text='2 Day Screens:',font=NORM_FONT).grid(row=2,column=2,sticky='e')
        self.firstgreen = ttk.Checkbutton(self,variable=self.daymin2)
        self.firstgreen.grid(row=2,column=3)

        self.go_button = ttk.Button(self,text='Commence Screening', command=lambda : self.run()).grid(row=5,sticky='ew',pady=5,columnspan=14)

    def run(self):
        try:
            passed = Decimal(self.passed.get())
        except InvalidOperation:
            passed = 15
        try:
            win = Decimal(self.win.get())
        except InvalidOperation:
            win = 80
        try:
            loss = Decimal(self.loss.get())
        except InvalidOperation:
            loss = 20
        try:
            avg = Decimal(self.avg.get())
        except InvalidOperation:
            avg = 5
        daymin1 = self.daymin1.get()
        daymin2 = self.daymin2.get()
        
        set_ms_crit(passed,win,loss,avg)
        screener_of_screeners()
        
        with open(files.best_screens, newline = "") as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
               c = 0
               for row in col:
                  label = tk.Label(self, width = 10, height = 2, \
                                        text = row, relief = 'groove')
                  label.grid(row = r+6, column = c)
                  c += 1
               r += 1


        

app = SuperScreener()
app.mainloop()

