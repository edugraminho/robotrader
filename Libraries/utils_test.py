import os
import csv
import re
from pathlib import Path, PurePath
import os
from datetime import datetime
import math
import pandas as pd


TODAY = datetime.today().strftime("%d%m - %H:%M")
# ==================== CHROME ==========================
URL = "https://www.binance.com/"
URL_SIGNALS = "https://t.me/s/signalscryptoglobal"
URL_APK = "http://localhost:4723/wd/hub"

BROWSER_DIRECTORY = "C:\\Projects\\robotrader\\GoogleChromePortable\\App\\Chrome-bin\\chrome.exe"
CHROMEDRIVER_DIRECTORY = "C:\\Projects\\robotrader\\chromedriver\\chromedriver.exe"
# ======================================================

# =================== Timeout Robot ====================
DEFAULT_SELENIUM_TIMEOUT = '40 seconds'
DEFAULT_DOWNLOAD_TIMEOUT = '60 seconds'
# ======================================================

# ====================== DIRETÓRIOS LOCAIS ======================
ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
NOW = datetime.now().strftime("%d%m - %H:%M")
DATA_DIRECTORY = os.path.join(ROOT, "Data")
# ===============================================================

value = """꧁༺ 𝓢𝓒𝓐𝓛𝓟𝓘𝓝𝓖 300 ༻꧂

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

# value = '''
# Binance Futures, ByBit USDT
# #ADA/USDT All take-profit targets achieved 😎

# '''
# Binance Futures
#ZEN/USDT Closed due to opposite direction signal ⚠


# Binance Futures
#GTC/USDT All entry targets achieved

def insert_csv(value):
    now = datetime.now().strftime("%d/%m-%H:%M")
    fieldname = [
        "index",
        "index_signal",
        "date",
        "crypto_name",
        "direction",
        "signal_type", 
        "buy_or_sell",
        "status"
        ]

    new_crypto = re.search('(?<=I... )(.[^#]*USDT)', value)
    closed_crypto = re.search('(?<=#)(.[^#]*USDT)', value)

    direction = re.search('LONG|SHORT', value)

    closed_signal = re.search('Closed|All entry|All take-profit', value)


    crypto_name = None
    direction = None
    signal_type = None
    
    if new_crypto != None:
        crypto_name = new_crypto[0].strip()
        signal_type = "new"

    if closed_crypto != None:
        crypto_name = closed_crypto[0].strip().replace("/", "")
    
    if closed_signal != None:
        signal_type = "closed"

    if direction != None:
        direction = direction[0].strip()
    else:
        direction = "-"


insert_csv(value)

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


def buy_or_sell():
    df = pd.read_csv("C:\\Projects\\cryptobot\\Data\\markettest.csv")

    ind = df.loc[lambda df: df['index'] == 5081]
    print(ind.index[0])

    df._set_value(ind.index[0],'buy_or_sell','testa')

    df.to_csv("C:\\Projects\\cryptobot\\Data\\markettest.csv", index=False)


# buy_or_sell()


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


def last_index():
    # retorna o ultimo index + 1
    with open("C:\\Projects\\cryptobot\\Data\\market.csv", "r",encoding="utf-8", newline='') as f:
        reader = f.readlines()[-1].split(",")
        return int(reader[0])

# print(last_index())



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
