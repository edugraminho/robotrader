import os
import csv
import re
from datetime import datetime
import pandas as pd
from pathlib import Path, PurePath
import os
from datetime import datetime



ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
NOW = datetime.now().strftime("%d%m - %H:%M")
DATA_DIRECTORY = os.path.join(ROOT, "Data")

def insert_csv(value, index_signal, index):
    try:
        now = datetime.now().strftime("%d/%m-%H:%M")
        fieldname = [
            "index",
            "index_signal",
            "date",
            "crypto_name",
            "direction",
            "signal_type", 
            "status"
            ]

        new_crypto = re.search('(?<=I... )(.[^#]*USDT)', value)
        closed_crypto = re.search('(?<=#)(.[^#]*USDT)', value)

        direction = re.search('LONG|SHORT', value)

        closed_signal = re.search('Closed|All entry|All take-profit', value)

        crypto_name = None
        direction_type = None
        signal_type = None
        insert = False
        
        if new_crypto != None:
            crypto_name = new_crypto[0].strip()
            signal_type = "new"

        if closed_crypto != None:
            crypto_name = closed_crypto[0].strip().replace("/", "")
        
        if closed_signal != None:
            signal_type = "closed"
            insert = True

        if direction != None:
            direction_type = direction[0].strip().lower()
            insert = True
        else:
            direction = "-"

        with open(f"{DATA_DIRECTORY}\\market.csv", "a",encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldname)

            if (os.stat(f"{DATA_DIRECTORY}\\market.csv").st_size == 0):
                writer.writeheader()

            if insert:
                writer.writerow({
                    "index": int(index),
                    "index_signal": index_signal,
                    "date": now,
                    "crypto_name": crypto_name,
                    "direction": direction_type,
                    "signal_type": signal_type,  
                    "status": "-"
                })
                
    except Exception as e:
        print(
            f"Falha ao inserir CSV. Detalhes: {e}")


def last_line_index_signal():
    # retorna o ultimo index do sinal + 1
    try:
        with open(f"{DATA_DIRECTORY}/market.csv", "r",encoding="utf-8", newline='') as f:
            reader = f.readlines()[-1].split(",")
            return int(reader[1]) + 1
    except Exception as e:
        return ''

def last_spot_dict():
    try:
        with open(f"{DATA_DIRECTORY}/market.csv", "r",encoding="utf-8", newline='') as f:
            reader = f.readlines()[-1].split(",")
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
    except Exception as e:
        print(
            f"Falha ao retornar o ultimo dicionario de SPOTs. Detalhes: {e}")


def last_index():
    # retorna o ultimo index + 1
    try:
        with open(f"{DATA_DIRECTORY}/market.csv", "r",encoding="utf-8", newline='') as f:
            reader = f.readlines()[-1].split(",")
            return int(reader[0]) + 1

    except Exception as e:
        return ''



def last_line_status():
    # retorna a ultima crytpo
    try:
        with open(f"{DATA_DIRECTORY}/market.csv", "r",encoding="utf-8", newline='') as f:
            reader = f.readlines()[-1].split(",")
            return str(reader[6].strip())
    except Exception as e:
        print(
            f"Falha ao pegar o ultimo status. Detalhes: {e}")


def read_csv():
    csv_list = []
    with open(f"{DATA_DIRECTORY}/market.csv", "r",encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            csv_list.append(row)
    return csv_list

"""
def pay_a_percentage(balance):
    value = int(balance) * (1 - PURCHASE_PERCENTAGE / 100)
    return PURCHASE_VALUE 
    #return round(balance - value, 2)


def calculate_stop_limit(price):
    value = int(price * 100) * STOP_LOSS_PERCENTAGE / 100
    return round(price - (value / 100), 3)


def convert_to_int(str_balance):
    number = round(float(str_balance.split(" ")[0]), 2)

    if number < 0.5:
        return 0
    return number


def convert_balance_crypto_to_float(str_balance):
    # para nao arrendondar os numeros decimais. Ex: 0.59999
    try: 
        split_str = str_balance.split(" ")[0].split(".")
        number = split_str[0] + "." + split_str[1][:2]

        return float(number)
    except Exception as e:
        print(
            f"Falha ao converter balanco para float. Detalhes: {e}")


def convert_balance_crypto_to_stop(str_balance):
    try:
        split_str = str_balance.split(" ")[0].split(".")
        number = float(split_str[0] + "." + split_str[1][:2])

        if number < 10:
            return str(number)
        elif number < 100:
            return str(number)[:-1]
        return str(int(number))

    except Exception as e:
        print(
            f"Falha ao converter balanco stop. Detalhes: {e}")


def insert_csv_buy_or_sell(c_index, b_or_s):
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")
        ind = df.loc[lambda df: df['index'] == int(c_index)]
        df._set_value(ind.index[0],'buy_or_sell',b_or_s)
        df.to_csv(f"{DATA_DIRECTORY}/market.csv", index=False)

    except Exception as e:
            print(
                f"Falha na inserção do status de compra e venda no CSV. Detalhes: {e}")
"""