import os
import csv
import re
from pathlib import Path, PurePath
import os
from datetime import datetime
import math
import pytz
from logger import get_logger

logger = get_logger(__name__)


TODAY = datetime.today().strftime("%d%m - %H:%M")

# ====================== DIRETÓRIOS LOCAIS ======================
ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
NOW = datetime.now().strftime("%d%m - %H:%M")
DATA_DIRECTORY = os.path.join(ROOT, "Data")
# ===============================================================
"""꧁༺ 𝓢𝓒𝓐𝓛𝓟𝓘𝓝𝓖 300 ༻꧂

✬S◦C°A˚L°P◦I... GTCUSDT ...N◦G°3˚0°0◦0✬
𝓓𝓲𝓻𝓮𝓬𝓽𝓲𝓸𝓷 : LONG
Leverage : Cross 20x
★ Entry : 2.402 - 2.375 ★

🔥Stoploss : 2.20984🔥

ミ★ SCALPING ★彡
Target 1 - 2.41401
Target 2 - 2.42602
Target 3 - 2.45004
ミ★ DAY TRADING ★彡
Target 4 - 2.47406
Target 5 - 2.49808"""



value = """
🔥 #100XX/USDT (Long📉, x20) 🔥

Entry - 0.0337
SL - 25-30%

Take-Profit:
🥇 0.03304 (40% of profit)
🥈 0.03272 (60% of profit)
🥉 0.0324 (80% of profit)
🚀 0.0321 (100% of profit)

"""


def insert_csv(untreated_data):
        all_msgs_data = []


        new_crypto = re.search("#(\w+)/", untreated_data)
                # closed_crypto = re.search('(?<=#)(.[^#]*USDT)', data)

        direction = re.search("\((\w+)\S*,", untreated_data)
        logger.info(new_crypto[1].strip().upper())
        logger.info(direction[1].strip().upper())

        return

        for data in untreated_data:
            if data != None:

                # _date = data.date.astimezone(
                #     pytz.timezone("America/Sao_Paulo")).strftime("%d/%m %H:%M:%S")

                # reply_to = data.reply_to.reply_to_msg_id \
                #     if data.reply_to is not None else ""

                new_crypto = re.search("#(\w+)/", data)
                # closed_crypto = re.search('(?<=#)(.[^#]*USDT)', data)

                direction = re.search("\((\w+)\S*,", data)

                # closed_signal = re.search(
                    # 'Closed|All entry|Cancelled', data.message)

                # all_take_profit = re.search('All take-profit', data.message)

                logger.info(new_crypto)
                logger.info(direction)

                crypto_name = None
                direction_type = None
                signal_type = None
                insert = False

                if new_crypto != None:
                    crypto_name = new_crypto[0].strip().upper()
                    signal_type = "NEW"

                # if closed_crypto != None:
                #     crypto_name = closed_crypto[0].strip().replace(
                #         "/", "").upper()

                # if closed_signal != None:
                #     signal_type = "CLOSE"
                #     insert = True
                #     direction_type = "OPEN_ORDER"

                # if all_take_profit != None:
                #     signal_type = "ALL_TAKE_PROFIT"
                #     insert = True
                #     direction_type = "OPEN_ORDER"

                if direction != None:
                    direction_type = direction[0].strip().upper()
                    insert = True

                if insert:
                    signal_message = {
                        "_id": data.id,
                        "reply_to": reply_to,
                        # "date": str(_date),
                        "crypto_name": crypto_name,
                        "direction": direction_type,
                        "signal_type": signal_type,
                        "status": "",
                        "price_buy": "",
                        "stop_price": "",
                        "qty": "",
                    }

                    all_msgs_data.append(signal_message)
        return all_msgs_data


insert_csv(value)





def processing_signal_messages(untreated_data):
    try:
        #logger.info(f"Processando as mensagem...")

        all_msgs_data = []

        for data in untreated_data:
            if data.message != None:

                _date = data.date.astimezone(
                    pytz.timezone("America/Sao_Paulo")).strftime("%d/%m %H:%M:%S")

                reply_to = data.reply_to.reply_to_msg_id \
                    if data.reply_to is not None else ""

                new_crypto = re.search('(?<=I... )(.[^#]*USDT)', data.message)
                closed_crypto = re.search('(?<=#)(.[^#]*USDT)', data.message)

                direction = re.search('LONG|SHORT', data.message)

                closed_signal = re.search(
                    'Closed|All entry|Cancelled', data.message)

                all_take_profit = re.search('All take-profit', data.message)

                crypto_name = None
                direction_type = None
                signal_type = None
                insert = False

                if new_crypto != None:
                    crypto_name = new_crypto[0].strip().upper()
                    signal_type = "NEW"

                if closed_crypto != None:
                    crypto_name = closed_crypto[0].strip().replace(
                        "/", "").upper()

                if closed_signal != None:
                    signal_type = "CLOSE"
                    insert = True
                    direction_type = "OPEN_ORDER"

                if all_take_profit != None:
                    signal_type = "ALL_TAKE_PROFIT"
                    insert = True
                    direction_type = "OPEN_ORDER"

                if direction != None:
                    direction_type = direction[0].strip().upper()
                    insert = True

                if insert:
                    signal_message = {
                        "_id": data.id,
                        "reply_to": reply_to,
                        "date": str(_date),
                        "crypto_name": crypto_name,
                        "direction": direction_type,
                        "signal_type": signal_type,
                        "status": "",
                        "price_buy": "",
                        "stop_price": "",
                        "qty": "",
                    }

                    all_msgs_data.append(signal_message)
        return all_msgs_data
    except Exception as e:
        logger.error(e)
        pass











def read_csv():
    new_dict = []
    with open(f"C:\\Projects\\cryptobot\\Data\\market.csv") as f:
        reader = csv.DictReader(f)
        print(reader)
        for row in reader:
            
            new_dict.append(row)

    print(new_dict)
# read_csv()

PERCENT = 3
def pay_a_percentage(balance):
    value = int(balance) * (1 - PERCENT / 100)
    return round(15)
    return round(balance - value, 2)

#print(pay_a_percentage(4000))

STOP_LOSS_PERCENTAGE = 8.6
def calculate_stop_limit(price):
    value = int(price * 100) * STOP_LOSS_PERCENTAGE / 100
    return round(price - (value / 100), 3)

# print(calculate_stop_limit(0.223))

x = "323.11220 USDT"

def convert_to_int(str_bal):
    number = round(float(str_bal.split(" ")[0]), 2)
    if number < 1:
        return 0
    
    return int(number)

# print(convert_to_int(x))
from math import floor
def convert_pryce_crypto_to_int(str_balance):
    split_str = str_balance.split(" ")[0].split(".")
    number = float(split_str[0] + "." + split_str[1][:2])
    if number < 10:
        return str(number)
    elif number < 100:
        return str(number)[:-1]

    return str(int(number))

# print(convert_pryce_crypto_to_int("09.9"))



import time

def test(list_spot):
    for index, spot in enumerate(list_spot):
        while spot["crypto_name"] == '':
            print(f'babala {spot["crypto_name"]}')
            time.sleep(3)


# test(list_spot)


def last_line():
    with open(f"C:\\Projects\\cryptobot\\Data\\market.csv", "r",encoding="utf-8", newline='') as f:
        reader = f.readlines()[-1].split(",")
        return reader

# print(last_line())


def last_line_index_signal():
    # retorna o ultimo index + 1
    with open(f"C:\\Projects\\cryptobot\\Data\\market.csv", "r",encoding="utf-8", newline='') as f:
        reader = f.readlines()[-1].split(",")
        return int(reader[1]) + 1

# print(last_line_index_signal())


def last_spot_dict():
    with open("C:\\Projects\\cryptobot\\Data\\market.csv", "r",encoding="utf-8", newline='') as f:
        reader = f.readlines()[-1].split(",")
        # ['40', '5142', 'TRUUSDT', 'New signal', '12-08 - 21:15', '20:40', 'new\r\n']
        spot = {
                "index": int(reader[0].rstrip()),
                "index_signal": int(reader[1].rstrip()),
                "date": str(reader[4].rstrip()), 
                "crypto_name": str(reader[2].rstrip()),
                "signal_type" : str(reader[3].rstrip()), 
                "hour_spot": str(reader[5].rstrip()),
                "buy_or_sell": str(reader[6].rstrip())
                }
        return spot
# print(last_spot_dict())