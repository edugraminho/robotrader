from shutil import ExecError
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
            # closed_market(
            #     index=last_spot["index"],
            #     crypto=last_spot["crypto_name"],
            #     direction=last_spot["direction"],
            # )
            
            insert_csv_status(
                c_index=last_spot["index"],
                signal_type='ERROR BUY',
                status='ERROR',
                direction='ERROR',
            )
            print(f'Erro ao comprar moeda. Error: {e}')
            pass
        

        ########################################################################
        ############################### CLOSED #################################

        if last_spot["signal_type"] == "CLOSED" and \
            last_spot["status"] == "" :
            print(50*"=")
            print(f'Nova ordem de VENDA, id: {last_spot["index"]} ')
            try:

                status_closed = closed_market(
                    index=last_spot["index"],
                    crypto=last_spot["crypto_name"],
                    direction=last_spot["direction"],
                )

                if status_closed["side"] == "SELL" and status_closed["status"] == "NEW":
                    price = get_current_price_crypto(last_spot["crypto_name"])
                    insert_csv_status(
                        c_index=last_spot["index"],
                        signal_type=status_closed["status"],
                        status=status_closed["side"],
                        direction=status_closed["positionSide"],
                        price_buy=price,
                        qtd=status_closed['origQty']
                        )
                else:
                    insert_csv_status(
                        c_index=last_spot["index"],
                        signal_type=status_closed["status"],
                        direction="NOT TRADED",
                        status="NOT TRADED"
                        )

            except Exception as e:
                print(f'Erro ao Fechar o sinal: {last_spot["index"]} - {e}')
                pass



        ###########################################################################
        ############################### CLOSED ALL #################################
        try:
            check_all = check_all_closed_spots()

            for c in check_all.iterrows():
                print(c[1]['index'], c[1]['crypto_name'], c[1]['direction'])

                all_closed = closed_market(
                    index=c[1]['index'],
                    crypto=c[1]['crypto_name'],
                    direction=c[1]['direction'],
                )
                if all_closed["side"] == "SELL" and all_closed["status"] == "NEW":
                    insert_csv_status(
                        c_index=c[1]['index'],
                        signal_type=all_closed["status"],
                        status=all_closed["side"],
                        direction=all_closed["positionSide"],
                        )
                else:
                    insert_csv_status(
                        c_index=c[1]['index'],
                        signal_type=all_closed["status"],
                        direction="NOT TRADED",
                        status="NOT TRADED"
                        )
        except:
            continue


        ###########################################################################
        ############################### STOP LOSS #################################
        try:
            if last_spot["status"] == "BUY":
                status_s = stop_loss_closed()
                if status_s[0]:
                    price = get_current_price_crypto(last_spot["crypto_name"])
                    insert_csv_status(
                        c_index=last_spot["index"],
                        signal_type=status_s[1]["status"],
                        status=status_s[1]["side"], 
                        direction=status_s[1]["positionSide"],
                        price_buy=price,
                        qtd=status_s[1]['origQty']
                    )
        except:
            print(f'Erro no Stop Loss: {last_spot["index"]}')
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