import pyupbit
import numpy as np

# OHLCV(open, high, low, close, volume)로 당일 시가, 고가 , 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-BTC",count=7)

# 변동폭 * k 계산 , (고가 - 저가) * k 값
df['range'] = (df['high'] - df['low']) * 0.5

#target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))  -> 전날 변동폭을 기준으로 매수지점 확인
df['target'] = df['open'] + df['range'].shift(1)

#fee(수수료)
fee = 0.05

# ror(수익율), np.where(조건문, 참일떄 값, 거짓일떄 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)

# 누적 곱 계산(cumprod) => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# 하락폭  Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100


print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")