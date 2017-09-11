import datetime as dt
from decimal import *
import os
import math


class files:
    screen_folder = ''
    ticker_list = ''
    csv_folder = ''
    analysis_file = ''
    screener_file = ''
    analysis_file = ''
    best_screens = ''

def make_screener_files(var):
    files.screen_folder = 'recent_screens/' + var + '/'
    files.ticker_list = files.screen_folder + 'tickers.pickle'
    files.analysis_file = files.screen_folder + 'analysis.csv'
    files.screener_file = files.screen_folder + 'screener.csv'
    files.best_screens = files.screen_folder + 'best_screens.csv'


class data:
    (Date, Open, High, Low, Close, Vol) = ([] for i in range(6))
    start_string = ''
    end_string = ''
    start = None 
    end = None

def set_dates_from_entry(start_year, start_month, start_day, end_year, end_month, end_day):
    data.start_string = str(start_year) + '-' + str(start_month) + '-' + str(start_day)
    data.end_string = str(end_year) + '-' + str(end_month) + '-' + str(end_day)
    data.start = dt.datetime(start_year, start_month, start_day)
    data.end = dt.datetime(end_year, end_month, end_day)
    files.csv_folder = 'stock_data/' + data.start_string + ' to ' + data.end_string + '/'
    if not os.path.exists(files.csv_folder):
        os.makedirs(files.csv_folder)

def set_dates_from_prev(file):
    dates = [int(s) for s in file.replace('-',' ').replace('/',' ').split() if s.isdigit()]
    data.start_string = '-'.join(str(dates[0:2]))
    data.end_string = '-'.join(str(dates[3:5]))
    data.start = dt.datetime(dates[0], dates[1], dates[2])
    data.end = dt.datetime(dates[3], dates[4], dates[5])
    files.csv_folder = 'stock_data/' + file + '/'

def makeD(var):
    return Decimal(var.replace('%', ''))

def get_base_line(i):
    return ','.join([str(data.Date[i]), str(data.Open[i]), str(data.High[i]),
                     str(data.Low[i]), str(data.Close[i]), str(data.Vol[i])])

def get_percents_line(i):
    pct_oc = str('%.2f' %(100*(data.Close[i]-data.Open[i])/data.Open[i])) + '%'
    pct_gap = str('%.2f' %(100*(data.Open[i]-data.Close[i-1])/data.Close[i-1])) + '%'
    pct_cc = str('%.2f' %(100*(data.Close[i]-data.Close[i-1])/data.Close[i-1])) + '%'
    pct_2 = str('%.2f' %(100*(data.Close[i]-data.Close[i-2])/data.Close[i-2])) + '%'
    pct_3 = str('%.2f' %(100*(data.Close[i]-data.Close[i-3])/data.Close[i-3])) + '%'
    oo2 = str('%.2f' %(100*(data.Open[i+2]-data.Open[i+1])/data.Open[i+1])) + '%'
    oc2 = str('%.2f' %(100*(data.Close[i+2]-data.Open[i+1])/data.Open[i+1])) + '%'
    ocd2 = str('%.2f' %(100*(data.Close[i+1]-data.Open[i+1])/data.Open[i+1])) + '%'
    ccd2 = str('%.2f' %(100*(data.Close[i+1]-data.Close[i])/data.Close[i])) + '%'
    ccd3 = str('%.2f' %(100*(data.Close[i+2]-data.Close[i+1])/data.Close[i+1])) + '%'
    gapd2 = str('%.2f' %(100*(data.Open[i+1]-data.Close[i])/data.Close[i])) + '%'
    return ','.join([pct_oc, pct_gap, pct_cc, pct_2, pct_3]) + ',,' + ','.join([oo2, oc2, ocd2, ccd2, ccd3, gapd2])


class screen:
    (Date, Open, High, Low, Close, Vol, oc,
     gap, cc, cc2, cc3, oo2s, oc2s, ocs,
     ccs, cc2s, gaps) = ([] for i in range(17))
    (d1min, d1max, d2min, d2max, d3min, d3max, gmin, gmax, pmin, pmax,
     vmin, vmax) = ('' for i in range(12))
    soo2s, soc2s, socs, sccs, scc2s, sgaps = ([] for i in range(6))

def makeD(var):
    return Decimal(var.replace('%', ''))

def clear_strats():
    screen.soo2s, screen.soc2s, screen.socs, screen.sccs, screen.scc2s, screen.sgaps = ([] for i in range(6))

def set_entries(d1min,d1max,d2min,d2max,d3min,d3max,gmin,gmax,pmin,pmax,vmin,vmax):
    screen.d1min = d1min
    screen.d1max = d1max
    screen.d2min = d2min
    screen.d2max = d2max
    screen.d3min = d3min
    screen.d3max = d3max
    screen.gmin = gmin
    screen.gmax = gmax
    screen.pmin = pmin
    screen.pmax = pmax
    screen.vmin = vmin
    screen.vmax = vmax

def set_screen_basics(arr):
    (screen.Date, screen.Open, screen.High, screen.Low, screen.Close, screen.Vol, screen.oc,
     screen.gap, screen.cc, screen.cc2, screen.cc3, screen.oo2s, screen.oc2s, screen.ocs,
     screen.ccs, screen.cc2s, screen.gaps) = ([] for i in range(17))
    screen.Date = arr[0]
    screen.Open = arr[1]
    screen.High = arr[2]
    screen.Low = arr[3]
    screen.Close = arr[4]
    screen.Vol = arr[5]
    screen.oc = arr[6]
    screen.gap = arr[7]
    screen.cc = arr[8]
    screen.cc2 = arr[9]
    screen.cc3 = arr[10]
    screen.oo2s = arr[12]
    screen.oc2s = arr[13]
    screen.ocs = arr[14]
    screen.ccs = arr[15]
    screen.cc2s = arr[16]
    screen.gaps = arr[17]

def basic_screen(f, ticker):
    for i in range(1, len(screen.Date)-1):
        if (makeD(screen.cc[i])>screen.d1min and makeD(screen.cc[i])<screen.d1max and
            makeD(screen.cc2[i])>screen.d2min and makeD(screen.cc2[i])<screen.d2max and
            makeD(screen.cc3[i])>screen.d3min and makeD(screen.cc3[i])<screen.d3max and
            makeD(screen.gaps[i])>screen.gmin and makeD(screen.gaps[i])<screen.gmax and
            makeD(screen.Open[i])>screen.pmin and makeD(screen.Open[i])<screen.pmax and
            makeD(screen.Vol[i])>screen.vmin and makeD(screen.Vol[i])<screen.vmax):
            day1 = ','.join([ticker, screen.Date[i], screen.Open[i], screen.High[i], screen.Low[i], screen.Close[i],
                             screen.Vol[i], screen.oc[i], screen.gap[i], screen.cc[i], screen.cc2[i], screen.cc2[i]])
            day2 = ','.join([screen.Open[i+1], screen.High[i+1], screen.Low[i+1], screen.Close[i+1], screen.Vol[i+1]])
            strats = ','.join([screen.ocs[i], screen.oo2s[i], screen.oc2s[i], screen.ccs[i], screen.cc2s[i], screen.gaps[i]])
            f.write(',,'.join([day1, day2, strats]) + '\n')
            screen.socs.append(screen.ocs[i])
            screen.soo2s.append(screen.oo2s[i])
            screen.soc2s.append(screen.oc2s[i])
            screen.sccs.append(screen.ccs[i])
            screen.scc2s.append(screen.cc2s[i])
            screen.sgaps.append(screen.gaps[i])

def green_screen(f, ticker):
    for i in range(2, len(screen.Date)-1):
        if (makeD(screen.cc[i])>screen.d1min and makeD(screen.cc[i])<screen.d1max and
            makeD(screen.cc2[i])>screen.d2min and makeD(screen.cc2[i])<screen.d2max and
            makeD(screen.cc3[i])>screen.d3min and makeD(screen.cc3[i])<screen.d3max and
            makeD(screen.gaps[i])>screen.gmin and makeD(screen.gaps[i])<screen.gmax and
            makeD(screen.Open[i])>screen.pmin and makeD(screen.Open[i])<screen.pmax and
            makeD(screen.Vol[i])>screen.vmin and makeD(screen.Vol[i])<screen.vmax and
            makeD(screen.cc[i-1])>0):
            day1 = ','.join([ticker, screen.Date[i], screen.Open[i], screen.High[i], screen.Low[i], screen.Close[i],
                             screen.Vol[i], screen.oc[i], screen.gap[i], screen.cc[i], screen.cc2[i], screen.cc2[i]])
            day2 = ','.join([screen.Open[i+1], screen.High[i+1], screen.Low[i+1], screen.Close[i+1], screen.Vol[i+1]])
            strats = ','.join([screen.ocs[i], screen.oo2s[i], screen.oc2s[i], screen.ccs[i], screen.cc2s[i], screen.gaps[i]])
            f.write(',,'.join([day1, day2, strats]) + '\n')
            screen.socs.append(screen.ocs[i])
            screen.soo2s.append(screen.oo2s[i])
            screen.soc2s.append(screen.oc2s[i])
            screen.sccs.append(screen.ccs[i])
            screen.scc2s.append(screen.cc2s[i])
            screen.sgaps.append(screen.gaps[i])

def red_screen(f, ticker):
    for i in range(2, len(screen.Date)-1):
        if (makeD(screen.cc[i])>screen.d1min and makeD(screen.cc[i])<screen.d1max and
            makeD(screen.cc2[i])>screen.d2min and makeD(screen.cc2[i])<screen.d2max and
            makeD(screen.cc3[i])>screen.d3min and makeD(screen.cc3[i])<screen.d3max and
            makeD(screen.gaps[i])>screen.gmin and makeD(screen.gaps[i])<screen.gmax and
            makeD(screen.Open[i])>screen.pmin and makeD(screen.Open[i])<screen.pmax and
            makeD(screen.Vol[i])>screen.vmin and makeD(screen.Vol[i])<screen.vmax and
            makeD(screen.cc[i-1])<0):
            day1 = ','.join([ticker, screen.Date[i], screen.Open[i], screen.High[i], screen.Low[i], screen.Close[i],
                             screen.Vol[i], screen.oc[i], screen.gap[i], screen.cc[i], screen.cc2[i], screen.cc2[i]])
            day2 = ','.join([screen.Open[i+1], screen.High[i+1], screen.Low[i+1], screen.Close[i+1], screen.Vol[i+1]])
            strats = ','.join([screen.ocs[i], screen.oo2s[i], screen.oc2s[i], screen.ccs[i], screen.cc2s[i], screen.gaps[i]])
            f.write(',,'.join([day1, day2, strats]) + '\n')
            screen.socs.append(screen.ocs[i])
            screen.soo2s.append(screen.oo2s[i])
            screen.soc2s.append(screen.oc2s[i])
            screen.sccs.append(screen.ccs[i])
            screen.scc2s.append(screen.cc2s[i])
            screen.sgaps.append(screen.gaps[i])

def analysis():
    lines = []
    strategies = ['O/O', 'O/C2', 'O/C', 'C/C', 'C/C2', 'Gaps']
    count = 0
    for strat in [screen.soo2s, screen.soc2s, screen.socs, screen.sccs, screen.scc2s, screen.sgaps]:
        sums = 0
        total = len(strat)
        sum_up = 0
        sum_down = 0
        win_count = 0
        for stat in strat:
            stat = makeD(stat)
            sums += stat
            if stat > 0:
                win_count += 1
                sum_up += stat
            if stat < 0:
                sum_down += stat
        avg = str('%.2f' %(sums/total)) + '%'
        avg_up = str('%.2f' %(sum_up/total)) + '%'
        avg_down = str('%.2f' %(sum_down/total)) + '%'
        win_percent = str('%.2f' %(100*win_count/total)) + '%'
        lines += [','.join([strategies[count], win_percent, avg_up, str(sum_up) + '%', avg_down, str(sum_down) + '%', avg, str(sums) + '%'])]
        count += 1
    return '\n'.join(lines)
                               

class ms:
    stocks_passed = 15
    win_needed = 80
    loss_needed = 20
    avg_needed = 5
    numbers = [0, 5, 10, 20]
    oo2s, oc2s, ocs, ccs, cc2s, gaps = ([] for i in range(6))
    #(Date, Open, High, Low, Close)

def ms_analysis():
    lines = []
    strategies = ['O/O', 'O/C2', 'O/C', 'C/C', 'C/C2', 'Gaps']
    count = 0
    win_percents = []
    avgs = []
    sumss = []
    for strat in [screen.soo2s, screen.soc2s, screen.socs, screen.sccs, screen.scc2s, screen.sgaps]:
        sums = 0
        total = len(strat)
        sum_up = 0
        sum_down = 0
        win_count = 0
        for stat in strat:
            stat = makeD(stat)
            sums += stat
            if stat > 0:
                win_count += 1
                sum_up += stat
            if stat < 0:
                sum_down += stat
        avg = str('%.2f' %(sums/total)) + '%'
        avg_up = str('%.2f' %(sum_up/total)) + '%'
        avg_down = str('%.2f' %(sum_down/total)) + '%'
        win_percent = str('%.2f' %(100*win_count/total)) + '%'
        win_percents += '%.2f' %(100*win_count/total)
        avgs += '%.2f' %(sums/total)
        sumss += sums
        count += 1
    return strategies, win_percents, avgs, sumss

def set_ms_crit(passed,win,loss,avg):
    ms.line_1day = []
    ms.stocks_passed = passed
    ms.win_needed = win
    ms.loss_needed = loss
    ms.avg_needed = avg

def d1min_screen(d1min):
    for i in range(1,len(screen.Date)):
        try:
            if makeD(screen.cc[i])>d1min and makeD(screen.Vol[i]) > 100000:
                screen.socs.append(screen.ocs[i])
                screen.soo2s.append(screen.oo2s[i])
                screen.soc2s.append(screen.oc2s[i])
                screen.sccs.append(screen.ccs[i])
                screen.scc2s.append(screen.cc2s[i])
                screen.sgaps.append(screen.gaps[i])
        except (InvalidOperation, IndexError):
            pass

def ms_analysis(f, d1min):
    strats = ['O/O', 'O/C2', 'O/C', 'C/C', 'C/C2', 'Gaps']
    count = 0
    for strat in [screen.soo2s, screen.soc2s, screen.socs, screen.sccs, screen.scc2s, screen.sgaps]:
        win_count = 0
        sums = 0
        total = len(screen.soo2s)
        for stat in strat:
            stat = makeD(stat)
            if math.isnan(stat):
                print('fuck me')
                stat = 0
                total -= 1
            sums += stat
            if stat>0:
                win_count += 1
        win_percent = 100*(win_count/total)
        avg = sums/total
        if (avg>ms.avg_needed and win_percent>ms.win_needed and total>ms.stocks_passed or
            avg<-ms.avg_needed and win_percent<ms.loss_needed and total>ms.stocks_passed):
            f.write(','.join([strats[count], str(d1min), str('%.2f' %win_percent), str('%.2f' %avg), str(sums), str(total) + '\n']))
        count += 1
    
    
                
            
    
    












































    

    


