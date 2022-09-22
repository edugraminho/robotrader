import time
from Variables.config import *
from Libraries.utils import *
from Libraries.telegram_api import *
from Libraries.futures_api import *


def main():
    while True:
        get_messages_group()

"""
        connect_telegram()
        print("blas")
        time.sleep(2)

        last_spot = last_spot_dict()

        signal_type = ''
        
        if last_spot["signal_type"] == "new":
            signal_type = "BUY"
            value = find_value_to_aport(last_spot["crypto_name"])

            status_b = create_order_buy_long_or_short(
                index=last_spot["index"],
                crypto=last_spot["crypto_name"],
                buy_or_sell=signal_type,
                direction=last_spot["direction"].upper(),
                quantity=value,
                )

            if status_b == OK:
                #adicionar o valor da compra no csv
                price = get_current_price_crypto(last_spot["crypto_name"])
                insert_csv_status(last_spot["index"], "BUY", status_b['orderId'], price)




        if last_spot["signal_type"] == "closed":
            signal_type = "SELL"
            status_c = closed_market(
                index=last_spot["index"],
                crypto=last_spot["crypto_name"],
                direction=last_spot["direction"].upper(),
            )

            if status_c == OK:
                insert_csv_status(last_spot["index"], "SELL", status_c['orderId'], 0)

#main()

def stop_loss_closed():

    cryptos_data = read_csv()
    for c in cryptos_data:
        if c["status"] == "BUY":
            calculate_stop_limit(c["index"], c["crypto_name"], c["direction"], c["price_buy"])
            


stop_loss_closed()
    
"""
main()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(get_messages_group(client))
# loop.close()


# testar como se comporta quando tem duas posicoes, LONG e SHORT
# adicionar STOP_LOSS

# adicionar o valor de compra no csv. Percorrer ele, para cada crypto acionar buscar o valor da moeda atual.  get_current_price_crypto
# Caso seja short, >= current value + 3% - se positivo vende na hora.
# Caso seja long, <= current value - 3% - se positivo vende na hora.
# Chamando a funcao closed_market