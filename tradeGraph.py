import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
import jwt
import hashlib
import uuid
from urllib.parse import urlencode, unquote
import matplotlib.ticker as ticker

# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

access_key = 'your_access_key'
secret_key = 'your_secret_key'
server_url = 'https://api.upbit.com'

def get_order_history(market):

    params = {
    'states[]': ['done','cancel'],
    'market':market
    }
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization,
    }

    response = requests.get(server_url + '/v1/orders', params=params, headers=headers)

    return response.json()[:10]

def get_order_single_history(uid):

    params = {
    'uuid': uid
    }
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization,
    }

    response = requests.get(server_url + '/v1/order', params=params, headers=headers)

    return response.json()

def plot_order_history(order_history):
    buy_orders = [order for order in order_history if order['side'] == 'bid']
    sell_orders = [order for order in order_history if order['side'] == 'ask']

    buy_prices = []
    sell_prices=[]

    buy_uuid = [uuid['uuid'] for uuid in buy_orders]
    sell_uuid = [uuid['uuid'] for uuid in sell_orders]

    for uid in buy_uuid:
        list = get_order_single_history(uid) 
        trades=list['trades']
        trade = trades[0]
        price = trade['price']
        buy_prices.insert(0,price)
    
    for uid in sell_uuid:
        list = get_order_single_history(uid) 
        trades=list['trades']
        trade = trades[0]
        price = trade['price']
        sell_prices.insert(0,price)

    #print(buy_prices)
    #print(sell_prices)

    # buy_prices와 sell_prices를 숫자로 변환합니다.
    buy_prices = [float(price) for price in buy_prices]
    sell_prices = [float(price) for price in sell_prices]

    # 정렬된 리스트에 대한 인덱스를 생성합니다.
    indices_buy_sorted = range(len(buy_prices))
    indices_sell_sorted = range(len(sell_prices))

    # 3. 그래프 그리기

    fig, ax = plt.subplots()

    ax.plot(indices_buy_sorted,buy_prices,marker='o',label='buy',c='g')
    ax.plot(indices_sell_sorted,sell_prices,marker='o',label='sell',c='r')

    ax.legend(loc='upper right')

    plt.show()

if __name__ == "__main__":
    market = "KRW-BTC"
    order_history = get_order_history(market)
    plot_order_history(order_history)
