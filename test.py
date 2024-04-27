import time
import requests
import pandas as pd
import datetime
import os

start = datetime.datetime.now()

while(1):
    start_time = datetime.datetime.now()

    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    
    book = response.json()


    data = book['data']


    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0
    
    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1

    #print (bids)
    #print ("\n")
    #print (asks)
    #print(type(bids))
    #df = bids.append(asks)

    
    timestamp = datetime.datetime.now()
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    asks['quantity'] = asks['quantity'].round(decimals=4)
    asks['timestamp'] = req_timestamp

    print (asks)
    print ("\n")


    fn = "./" + str(start_time.year) + "-" + str(start_time.month) + "-" + str(start_time.day) + "-bithumb-orderbook.csv"


    should_write_header = os.path.exists(fn)
    if should_write_header == False:
         asks.to_csv("./" + str(start_time.year) + "-" + str(start_time.month) + "-" + str(start_time.day) + "-bithumb-orderbook.csv", index=False, header=True, mode = 'a', sep = '|')
    else:
         asks.to_csv("./" + str(start_time.year) + "-" + str(start_time.month) + "-" + str(start_time.day) + "-bithumb-orderbook.csv", index=False, header=False, mode = 'a', sep = '|')


    end_time = datetime.datetime.now()
    execution_time = end_time - start_time
    time.sleep(5 - (execution_time.seconds))

    if((end_time-start).seconds/3600 == 24):break

    



  
