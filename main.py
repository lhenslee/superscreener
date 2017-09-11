from bs4 import BeautifulSoup as bs
from functions import *
import pandas as pd
import numpy as np
import os
import pandas_datareader as pdr
from pandas_datareader._utils import RemoteDataError
import pickle
from urllib.request import urlopen as uReq


def new_ticker_list(my_url):
    count = 1
    tickers = []
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    soup = bs(page_html,'html.parser')
    screen_name = soup.title.text.replace('Stock Screener - Overview','').title().strip()
    make_screener_files(screen_name)
    if not os.path.exists(files.screen_folder):
        os.makedirs(files.screen_folder)
    page_classes = soup.findAll('a', {'class' : 'screener-pages'})
    last_page_holder = len(page_classes)-1
    last_page = page_classes[last_page_holder].text

    for number in range(int(last_page)):
        my_url = my_url + '&r=' + str(count)
        uClient = uReq(my_url)
        page_html = uClient.read()
        soup = bs(page_html,'html.parser')
        count += 20
        ticker_holders = soup.findAll('a',{'class':'screener-link-primary'})

        for ticker_holder in ticker_holders:
            ticker = ticker_holder.text
            tickers.append(ticker)
            
    with open(files.ticker_list, 'wb') as f:
        pickle.dump(tickers, f)

def store_stock_data():
    with open(files.ticker_list, 'rb') as f:
        tickers = pickle.load(f)

    for ticker in tickers:
        
        if not os.path.exists(files.csv_folder + ticker + '.csv'):
            try:
                f = open(files.csv_folder + ticker + '.csv', 'w')
                f.write('Date,Open,High,Low,Close,Volume,O/C,Gap,C/C,2Days,3Days,Strats,O/O2,O/C2,O/C,C/C,C/C2,Gap\n')
                df = pdr.DataReader(ticker, 'google', data.start, data.end).reset_index()
                data.Date = df['Date']
                data.Open = df['Open']
                data.High = df['High']
                data.Low = df['Low']
                data.Close = df['Close']
                data.Vol = df['Volume']
                for i in range(3, len(data.Date)-2):
                    line = get_base_line(i) + ',' + get_percents_line(i) + '\n'
                    f.write(line)
                f.close()
            except RemoteDataError:
                print(ticker + ' was banned by le RemoteDataError')
                tickers.remove(ticker)
    with open(files.ticker_list, 'wb') as f:
        pickle.dump(tickers, f)

def user_input_screener(prev_red, prev_green):
    clear_strats()
    with open(files.ticker_list, 'rb') as f:
        tickers = pickle.load(f)
    f = open(files.screener_file, 'w')
    f.write('Ticker,Date,Open,High,Low,Close,Volume,O/C,Gap,C/C,2Days,3Days,Day2,' +
            'Open,High,Low,Close,Volume,Strats,O/C,O/O2,O/C2,C/C,C/C2,Gap\n')
    for ticker in tickers:
        try:
            arr = np.loadtxt(files.csv_folder + ticker + '.csv',
                             delimiter = ',',
                             unpack = True,
                             dtype = 'str')
            set_screen_basics(arr)
            if prev_red == 0 and prev_green == 0:
                basic_screen(f, ticker)
            if prev_red == 1 and prev_green == 0:
                red_screen(f, ticker)
            if prev_red == 0 and prev_green == 1:
                green_screen(f, ticker)
            else:
                pass
        except InvalidOperation:
            print(ticker + ' was banned for bad info')
            #tickers.remove(ticker)
    f.close()
    f = open(files.analysis_file, 'w')
    f.write('Strats,Win%,Avg Up,Sum Up,Avg Down,Sum Down,Avg,Sum' + ',' + str(len(screen.soo2s)) + '\n')
    f.write(analysis())
    f.close()
##    with open(files.ticker_list, 'wb') as f:
##        pickle.dump(ticker, f)

def screener_of_screeners():
    with open(files.ticker_list, 'rb') as f:
        tickers = pickle.load(f)
    f = open(files.best_screens, 'w')
    f.write('Strat,1Day Min,Win%,Avg,Sum,Passed\n')
    for d1min in ms.numbers:
        clear_strats()
        for ticker in tickers:
        #try:
            arr = np.loadtxt(files.csv_folder + ticker + '.csv',
                             delimiter = ',',
                             unpack = True,
                             dtype = 'str')
            set_screen_basics(arr)
            d1min_screen(d1min)
        ms_analysis(f, d1min)
    #except InvalidOperation:
        #print(ticker + ' was banned for bad info')
        #tickers.remove(ticker)
    
    f.close()





























