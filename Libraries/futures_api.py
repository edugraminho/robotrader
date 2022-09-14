from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from datetime import datetime
import time
# from utils import *

# from binance.cm_futures import CMFutures
# futures_client = CMFutures(API_KEY, API_SECRET)

API_KEY = "L8vTV38sqckhCZCT403TlRqxZHSGuASm95QckB9y5Hmg6g1OUddff79Y1k9DGGLb"
API_SECRET = "X4TE8ehw2891qrLgT4iQSoFn6kwnQXy1V6ispA34cdWf0kq9PXP9Xa1d1EW880Nt"

client = Client(API_KEY, API_SECRET)


def get_current_price_crypto(crypto):
    date_price = client.get_recent_trades(symbol=crypto, limit=1)
    price = float(date_price[0]["price"])

    # descontando uma porcentagem para garantir que a ordem seja fechada
    # price = get_current_price_crypto(crypto)
    # #deconto de 1%
    # value =  price - (price * 0.01)



    return price


def create_order_buy_long_or_short(index, crypto, buy_or_sell, direction, quantity):

    res = client.futures_create_order(
        symbol=crypto,
        side=buy_or_sell,
        positionSide=direction,
        dualSidePosition= False,
        type='MARKET',
        quantity=quantity
        )

    # if res["status"] == "NEW":
    #     insert_csv_status(index, buy_or_sell, res['orderId'])
    return res['status']

    # pegar o retorno e armnazenar o orderId
    futures_order = {
        "orderId":74842174826,
        "symbol":"BTCUSDT",
        "status":"NEW",
        "clientOrderId":"pjUADBlrl43eKRQkt1WhBy",
        "price":"0",
        "avgPrice":"0.00000",
        "origQty":"0.010",
        "executedQty":"0",
        "cumQty":"0",
        "cumQuote":"0",
        "timeInForce":"GTC",
        "type":"MARKET",
        "reduceOnly":False,
        "closePosition":False,
        "side":"BUY",
        "positionSide":"LONG",
        "stopPrice":"0",
        "workingType":"CONTRACT_PRICE",
        "priceProtect":False,
        "origType":"MARKET",
        "updateTime":1662843258272
        }


# print(create_order_buy_long_or_short(1,'BTCUSDT', 'BUY' ,'LONG', 0.001))

def create_stop_limit(crypto, buy_or_sell, direction, quantity):
    price = get_current_price_crypto(crypto)
    #deconto de 1%
    print(price)
    value =  price - (price * 0.03)
    print(value)

    # info = client.get_symbol_info(crypto)
    # print(info)

    order = client.futures_create_order(
        symbol='BTCUSDT',
        type='STOP_MARKET',
        side='BUY',
        direction='LONG',
        stopPrice=int(value),
        closePosition=True
   )
    
    return order['status']

print(create_stop_limit('BTCUSDT', 'SELL' ,'LONG', 0.001))

def closed_market(index, crypto, direction):
    try:

        create_order = client.futures_create_order(
            symbol=crypto,
            side="SELL",
            positionSide=direction,
            dualSidePosition= False,
            type='MARKET',
            quantity=100,
            )


        if create_order:
            print("deu", create_order)
            # insert_csv_status(index, buy_or_sell, res['orderId'])

        return create_order
    except ValueError as e:

        raise BinanceAPIException(e.response, e.status_code, e.text)
        print(e.status_code)
        print(e.message)
        print(e.response)
        print(e.request)
        print(e.code)

# print(closed_market(1, "ETHUSDT", "LONG"))


def get_quantity(crypto):
    # para obter a quantidade comprada
    my_trades = client.get_my_trades(symbol=crypto)
    for trade in my_trades:
        if trade['isBuyer']:
            return trade['price']
