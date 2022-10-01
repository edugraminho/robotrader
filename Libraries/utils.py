import os
import csv
import re
import time 
import pandas as pd
from Variables.config import *
from Libraries.logger import get_logger

logger = get_logger(__name__)

def insert_csv(value, index):
    try:
        fieldname = [
            "index",
            "date",
            "crypto_name",
            "direction",
            "signal_type", 
            "status",
            "price_buy",
            "stop_price",
            "qtd"
            ]

        new_crypto = re.search('(?<=I... )(.[^#]*USDT)', value)
        closed_crypto = re.search('(?<=#)(.[^#]*USDT)', value)

        direction = re.search('LONG|SHORT', value)

        closed_signal = re.search('Closed|All entry|All take-profit', value)

        all_take_profit = re.search('All take-profit', value)

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


        with open(f"{DATA_DIRECTORY}/market.csv", "a",encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldname)

            if (os.stat(f"{DATA_DIRECTORY}/market.csv").st_size == 0):
                writer.writeheader()

            #Verifica a ultima cripto para nao inserir repetido
            with open(f"{DATA_DIRECTORY}/market.csv", "r") as f:
                last_crypto = f.readlines()[-1].split(",")
                last_crypto_name = last_crypto[2]
                last_signal_type = last_crypto[4]
                if last_crypto_name == crypto_name and last_signal_type == signal_type:
                    insert = False

            if insert:
                writer.writerow({
                    "index": index,
                    "date": str(NOW),
                    "crypto_name": crypto_name,
                    "direction": direction_type,
                    "signal_type": signal_type
                })

                return True
            return False
                
    except Exception as e:
        logger.error(f"Falha ao inserir CSV. Detalhes: {e}")
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
                    "price_buy":reader[6].rstrip(),
                    "stop_price":reader[7].rstrip(),
                    "qtd": str(reader[8].rstrip())
                    }
            return spot
    except Exception as e:
        logger.error(
            f"Falha ao retornar o ultimo dicionario de SPOTs. Detalhes: {e}")
        pass


def csv_to_list():
    csv_list = []
    with open(f"{DATA_DIRECTORY}/market.csv", "r",encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            csv_list.append(row)
    return csv_list



def insert_csv_status(
    c_index, signal_type, status, direction, price_buy=0, stop_price=0, qtd=0):
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")
        ind = df.loc[lambda df: df['index'] == int(c_index)]
        if not ind.empty:
            df._set_value(ind.index[0],'signal_type', signal_type)
            df._set_value(ind.index[0],'status', status)
            df._set_value(ind.index[0],'direction', direction)
            # df._set_value(ind.index[0],'reply_to',reply_to)
            df._set_value(ind.index[0],'price_buy', price_buy)
            df._set_value(ind.index[0],'stop_price', stop_price)
            df._set_value(ind.index[0],'qtd', qtd)


        df.to_csv(f"{DATA_DIRECTORY}/market.csv", index=False)

    except Exception as e:
        logger.error(f"Falha na inserção do status. Erro: {e}")
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

        return ("", 0, 0)
    except Exception as e:
        print(e)
        return ("", 0, 0)
                       

def check_all_spots_closed():
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")

        closed = df.loc[lambda df: 
            ((df["signal_type"] == "CLOSE") | (df["signal_type"] == "ALL_TAKE_PROFIT")) 
            & (df.direction != "NOT_TRADED")]
            
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



def check_position_closing(all_positions):
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")

        for positions in all_positions:
            close = df.loc[
                lambda df: ((df['signal_type'] == 'CLOSE') | (df['signal_type'] == 'ALL_TAKE_PROFIT'))
                            & (df['direction'] == 'OPEN_ORDER') 
                            & (df['crypto_name'] == positions["symbol"])]

            # close = df.loc[
            #     lambda df: (df['crypto_name'] == positions["symbol"]) 
            #         & (df['direction'] == 'OPEN_ORDER') 
            #         & (df['status'] != 'SELL')]

            if not close.empty:
                # adiciona a direcao do spot na coluna
                df._set_value(close.index[0],'direction', positions["positionSide"])
                df.to_csv(f"{DATA_DIRECTORY}/market.csv", index=False)

                return (True, close, positions["positionSide"])

        return (False, "", "")

    except Exception as e:
        logger.error("check_position_closing", e) 
        return (False, "")
