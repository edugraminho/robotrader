import pdb
import re
import pytz
from Variables.config import *
from Libraries.logger import get_logger

logger = get_logger(__name__)


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

                new_crypto = re.search("#(\w+)/", data.message)
                # closed_crypto = re.search('(?<=#)(.[^#]*USDT)', data.message)

                direction = re.search("\((\w+)\S*,", data.message)

                # closed_signal = re.search(
                #     'Closed|All entry|Cancelled', data.message)

                # all_take_profit = re.search('All take-profit', data.message)

                crypto_name = None
                direction_type = None
                signal_type = None
                insert = False

                if new_crypto != None:
                    crypto_name = new_crypto[1].strip().upper()
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

                if direction != None and reply_to == "":
                    direction_type = direction[1].strip().upper()
                    insert = True

                if insert:
                    signal_message = {
                        "_id": data.id,
                        "reply_to": reply_to,
                        "date": str(_date),
                        "crypto_name": f"{crypto_name}USDT",
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


'''

def last_spot_dict():
    try:
        with open(f"{DATA_DIRECTORY}/market.csv", "r", encoding="utf-8", newline='') as f:
            reader = f.readlines()[-1].split(",")
            spot = {
                "index": int(reader[0].rstrip()),
                "date": reader[1].rstrip(),
                "crypto_name": str(reader[2].rstrip()),
                "direction": str(reader[3].rstrip()),
                "signal_type": str(reader[4].rstrip()),
                "status": str(reader[5].rstrip()),
                "price_buy": reader[6].rstrip(),
                "stop_price": reader[7].rstrip(),
                "qty": str(reader[8].rstrip())
            }
            return spot
    except Exception as e:
        logger.error(e)
        pass


def csv_to_list():
    csv_list = []
    with open(f"{DATA_DIRECTORY}/market.csv", "r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            csv_list.append(row)
    return csv_list


def insert_csv_status(
        c_index, signal_type, status, direction, price_buy=0, stop_price=0, qty=0):
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")
        ind = df.loc[lambda df: df['index'] == int(c_index)]
        if not ind.empty:
            df._set_value(ind.index[0], 'signal_type', signal_type)
            df._set_value(ind.index[0], 'status', status)
            df._set_value(ind.index[0], 'direction', direction)
            # df._set_value(ind.index[0],'reply_to',reply_to)
            df._set_value(ind.index[0], 'price_buy', price_buy)
            df._set_value(ind.index[0], 'stop_price', stop_price)
            df._set_value(ind.index[0], 'qty', qty)

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
            qty = _df['qty'].values[0]

            if direction:
                return (direction, reply_to, int(qty))

        return ("", 0, 0)
    except Exception as e:
        print(e)
        return ("", 0, 0)


def check_all_spots_closed():
    try:
        df = pd.read_csv(f"{DATA_DIRECTORY}/market.csv")

        closed = df.loc[lambda df:
                        ((df["signal_type"] == "CLOSE") |
                         (df["signal_type"] == "ALL_TAKE_PROFIT"))
                        & (df.direction != "NOT_TRADED")]

        if not closed.empty:
            return (True, closed)

        return (False, '')
    except:
        return (False, '')



'''

