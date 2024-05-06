import time
import pyupbit
import datetime
import schedule
from prophet import Prophet 

predicted_close_price = 0

ticker="KRW-BTC"

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


"""Prophet으로 당일 종가 가격 예측"""
df = pyupbit.get_ohlcv(ticker, interval="minute30")

df = df.reset_index()
df['ds'] = df['index']
df['y'] = df['close']
data = df[['ds','y']]
model = Prophet()
model.fit(data)
future = model.make_future_dataframe(periods=4, freq='h')
forecast = model.predict(future)

fig1 = model.plot(forecast)
fig2 = model.plot_components(forecast)


df['forecast']=forecast['yhat']
#df.to_excel("pd1.xlsx")
#forecast.to_excel("pd2.xlsx")

predicted_close_price = forecast['yhat'].values[-1]


