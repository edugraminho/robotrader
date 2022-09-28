import os
import csv
import re
import pandas as pd
from Variables.config import *


def insert_csv(value, date, index, direction_closed, reply_to_index, qtd=0):
    try:
        fieldname = [
            "index",
            "date",
            "crypto_name",
            "direction",
            "signal_type", 
            "status",
            "reply_to",
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
            direction_type = direction_closed

        if direction != None:
            direction_type = direction[0].strip().upper()
            insert = True


        with open(f"{DATA_DIRECTORY}/market.csv", "a",encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldname)

            if (os.stat(f"{DATA_DIRECTORY}/market.csv").st_size == 0):
                writer.writeheader()

            #Verifica a ultima cripto para nao inserir repetido
            with open(f"{DATA_DIRECTORY}/market.csv", "r") as f:
                last_crypto_name = f.readlines()[-1].split(",")[2]
                if last_crypto_name == crypto_name:
                    insert = False

            if insert:
                writer.writerow({
                    "index": index,
                    "date": date.strftime("%d-%m %H:%M"),
                    "crypto_name": crypto_name,
                    "direction": direction_type,
                    "signal_type": signal_type,
                    "reply_to": reply_to_index,
                    "qtd": qtd,

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
                    "reply_to": str(reader[6].rstrip()),
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


def last_crypto_name():
    with open(f"{DATA_DIRECTORY}/market.csv", "r",encoding="utf-8", newline='') as f:
        reader = f.readlines()[-1].split(",")
        return reader[2]


def read_csv():
    csv_list = []
    with open(f"{DATA_DIRECTORY}/market.csv", "r",encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            csv_list.append(row)
    return csv_list



def insert_csv_status(
    c_index, signal_type, status, direction, reply_to=0, price_buy=0, stop_price=0, qtd=0, error=""):
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")
        ind = df.loc[lambda df: df['index'] == int(c_index)]
        if not ind.empty:
            df._set_value(ind.index[0],'signal_type',signal_type)
            df._set_value(ind.index[0],'status',status)
            df._set_value(ind.index[0],'direction',direction)
            df._set_value(ind.index[0],'reply_to',reply_to)
            df._set_value(ind.index[0],'price_buy',price_buy)
            df._set_value(ind.index[0],'stop_price',stop_price)
            df._set_value(ind.index[0],'qtd',qtd)
            df._set_value(ind.index[0],'error',error)


        df.to_csv(f"{DATA_DIRECTORY}/market.csv", index=False)

    except Exception as e:
        print(f"Falha na inserção do status. Erro: {e}")
        pass


def check_index_repeated(index):
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")
        ind = df.loc[lambda df: df['index'] == int(index)]
        return ind.empty

    except:
        return True
            
def check_reply_to(message):
    try:
        if message.reply_to:
            reply_to = message.reply_to.reply_to_msg_id

            df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")
            _df = df.loc[lambda df: df['index'] == int(reply_to)]
            direction = _df['direction'].values[0]
            qtd = _df['qtd'].values[0]
            if direction:
                return (direction, reply_to, int(qtd))
            
        return ("NOT_TRADED", 0, 0)
    except:
        return ("NOT_TRADED", 0, 0)
                       

def check_all_closed_spots():
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")
        _df = df.loc[lambda df: df['direction'] != 'NOT_TRADED']
        closed = _df.loc[lambda df: df['signal_type'] == 'CLOSED']
            
        if not closed.empty:
            return (True, closed)
            
        return (False, '')
    except:
        return (False, '')


def check_all_stop_loss():
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")
        _df = df.loc[lambda df: df['status'] == 'BUY']
        stop_long = _df.loc[lambda df: df['direction'] == 'LONG']
        stop_short = _df.loc[lambda df: df['direction'] == 'SHORT']
            
        if not stop_long.empty:
            return (True, stop_long)

        if not stop_short.empty:
            return (True, stop_short)
            
        return (False, "")
    except:
        return (False, "")
