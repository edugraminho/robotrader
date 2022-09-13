from binance.client import Client
from binance.enums import *
from datetime import datetime
import time

# from binance.cm_futures import CMFutures
# futures_client = CMFutures(API_KEY, API_SECRET)

API_KEY = "L8vTV38sqckhCZCT403TlRqxZHSGuASm95QckB9y5Hmg6g1OUddff79Y1k9DGGLb"
API_SECRET = "X4TE8ehw2891qrLgT4iQSoFn6kwnQXy1V6ispA34cdWf0kq9PXP9Xa1d1EW880Nt"

client = Client(API_KEY, API_SECRET)


def create_order_buy_long_or_short(crypto, buy_or_sell, direction, quantity):
    res_create_order = client.futures_create_order(
        symbol=crypto,
        side=buy_or_sell,
        positionSide=direction,
        dualSidePosition= False,
        type='MARKET',
        quantity=quantity
        )
    
    return res_create_order
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

# LONG
# 'orderId': 74866849603

# print(create_order_buy_long_or_short('BTCUSDT', 'BUY' ,'LONG', 0.002))



def create_order_closed_signal(crypto, direction, stop_price):
    create_order = client.futures_create_order(
        symbol=crypto,
        side='SELL',
        positionSide=direction,
        dualSidePosition=False,
        type='TAKE_PROFIT_MARKET',
        stopPrice=stop_price,
        closePosition=True
        )

    return create_order

    # pegar o stop_price da fucnao get_current_price_crypto
    # e diminuir uma porcentagem para sempre fechar a ordem

# print(create_order_closed_signal())

# /origClientOrderIdList

def get_current_price_crypto(crypto):
    price = client.get_recent_trades(symbol=crypto, limit=1)
    return price

# print(get_current_price_crypto("BTCUSDT"))

def get_quantity(crypto):
    # para obter a quantidade comprada
    my_trades = client.get_my_trades(symbol=crypto)
    for trade in my_trades:
        if trade['isBuyer']:
            return trade['price']

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





# from binance.cm_futures import CMFutures
# cm_futures_client = CMFutures(API_KEY, API_SECRET)
# open0 = cm_futures_client.get_account_trades(pair='BTCUSDT')


# for order in all_orders:
#     order["time"] = datetime.fromtimestamp(order["time"]/1000).strftime('%d-%m-%y %H:%M')
#     orders.append(order)




def test():
    while True:

        try:
            balance = client.futures_account_balance()
            time.sleep(0.25)
            account = client.futures_account()
        except Exception as e:
            print(e.message)
            pass
        
        usdtbalance = 0

        for b1 in account['assets']:
            if b1['asset'] == 'USDT':
                initialmargin = float(b1['initialMargin'])
                unrealizedprofit = float(b1['unrealizedProfit'])
                pnl=float(b1['crossUnPnl'])
                roe = unrealizedprofit / initialmargin*100
        print('PNL: '+str(pnl)+'USDT')
        print('ROE: '+str(roe)+'%')
        time.sleep(2)

# test()

#copyright by Bitone Great
# Explanation is available at https://www.youtube.com/watch?v=Hr-wEgcmw98
#pip install python-binance