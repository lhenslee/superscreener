from alpha_vantage.timeseries import TimeSeries
from bs4 import BeautifulSoup as bs
import datetime as dt
from decimal import *
import numpy as np
import os
import pandas as pd
import pandas_datareader as pdr
from pandas_datareader._utils import RemoteDataError
import pickle
import threading
from urllib.request import urlopen as uReq
from queue import Queue

my_api = 'SJVPVKHFF14WYJ5Q'


class C:
    screen_folder = ''
    pickle_file = ''
    csv_folder = ''
    screener_csv = ''
    analysis_file = ''

# Used in setting up the list of tickers

def set_recent_screener(a,b):
    C.screen_folder = a
    C.pickle_file = b

def new_ticker_list(my_url):
    count = 1
    tickers = []
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    soup = bs(page_html,'html.parser')
    screen_name = soup.title.text.replace('Stock Screener - Overview','').title().strip()
    list_name = screen_name.replace(" ","")+'.pickle'
    C.screen_folder = 'Recent Screens/'+screen_name+'/'
    C.pickle_file = C.screen_folder+list_name
    if not os.path.exists(C.screen_folder):
        os.makedirs(C.screen_folder)
    page_classes = soup.findAll('a',{'class':'screener-pages'})
    last_page_holder = len(page_classes)-1
    last_page = page_classes[last_page_holder].text
    print('You have '+str(last_page)+' pages to go through.')

    for number in range(int(last_page)):
        my_url = my_url+'&r='+str(count)
        uClient = uReq(my_url)
        page_html = uClient.read()
        soup = bs(page_html,'html.parser')
        count+=20
        ticker_holders = soup.findAll('a',{'class':'screener-link-primary'})

        for ticker_holder in ticker_holders:
            ticker = ticker_holder.text
            tickers.append(ticker)

    with open(C.pickle_file,'wb') as f:
        pickle.dump(tickers,f)
    print(tickers)

# Used in gathering data for each ticker in the list

class V:
    Date = []
    Open = []
    High = []
    Low = []
    Close = []
    Vol = []
    

def pct_oc(i):
    return str('%.2f' %(100*(V.Close[i]-V.Open[i])/V.Open[i]))+'%'
def pct_gap(i):
    if i<1:
        return 'nan'
    else:
        return str('%.2f' %(100*(V.Open[i]-V.Close[i-1])/V.Close[i-1]))+'%'
def pct_cc(i):
    if i<1:
        return 'nan'
    else:
        return str('%.2f' %(100*(V.Close[i]-V.Close[i-1])/V.Close[i-1]))+'%'
def pct_2(i):
    if i<2:
        return 'nan'
    else:
        return str('%.2f' %(100*(V.Close[i]-V.Close[i-2])/V.Close[i-2]))+'%'
def pct_3(i):
    if i<3:
        return 'nan'
    else:
        return str('%.2f' %(100*(V.Close[i]-V.Close[i-3])/V.Close[i-3]))+'%'

def make_percents(csv_file):
    f = open(C.csv_folder+csv_file,'w')
    headers = 'Date,Open,High,Low,Close,Volume,O/C%,Gap%,C/C%,2Days,3Days+\n'
    f.write(headers)

    for i in range(len(V.Date)):
        line = (str(V.Date[i])+','+str(V.Open[i])+','+str(V.High[i])+','+str(V.Low[i])+','+str(V.Close[i])+','+
                str(V.Vol[i])+','+pct_oc(i)+','+pct_gap(i)+','+pct_cc(i)+','+pct_2(i)+','+pct_3(i)+'\n')
        f.write(line)
    f.close()

def get_data(start_year,start_month,start_day,end_year,end_month,end_day):
    with open(C.pickle_file,'rb') as f:
        tickers = pickle.load(f)

    start_string = str(start_year)+'-'+str(start_month)+'-'+str(start_day)
    end_string = str(end_year)+'-'+str(end_month)+'-'+str(end_day)
    start = dt.datetime(start_year,start_month,start_day)
    end = dt.datetime(end_year,end_month,end_day)

    C.csv_folder = 'stock_dfs/'+start_string+' to '+end_string+'/'
    if not os.path.exists(C.csv_folder):
        os.makedirs(C.csv_folder)
    for ticker in tickers:
        csv_file = ticker+'.csv'
        if not os.path.exists(C.csv_folder+csv_file):
            try:
                df = pdr.DataReader(ticker,'google',start,end).reset_index()
                V.Date = df['Date']
                V.Open = df['Open']
                V.High = df['High']
                V.Low = df['Low']
                V.Close = df['Close']
                V.Vol = df['Volume']
                make_percents(csv_file)              
            except RemoteDataError:
                print('Unable to read '+ticker)
                tickers.remove(ticker)
    with open(C.pickle_file,'wb') as f:
        pickle.dump(tickers,f)

''' This screener takes screen criteria that the user inputs
    into the GUI.'''

class S:
    Date,Open,High,Low,Close,Vol,oc,gap,cc,cc2,cc3 = ([] for i in range(11))
    (d1min,d1max,d2min,d2max,d3min,d3max,
     gmin,gmax,pmin,pmax,vmin,vmax) = ('' for i in range(12))
    oo2ar,oc2ar,ocar,ccar,cc2ar,gapar =([] for i in range(6))

def set_entries(d1min,d1max,d2min,d2max,d3min,d3max,gmin,gmax,pmin,pmax,vmin,vmax):
    S.d1min = d1min
    S.d1max = d1max
    S.d2min = d2min
    S.d2max = d2max
    S.d3min = d3min
    S.d3max = d3max
    S.gmin = gmin
    S.gmax = gmax
    S.pmin = pmin
    S.pmax = pmax
    S.vmin = vmin
    S.vmax = vmax

def big_nan(var):
    pos = str(1000000000000)
    return Decimal(var.replace('%','').replace('nan',pos))
def small_nan(var):
    neg = str(-1000000000000)
    return Decimal(var.replace('%','').replace('nan',neg))
def makeD(var):
    return Decimal(var.replace('%',''))

def comb_screens(f,ticker):
    for i in range(1,len(S.Date)-2):
        if (small_nan(S.cc[i])>S.d1min and big_nan(S.cc[i])<S.d1max and
            small_nan(S.cc2[i])>S.d2min and big_nan(S.cc2[i])<S.d2max and
            small_nan(S.cc3[i])>S.d3min and big_nan(S.cc3[i])<S.d2max and
            small_nan(S.gap[i+1])>S.gmin and big_nan(S.gap[i+1])<S.gmax and
            small_nan(S.Open[i])>S.pmin and big_nan(S.Open[i])<S.pmax and
            small_nan(S.Vol[i])>S.vmin and big_nan(S.Vol[i])<S.pmax):
            oc2 = str('%.2f' %(100*(makeD(S.Close[i+2])-makeD(S.Open[i+1]))/makeD(S.Open[i+1])))+'%'
            oo2 = str('%.2f' %(100*(makeD(S.Open[i+2])-makeD(S.Open[i+1]))/makeD(S.Open[i+1])))+'%'
            S.oo2ar.append(oo2)
            S.oc2ar.append(oc2)
            S.ocar.append(S.oc[i+1])
            S.ccar.append(S.cc[i+1])
            S.cc2ar.append(S.cc[i+2])
            S.gapar.append(S.gap[i+1])
            line = (ticker+','+S.Date[i]+','+S.Open[i]+','+S.High[i]+','+S.Low[i]+','+
                    S.Close[i]+','+S.Vol[i]+','+S.oc[i]+','+S.gap[i]+','+S.cc[i]+','+S.cc2[i]+
                    ','+S.cc3[i]+',,'+S.Open[i+1]+','+S.High[i+1]+','+S.Low[i+1]+','+S.Close[i+1]+
                    ','+S.Vol[i+1]+',,'+S.oc[i+1]+','+oo2+','+oc2+','+S.cc[i+1]+','+
                    S.cc[i+2]+','+S.gap[i+1]+'\n')
            f.write(line)
def firstred(f,ticker):
    for i in range(1,len(S.Date)-2):
        if (small_nan(S.cc[i])>S.d1min and big_nan(S.cc[i])<S.d1max and
            small_nan(S.cc2[i])>S.d2min and big_nan(S.cc2[i])<S.d2max and
            small_nan(S.cc3[i])>S.d3min and big_nan(S.cc3[i])<S.d2max and
            small_nan(S.gap[i+1])>S.gmin and big_nan(S.gap[i+1])<S.gmax and
            small_nan(S.Open[i])>S.pmin and big_nan(S.Open[i])<S.pmax and
            small_nan(S.Vol[i])>S.vmin and big_nan(S.Vol[i])<S.pmax and
            small_nan(S.cc[i-1])>0):
            oc2 = str('%.2f' %(100*(makeD(S.Close[i+2])-makeD(S.Open[i+1]))/makeD(S.Open[i+1])))+'%'
            oo2 = str('%.2f' %(100*(makeD(S.Open[i+2])-makeD(S.Open[i+1]))/makeD(S.Open[i+1])))+'%'
            S.oo2ar.append(oo2)
            S.oc2ar.append(oc2)
            S.ocar.append(S.oc[i+1])
            S.ccar.append(S.cc[i+1])
            S.cc2ar.append(S.cc[i+2])
            S.gapar.append(S.gap[i+1])
            line = (ticker+','+S.Date[i]+','+S.Open[i]+','+S.High[i]+','+S.Low[i]+','+
                    S.Close[i]+','+S.Vol[i]+','+S.oc[i]+','+S.gap[i]+','+S.cc[i]+','+S.cc2[i]+
                    ','+S.cc3[i]+',,'+S.Open[i+1]+','+S.High[i+1]+','+S.Low[i+1]+','+S.Close[i+1]+
                    ','+S.Vol[i+1]+',,'+S.oc[i+1]+','+oo2+','+oc2+','+S.cc[i+1]+','+
                    S.cc[i+2]+','+S.gap[i+1]+'\n')
            f.write(line)
def firstgreen(f,ticker):
    for i in range(1,len(S.Date)-2):
        if (small_nan(S.cc[i])>S.d1min and big_nan(S.cc[i])<S.d1max and
            small_nan(S.cc2[i])>S.d2min and big_nan(S.cc2[i])<S.d2max and
            small_nan(S.cc3[i])>S.d3min and big_nan(S.cc3[i])<S.d2max and
            small_nan(S.gap[i+1])>S.gmin and big_nan(S.gap[i+1])<S.gmax and
            small_nan(S.Open[i])>S.pmin and big_nan(S.Open[i])<S.pmax and
            small_nan(S.Vol[i])>S.vmin and big_nan(S.Vol[i])<S.pmax and
            big_nan(S.cc[i-1])<0):
            oc2 = str('%.2f' %(100*(makeD(S.Close[i+2])-makeD(S.Open[i+1]))/makeD(S.Open[i+1])))+'%'
            oo2 = str('%.2f' %(100*(makeD(S.Open[i+2])-makeD(S.Open[i+1]))/makeD(S.Open[i+1])))+'%'
            S.oo2ar.append(oo2)
            S.oc2ar.append(oc2)
            S.ocar.append(S.oc[i+1])
            S.ccar.append(S.cc[i+1])
            S.cc2ar.append(S.cc[i+2])
            S.gapar.append(S.gap[i+1])
            line = (ticker+','+S.Date[i]+','+S.Open[i]+','+S.High[i]+','+S.Low[i]+','+
                    S.Close[i]+','+S.Vol[i]+','+S.oc[i]+','+S.gap[i]+','+S.cc[i]+','+S.cc2[i]+
                    ','+S.cc3[i]+',,'+S.Open[i+1]+','+S.High[i+1]+','+S.Low[i+1]+','+S.Close[i+1]+
                    ','+S.Vol[i+1]+',,'+S.oc[i+1]+','+oo2+','+oc2+','+S.cc[i+1]+','+
                    S.cc[i+2]+','+S.gap[i+1]+'\n')
            f.write(line)

def analysis(col):
    total = len(col)
    win_count = 0
    sums = 0
    sumdown = 0
    sumup = 0
    for i in range(total):
        sums+=makeD(col[i])
        if makeD(col[i])<0:
            sumdown+=makeD(col[i])
        if makeD(col[i])>0:
            win_count+=1
            sumup+=makeD(col[i])
    win_percent = str('%.2f' %(win_count/total*100))+'%'
    avgdown = str('%.2f' %(sumdown/total))+'%'
    avgup = str('%.2f' %(sumup/total))+'%'
    avg = str('%.2f' %(sums/total))
    return (win_percent, avgup, str(sumup)+'%', avgdown, str(sumdown)+'%', avg, str(sums)+
            '%', (','.join([win_percent, avgup, str(sumup)+'%', avgdown, str(sumdown)+'%', avg, str(sums)+
            '%\n'])))

def screener_analysis():
    C.analysis_file = C.screen_folder+'analysis.csv'
    f = open(C.analysis_file,'w')
    file = ('Strats,Win%,Avg Up,Sum Up,Avg Down,Sum Down,Avg,Sum,'+str(len(S.ocar))+' Passed'+'\n'+
            'O/C,'+analysis(S.ocar)[7]+'O/O2,'+analysis(S.oo2ar)[7]+'O/C2,'+analysis(S.oc2ar)[7]+'C/C,'+analysis(S.ccar)[7]+
            'C/C2,'+analysis(S.cc2ar)[7]+'Gap,'+analysis(S.gapar)[7])
    f.write(file)
    f.close()
    

def screener(gr,rg):
    S.oo2ar,S.oc2ar,S.ocar,S.ccar,S.cc2ar,S.gapar =([] for i in range(6))
    C.screener_csv = C.screen_folder+'screener.csv'
    with open(C.pickle_file,'rb') as f:
        tickers = pickle.load(f)
    f = open(C.screener_csv,'w')
    headers = ('Ticker,Date,Open,High,Low,Close,Volume,O/C,Gap,C/C,2Days,3Days,Day2'+
               ',Open,High,Low,Close,Volume,Srats,O1/C1,O/O2,O1/C2,C/C1,C1/C2,Gap\n')
    f.write(headers)
    for ticker in tickers:
        try:
            (S.Date,S.Open,S.High,S.Low,S.Close,S.Vol,S.oc,
             S.gap,S.cc,S.cc2,S.cc3) = np.loadtxt(C.csv_folder+ticker+'.csv',
                                                  delimiter=',',
                                                  unpack=True,
                                                  dtype='str')
            if gr==1 and rg==0:
                firstred(f,ticker)
            if gr==0 and rg==1:
                firstgreen(f,ticker)
            if gr==1 and rg==1:
                pass
            if gr==0 and rg==0:
                comb_screens(f,ticker)
        except InvalidOperation:
            print(ticker+' was banned for being empty')
            tickers.remove(ticker)       
    f.close()
    screener_analysis()
    with open(C.pickle_file,'wb') as f:
        pickle.dump(tickers,f)
    return C.analysis_file

'''
This is the screener of every combination of screeners. A screen will be ran
for each input for the screener function. The user can identify stocks needed
to pass the screen, winning percent, and the average needed for the screen
strategy to appear. The user close on the first, second and third day. User may
specify the previous day as a positive or negative. User can decide whether or
not gap ups are involved in checking the strategies as well.
'''

class ms:
    stocks_passed = 15
    win_needed = 80
    loss_needed = 20
    avg_needed = 5
    numbers = [0,5,10,15,20]
    line_1day = []
    tickers = []
    volume = 10000

def set_ms_crit(passed,win,loss,avg):
    ms.line_1day = []
    ms.stocks_passed = passed
    ms.win_needed = win
    ms.loss_needed = loss
    ms.avg_needed = avg

def single_day_screen(d1min):
    (S.oo2ar,S.oc2ar,S.ocar,S.ccar,S.cc2ar,S.gapar) =([] for i in range(6))
    for ticker in ms.tickers:
        try:
            (S.Date,S.Open,S.High,S.Low,S.Close,S.Vol,S.oc,
             S.gap,S.cc,S.cc2,S.cc3) = np.loadtxt(C.csv_folder+ticker+'.csv',
                                                  delimiter=',',
                                                  unpack=True,
                                                  dtype='str')
            for i in range(1,len(S.Date)-2):
                if small_nan(S.cc[i])>d1min:
                    oc2 = str('%.2f' %(100*(makeD(S.Close[i+2])-makeD(S.Open[i+1]))/makeD(S.Open[i+1])))+'%'
                    oo2 = str('%.2f' %(100*(makeD(S.Open[i+2])-makeD(S.Open[i+1]))/makeD(S.Open[i+1])))+'%'
                    S.oo2ar.append(oo2)
                    S.oc2ar.append(oc2)
                    S.ocar.append(S.oc[i+1])
                    S.ccar.append(S.cc[i+1])
                    S.cc2ar.append(S.cc[i+2])
                    S.gapar.append(S.gap[i+1])
                    strats = ['O/O2','O/C2','O/C','C/C1','C/C2','Gap']
                    count = 0
                    for x in [S.oo2ar,S.oc2ar,S.ocar,S.ccar,S.cc2ar,S.gapar]:
                        temp = analysis(x)
                        if (makeD(temp[0])>ms.win_needed and makeD(temp[5])>ms.avg_needed and len(S.ocar)>ms.stocks_passed or
                            makeD(temp[0])<ms.loss_needed and makeD(temp[5])<-ms.avg_needed and len(S.ocar)>ms.stocks_passed):
                            ms.line_1day.append(','.join([strats[count], str(d1min)+'%', temp[0], temp[5], temp[6], str(len(S.ocar))]))
                        count+=1
                        
        except (InvalidOperation, FileNotFoundError):
            print(ticker+' was banned for being empty')
            ms.tickers.remove(ticker)

def print_strats():
    with open(C.pickle_file,'rb') as f:
        ms.tickers = pickle.load(f)
    C.best_screens_file = C.screen_folder+'bestscreens.csv'
    f = open(C.best_screens_file,'w')
    f.write('Strat,1Day min,Win%,Avg,Sum,Passed\n')
    for d1min in ms.numbers:
        single_day_screen(d1min)
    file = '\n'.join(ms.line_1day)
    f.write(file)
    f.close()
    with open(C.pickle_file,'wb') as f:
        pickle.dump(ms.tickers,f)
    return C.best_screens_file


        



    
