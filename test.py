import pyupbit
from prophet import Prophet
import math

access = "your-access"
secret = "your-secret"

upbit = pyupbit.Upbit(access, secret)


# RSI 계산
def rsi_calculation(df, period=14):

    # 전일 대비 변동 평균
    df['change'] = df['close'].diff()

    # 상승한 가격과 하락한 가격
    df['up'] = df['change'].apply(lambda x: x if x > 0 else 0)
    df['down'] = df['change'].apply(lambda x: -x if x < 0 else 0)

    # 상승 평균과 하락 평균
    df['avg_up'] = df['up'].ewm(alpha=1/period).mean()
    df['avg_down'] = df['down'].ewm(alpha=1/period).mean()

    # 상대강도지수(RSI) 계산
    df['rs'] = df['avg_up'] / df['avg_down']
    df['rsi'] = 100 - (100 / (1 + df['rs']))
    rsi = df['rsi']

    return rsi


# 볼린저 밴드 계산
def bollinger_bands(df, period=20, num_of_std=2):
    sma = df['close'].rolling(window=period).mean()
    rstd = df['close'].rolling(window=period).std()

    upper_band = sma + num_of_std * rstd
    lower_band = sma - num_of_std * rstd
    return upper_band, lower_band



def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


balances = upbit.get_balances()
krw= get_balance("KRW")

btc_avg=upbit.get_avg_buy_price("BTC")
btc= upbit.get_balance("BTC")

target_income = btc_avg+500000.0
target_loss = btc_avg-500000.0

krw = get_balance("KRW")

#print(math.floor(krw*1.0))

list = upbit.get_individual_order('e2802724-5c69-4a42-8ab1-b53481ce0a30') 

print(list)

trades=list['trades']
price = trades[0]
print(price['price'])


#a= [order for order in list if order['trades'] ]

#print(upbit.get_individual_order('14920ba4-a0f4-43da-81e2-6bae46b7255f') )


# assistant = client.beta.assistants.create(
#   name="Data visualizer",
#   description="You are great at creating beautiful data visualizations. You analyze data present in .xlsx files, understand trends, and come up with data visualizations relevant to those trends. You also share a brief text summary of the trends observed.",
#   model="gpt-3.5-turbo",
#   tools=[{"type": "code_interpreter"}],
#   tool_resources={
#     "code_interpreter": {
#       "file_ids": [file.id]
#     }
#   }
# )
