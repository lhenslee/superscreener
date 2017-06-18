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



def comb(f,ticker,date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg):
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
            line = (ticker+','+date[i]+','+_open[i]+','+high[i]+','+low[i]+','+close[i]
                    +','+vol[i]+','+oc[i]+','+gap[i]+','+cc[i]+','+cc2[i]+','+cc3[i]+',,'
                    +_open[i+1]+','+high[i+1]+','+low[i+1]+','+close[i+1]+','+vol[i+1]
                    +','+gap[i+1]+','+oc[i+1]+','+cc[i+1]+','+o1o2+','+o1c2+'\n')
            f.write(line)

def firstred(f,ticker,date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg):
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
            line = (ticker+','+date[i]+','+_open[i]+','+high[i]+','+low[i]+','+close[i]
                    +','+vol[i]+','+oc[i]+','+gap[i]+','+cc[i]+','+cc2[i]+','+cc3[i]+',,'
                    +_open[i+1]+','+high[i+1]+','+low[i+1]+','+close[i+1]+','+vol[i+1]
                    +','+gap[i+1]+','+oc[i+1]+','+cc[i+1]+','+o1o2+','+o1c2+'\n')
            f.write(line)

def firstgreen(f,ticker,date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg):
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
            line = (ticker+','+date[i]+','+_open[i]+','+high[i]+','+low[i]+','+close[i]
                    +','+vol[i]+','+oc[i]+','+gap[i]+','+cc[i]+','+cc2[i]+','+cc3[i]+',,'
                    +_open[i+1]+','+high[i+1]+','+low[i+1]+','+close[i+1]+','+vol[i+1]
                    +','+gap[i+1]+','+oc[i+1]+','+cc[i+1]+','+o1o2+','+o1c2+'\n')
            f.write(line)

def win_percent(col):
    win_count = 0
    for i in range(len(col)):
        if Decimal(col[i].replace('%',''))>0:
            win_count+=1
    line = str('%.2f' %(win_count/len(col)*100))+'%'
    return line

def sums(col):
    sums = 0
    for i in range(len(col)):
        sums+=Decimal(col[i].replace('%',''))
    return str(sums)+'%'

def avg(col):
    sums = 0
    for i in range(len(col)):
        sums+=Decimal(col[i].replace('%',''))
    return str('%.2f' %(sums/len(col)))+'%'

def avgup(col):
    sums = 0
    for i in range(len(col)):
        if Decimal(col[i].replace('%',''))>=0:
            sums+=Decimal(col[i].replace('%',''))
    return str('%.2f' %(sums/len(col)))+'%',str(sums)

def avgdown(col):
    sums = 0
    for i in range(len(col)):
        if Decimal(col[i].replace('%',''))<0:
            sums+=Decimal(col[i].replace('%',''))
    return str('%.2f' %(sums/len(col)))+'%',str(sums)
    


            #,d3,gd,gu
def screener(folder_name,percent_folder,pickle_file,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg):
    del oo2ar[:]
    del oc2ar[:]
    del ocar[:]
    del ccar[:]
    del cc2ar[:]
    del gapar[:]

    fscreener = folder_name+'/screener.csv'
    #fscreener = folder_name+'/screener.csv'

    with open(pickle_file,'rb') as f:
        tickers = pickle.load(f)
    f = open(fscreener,'w')
    headers = ('Ticker,Date,Open,High,Low,Close,Volume,0/C,Gap,C/C,2Days,3Days,Day2,Open,High,Low,Close,Volume,Gap,O/C,C/C,O1/O2,O1/C2\n')
    f.write(headers)
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
            firstgreen(f,ticker,date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
        else:
            comb(f,ticker,date,_open,high,low,close,vol,oc,gap,cc,cc2,cc3,cc4,cc5,d1,dm1,d2,dm2,d3,dm3,g,gm,p,pm,v,vm,gr,rg)
    f.close()
    fanalysis = folder_name+'/analysis.csv'
    f = open(fanalysis,'w')
    headers = 'Strats,O/C,O1/O2,O1/C2,C/C,C/C2,Gap,'+str(len(ocar))+' Passed'+'\n'
    f.write(headers)
    f.write('Win%'+','+win_percent(ocar)+','+win_percent(oo2ar)+','+win_percent(oc2ar)+','+win_percent(ccar)+','+
            win_percent(cc2ar)+','+win_percent(gapar)+'\n')   
    f.write('Avg Up'+','+avgup(ocar)[0]+','+avgup(oo2ar)[0]+','+avgup(oc2ar)[0]+','+avgup(ccar)[0]+','+
            avgup(cc2ar)[0]+','+avgup(gapar)[0]+'\n')
    f.write('Sum Up'+','+avgup(ocar)[1]+','+avgup(oo2ar)[1]+','+avgup(oc2ar)[1]+','+avgup(ccar)[1]+','+
            avgup(cc2ar)[1]+','+avgup(gapar)[1]+'\n')
    f.write('Avg Down'+','+avgdown(ocar)[0]+','+avgdown(oo2ar)[0]+','+avgdown(oc2ar)[0]+','+avgdown(ccar)[0]+','+
            avgdown(cc2ar)[0]+','+avgdown(gapar)[0]+'\n')
    f.write('Sum Dowm'+','+avgdown(ocar)[1]+','+avgdown(oo2ar)[1]+','+avgdown(oc2ar)[1]+','+avgdown(ccar)[1]+','+
            avgdown(cc2ar)[1]+','+avgdown(gapar)[1]+'\n')
    f.write('Avg'+','+avg(ocar)+','+avg(oo2ar)+','+avg(oc2ar)+','+avg(ccar)+','+
            avg(cc2ar)+','+avg(gapar)+'\n')
    f.write('Sum'+','+sums(ocar)+','+sums(oo2ar)+','+sums(oc2ar)+','+sums(ccar)+','+sums(cc2ar)+','+sums(gapar)+'\n')
    f.close()
    return fscreener, fanalysis


