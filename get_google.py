import datetime as dt
from decimal import *
import numpy as np
import os
import pandas as pd
import pandas_datareader as pdr
from pandas_datareader._utils import RemoteDataError
import pickle

def get_data(folder_name,pfile_name, start_year,start_month,start_day,end_year,end_month,end_day):
    
    with open(pfile_name,'rb') as f:
        tickers = pickle.load(f)
            
    # user inputs dates
##    start_year = int(input('Start Year: '))
##    start_month = int(input('Start Month: '))
##    start_day = int(input('Start Day: '))
    start_string = str(start_year)+','+str(start_month)+','+str(start_day)
##    end_year = int(input('End Year: '))
##    end_month = int(input('End Month: '))
##    end_day = int(input('End Day: '))
    end_string = str(end_year)+','+str(end_month)+','+str(end_day)
    start = dt.datetime(start_year,start_month,start_day)
    end = dt.datetime(end_year,end_month,end_day)
    
    csv_folder = 'stock_dfs/'+start_string+' to '+end_string
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    tickers_successful = []    
    for ticker in tickers:
        if not os.path.exists(csv_folder+'/{}.csv'.format(ticker)):
            try:
                df = pdr.DataReader(ticker,'google',start,end)
                df.to_csv(csv_folder+'/{}.csv'.format(ticker))
                tickers_successful.append(ticker)
            except RemoteDataError:
                print('Unable to read Ticker: {}'.format(ticker))
        else:
            tickers_successful.append(ticker)

    with open(pfile_name,'wb') as f:
        pickle.dump(tickers_successful,f)

    pfile = folder_name+'/'+pfile_name
    percent_folder = csv_folder+'/Percents'
    with open(pfile_name,'rb') as f:
        tickers = pickle.load(f)
        
    if not os.path.exists(percent_folder):
        os.makedirs(percent_folder)
    for ticker in tickers:
        _date,_open,_high,_low,_close,_vol = np.loadtxt(csv_folder+'/{}.csv'.format(ticker),
                                                            delimiter=',',
                                                            unpack=True,
                                                            dtype='str',)

        try:
            f= open(percent_folder+'/{}.csv'.format(ticker),'w')
            headers = 'Date,Open,High,Low,Close,Volume,O/C%,Gap%,C/C%,2Days,3Days,4Days,5Days\n'
            f.write(headers)

            def base_string(i):
                pct_oc = '%.2f' %((Decimal(_close[i])-Decimal(_open[i]))/Decimal(_open[i])*100)+'%'
                base_string = _date[i]+','+_open[i]+','+_high[i]+','+_low[i]+','+_close[i]+','+_vol[i]+','+str(pct_oc)
                if i==1:
                    for j in range(1,7):
                        base_string +=',NaN'               
                return base_string
            
            def get_1day(i):
                ccs = ''
                try:
                    pct_gap = '%.2f' %(100*(Decimal(_open[i])-Decimal(_close[i-1]))/Decimal(_close[i-1]))+'%'
                except InvalidOperation:
                    pct_gap = 'NaN'
                if i>5:
                    k=6
                else:
                    k=i
                for j in range(1,k):
                    try:
                        pct_cc = '%.2f' %(100*(Decimal(_close[i])-Decimal(_close[i-j]))/Decimal(_close[i-j]))+'%'                      
                    except InvalidOperation:
                        pct_cc = 'NaN'
                    ccs += (','+str(pct_cc))
                if i < 6:
                    for l in range(i,6):
                        ccs+=',NaN' 
                                       
                day1_string = base_string(i)+','+str(pct_gap)+ccs
                return day1_string

            for i in range(1,len(_open)):
                if i==1:
                    f.write(base_string(i)+'\n')
                if 1<i<len(_open):
                    f.write(get_1day(i)+'\n')
        except (IndexError, InvalidOperation):
            print(ticker+' is retarded')
            os.remove(csv_folder+'/{}.csv'.format(ticker))
            tickers.remove(ticker)
    with open(pfile_name,'wb') as f:
        pickle.dump(tickers, f)         
    f.close()
        
    return csv_folder
