import time
from Variables.config import *
from Libraries.utils import *
from Libraries.telegram_api import *
from Libraries.futures_api import *
import asyncio


def trade():

    client = connect()

    while True:
        time.sleep(3)

        get_messages_group(client)

        last_spot = last_spot_dict()
        ###########################################################################
        ################################## BUY ####################################
        try:
            
            if last_spot["signal_type"] == "NEW" and last_spot["status"] == "":
                crypto_name = last_spot["crypto_name"]

                value = find_value_to_aport(crypto_name)
                print(50*"=")
                print(f"Nova ordem de COMPRA. Moeda: {crypto_name} - {value}")

                status_buy = create_order_buy_long_or_short(
                    index=last_spot["index"],
                    crypto=crypto_name,
                    buy_or_sell="BUY",
                    direction=last_spot["direction"],
                    quantity=value,
                    )
                price = get_current_price_crypto(crypto_name)
                stop_price = calculate_price_stop_limit(crypto_name)

                if status_buy["status"] == "NEW" and price != 'ERROR' and stop_price != 'ERROR':
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
                status='ERROR',
                error=e
            )
            pass
        

        ########################################################################
        ############################### CLOSED #################################
        
        if last_spot["signal_type"] == "CLOSED" and last_spot["status"] == "" :
            
            try:
                status_closed = closed_market(
                    index=last_spot["index"],
                    crypto=last_spot["crypto_name"],
                    direction=last_spot["direction"],
                    qtd=last_spot["qtd"]
                )

                if status_closed["side"] == "SELL" and status_closed["status"] == "NEW":
                    price = get_current_price_crypto(last_spot["crypto_name"])
                    insert_csv_status(
                        c_index=last_spot["index"],
                        direction=last_spot["direction"],
                        signal_type=last_spot["signal_type"],
                        status=status_closed["side"],
                        price_buy=price,
                        qtd=last_spot["qtd"]
                        )

                    print(50*"=")
                    print(f'Nova ordem de VENDA, id: {last_spot["index"]} ')

                elif last_spot["status"] == "BUY":
                    insert_csv_status(
                        c_index=last_spot["index"],
                        direction="NOT_TRADED",
                        signal_type=last_spot["signal_type"],
                        status="NOT_TRADED"
                        )

            except Exception as e:
                insert_csv_status(
                    c_index=last_spot["index"],
                    direction=last_spot["direction"],
                    signal_type=last_spot["signal_type"],
                    status="ERROR_CLOSED",
                    error=e
                    )
                pass


        ###########################################################################
        ############################### CLOSED ALL #################################
        try:
            check_all = check_all_closed_spots()
            if check_all[0]:
                for c in check_all[1].iterrows():
                    all_closed = closed_market(
                        index=c[1]['index'],
                        crypto=c[1]['crypto_name'],
                        direction=c[1]['direction'],
                        qtd=c[1]['qtd'],
                    )

                    if all_closed["side"] == "SELL" and all_closed["status"] == "NEW":
                        insert_csv_status(
                            c_index=c[1]['index'],
                            direction=c[1]['direction'],
                            signal_type=c[1]['signal_type'],
                            status=all_closed["side"],
                            )

        except Exception as e:
            print(f"Erro Closed All: {e}")
            pass

        
        ###########################################################################
        ############################### STOP LOSS #################################
        try:
            check_stop = check_all_stop_loss()

            if check_stop[0]: 
                for s in check_stop[1].iterrows():
                    cur_price = float(get_current_price_crypto(s[1]['crypto_name']))
                    #print(s[1]['index'], s[1]['crypto_name'], s[1]['direction'], float(cur_price), "stop", float(s[1]['stop_price']), s[1]['qtd'])

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
            print("Erro STOP All", e)
            pass


loop = asyncio.get_event_loop()
loop.run_until_complete(trade())
loop.close()


# testar como se comporta quando tem duas posicoes, LONG e SHORT
# adicionar STOP_LOSS

# adicionar o valor de compra no csv. Percorrer ele, para cada crypto acionar buscar o valor da moeda atual.  get_current_price_crypto
# Caso seja short, >= current value + 3% - se positivo vende na hora.
# Caso seja long, <= current value - 3% - se positivo vende na hora.
# Chamando a funcao closed_market