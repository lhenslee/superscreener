


def new_ticker_list():
    count = 1
    tickers = []
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    soup = bs(page_html,'html.parser')

def store_stock_data():
    pass

def user_input_screener():
    pass

def screener_of_screeners():
    pass
