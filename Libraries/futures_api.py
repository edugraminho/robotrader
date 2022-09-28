from binance.client import Client
from binance.enums import *
from Libraries.utils import *

# from binance.cm_futures import CMFutures
# futures_client = CMFutures(API_KEY, API_SECRET)

API_KEY = "L8vTV38sqckhCZCT403TlRqxZHSGuASm95QckB9y5Hmg6g1OUddff79Y1k9DGGLb"
API_SECRET = "X4TE8ehw2891qrLgT4iQSoFn6kwnQXy1V6ispA34cdWf0kq9PXP9Xa1d1EW880Nt"

PERCENTAGE_BUY = 5

PERCENTAGE_STOP = 3

client = Client(API_KEY, API_SECRET)


def adjuste_round(value):
    if value < 1:
        return round(value, 4)
    if value < 100:
        return round(value, 2)
    if value < 500:
        return round(value, 1)
    else:
        return int(value)


def get_current_price_crypto(crypto):
    try: 
        date_price = client.get_recent_trades(symbol=crypto, limit=1)
        price = float(date_price[0]["price"])

        return adjuste_round(price)

    except Exception as e:
        print(f"get_current_price_crypto. Erro: {e}")
        return 'ERROR'


def create_order_buy_long_or_short(index, crypto, buy_or_sell, direction, quantity):

    res = client.futures_create_order(
        symbol=crypto,
        side=buy_or_sell,
        positionSide=direction,
        dualSidePosition= False,
        type='MARKET',
        quantity=quantity
        )

    return res



def closed_market(index, crypto, direction, qtd=999):
    try:
        price_crypto = get_current_price_crypto(crypto)
        qtd = 999

        if price_crypto <= 0.9:
            qtd = 9999
        if price_crypto <= 0.09:
            qtd = 99999        
        if price_crypto <= 0.009:
            qtd = 999999
  
        if price_crypto > 1000:
            qtd = 9

        if direction != "NOT TRADED":
            res = client.futures_create_order(
                symbol=crypto,
                side="SELL",
                positionSide=direction,
                dualSidePosition= False,
                type='MARKET',
                quantity=int(qtd),
                )
            return res
        else:
            return {"side":"ERROR","status": "CLOSED_ERROR"}

    except Exception as e:
        return {"side":"ERROR","status": "CLOSED_ERROR", "error": e}

#APIError(code=-2022): ReduceOnly Order is rejected
#APIError(code=-4005): Quantity greater than max quantity.
#{"code":-1102,"msg":"Mandatory parameter \'positionSide\' was not sent, was empty/null, or malformed."}
#{"code":-4005,"msg":"Quantity greater than max quantity."

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

    percentage = PERCENTAGE_BUY / 100

    _value = ((value_available * 20) * percentage) / price_crypto

    if _value < 1:
        return round(_value, 3)
    if _value < 10:
        return round(_value, 2)
    else:
        return int(_value)



def calculate_price_stop_limit(crypto):
    try: 
        print("Adicionando stop_price: ", crypto)
        cur_price = get_current_price_crypto(crypto)

        #desconto de 3%
        perc = PERCENTAGE_STOP / 100
        stop_price = float(cur_price - (cur_price * perc))

        return adjuste_round(stop_price)

    except Exception as e:
        print(f"calculate_price_stop_limit. Erro: {e}")
        return 'ERROR'
