import time
import asyncio
from Variables.config import *
from Libraries.utils import *
from Libraries.telegram_api import *
from Libraries.futures_api import *
from Libraries.logger import get_logger

logger = get_logger(__name__)


def trade():

    client = connect()
    while True:
        start = time.time()
        # time.sleep(1)
        get_messages_group(client)

        last_spot = last_spot_dict()
        ###########################################################################
        ################################## BUY ####################################
        try:
            all_open_positions = get_all_open_positions()
            for positions in all_open_positions:
                if last_spot["crypto_name"] == positions["symbol"]:
                    pass
                    # insert_csv_status(
                    #     c_index=last_spot["index"],
                    #     direction=last_spot["direction"],
                    #     signal_type=last_spot["signal_type"],
                    #     status="DUPLICATE"
                    #     )

            if last_spot["signal_type"] == "NEW" and last_spot["status"] == "":
                crypto_name = last_spot["crypto_name"]

                value = find_value_to_aport(crypto_name)
                logger.info(50*"=")
                logger.info(f"Nova ordem de COMPRA. Moeda: {crypto_name} - {value}")
                
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
                stop_price = calculate_price_stop_limit(crypto_name)


                if status_buy["status"] == "NEW":
                    #adicionar o valor da compra no csv
                    insert_csv_status(
                        c_index=last_spot["index"],
                        signal_type=status_buy["status"],
                        status=status_buy["side"],
                        direction=status_buy["positionSide"],
                        price_buy=price,
                        stop_price=stop_price,
                        qtd=status_buy['origQty']
                        )

        except Exception as e:
            insert_csv_status(
                c_index=last_spot["index"],
                direction=last_spot["direction"],
                signal_type='BUY',
                status='ERROR'
            )
            logger.error(f'Erro ao Efetuar a compra: {last_spot["index"]} - {e}')
            pass
        


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
                        qtd=qtd,
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

            if check_stop[0]: 
                for s in check_stop[1].iterrows():
                    cur_price = float(get_current_price_crypto(s[1]['crypto_name']))

                    index = s[1]['index']
                    crypto_name = s[1]['crypto_name']
                    direction = s[1]['direction']
                    signal_type = s[1]['signal_type']
                    status = s[1]['status']
                    price_buy = s[1]['price_buy']
                    stop_price = float(s[1]['stop_price'])
                    qtd = s[1]['qtd']


                    if status == "BUY" and direction == "LONG":
                        if cur_price <= stop_price:
                            closed_res = closed_market(
                                index=index,
                                crypto=crypto_name,
                                direction=direction,
                                qtd=qtd,
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
                                qtd=qtd,
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

        # print("TEMPO TOTAL DE EXEC: ", round(time.time() - start, 3))


asyncio.run(trade())


"""
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

"""