from bs4 import BeautifulSoup as bs
import numpy as np
import os
import pickle
from urllib.request import urlopen as uReq


def save_tickers(my_url):
    count = 1
    tickers = []
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    soup = bs(page_html,'html.parser')
    folder_name = soup.title.text.replace('Stock Screener - Overview','').title().strip()
    pfile_name = folder_name.replace(" ","")+'.pickle'
    if not os.path.exists('Recent Screens/'+folder_name):
        os.makedirs('Recent Screens/'+folder_name)
    else:
        print('Already ran this screener')
        return folder_name,pfile_name
    page_classes = soup.findAll('a',{'class':'screener-pages'})
    last_page_holder = len(page_classes)
    last_page = page_classes[last_page_holder-1].text
    print('You have ' + str(last_page) + ' pages to go through.')

    for number in range(1,int(last_page)+1):
        my_url_looped = my_url + '&r=' + str(count)
        uClient = uReq(my_url_looped)
        page_html = uClient.read()
        uClient.close()
        soup = bs(page_html,'html.parser')
        count = count+20

        for ticker_holder in soup.findAll('a',{'class':'screener-link-primary'}):
            ticker = ticker_holder.text
            tickers.append(ticker)
        
    with open('Recent Screens/'+str(folder_name)+'/'+str(pfile_name),'wb') as f:
        pickle.dump(tickers,f)
    print(tickers)
    return folder_name,pfile_name



