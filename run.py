import time
import asyncio
import pdb
from Libraries.mongo_db import MongoDb
from Libraries.logger import get_logger
from Variables.config import *
from Libraries.telegram_api import get_messages_group
from Libraries.utils import (
    processing_signal_messages
)
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

        untreated_message = get_messages_group()

        signal_data = processing_signal_messages(untreated_message)

        insert_new_signal_db(signal_data)

        ##########################################################################
        ################################# BUY ####################################

        new_orders = new_buy_orders()

        logger.info("BUY")

        all_open_positions = get_all_open_positions_binance()

        for new_buy_order in new_orders:
            _ID = new_buy_order["_id"]
            _CRYPTO_NAME = new_buy_order["crypto_name"]
            _DIRECTION = new_buy_order["direction"]

            try:
                #Verifica se há DUPLICIDADE, e atualiza se ouver
                for positions in all_open_positions:
                    if _CRYPTO_NAME == positions["symbol"]:
                        logger.info(f'DUPLICIDADE na crypto: {_CRYPTO_NAME}')
                        _id = {"_id": _ID}

                        update = {"$set": {"status": "DUPLICATE"}}
                        update_one(_id, update)
                        break

                value = find_value_to_aport(_CRYPTO_NAME)


                logger.info(
                    f'{50*"="}\n Nova ordem de COMPRA. Moeda: {_CRYPTO_NAME} - ${value}')
                
                buy_or_sell = "BUY"

                if _DIRECTION == "SHORT":
                    buy_or_sell = "SELL"

                status_buy = create_order_buy_long_or_short(
                    crypto=_CRYPTO_NAME,
                    buy_or_sell=buy_or_sell,
                    direction=_DIRECTION,
                    quantity=value,
                )

                if status_buy[0]:

                    price = get_current_price_crypto(_CRYPTO_NAME)
                    stop_price = calculate_price_stop_limit(
                        _CRYPTO_NAME, _DIRECTION)
                    add_stop_limit(_CRYPTO_NAME, _DIRECTION, stop_price)

                    status_take = add_take_profit(_CRYPTO_NAME, _DIRECTION)
                    logger.info(
                        f"Take-Profit. Moeda: {_CRYPTO_NAME} - {status_take[1]}")

                    if status_buy[1]["status"] == "NEW":
                        # adicionar o status da compra no banco
                        id_obj = {"_id": _ID}
                        data_update = {
                            "$set": {
                                "signal_type": status_buy[1]["status"],
                                "status": status_buy[1]["side"],
                                "direction": status_buy[1]["positionSide"],
                                "price_buy": str(price),
                                "stop_price": str(stop_price),
                                "qty": str(status_buy[1]['origQty'])
                            }}
                        update_one(id_obj, data_update)

                else:
                    id_obj = {"_id": _ID}
                    _error = f"ERROR {status_buy[1].code}"
                    data_update = {
                        "$set": {
                            "signal_type": "ERROR",
                            "status": _error
                        }}
                    update_one(id_obj, data_update)

            except Exception as e:
                id_obj = {"_id": _ID}
                data_update = {
                    "$set": {
                        "signal_type": "ERROR",
                        "status": "EXCEPTION"
                    }}
                update_one(id_obj, data_update)
                logger.error(f'Exception na compra: {_ID} - {e}')
                pass


        ########################################################################
        ############################### CLOSE ##################################

        all_open_positions = get_all_open_positions_binance()

        closing_orders = check_closing_orders_db()

        if closing_orders[0]:
            for close_order in closing_orders[1]:

                _ID = close_order["_id"]
                _REPLY_TO = close_order["reply_to"]
                _SIGNAL_TYPE = close_order["signal_type"]
                _CRYPTO_NAME = close_order["crypto_name"]
                _DIRECTION = close_order["direction"]


                try:
                    for positions in all_open_positions:

                        if _CRYPTO_NAME == positions["symbol"]:
                            logger.info(" ")
                            logger.info(50*"-")
                            logger.info(f'Fechando posicao:  {_CRYPTO_NAME}')

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
                                        "status": status_closing[1]["side"],
                                        "direction": status_closing[1]["positionSide"],
                                        "qty": str(status_closing[1]['origQty'])
                                    }}
                                update_one(_id, data_update)

                                _id_reply = {"reply_to": _REPLY_TO}
                                data_update = {
                                    "$set": {
                                        "status": status_closing[1]["side"],
                                        "signal_type" : _SIGNAL_TYPE,
                                    }}
                                update_one(_id_reply, data_update)

                except Exception as e:
                    id_obj = {"_id": _ID}
                    data_update = {
                        "$set": {
                            "signal_type": "ERROR",
                            "status": "EXCEPTION"
                        }}

                    # update_one(cll, id_obj, data_update)
                    logger.error(f'Exception na VENDA: {_ID} - {e}')
                    pass


        ###########################################################################
        ############################### STOP LOSS MANUAL #################################

        open_orders = open_orders_db()

        #all_open_positions = get_all_open_positions_binance()

        logger.info("all_open_positions")

        for open_order in open_orders:
            _ID = open_order["_id"]
            _CRYPTO_NAME = open_order["crypto_name"]
            _DIRECTION = open_order["direction"]
            _STATUS = open_order["status"]
            _STOP_PRICE = float(open_order["stop_price"])
            
            for positions in all_open_positions:
                if _CRYPTO_NAME == positions["symbol"]:

                    _CURRENT_PRICE = float(
                        get_current_price_crypto(_CRYPTO_NAME))
                    
                    try:

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


        # mongo_db.delete_old_date()

        # time.sleep(10)


asyncio.run(trade())


"""

> Usar a funcao get_all_open_positions_binance para verificar se ja existem posicoes abertas
para evitar comprar 2X. 

Se symbol == crypto_name and .....

"""
