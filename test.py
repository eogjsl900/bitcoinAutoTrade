import pyupbit

access="your-access"
secret="your-secret"

upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-SOL"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회

print(pyupbit.get_current_price("KRW-SOL"))