from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from datetime import datetime
from Libraries.utils import *

# from binance.cm_futures import CMFutures
# futures_client = CMFutures(API_KEY, API_SECRET)

API_KEY = "L8vTV38sqckhCZCT403TlRqxZHSGuASm95QckB9y5Hmg6g1OUddff79Y1k9DGGLb"
API_SECRET = "X4TE8ehw2891qrLgT4iQSoFn6kwnQXy1V6ispA34cdWf0kq9PXP9Xa1d1EW880Nt"

PERCENTAGE_BUY = 5

PERCENTAGE_STOP = 3

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

    # para encontrar o quantidade, tenho q pegar meu saldo + 20x

    res = client.futures_create_order(
        symbol=crypto,
        side=buy_or_sell,
        positionSide=direction,
        dualSidePosition= False,
        type='MARKET',
        quantity=quantity
        )


    return res

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



# print(create_stop_limit('BTCUSDT', 'SELL' ,'LONG', 0.001))

def closed_market(index, crypto, direction):
    try:

        res = client.futures_create_order(
            symbol=crypto,
            side="SELL",
            positionSide=direction,
            dualSidePosition= False,
            type='MARKET',
            quantity=999,
            )

        return res
    except Exception as e:
        # print(f"closed_market. Erro: {e}")
        pass


# print(closed_market(1, "ETHUSDT", "LONG"))


def get_balance():
    # para obter a quantidade comprada
    balances = client.futures_account_balance()
    wallet = []

    for b in balances:
        if 'USDT' in b.values():
            wallet.append({
                "total_balance": round(float(b["balance"]), 2),
                "available_balance": round(float(b["withdrawAvailable"]), 2)
                })

    return wallet



def find_value_to_aport(crypto):
    price_crypto = get_current_price_crypto(crypto)
    value_available = get_balance()[0]["available_balance"]

    print("price_crypto", price_crypto)

    percentage = PERCENTAGE_BUY / 100

    _value = ((value_available * 20) * percentage) / price_crypto

    if _value < 1:
        return round(float(_value), 3)
    else:
        return int(_value)


def calculate_price_stop_limit(crypto):
    try: 
        cur_price = get_current_price_crypto(crypto)
        #deconto de 1%
        perc = PERCENTAGE_STOP / 100
        stop_price =  round(float(cur_price - (cur_price * perc)), 2)
        print("Adicionando stop_price: ", crypto)

        return stop_price
    except Exception as e:
        print(f"calculate_price_stop_limit. Erro: {e}")
        pass


def stop_loss_closed():

    cryptos_data = read_csv()
    for c in cryptos_data:
        cur_price = get_current_price_crypto(c["crypto_name"])

        if c["status"] == "BUY" and c["direction"] == "LONG":
            if float(cur_price) <= float(c["stop_price"]):
                print(f'Efetuando StopLoss, crypto: {c["crypto_name"]}')
                order = closed_market(c["index"], c["crypto_name"], c["direction"])
                print(f'STOP LOSS: {c["index"]} - {c["crypto_name"]} - {c["direction"]}')
                return (True, order)

        if c["status"] == "BUY" and c["direction"] == "SHORT":
            if float(cur_price) >= float(c["stop_price"]):
                print(f'Efetuando StopLoss, crypto: {c["crypto_name"]}')
                order = closed_market(c["index"], c["crypto_name"], c["direction"])
                print(f'STOP LOSS: {c["index"]} - {c["crypto_name"]} - {c["direction"]}')

                return (True, order)

    return (False, "NOP")