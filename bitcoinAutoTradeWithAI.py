import time
import pyupbit
import datetime
import schedule
from prophet import Prophet
import openaiAPI


access = "your-access"
secret = "your-secret"

ticker="KRW-BTC"

df = pyupbit.get_ohlcv(ticker, interval="minute30")


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



def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

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

    return df['rsi'].values[-1]

def predict_price(ticker):
    """Prophet으로 periods=4 시간 뒤 방향성 예측"""
    df = pyupbit.get_ohlcv(ticker, interval="minute30")
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds','y']]
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=4, freq='h')
    forecast = model.predict(future)
    return forecast['yhat']


forecast = predict_price(ticker)
AI_State=openaiAPI.state
rsi = rsi_calculation(df)

def predict_and_trade(ticker):

    global forecast
    global AI_State
    global rsi

    forecast = predict_price(ticker)
    AI_State = openaiAPI.state
    df = pyupbit.get_ohlcv(ticker, interval="minute30")
    rsi = rsi_calculation(df)
    print('close_price: ',forecast.values[-5])
    print('predicted_close_price: ',forecast.values[-1])
    print('AI_State: ',AI_State)
    print('rsi: ',rsi)

schedule.every(30).minutes.do(lambda: predict_and_trade(ticker))


print('close_price: ',forecast.values[-5])
print('predicted_close_price: ',forecast.values[-1])
print('AI_State: ',AI_State)
print('rsi: ',rsi)

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        schedule.run_pending()

        current_price = get_current_price(ticker)
        btc_avg=upbit.get_avg_buy_price("BTC")

        target_income = btc_avg+500000.0
        target_loss = btc_avg-500000.0


        # 현재가격보다 상승으로 예측 하면서 뉴스 분석이 긍정일때 매수
        # periods=4 , forecast.values[-1] 2시간뒤 예측값
        if (forecast.values[-5]+500000.0 < forecast.values[-1]) and (AI_State == 'hold' or AI_State == 'buy') :
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order(ticker, krw*0.9995)
                print('매수가격:',current_price)

        # RSI 가 20보다 작으면 매수
        elif rsi<20 : 
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order(ticker, krw*0.9995)
                print('매수가격:',current_price)

        # 매수가 + 500000 가 됐으면 이익실현
        elif target_income < current_price:
            btc = upbit.get_balance("BTC")
            if btc > 0.00015:
                upbit.sell_market_order(ticker, btc)
                print('익절가격:',current_price)

        # 매수가 - 500000 가 됐으면 손절
        elif target_loss > current_price:
            btc = upbit.get_balance("BTC")
            if btc > 0.00015:
                upbit.sell_market_order(ticker, btc)
                print('손절가격:',current_price)


        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)