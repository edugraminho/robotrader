import time
import asyncio
from Variables.config import *
from Libraries.utils import processing_signal_messages
from Libraries.telegram_api import get_messages_group
from Libraries.futures_api import *
from Libraries.mongo_db import connect_db, insert_new_signal_db, get_last_insert, update_one
from Libraries.logger import get_logger

logger = get_logger(__name__)

cll = connect_db()


def trade():

    while True:

        untreated_message = get_messages_group()

        signal_data = processing_signal_messages(untreated_message)

        insert_signal_status = insert_new_signal_db(cll, signal_data)

        # if insert_signal[0]:
        #     print(f'Sinal inserido no banco: {insert_signal[1]}')


        #{'_id': 55601, 'date': '25-01-23 09:09:35', 'crypto_name': 'IOTXUSDT', 'direction': 'OPEN_ORDER', 'signal_type': 'CLOSE'}

        last_spot = get_last_insert(cll)

        last_spot = {"_id":{"$numberInt":"57848"},"date":"07-02 02:33:38","crypto_name":"EGLDUSDT","direction":"LONG","signal_type":"NEW","status":"","price_buy":"","stop_price":"","qty":""}
        # time.sleep(10)



        ##########################################################################
        ################################# BUY ####################################
        try:
            '''
            all_open_positions = get_all_open_positions()

            for positions in all_open_positions:
                if last_spot["crypto_name"] == positions["symbol"]:

                    filter = {"_id": last_spot["_id"]}

                    update = {"$set": {"status": "DUPLICATE"}}
                    status = update_one(cll, filter, update)
            '''


            if last_spot["signal_type"] == "NEW" and last_spot["status"] == "":
                crypto_name = last_spot["crypto_name"]

                value = find_value_to_aport(crypto_name)
                logger.info(50*"=")
                logger.info(f"Nova ordem de COMPRA. Moeda: {crypto_name} - ${value}")
                
                buy_or_sell = "BUY"
                
                if last_spot["direction"] == "SHORT":
                    buy_or_sell = "SELL"
            
                status_buy = create_order_buy_long_or_short(
                    crypto=crypto_name,
                    buy_or_sell=buy_or_sell,
                    direction=last_spot["direction"],
                    quantity=value,
                    )
                price = get_current_price_crypto(crypto_name)
                stop_price = calculate_price_stop_limit(crypto_name, last_spot["direction"])


                add_stop_limit(last_spot["crypto_name"], last_spot["direction"], stop_price)

                status_take = add_take_profit(last_spot["crypto_name"], last_spot["direction"])
                logger.info(f"Take-Profit. Moeda: {crypto_name} - {status_take[1]}")


                if status_buy["status"] == "NEW":
                    #adicionar o status da compra no banco
                    id_obj = {"_id": last_spot["_id"].get("$numberInt")}

                    data_update = {
                        "$set": {
                            "signal_type" : status_buy["status"],
                            "status" : status_buy["side"],
                            "direction" : status_buy["positionSide"],
                            "price_buy" : str(price),
                            "stop_price" : str(stop_price),
                            "qty" : str(status_buy['origQty'])
                    }}

                    update_one(cll, id_obj, data_update)



        except Exception as e:

            filter = {"_id": last_spot["_id"]}

            update = {
                "$set": {
                    "signal_type" : status_buy["status"],
                    "status" : "ERROR"

            }}

            # status = update_one(cll, filter, update)

            # insert_csv_status(
            #     c_index=last_spot["index"],
            #     direction=last_spot["direction"],
            #     signal_type='BUY',
            #     status='ERROR'
            # )
            logger.error(f'Erro ao Efetuar a compra: {last_spot["_id"]} - {e}')
            raise e
        
        """

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

        except Exception as e:
            logger.error(f"Erro ao fechar posicao: {e}")
            pass


        ###########################################################################
        ############################### STOP LOSS #################################
        try:
            check_stop = check_all_stop_loss()

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
"""

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