from binance.client import Client
import math
from binance.enums import *
from Libraries.utils import *
from Libraries.logger import get_logger
from Variables.config import * 


client = Client(API_KEY, API_SECRET)

logger = get_logger(__name__)


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



def calculate_price_stop_limit(crypto):
    try: 
        cur_price = get_current_price_crypto(crypto)

        #desconto de 3%
        perc = PERCENTAGE_STOP / 100
        stop_price = float(cur_price - (cur_price * perc))

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
