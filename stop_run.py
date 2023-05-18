import time
import asyncio
import pdb
from Libraries.mongo_db import MongoDb
from Libraries.logger import get_logger
from Variables.config import *
from Libraries.futures_api import (
    get_all_open_positions_binance,
    find_value_to_aport,
    create_order_buy_long_or_short,
    get_current_price_crypto,
    calculate_price_stop_limit,
    add_stop_limit,
    add_take_profit,
    closed_market,
)
from Libraries.queries import (
    insert_new_signal_db,
    new_buy_orders,
    update_one,
    check_closing_orders_db,
    open_orders_db
)

logger = get_logger(__name__)

mongo_db = MongoDb()

mongo_db.test_connection_db()


def trade():

    while True:
        initial_time = time.time()
        ############### STOP LOSS MANUAL ################
        all_open_positions = get_all_open_positions_binance()

        open_orders = open_orders_db()

        for open_order in open_orders:
            _ID = open_order["_id"]
            _CRYPTO_NAME = open_order["crypto_name"]
            _DIRECTION = open_order["direction"]
            _STATUS = open_order["status"]
            _STOP_PRICE = float(open_order["stop_price"])
            
            for positions in all_open_positions:
                if _CRYPTO_NAME == positions["symbol"]:
                    
                    try:
                        _CURRENT_PRICE = float(
                            get_current_price_crypto(_CRYPTO_NAME))

                        if _STATUS == "BUY" and _DIRECTION == "LONG" and\
                            _CURRENT_PRICE <= _STOP_PRICE:

                            logger.info(f"STOP LOSS na crypto: {_CRYPTO_NAME}")

                            status_closing = closed_market(
                                crypto=_CRYPTO_NAME,
                                direction=positions["positionSide"],
                                amount=positions["positionAmt"],
                            )

                            if status_closing[0] and \
                                    status_closing[1]["status"] == "NEW":

                                _id = {"_id": _ID}
                                data_update = {
                                    "$set": {
                                        "status": "STOP_LOSS",
                                    }}
                                update_one(_id, data_update)



                        if _STATUS == "BUY" and _DIRECTION == "SHORT" and\
                            _CURRENT_PRICE >= _STOP_PRICE:

                            logger.info(f"STOP LOSS na crypto: {_CRYPTO_NAME}")

                            status_closing = closed_market(
                                crypto=_CRYPTO_NAME,
                                direction=positions["positionSide"],
                                amount=positions["positionAmt"],
                            )

                            if status_closing[0] and \
                                    status_closing[1]["status"] == "NEW":

                                _id = {"_id": _ID}
                                data_update = {
                                    "$set": {
                                        "status": "STOP_LOSS",
                                    }}
                                update_one(_id, data_update)


                    except Exception as e:
                        logger.error("Erro STOP LOSS", e)
                        pass

        actual_time = time.time()
        exec_time = actual_time - initial_time
        print(f"Tempo de execução: {exec_time:.2f} segundos", end="\r")


        time.sleep(10)


asyncio.run(trade())


"""

> Usar a funcao get_all_open_positions_binance para verificar se ja existem posicoes abertas
para evitar comprar 2X. 

Se symbol == crypto_name and .....

"""
