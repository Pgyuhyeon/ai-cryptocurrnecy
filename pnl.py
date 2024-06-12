import pandas as pd

# CSV 파일 경로
csv_file = "ai-crypto-project-3-live-btc-krw.csv"

# CSV 파일 읽기
df = pd.read_csv(csv_file)

# PnL 계산 및 누적
cumulative_pnl = 0
for index, row in df.iterrows():
    pnl = 0
    if row['side'] == 0:  # 매도 거래인 경우
        pnl = (row['price'] - row['amount'] / row['quantity']) * row['quantity'] - row['fee']
    elif row['side'] == 1:  # 매수 거래인 경우
        pnl = (row['amount'] / row['quantity'] - row['price']) * row['quantity'] - row['fee']
    cumulative_pnl += pnl

# 누적 PnL 출력
print("누적 PnL:", cumulative_pnl)

##이 코드는 거래 데이터를 담은 CSV 파일을 읽어와 매도 및 매수 거래의 손익(PnL)을 계산한 후, 
# 이를 누적하여 출력합니다. 각 거래에서 매도 또는 매수 여부에 따라 손익을 계산하고, 
# 거래 수수료를 차감한 후 누적 PnL에 더합니다. 최종적으로 누적된 PnL 값을 계산해 출력합니다. 
# CSV 파일 경로와 거래 데이터를 처리하는 부분이 포함되어 있습니다.