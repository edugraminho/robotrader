import os
import csv
import re
import pandas as pd
from Variables.config import *


def insert_csv(value, date, index):
    try:
        fieldname = [
            "index",
            "date",
            "crypto_name",
            "direction",
            "signal_type", 
            "status",
            "order_id",
            "price_buy",
            "stop_price",
            "qtd"
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
            crypto_name = new_crypto[0].strip().upper()
            signal_type = "NEW"

        if closed_crypto != None:
            crypto_name = closed_crypto[0].strip().replace("/", "").upper()
        
        if closed_signal != None:
            signal_type = "CLOSED"
            insert = True

        if direction != None:
            direction_type = direction[0].strip().upper()
            insert = True


        with open(f"{DATA_DIRECTORY}/market.csv", "a",encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldname)

            if (os.stat(f"{DATA_DIRECTORY}/market.csv").st_size == 0):
                writer.writeheader()

            if insert:
                writer.writerow({
                    "index": index,
                    "date": date.strftime("%d-%m-%y %H:%M"),
                    "crypto_name": crypto_name,
                    "direction": direction_type,
                    "signal_type": signal_type
                })

                return True
            return False
                
    except Exception as e:
        print(f"Falha ao inserir CSV. Detalhes: {e}")
        pass


def last_line_index_signal():
    # retorna o ultimo index do sinal + 1
    try:
        with open(f"{DATA_DIRECTORY}/market.csv", "r",encoding="utf-8", newline='') as f:
            reader = f.readlines()[-1].split(",")
            return int(reader[1]) + 1
    except Exception as e:
        print(f'Error last_line_index_signal: {e}')
        pass

def last_spot_dict():
    try:
        with open(f"{DATA_DIRECTORY}/market.csv", "r",encoding="utf-8", newline='') as f:
            reader = f.readlines()[-1].split(",")
            spot = {
                    "index": int(reader[0].rstrip()),
                    "date": reader[1].rstrip(),
                    "crypto_name": str(reader[2].rstrip()), 
                    "direction": str(reader[3].rstrip()),
                    "signal_type" : str(reader[4].rstrip()), 
                    "status": str(reader[5].rstrip()),
                    "order_id": str(reader[6].rstrip()),
                    "price_buy":reader[7].rstrip(),
                    "stop_price":reader[8].rstrip(),
                    "qtd": str(reader[9].rstrip())
                    }
            return spot
    except Exception as e:
        print(
            f"Falha ao retornar o ultimo dicionario de SPOTs. Detalhes: {e}")
        pass


def last_index():
    # retorna o ultimo index + 1
    try:
        with open(f"{DATA_DIRECTORY}/market.csv", "r",encoding="utf-8", newline='') as f:
            reader = f.readlines()[-1].split(",")
            return int(reader[0])

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



def insert_csv_status(c_index, b_or_s, order_id=0, price_buy=0, stop_price=0, qtd=0):
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")
        ind = df.loc[lambda df: df['index'] == int(c_index)]
        if not ind.empty:
            df._set_value(ind.index[0],'status',b_or_s)
            df._set_value(ind.index[0],'order_id',order_id)
            df._set_value(ind.index[0],'price_buy',price_buy)
            df._set_value(ind.index[0],'stop_price',stop_price)
            df._set_value(ind.index[0],'qtd',qtd)


        df.to_csv(f"{DATA_DIRECTORY}/market.csv", index=False)

    except Exception as e:
        print(f"Falha na inserção do status. Erro: {e}")
        pass


def check_its_repeated(index):
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")
        ind = df.loc[lambda df: df['index'] == int(index)]
        return ind.empty

    except:
        return True
            
            

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


"""