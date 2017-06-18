import csv
from decimal import *
import get_google as gg
import pandas as pd
import tkinter as tk
from tkinter import ttk
import save_tickers as st
import screener_settings as ss
import os


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

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self,default='rari.ico')
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
        button2 = ttk.Button(self,text='Enter New Screener',
                             command = lambda : controller.show_frame(NewScreen))
        
        self.button = {}
        for i in (range(len(SuperScreener.prev_screens))):
            self.button[i] = ttk.Button(self,text=SuperScreener.prev_screens[i], command = lambda i=i : self.onclick(i))
            self.button[i].pack()
        button2.pack()
        

    def onclick(self,i):
        SuperScreener.screen_folder='Recent Screens/'+SuperScreener.prev_screens[i]
        SuperScreener.pickle_file = SuperScreener.screen_folder+'/'+SuperScreener.prev_screens[i].replace(" ","")+'.pickle'        
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
        temp = st.save_tickers(self.entry.get())
        SuperScreener.screen_folder = 'Recent Screens/'+temp[0]
        SuperScreener.pickle_file = SuperScreener.screen_folder+'/'+temp[1]
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
    
        self.esyear = tk.Entry(self,width=5)
        self.esyear.grid(row=1,column=1)
        self.esmonth = tk.Entry(self,width=5)
        self.esmonth.grid(row=2,column=1)
        self.esday = tk.Entry(self,width=5)
        self.esday.grid(row=3,column=1)
        self.eeyear = tk.Entry(self,width=5)
        self.eeyear.grid(row=1,column=3)
        self.eemonth = tk.Entry(self,width=5)
        self.eemonth.grid(row=2,column=3)
        self.eeday = tk.Entry(self,width=5)
        self.eeday.grid(row=3,column=3)

        tk.Label(self,text='Recent Date Entries',font=NORM_FONT).grid(row=4,columnspan=4,pady=5)

        self.button = {}
        for i in (range(len(SuperScreener.prev_dates))):
            self.button[i] = ttk.Button(self,text=SuperScreener.prev_dates[i], command = lambda i=i : self.onclick(i))
            self.button[i].grid(row=5+i,column=0,columnspan=4)

        self.button1 = ttk.Button(self,text='Enter Dates',command = lambda : self.newEntry())
        self.button1.grid(row=1,rowspan=3,column=4)
        
    def onclick(self,i):
        SuperScreener.csv_folder = 'stock_dfs/'+SuperScreener.prev_dates[i]
        SuperScreener.percent_folder = SuperScreener.csv_folder+'/'+'Percents/'
        self.controller.show_frame(ScreenSettings)
        

    def newEntry(self):
        SuperScreener.csv_folder = 'stock_dfs/'+gg.get_data(SuperScreener.screen_folder,SuperScreener.pickle_file,int(self.esyear.get()),
                                               int(self.esmonth.get()),int(self.esday.get()),int(self.eeyear.get()),
                                               int(self.eemonth.get()),int(self.eeday.get()))
        SuperScreener.percent_folder = SuperScreener.csv_folder+'/'+'Percents/'
        self.controller.show_frame(ScreenSettings)

class ScreenSettings(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        label = tk.Label(self,text='Specify Your Screener Settings Below',font=LARGE_FONT)
        label.grid(row=0,columnspan=14,pady=10,padx=10)

        tk.Label(self,text='1 Day Min:',font=NORM_FONT).grid(row=1,column=0,sticky='e')
        self.dayinc1 = tk.Entry(self,width=5)
        self.dayinc1.grid(row=1,column=1)

        tk.Label(self,text='1 Day Max:',font=NORM_FONT).grid(row=2,column=0,sticky='e')
        self.daymax1 = tk.Entry(self,width=5)
        self.daymax1.grid(row=2,column=1)

        tk.Label(self,text='2 Day Min:',font=NORM_FONT).grid(row=1,column=2,sticky='e')
        self.dayinc2 = tk.Entry(self,width=5)
        self.dayinc2.grid(row=1,column=3)

        tk.Label(self,text='2 Day Max:',font=NORM_FONT).grid(row=2,column=2,sticky='e')
        self.daymax2 = tk.Entry(self,width=5)
        self.daymax2.grid(row=2,column=3)

        tk.Label(self,text='3 Day Min:',font=NORM_FONT).grid(row=1,column=4,sticky='e')
        self.dayinc3 = tk.Entry(self,width=5)
        self.dayinc3.grid(row=1,column=5)

        tk.Label(self,text='3 Day Max:',font=NORM_FONT).grid(row=2,column=4,sticky='e')
        self.daymax3 = tk.Entry(self,width=5)
        self.daymax3.grid(row=2,column=5)

        tk.Label(self,text='Gap Min:',font=NORM_FONT).grid(row=1,column=6,sticky='e')
        self.gapup = tk.Entry(self,width=5)
        self.gapup.grid(row=1,column=7)

        tk.Label(self,text='Gap Max:',font=NORM_FONT).grid(row=2,column=6,sticky='e')
        self.gapdown = tk.Entry(self,width=5)
        self.gapdown.grid(row=2,column=7)

        tk.Label(self,text='First Red Day:',font=NORM_FONT).grid(row=1,column=8,sticky='e')
        self.firstred = tk.Entry(self,width=5)
        self.firstred.grid(row=1,column=9)

        tk.Label(self,text='First Green Day:',font=NORM_FONT).grid(row=2,column=8,sticky='e')
        self.firstgreen = tk.Entry(self,width=5)
        self.firstgreen.grid(row=2,column=9)

        tk.Label(self,text='Price Min:',font=NORM_FONT).grid(row=1,column=10,sticky='e')
        self.pricemin = tk.Entry(self,width=5)
        self.pricemin.grid(row=1,column=11)

        tk.Label(self,text='Price Max:',font=NORM_FONT).grid(row=2,column=10,sticky='e')
        self.pricemax = tk.Entry(self,width=5)
        self.pricemax.grid(row=2,column=11)

        tk.Label(self,text='Volume Min:',font=NORM_FONT).grid(row=1,column=12,sticky='e')
        self.volmin = tk.Entry(self,width=5)
        self.volmin.grid(row=1,column=13)

        tk.Label(self,text='Volume Max:',font=NORM_FONT).grid(row=2,column=12,sticky='e')
        self.volmax = tk.Entry(self,width=5)
        self.volmax.grid(row=2,column=13)

        self.mscreen = ttk.Button(self,text='Mega Screener',command=lambda : controller.show_frame(MegaScreen))
        self.mscreen.grid(row=3,sticky='ew',pady=5,columnspan=14)

        tk.Label(self,width=10).grid(row=1000,column=0)
        tk.Label(self,width=10).grid(row=1000,column=2)
        tk.Label(self,width=10).grid(row=1000,column=4)
        tk.Label(self,width=10).grid(row=1000,column=6)
        tk.Label(self,width=10).grid(row=1000,column=8)

        self.go_button = ttk.Button(self,text='Commence Screening', command=lambda : self.run()).grid(row=4,sticky='ew',pady=5,columnspan=14)

        

##        day3, day4, day5, green1, red1, min price, max price
        
        

    def run(self):
        mini = -10000000000
        maxi = 10000000000
        try:
            d1 = Decimal(self.dayinc1.get())
        except InvalidOperation:
            d1 = mini
        try:
            dm1 = Decimal(self.daymax1.get())
        except InvalidOperation:
            dm1 = maxi
        try:
            d2 = Decimal(self.dayinc2.get())
        except InvalidOperation:
            d2 = mini
        try:
            dm2 = Decimal(self.daymax2.get())
        except InvalidOperation:
            dm2 = maxi
        try:
            d3 = Decimal(self.dayinc3.get())
        except InvalidOperation:
            d3 = mini
        try:
            dm3 = Decimal(self.daymax3.get())
        except InvalidOperation:
            dm3 = maxi
        try:
            g = Decimal(self.gapup.get())
        except InvalidOperation:
            g = mini
        try:
            gm = Decimal(self.gapdown.get())
        except InvalidOperation:
            gm = maxi
        try:
            gr = Decimal(self.firstred.get())
        except InvalidOperation:
            gr = maxi
        try:
            rg = Decimal(self.firstgreen.get())
        except InvalidOperation:
            rg = mini
        try:
            p = Decimal(self.pricemin.get())
        except InvalidOperation:
            p = mini
        try:
            pm = Decimal(self.pricemax.get())
        except InvalidOperation:
            pm = maxi
        try:
            v = Decimal(self.volmin.get())
        except InvalidOperation:
            v = 100000
        try:
            vm = Decimal(self.volmax.get())
        except InvalidOperation:
            vm = maxi
        temp = ss.screener(SuperScreener.screen_folder,SuperScreener.percent_folder,SuperScreener.pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
        SuperScreener.fscreener = temp[0]
        SuperScreener.fanalysis = temp[1]
        with open(SuperScreener.fanalysis, newline = "") as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
               c = 0
               for row in col:
                  label = tk.Label(self, width = 10, height = 2, \
                                        text = row, relief = 'groove')
                  label.grid(row = r+5, column = c)
                  c += 1
               r += 1

class MegaScreen(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text='Ideal Screeners',font=LARGE_FONT)
        label.grid(pady=10,padx=10,columnspan=20)

        self.go_button = ttk.Button(self,text='Commence Screening', command=lambda : self.run()).grid(row=4,sticky='ew',pady=5,columnspan=14)



        

app = SuperScreener()
app.mainloop()

