import time
import requests
import pandas as pd
import datetime
import os

start = datetime.datetime.now() # 시작시간

while(1):
    start_time = datetime.datetime.now()

    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5') # 비트코인 api
    book = response.json()
    data = book['data']

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0

    timestamp = datetime.datetime.now()
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')  ## 밀리초까지 %f

    bids['quantity'] = bids['quantity'].round(decimals=4)
    bids['timestamp'] = req_timestamp
    
    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1
    
    timestamp = datetime.datetime.now()
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')  ## 밀리초까지 %f

    asks['quantity'] = asks['quantity'].round(decimals=4)
    asks['timestamp'] = req_timestamp
    
    print(bids)
    print ("\n")
    print (asks)

    orderbook = pd.concat([bids, asks])

    fn = "book-" + str(start_time.year) + "-" + str(start_time.month) + "-" + str(start_time.day) + "-bithumb-btc.csv"

    should_write_header = not os.path.exists(fn)
    with open(fn, 'a') as f:
        if should_write_header:
            f.write('price\t|quantity|type|timestamp\n')        
        orderbook.to_csv(f, index=False, header=False, sep='|')


    end_time = datetime.datetime.now()

    if((end_time-start).seconds >= 24 * 3600):break  ## 24시간 실행
    
    execution_time = end_time - start_time

    time.sleep(5 - (execution_time.seconds)) ## 5초 맞추기