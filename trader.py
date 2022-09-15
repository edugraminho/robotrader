import time
from Variables.config import *
from Libraries.utils import *
from Libraries.telegram_api import *


def main():
    while True:

        connect_telegram()
        print("blas")
        time.sleep(2000)

    # pegar a ultima linha csv
    find_value_to_aport("ETHUSDT")
    
    status = create_order_buy_long_or_short(index, crypto, buy_or_sell, direction, quantity)
    
    # adicionar status e o numero da ordem no csv

    # if res["status"] == "NEW":
    #     insert_csv_status(index, buy_or_sell, res['orderId'])

    # adicionar stop limit. TEM Q IMPLEMENTAR AINDA

    # Fechar mercado
    closed_market(index, crypto, direction)

main()


# loop = asyncio.get_event_loop()
# loop.run_until_complete(get_messages_group(client))
# loop.close()


# testar como se comporta quando tem duas posicoes, LONG e SHORT
# adicionar STOP_LOSS