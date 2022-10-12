from binance.client import Client
import math
from binance.enums import *
from Libraries.utils import *
from Libraries.logger import get_logger
from Variables.config import * 


client = Client(API_KEY, API_SECRET)

logger = get_logger(__name__)


def adjuste_round(value):
    if value < 0.01:
        return round(float(value), 5)
    if value < 0.1:
        return round(float(value), 4)
    if value < 1:
        return round(float(value), 3)
    if value < 10:
        return round(float(value), 2)
    if value < 300:
        return round(float(value), 1)
    # if value < 500:
    #     return round(value, 1)
    else:
        return int(value)


def adjust_leverage(crypto):
    try:
        return client.futures_change_leverage(
            symbol=crypto, 
            leverage=LEVERAGE
            )

    except Exception as e:
        logger.error(f"adjust_leverage. Erro: {e}")
        pass

def get_current_price_crypto(crypto):
    try: 
        date_price = client.get_recent_trades(symbol=crypto, limit=1)
        price = float(date_price[0]["price"])

        return adjuste_round(price)

    except Exception as e:
        logger.error(f"get_current_price_crypto. Erro: {e}")
        return 'ERROR'


def create_order_buy_long_or_short(crypto, buy_or_sell, direction, quantity):
    try:
        res = client.futures_create_order(
            symbol=crypto,
            side=buy_or_sell,
            positionSide=direction,
            dualSidePosition= False,
            type='MARKET',
            quantity=quantity
            )

        return res
    except Exception as e:
        logger.error(f'Erro create_order_buy_long_or_short: {e}')
        pass


def closed_market(index, crypto, direction, qtd):
    try:
        all_positions = get_all_open_positions()

        for position in all_positions:
            if position["symbol"] == crypto:
                current_amount = int(math.ceil(abs(float(position["positionAmt"])))*1.2)

                buy_or_sell = "SELL"

                if direction == "SHORT":
                    buy_or_sell = "BUY"

                res = client.futures_create_order(
                    symbol=crypto,
                    side=buy_or_sell,
                    positionSide=direction,
                    dualSidePosition= False,
                    type='MARKET',
                    quantity=current_amount,
                    )

                return res
        else:
            logger.error(f'Erro closed_market: {index} - {crypto}')
            return {"side":"ERROR","status": "CLOSE_ERROR"}

    except Exception as e:
        logger.error(f'Erro closed_market: {e}')
        return {"side":"ERROR","status": "CLOSE_ERROR", "error": e}



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
    try:

        price_crypto = get_current_price_crypto(crypto)
        total_balance = get_balance()[0]["total_balance"]

        _value = ((total_balance * LEVERAGE) / QNT_CRYPTOS_TO_PURCHASE) / price_crypto

        if _value < 1:
            return round(_value, 3)
        if _value < 10:
            return round(_value, 2)
        else:
            return int(_value)
    except Exception as e:
        logger.error(f"find_value_to_aport. Erro: {e}")



def calculate_price_stop_limit(crypto, direction):
    try: 
        cur_price = get_current_price_crypto(crypto)

        #desconto de 3%
        perc = PERCENTAGE_STOP / 100

        stop_price = float(cur_price - (cur_price * perc))
        if direction == "SHORT":
            stop_price = float(cur_price + (cur_price * perc))

        return adjuste_round(stop_price)

    except Exception as e:
        logger.error(f"calculate_price_stop_limit. Erro: {e}")
        return 'ERROR'


def get_all_open_positions():
    try:
        all_open_positions_list = []

        all_open_positions = client.futures_position_information()
        for positions in all_open_positions:
            amount = positions["positionAmt"]
            unrealized = float(positions['unRealizedProfit'])
            if amount != "0" and unrealized != 0.00000000:
                all_open_positions_list.append(positions)


        return all_open_positions_list

    except Exception as e:
        logger.error(f"get_all_open_positions. Erro: {e}")



def add_stop_limit(crypto, direction, stop_price):
    try:
        buy_or_sell = "SELL"

        if direction == "SHORT":
            buy_or_sell = "BUY"

        res = client.futures_create_order(
            symbol=crypto,
            side=buy_or_sell,
            type='STOP_MARKET',
            positionSide=direction,
            stopPrice=stop_price,
            closePosition=True,
            timeInForce='GTE_GTC'
            )
        return res

    except Exception as e:
        logger.error(f'Erro add_stop_limit: {e}')
        return {"side":"ERROR","status": "CLOSE_ERROR", "error": e}


def cancel_open_order():
    try:
        all_positions = get_all_open_positions()
        all_open_orders = client.futures_get_open_orders()

        for position in all_positions:
            for open_orders in all_open_orders:
                if position["symbol"] != open_orders["symbol"]:
                    client.futures_cancel_order(
                        symbol=open_orders["symbol"],
                        orderId=open_orders["orderId"]
                        )
    except Exception as e:
        logger.error(f'Erro cancel_open_order: {e}')
        raise e


def add_take_profit(crypto, direction):
    try:
        all_positions = get_all_open_positions()

        for position in all_positions:
            if position["symbol"] == crypto:

                buy_or_sell = "SELL"

                if direction == "SHORT":
                    buy_or_sell = "BUY"
                
                # pego a quantidade de take profits + 1 do close position
                take_profits = len(LIST_PERCENTAGE_TAKE_PROFITS) + 1
                amount_per_profits = round(float(position["positionAmt"]) / take_profits, 3)
                _amount = adjuste_round(amount_per_profits)

                for perc_take_profit in LIST_PERCENTAGE_TAKE_PROFITS:

                    perc = perc_take_profit / 100
                    stop_price = float(position["entryPrice"]) + (float(position["entryPrice"]) * perc)
                    
                    if direction == "SHORT":
                        stop_price = float(position["entryPrice"]) - (float(position["entryPrice"]) * perc)

                    _stop = adjuste_round(stop_price)

                    client.futures_create_order(
                        symbol=crypto,
                        side=buy_or_sell,
                        type="TAKE_PROFIT_MARKET",
                        positionSide=direction,
                        stopPrice=_stop,
                        quantity=abs(_amount),
                        timeInForce='GTE_GTC',
                        )
                    
    except Exception as e:
        logger.error(f'Erro add_take_profit: {e}')
        raise e


'''
[
   {
      "orderId":6603176803,
      "symbol":"GRTUSDT",
      "status":"NEW",
      "clientOrderId":"3qzLPi0yH9npDq2Cemg4T7",
      "price":"0",
      "avgPrice":"0",
      "origQty":"0",
      "executedQty":"0",
      "cumQuote":"0",
      "timeInForce":"GTC",
      "type":"STOP_MARKET",
      "reduceOnly":true,
      "closePosition":true,
      "side":"SELL",
      "positionSide":"LONG",
      "stopPrice":"0.09570",
      "workingType":"CONTRACT_PRICE",
      "priceProtect":false,
      "origType":"STOP_MARKET",
      "time":1665229560351,
      "updateTime":1665229560351
   },
   {
      "orderId":82028560617,
      "symbol":"BTCUSDT",
      "status":"NEW",
      "clientOrderId":"NHMmGcmHPdpj6PjnLhsuc4",
      "price":"0",
      "avgPrice":"0",
      "origQty":"0",
      "executedQty":"0",
      "cumQuote":"0",
      "timeInForce":"GTC",
      "type":"STOP_MARKET",
      "reduceOnly":true,
      "closePosition":true,
      "side":"SELL",
      "positionSide":"LONG",
      "stopPrice":"19134",
      "workingType":"CONTRACT_PRICE",
      "priceProtect":false,
      "origType":"STOP_MARKET",
      "time":1665228609662,
      "updateTime":1665228609662
   },
   {
      "orderId":7798392109,
      "symbol":"MANAUSDT",
      "status":"NEW",
      "clientOrderId":"eKegDwf2A7GS3UVBNuKlMM",
      "price":"0",
      "avgPrice":"0",
      "origQty":"0",
      "executedQty":"0",
      "cumQuote":"0",
      "timeInForce":"GTC",
      "type":"STOP_MARKET",
      "reduceOnly":true,
      "closePosition":true,
      "side":"SELL",
      "positionSide":"LONG",
      "stopPrice":"0.6840",
      "workingType":"CONTRACT_PRICE",
      "priceProtect":false,
      "origType":"STOP_MARKET",
      "time":1665230733961,
      "updateTime":1665230733961
   },
   {
      "orderId":4389712130,
      "symbol":"ALICEUSDT",
      "status":"NEW",
      "clientOrderId":"50cOegmBrBwc4spn8US5XU",
      "price":"0",
      "avgPrice":"0",
      "origQty":"0",
      "executedQty":"0",
      "cumQuote":"0",
      "timeInForce":"GTC",
      "type":"STOP_MARKET",
      "reduceOnly":true,
      "closePosition":true,
      "side":"SELL",
      "positionSide":"LONG",
      "stopPrice":"1.690",
      "workingType":"CONTRACT_PRICE",
      "priceProtect":false,
      "origType":"STOP_MARKET",
      "time":1665233129388,
      "updateTime":1665233129388
   },
   {
      "orderId":1726773133,
      "symbol":"GTCUSDT",
      "status":"NEW",
      "clientOrderId":"5AWBGCloGlYxHalVgyuELI",
      "price":"0",
      "avgPrice":"0",
      "origQty":"0",
      "executedQty":"0",
      "cumQuote":"0",
      "timeInForce":"GTC",
      "type":"STOP_MARKET",
      "reduceOnly":true,
      "closePosition":true,
      "side":"SELL",
      "positionSide":"LONG",
      "stopPrice":"1.790",
      "workingType":"CONTRACT_PRICE",
      "priceProtect":false,
      "origType":"STOP_MARKET",
      "time":1665212470273,
      "updateTime":1665212470274
   },
   {
      "orderId":2996539940,
      "symbol":"HBARUSDT",
      "status":"NEW",
      "clientOrderId":"XcsJyD9XawPDzdtFdKMnsX",
      "price":"0",
      "avgPrice":"0",
      "origQty":"0",
      "executedQty":"0",
      "cumQuote":"0",
      "timeInForce":"GTC",
      "type":"STOP_MARKET",
      "reduceOnly":true,
      "closePosition":true,
      "side":"SELL",
      "positionSide":"LONG",
      "stopPrice":"0.05860",
      "workingType":"CONTRACT_PRICE",
      "priceProtect":false,
      "origType":"STOP_MARKET",
      "time":1665217821276,
      "updateTime":1665217821276
   },
   {
      "orderId":4629827564,
      "symbol":"ONEUSDT",
      "status":"NEW",
      "clientOrderId":"qlpIvea0LAdRDh1VPPNDf2",
      "price":"0",
      "avgPrice":"0",
      "origQty":"0",
      "executedQty":"0",
      "cumQuote":"0",
      "timeInForce":"GTC",
      "type":"STOP_MARKET",
      "reduceOnly":true,
      "closePosition":true,
      "side":"SELL",
      "positionSide":"LONG",
      "stopPrice":"0.01880",
      "workingType":"CONTRACT_PRICE",
      "priceProtect":false,
      "origType":"STOP_MARKET",
      "time":1665212423843,
      "updateTime":1665212423843
   },
   {
      "orderId":7866666382,
      "symbol":"ZILUSDT",
      "status":"NEW",
      "clientOrderId":"cf8AYY647dBV2s3sTXmCI6",
      "price":"0",
      "avgPrice":"0",
      "origQty":"0",
      "executedQty":"0",
      "cumQuote":"0",
      "timeInForce":"GTC",
      "type":"STOP_MARKET",
      "reduceOnly":true,
      "closePosition":true,
      "side":"SELL",
      "positionSide":"LONG",
      "stopPrice":"0.03100",
      "workingType":"CONTRACT_PRICE",
      "priceProtect":false,
      "origType":"STOP_MARKET",
      "time":1665222311694,
      "updateTime":1665222311694
   }
]
'''