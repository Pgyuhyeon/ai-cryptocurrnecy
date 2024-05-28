## https://github.com/Pgyuhyeon 박규현, 김우리

import pandas as pd

def calculate_mid_price(group):
    return group['price'].mean()

def calculate_book_imbalance(group):
    buy_quantity = group[group['type'] == 0]['quantity'].sum()
    sell_quantity = group[group['type'] == 1]['quantity'].sum()
    return buy_quantity - sell_quantity

def calculate_total_quantity(group):
    return group['quantity'].sum()

def calculate_avg_trade_price(group):
    return group['price'].mean()

def calculate_price_volatility(group):
    return group['price'].std()

def calculate_buy_sell_ratio(group):
    buy_quantity = group[group['type'] == 0]['quantity'].sum()
    sell_quantity = group[group['type'] == 1]['quantity'].sum()
    if sell_quantity == 0:  # Zero division protection
        return float('inf')
    return buy_quantity / sell_quantity

# 데이터 파일 읽기
df = pd.read_csv('2024-05-01-upbit-BTC-book.csv', sep=',')

# 숫자로 변환 가능한 열에 대해 숫자로 변환
numeric_columns = ['price', 'quantity', 'type']  # 숫자로 변환할 열 지정
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors='coerce')  # errors='coerce'를 사용하여 변환할 수 없는 값을 NaN으로 처리

# timestamp 열을 datetime 형식으로 변환
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 24시간 분량의 데이터만 선택
start_time = df['timestamp'].min()
end_time = start_time + pd.Timedelta(days=1)  # 24시간 후로 설정
df = df[(df['timestamp'] >= start_time) & (df['timestamp'] < end_time)]

# 그룹화하여 시간대별로 데이터 분리
groups = df.groupby('timestamp')

# 특성 계산 및 저장
result = []
for timestamp, group in groups:
    # 중간 가격 계산
    mid_price = calculate_mid_price(group)
    
    # Order imbalance 계산
    book_imbalance = calculate_book_imbalance(group)
    
    # 총 거래량 계산
    total_quantity = calculate_total_quantity(group)
    
    # 평균 거래 가격 계산
    avg_trade_price = calculate_avg_trade_price(group)
    
    # 가격 변동성 계산
    price_volatility = calculate_price_volatility(group)
    
    # 매수/매도 비율 계산
    buy_sell_ratio = calculate_buy_sell_ratio(group)
    
    result.append([buy_sell_ratio, book_imbalance, mid_price, total_quantity, avg_trade_price, price_volatility, timestamp])

# DataFrame 생성
result_df = pd.DataFrame(result, columns=[
    'buy_sell_ratio',
    'book-imbalance-0.2-5-1',
    'mid_price',
    'total_quantity',
    'avg_trade_price',
    'price_volatility',
    'timestamp'
])

# 결과 저장
result_df.to_csv('2024-05-01-upbit-BTC-feature.csv', sep='|', index=False)
