import math
import time
from binance.client import Client
from binance.enums import *
from Libraries.utils import *
from Libraries.logger import get_logger
from Variables.config import *


client = Client(API_KEY, API_SECRET)

logger = get_logger(__name__)


def adjuste_round_value_aport(value):

    if value < 0.01:
        return round(float(value), 4)
    if value < 0.1:
        return round(float(value), 3)
    if value < 1:
        return round(float(value), 2)
    if value < 10:
        return round(float(value), 1)
    else:
        return int(value)


def adjuste_round_stop_price(value):

    if value < 0.01:
        return round(float(value), 5)
    if value < 0.1:
        return round(float(value), 4)
    if value < 1:
        return round(float(value), 3)
    if value < 999:
        return round(float(value), 2)
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

        return adjuste_round_value_aport(price)

    except Exception as e:
        logger.error(f"get_current_price_crypto. Erro: {e}")
        return 'ERROR'


def create_order_buy_long_or_short(crypto, buy_or_sell, direction, quantity):
    try:
        precision = 5
        qty = quantity

        while True:
            try:
                res = client.futures_create_order(
                    symbol=crypto,
                    side=buy_or_sell,
                    positionSide=direction,
                    dualSidePosition=False,
                    type='MARKET',
                    quantity=qty
                )

                return (True, res)

            except Exception as e:
                '''
                    Erro -1111 eh quando a precisao esta acima para o ativo
                    vai diminuindo as casas decimais ate dar certo
                '''
                if e.code == -1111:
                    precision -= 1
                    if precision == 0:
                        qty = int(qty)
                    qty = round(
                        float(qty), precision)
                    continue
                else:
                    raise e

    except Exception as e:
        logger.error(f'Erro create_order_buy_long_or_short: {e}')
        return (False, e)


def closed_market(crypto, direction, amount):
    try:

        # aumenta 10% de qq valor, e para valores como 0.002 arredonda pra 1
        current_amount = int(math.ceil(abs(float(amount) + (float(amount) * 0.1))))

        buy_or_sell = "SELL"

        if direction == "SHORT":
            buy_or_sell = "BUY"

        status = client.futures_create_order(
            symbol=crypto,
            side=buy_or_sell,
            positionSide=direction,
            dualSidePosition=False,
            type='MARKET',
            quantity=current_amount,
        )

        return (True, status)

    except Exception as e:
        logger.error(f'Erro closed_market: {e}')
        return (False, e)


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

        _value = ((total_balance * LEVERAGE) /
                  QNT_CRYPTOS_TO_PURCHASE) / price_crypto

        if _value < 0.1:
            return round(_value, 3)
        if _value < 1:
            return round(_value, 2)
        if _value < 10:
            return round(_value, 1)
        else:
            return int(_value)
    except Exception as e:
        logger.error(f"find_value_to_aport. Erro: {e}")


def calculate_price_stop_limit(crypto, direction):
    try:
        cur_price = get_current_price_crypto(crypto)

        # desconto de 3%
        perc = PERCENTAGE_STOP / 100

        stop_price = float(cur_price - (cur_price * perc))
        if direction == "SHORT":
            stop_price = float(cur_price + (cur_price * perc))

        return adjuste_round_stop_price(stop_price)

    except Exception as e:
        logger.error(f"calculate_price_stop_limit. Erro: {e}")
        return 'ERROR'


def get_all_open_positions_binance():
    success = False
    max_tries = 5
    tries = 0
    while not success and tries < max_tries:
        try:
            all_open_positions_list = []
            all_open_positions = client.futures_position_information(timeout=30)
            for positions in all_open_positions:
                amount = positions["positionAmt"]
                unrealized = float(positions['unRealizedProfit'])
                if amount != "0" and unrealized != 0.00000000:
                    all_open_positions_list.append(positions)

            success = True

        except Exception as e:
            logger.error(f"get_all_open_positions_binance. Erro: {e}")
            tries += 1
            time.sleep(10) # espera 10 segundos antes de tentar novamente

    return all_open_positions_list




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
        return {"side": "ERROR", "status": "CLOSE_ERROR", "error": e}


def cancel_open_order():
    try:
        all_positions = get_all_open_positions_binance()
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
        all_positions = get_all_open_positions_binance()
        status_take_profit = 0

        for position in all_positions:
            if position["symbol"] == crypto:
                entry_price = float(position["entryPrice"])
                pos_amount = float(position["positionAmt"])
                buy_or_sell = "SELL"
                if direction == "SHORT":
                    buy_or_sell = "BUY"

                # pego a quantidade de take profits + 1 do close position
                take_profits = len(LIST_TARGETS_TAKE_PROFITS) + 1

                for sum_take_profit in LIST_TARGETS_TAKE_PROFITS:
                    precision = 5

                    ''' divide em partes iguais '''
                    amount_per_profits = round(pos_amount / take_profits, precision)

                    ''' Faz o calculo de quanto a moeda tem q custar pra vender 
                        EX: 6.10 + 0.20 = 6.30'''
                    _sum = sum_take_profit / 100
                    stop_price = entry_price + (entry_price * _sum)

                    if direction == "SHORT":
                        stop_price = float(position["entryPrice"]) - (entry_price * _sum)

                    _stop = adjuste_round_stop_price(stop_price)

                    while True:
                        try:
                            status = client.futures_create_order(
                                symbol=crypto,
                                side=buy_or_sell,
                                type="TAKE_PROFIT_MARKET",
                                positionSide=direction,
                                stopPrice=_stop,
                                quantity=abs(amount_per_profits),
                                timeInForce='GTE_GTC',
                            )

                            if status:
                                status_take_profit += 1

                            break
                        except Exception as e:
                            ''' Erro -1111 eh quando a precisao esta acima para o ativo
                                vai diminuindo as casas decimais ate dar certo'''
                            if e.code == -1111:
                                precision -= 1

                                if precision == 0:
                                    amount_per_profits = int(
                                        amount_per_profits)

                                amount_per_profits = round(
                                    float(amount_per_profits), precision)
                                continue
                            else:
                                return (False, status_take_profit)

        return (True, status_take_profit)

    except Exception as e:
        raise e
