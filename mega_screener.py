from decimal import *
import numpy as np
import os
import pandas as pd
import pandas_datareader as pdr
import pickle

pos = str(100000000000)
neg = str(-100000000000)
oo2ar = []
oc2ar = []
ocar = []
ccar = []
cc2ar = []
gapar = []


def makeD(var):
    return Decimal(var.replace('%',''))


def comb(ticker,date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg):
    for i in range(1,len(high)-2):
        if (Decimal(cc[i].replace('%','').replace('NaN',neg))>d1 and
        Decimal(cc[i].replace('%','').replace('NaN',pos))<dm1 and
        Decimal(cc2[i].replace('%','').replace('NaN',neg))>d2 and
        Decimal(cc2[i].replace('%','').replace('NaN',pos))<dm2 and
        Decimal(cc3[i].replace('%','').replace('NaN',neg))>d3 and
        Decimal(cc3[i].replace('%','').replace('NaN',pos))<dm3 and
        Decimal(gap[i+1].replace('%','').replace('NaN',neg))>g and
        Decimal(gap[i+1].replace('%','').replace('NaN',pos))<gm and
        Decimal(_open[i].replace('%','').replace('NaN',neg))>p and
        Decimal(_open[i].replace('%','').replace('NaN',pos))<pm and
        Decimal(vol[i].replace('%','').replace('NaN',neg))>v and
        Decimal(vol[i].replace('%','').replace('NaN',pos))<vm):
            #print(cc[i]+', '+cc2[i]+', '+cc3[i]+', '+gap[i+1]+', '+oc[i+1])
            o1o2 = str('%.2f' %(100*(Decimal(_open[i+2].replace('%',''))-Decimal(_open[i+1].replace('%','')))/Decimal(_open[i+1])))+'%'
            o1c2 = str('%.2f' %(100*(Decimal(close[i+2].replace('%',''))-Decimal(_open[i+1].replace('%','')))/Decimal(_open[i+1])))+'%'
            oo2ar.append(o1o2)
            oc2ar.append(o1c2)
            ocar.append(oc[i+1])
            ccar.append(cc[i+1])
            cc2ar.append(cc[i+2])
            gapar.append(gap[i+1])


def firstred(ticker,date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg):
    for i in range(1,len(high)-2):
        if (Decimal(cc[i].replace('%','').replace('NaN',neg))>d1 and
        Decimal(cc[i].replace('%','').replace('NaN',pos))<dm1 and
        Decimal(cc2[i].replace('%','').replace('NaN',neg))>d2 and
        Decimal(cc2[i].replace('%','').replace('NaN',pos))<dm2 and
        Decimal(cc3[i].replace('%','').replace('NaN',neg))>d3 and
        Decimal(cc3[i].replace('%','').replace('NaN',pos))<dm3 and
        Decimal(gap[i+1].replace('%','').replace('NaN',neg))>g and
        Decimal(gap[i+1].replace('%','').replace('NaN',pos))<gm and
        Decimal(_open[i].replace('%','').replace('NaN',neg))>p and
        Decimal(_open[i].replace('%','').replace('NaN',pos))<pm and
        Decimal(vol[i].replace('%','').replace('NaN',neg))>v and
        Decimal(vol[i].replace('%','').replace('NaN',pos))<vm and
        Decimal(cc[i-1].replace('%','').replace('NaN',neg))>0 and
        Decimal(cc[i].replace('%','').replace('NaN',pos))<gr):
            #print(cc[i]+', '+cc2[i]+', '+cc3[i]+', '+gap[i+1]+', '+oc[i+1])
            o1o2 = str('%.2f' %(100*(Decimal(_open[i+2].replace('%',''))-Decimal(_open[i+1].replace('%','')))/Decimal(_open[i+1])))+'%'
            o1c2 = str('%.2f' %(100*(Decimal(close[i+2].replace('%',''))-Decimal(_open[i+1].replace('%','')))/Decimal(_open[i+1])))+'%'
            oo2ar.append(o1o2)
            oc2ar.append(o1c2)
            ocar.append(oc[i+1])
            ccar.append(cc[i+1])
            cc2ar.append(cc[i+2])
            gapar.append(gap[i+1])
            
def firstgreen(ticker,date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg):
    for i in range(1,len(high)-2):
        if (Decimal(cc[i].replace('%','').replace('NaN',neg))>d1 and
        Decimal(cc[i].replace('%','').replace('NaN',pos))<dm1 and
        Decimal(cc2[i].replace('%','').replace('NaN',neg))>d2 and
        Decimal(cc2[i].replace('%','').replace('NaN',pos))<dm2 and
        Decimal(cc3[i].replace('%','').replace('NaN',neg))>d3 and
        Decimal(cc3[i].replace('%','').replace('NaN',pos))<dm3 and
        Decimal(gap[i+1].replace('%','').replace('NaN',neg))>g and
        Decimal(gap[i+1].replace('%','').replace('NaN',pos))<gm and
        Decimal(_open[i].replace('%','').replace('NaN',neg))>p and
        Decimal(_open[i].replace('%','').replace('NaN',pos))<pm and
        Decimal(vol[i].replace('%','').replace('NaN',neg))>v and
        Decimal(vol[i].replace('%','').replace('NaN',pos))<vm and
        Decimal(cc[i-1].replace('%','').replace('NaN',neg))<0 and
        Decimal(cc[i].replace('%','').replace('NaN',pos))>rg):
            #print(cc[i]+', '+cc2[i]+', '+cc3[i]+', '+gap[i+1]+', '+oc[i+1])
            o1o2 = str('%.2f' %(100*(Decimal(_open[i+2].replace('%',''))-Decimal(_open[i+1].replace('%','')))/Decimal(_open[i+1])))+'%'
            o1c2 = str('%.2f' %(100*(Decimal(close[i+2].replace('%',''))-Decimal(_open[i+1].replace('%','')))/Decimal(_open[i+1])))+'%'
            oo2ar.append(o1o2)
            oc2ar.append(o1c2)
            ocar.append(oc[i+1])
            ccar.append(cc[i+1])
            cc2ar.append(cc[i+2])
            gapar.append(gap[i+1])

def win_percent(col):
    win_count = 0
    for i in range(len(col)):
        if Decimal(col[i].replace('%',''))>0:
            win_count+=1
    return '%.2f' %(win_count/len(col)*100)

def sums(col):
    sums = 0
    for i in range(len(col)):
        sums+=Decimal(col[i].replace('%',''))
    return sums

def avg(col):
    sums = 0
    for i in range(len(col)):
        sums+=Decimal(col[i].replace('%',''))
    return '%.2f' %(sums/len(col))


def screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg):
    del oo2ar[:]
    del oc2ar[:]
    del ocar[:]
    del ccar[:]
    del cc2ar[:]
    del gapar[:]

    with open(pickle_file,'rb') as f:
        tickers = pickle.load(f)
    for ticker in tickers:
        try:
            date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5 = np.loadtxt(percent_folder+'{}.csv'.format(ticker),
                                                                            delimiter=',',
                                                                            unpack=True,
                                                                            dtype='str')
        except FileNotFoundError:
            pass
        if Decimal(gr)!=10000000000:
            firstred(f,ticker,date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
        if Decimal(rg)!=-10000000000:
            firstgreen(ticker,date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
        else:
            comb(ticker,date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)

    Strats = 'O/C','O/O','O/C2','C/C','C/C2','Gap'
    win_percents = []
    avgs = []
    Sums = []
    del win_percents[:],avgs[:],Sums[:]
    for A in (ocar,oo2ar,oc2ar,ccar,cc2ar,gapar):
        win_percents.append(win_percent(A))
        avgs.append(avg(A))
        Sums.append(sums(A))
    return Strats,win_percents,avgs,Sums,len(ocar)

def MegaScreener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg):
    bestscreensFile = folder_name+'/BestScreens.csv'
    fb = open(bestscreensFile,'w')
    fb.write('Strat,1Day min,2Day min,3Day min,Gapup,Win%,Avg,Sum,Passed\n')
    numbers = [0,5,10,15,20]
    gapups = [0,1,2,3,4,5]
    winner = 80
    gains = 5
    losses = -5
    loser = 20
    times = 15
##    for g in gapups:
##        for d1 in numbers:
##            for d2 in numbers:
##                for d3 in numbers:
##                    temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
##                    Strats = temp[0]
##                    Win = temp[1]
##                    Avg = temp[2]
##                    Sum = temp[3]
##                    Passed = temp[4]
##                    for i in range(1,6):
##                        if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
##                            Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
##                            line = Strats[i]+','+str(d1)+'%,'+str(d2)+'%,'+str(d3)+'%,'+str(g)+'%,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
##                            print(line)
##                            fb.write(line)
##    for d1 in numbers:
##        for g in numbers:
##            for d3 in numbers:
##                temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
##                Strats = temp[0]
##                Win = temp[1]
##                Avg = temp[2]
##                Sum = temp[3]
##                Passed = temp[4]
##                for i in range(1,5):
##                    if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
##                        Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
##                        line = Strats[i]+','+str(d1)+'%,Skip,'+str(d3)+'%,'+str(g)+'%,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
##                        print(line)
##                        fb.write(line)
##    for d3 in numbers:
##        for d2 in numbers:
##            for g in numbers:
##                temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
##                Strats = temp[0]
##                Win = temp[1]
##                Avg = temp[2]
##                Sum = temp[3]
##                Passed = temp[4]
##                for i in range(1,5):
##                    if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
##                        Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
##                        line = Strats[i]+',Skip,'+str(d2)+'%,'+str(d3)+'%,'+str(g)+'%,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
##                        print(line)
##                        fb.write(line)
    for d1 in numbers:
        for d2 in numbers:
            for d3 in numbers:
                temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
                Strats = temp[0]
                Win = temp[1]
                Avg = temp[2]
                Sum = temp[3]
                Passed = temp[4]
                for i in range(1,6):
                    if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
                        Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
                        line = Strats[i]+','+str(d1)+'%,'+str(d2)+'%,'+str(d3)+'%,'+'Skip,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
                        print(line)
                        fb.write(line)
##    for g in gapups:
##        for d1 in numbers:
##            for d2 in numbers:
##                temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
##                Strats = temp[0]
##                Win = temp[1]
##                Avg = temp[2]
##                Sum = temp[3]
##                Passed = temp[4]
##                for i in range(1,6):
##                    if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
##                        Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
##                        line = Strats[i]+','+str(d1)+'%,'+str(d2)+'%,Skip,'+str(g)+'%,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
##                        print(line)
##                        fb.write(line)
##    for g in gapups:
##            temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
##            Strats = temp[0]
##            Win = temp[1]
##            Avg = temp[2]
##            Sum = temp[3]
##            Passed = temp[4]
##            for i in range(1,6):
##                if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
##                    Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
##                    line = Strats[i]+',Skip,Skip,Skip,'+str(g)+'%,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
##                    print(line)
##                    fb.write(line)
    for d1 in numbers:
        for d2 in numbers:
            temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
            Strats = temp[0]
            Win = temp[1]
            Avg = temp[2]
            Sum = temp[3]
            Passed = temp[4]
            for i in range(1,6):
                if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
                    Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
                    line = Strats[i]+','+str(d1)+'%,'+str(d2)+'%,Skip,Skip,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
                    print(line)
                    fb.write(line)
    for d1 in numbers:
        for d3 in numbers:
            temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
            Strats = temp[0]
            Win = temp[1]
            Avg = temp[2]
            Sum = temp[3]
            Passed = temp[4]
            for i in range(1,6):
                if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
                    Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
                    line = Strats[i]+','+str(d1)+'%,Skip,'+str(d3)+'%,Skip,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
                    print(line)
                    fb.write(line)
    for d2 in numbers:
        for d3 in numbers:
            temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
            Strats = temp[0]
            Win = temp[1]
            Avg = temp[2]
            Sum = temp[3]
            Passed = temp[4]
            for i in range(1,6):
                if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
                    Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
                    line = Strats[i]+',Skip,'+str(d2)+'%,'+str(d3)+'%,Skip,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
                    print(line)
                    fb.write(line)
    for d1 in numbers:
        temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
        Strats = temp[0]
        Win = temp[1]
        Avg = temp[2]
        Sum = temp[3]
        Passed = temp[4]
        for i in range(1,6):
            if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
                Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
                line = Strats[i]+','+str(d1)+'%,Skip,Skip,Skip,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
                print(line)
                fb.write(line)  
    for d2 in numbers:
        temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
        Strats = temp[0]
        Win = temp[1]
        Avg = temp[2]
        Sum = temp[3]
        Passed = temp[4]
        for i in range(1,6):
            if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
                Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
                line = Strats[i]+','+'Skip,'+str(d2)+'%,'+'Skip,Skip,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
                print(line)
                fb.write(line)
    for d3 in numbers:
        temp = screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
        Strats = temp[0]
        Win = temp[1]
        Avg = temp[2]
        Sum = temp[3]
        Passed = temp[4]
        for i in range(1,6):
            if (Decimal(Win[i])>winner and Decimal(Avg[i])>gains and Passed>times or
                Decimal(Win[i])<loser and Decimal(Avg[i])<losses and Passed>times):
                line = Strats[i]+','+'Skip'+'%,'+'Skip,'+str(d3)+'%,Skip,'+str(Win[i])+','+str(Avg[i])+','+str(Sum[i])+','+str(Passed)+'\n'
                print(line)
                fb.write(line)
    fb.close()
    print('done')
    return bestscreensFile

        
