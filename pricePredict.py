import time
import pyupbit
import datetime
import schedule
from prophet import Prophet 

predicted_close_price = 0

"""Prophet으로 당일 종가 가격 예측"""
df = pyupbit.get_ohlcv("KRW-BTC", interval="minute60")
df = df.reset_index()
df['ds'] = df['index']
df['y'] = df['close']
data = df[['ds','y']]
model = Prophet()
model.fit(data)
future = model.make_future_dataframe(periods=24, freq='H')
forecast = model.predict(future)
fig1 = model.plot(forecast)
fig2 = model.plot_components(forecast)
closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]
if len(closeDf) == 0:
    closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
closeValue = closeDf['yhat'].values[0]
predicted_close_price = closeValue