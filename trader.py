import time
from Variables.config import *
from Libraries.utils import *
from Libraries.telegram_api import *
from Libraries.futures_api import *
import asyncio


def trade():

    client = connect()

    while True:
        print("iniciando trader")
        get_messages_group(client)

        last_spot = last_spot_dict()

        ################# STOP LOSS ###################
        try:
            if last_spot["signal_type"] == "NEW" and last_spot["status"] == "":
                print("Nova ordem de COMPRA")
                value = find_value_to_aport(last_spot["crypto_name"])

                status_b = create_order_buy_long_or_short(
                    index=last_spot["index"],
                    crypto=last_spot["crypto_name"],
                    buy_or_sell="BUY",
                    direction=last_spot["direction"],
                    quantity=value,
                    )


                if status_b["status"] == "NEW":
                    #adicionar o valor da compra no csv
                    price = get_current_price_crypto(last_spot["crypto_name"])

                    stop_price = calculate_price_stop_limit(last_spot["crypto_name"])

                    insert_csv_status(
                        last_spot["index"], 
                        status_b["side"], 
                        status_b['orderId'], 
                        price,
                        stop_price,
                        status_b['origQty']
                        )
        except:
            print(f'Erro ao comprar moeda: {last_spot["index"]} - {last_spot["crypto_name"]}')
            continue

        ################# CLOSED ###################
        if last_spot["signal_type"] == "CLOSED" and \
            last_spot["status"] != "NOT TRADED":

            print(f'Nova ordem de VENDA, id: {last_spot["index"]} ')
            try:
                status_c = closed_market(
                    index=last_spot["index"],
                    crypto=last_spot["crypto_name"],
                    direction=last_spot["direction"],
                )

                if status_c["status"] == "SELL":
                    price = get_current_price_crypto(last_spot["crypto_name"])
                    insert_csv_status(
                        c_index=last_spot["index"], 
                        b_or_s=status_c["side"], 
                        order_id=status_c['orderId'], 
                        price_buy=price,
                        qtd=status_c['origQty']
                        )
                else:
                    insert_csv_status(
                        c_index=last_spot["index"], 
                        b_or_s="NOT TRADED"
                        )

            except:
                print(f'Erro ao Fechar o sinal: {last_spot["index"]}')
                continue


        ################# STOP LOSS ###################
        try:
            status_s = stop_loss_closed()
            if status_s[0]:
                price = get_current_price_crypto(last_spot["crypto_name"])
                insert_csv_status(
                    c_index=last_spot["index"], 
                    b_or_s=status_s[1]["side"], 
                    order_id=status_s[1]['orderId'], 
                    price_buy=price,
                    qtd=status_s[1]['origQty']
                )
        except:
                print(f'Erro no Stop Loss: {last_spot["index"]}')
                continue

        time.sleep(5)


#async def main():

    #await asyncio.gather(get_messages_group(), trade())
#asyncio.run(main())


loop = asyncio.get_event_loop()
loop.run_until_complete(trade())
loop.close()


# testar como se comporta quando tem duas posicoes, LONG e SHORT
# adicionar STOP_LOSS

# adicionar o valor de compra no csv. Percorrer ele, para cada crypto acionar buscar o valor da moeda atual.  get_current_price_crypto
# Caso seja short, >= current value + 3% - se positivo vende na hora.
# Caso seja long, <= current value - 3% - se positivo vende na hora.
# Chamando a funcao closed_market