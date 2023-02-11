import time
import asyncio
import pdb
from Variables.config import *
from Libraries.utils import processing_signal_messages, check_closing_orders_db
from Libraries.telegram_api import get_messages_group
from Libraries.futures_api import *
from Libraries.mongo_db import (
    connect_db,
    insert_new_signal_db,
    update_one,
    find_all
    )
from Libraries.logger import get_logger

logger = get_logger(__name__)

cll = connect_db()


def trade():

    while True:

        untreated_message = get_messages_group()

        signal_data = processing_signal_messages(untreated_message)

        insert_new_signal_db(cll, signal_data)

        # if insert_signal[0]:
        #     print(f'Sinal inserido no banco: {insert_signal[1]}')

        #{'_id': 55601, 'date': '25-01-23 09:09:35', 'crypto_name': 'IOTXUSDT', 'direction': 'OPEN_ORDER', 'signal_type': 'CLOSE'}

        #last_spot = get_last_insert(cll)

        #last_spot = {"_id":{"$numberInt":"57848"},"date":"07-02 02:33:38","crypto_name":"EGLDUSDT","direction":"LONG","signal_type":"NEW","status":"","price_buy":"","stop_price":"","qty":""}
        # time.sleep(10)

        # new_buy_orders = [{"_id":{"$numberInt":"57848"},"date":"07-02 02:33:38","crypto_name":"YYYYUSDT","direction":"LONG","signal_type":"NEW","status":"","price_buy":"","stop_price":"","qty":""},
        # {"_id":{"$numberInt":"57848"},"date":"07-02 02:33:38","crypto_name":"XXXXUSDT","direction":"LONG","signal_type":"NEW","status":"","price_buy":"","stop_price":"","qty":""},
        
        # ]
        ##########################################################################
        ################################# BUY ####################################
        query = {"signal_type": "NEW", "status": ""}
        new_buy_orders = find_all(cll, query)

        all_open_positions = get_all_open_positions()

        for new_buy_order in new_buy_orders:
            _ID = new_buy_order["_id"]
            _CRYPTO_NAME = new_buy_order["crypto_name"]
            _DIRECTION = new_buy_order["direction"]

            try:
                '''
                    Verifica se há DUPLICIDADE, e atualiza se ouver
                '''
                for positions in all_open_positions:
                    if _CRYPTO_NAME == positions["symbol"]:
                        logger.info(f'DUPLICIDADE na crypto: {_CRYPTO_NAME}')
                        _id = {"_id": _ID}

                        update = {"$set": {"status": "DUPLICATE"}}
                        update_one(cll, _id, update)

                value = find_value_to_aport(_CRYPTO_NAME)
                
                logger.info(" ")
                logger.info(50*"=")
                logger.info(f"Nova ordem de COMPRA. Moeda: {_CRYPTO_NAME} - ${value}")
                logger.info(50*"=")
                

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
                    stop_price = calculate_price_stop_limit(_CRYPTO_NAME, _DIRECTION)
                    add_stop_limit(_CRYPTO_NAME, _DIRECTION, stop_price)

                    status_take = add_take_profit(_CRYPTO_NAME, _DIRECTION)
                    logger.info(f"Take-Profit. Moeda: {_CRYPTO_NAME} - {status_take[1]}")

                    if status_buy[1]["status"] == "NEW":
                        # adicionar o status da compra no banco
                        id_obj = {"_id": _ID}
                        data_update = {
                            "$set": {
                                "signal_type" : status_buy[1]["status"],
                                "status" : status_buy[1]["side"],
                                "direction" : status_buy[1]["positionSide"],
                                "price_buy" : str(price),
                                "stop_price" : str(stop_price),
                                "qty" : str(status_buy[1]['origQty'])
                        }}
                        update_one(cll, id_obj, data_update)

                else:
                    id_obj = {"_id": _ID}
                    _error = f"ERROR {status_buy[1].code}"
                    data_update = {
                        "$set": {
                            "signal_type" : "ERROR",
                            "status" : _error
                    }}
                    update_one(cll, id_obj, data_update)


            except Exception as e:
                id_obj = {"_id": _ID}
                data_update = {
                    "$set": {
                        "signal_type" : "ERROR",
                        "status" : "EXCEPTION"
                }}
                update_one(cll, id_obj, data_update)
                logger.error(f'Exception na compra: {_ID} - {e}')
                pass
        

        ########################################################################
        ############################### CLOSE ##################################

        all_positions = get_all_open_positions()

        closing_orders = check_closing_orders_db(cll)

        if closing_orders[0]: 
            for close_order in closing_orders[1]:

                _ID = close_order["_id"]
                _CRYPTO_NAME = close_order["crypto_name"]
                _DIRECTION = close_order["direction"]

                try:
                    for positions in all_positions:

                        if _CRYPTO_NAME == positions["symbol"]:
                            logger.info(" ")
                            logger.info(50*"-")
                            logger.info(f'Fechando posicao:  {_CRYPTO_NAME}')

                            status_closing = closed_market(
                                crypto=_CRYPTO_NAME,
                                direction=positions["positionSide"],
                                amount=positions["positionAmt"],
                            )
                            # if status_closing[0] == False:
                            #     logger.info("(((((((((((((((((((9)))))))))))))))))))")

                            if status_closing[0] and \
                                status_closing[1]["status"] == "NEW":

                                _id = {"_id": _ID}
                                data_update = {
                                    "$set": {
                                        "status" : status_closing[1]["side"],
                                        "direction" : status_closing[1]["positionSide"],
                                        "qty" : str(status_closing[1]['origQty'])
                                }}
                                update_one(cll, _id, data_update)


                except Exception as e:
                    id_obj = {"_id": _ID}
                    data_update = {
                        "$set": {
                            "signal_type" : "ERROR",
                            "status" : "EXCEPTION"
                    }}
                    logger.info(f'****************:  {_CRYPTO_NAME}')

                    # update_one(cll, id_obj, data_update)
                    logger.error(f'Exception na VENDA: {_ID} - {e}')
                    raise e
                    pass


'''

        ###########################################################################
        ############################### STOP LOSS #################################
        # try:
        #     check_stop = check_all_stop_loss()

        ########################################################################
        ############################### CLOSE ##################################
        all_positions = get_all_open_positions()

        check_closing = check_position_closing(all_positions)

        try:
            if check_closing[0]: 
                for _c in check_closing[1].iterrows():

                    index = _c[1]['index']
                    crypto_name = _c[1]['crypto_name']
                    direction = check_closing[2]
                    signal_type = _c[1]['signal_type']
                    status = _c[1]['status']

                    logger.info(f"Fechando Moeda: {index} - {crypto_name}")

                    closing = closed_market(
                        index=index,
                        crypto=crypto_name,
                        direction=direction,
                        qty=0,
                    )

                    if closing["status"] == "NEW":
                        insert_csv_status(
                            c_index=index,
                            direction=direction,
                            signal_type=signal_type,
                            status=closing["side"],
                            )

        except Exception as e:s():
                    cur_price = float(get_current_price_crypto(s[1]['crypto_name']))

                    index = s[1]['index']
                    crypto_name = s[1]['crypto_name']
                    direction = s[1]['direction']
                    signal_type = s[1]['signal_type']
                    status = s[1]['status']
                    price_buy = s[1]['price_buy']
                    stop_price = float(s[1]['stop_price'])
                    qty = s[1]['qty']


                    if status == "BUY" and direction == "LONG":
                        if cur_price <= stop_price:
                            closed_res = closed_market(
                                index=index,
                                crypto=crypto_name,
                                direction=direction,
                                qty=qty,
                            )
                            if closed_res["side"] == "SELL" and closed_res["status"] == "NEW":
                                insert_csv_status(
                                    c_index=index,
                                    direction=direction,
                                    signal_type=signal_type,
                                    status="STOP_LOSS",
                                    price_buy=price_buy,
                                    stop_price=stop_price,
                                    )


                    if status == "BUY" and direction == "SHORT":
                        if cur_price >= stop_price:
                            closed_res = closed_market(
                                index=index,
                                crypto=crypto_name,
                                direction=direction,
                                qty=qty,
                            )

                            if closed_res["side"] == "SELL" and closed_res["status"] == "NEW":
                                insert_csv_status(
                                    c_index=index,
                                    direction=direction,
                                    signal_type=signal_type,
                                    status="STOP_LOSS",
                                    )
        except Exception as e:
            logger.error("Erro STOP All", e)
            pass
        
        #CASO DUPLIQUE O CODIGO, PARA EVITAR COMPRA REPETIDA
        if last_spot["signal_type"] == "NEW" and last_spot["status"] == "":
            logger.info(f'VERIFICAR COMPRA DUPLICADA!!! {last_spot["index"]} - {last_spot["crypto_name"]}')

        print("TEMPO TOTAL DE EXEC: ", round(time.time() - start, 3))
'''

asyncio.run(trade())
# trade()



"""
print(test())
> Usar a funcao get_all_open_positions para verificar se ja existem posicoes abertas
para evitar comprar 2X. 
Se symbol == crypto_name and .....

> Close market, a data tem q ser maior que a compra. (se nao tem vendas q nao foram fechadas e irá vender)

> Adicionar o ajuste de LEVERAGE (CROSS): client.futures_change_leverage(leverage=20)

> Adicionar o Cancelled no regex de CLOSE market

> STOP LOSS
        client.futures_create_order(
            symbol=crypto,
            side='SELL'
            type='STOP_MARKET',
            stopPrice='0.40',
            closePosition=True
            )

> TAKE_PROFIT
        client.futures_create_order(
            symbol=crypto,
            side='SELL'
            type='TAKE_PROFIT_MARKET',
            stopPrice='0.49',
            closePosition=True
            )



> Ajustar a DATA csv

"""