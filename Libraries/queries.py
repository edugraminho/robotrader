
import pdb
from Variables.config import *
from Libraries.logger import get_logger
from Libraries.mongo_db import MongoDb

logger = get_logger(__name__)

mongo_db = MongoDb()

def update_one(_id, query):
    return mongo_db.update_one(_id, query)

def insert_new_signal_db(data):

    if data is None:
        return (False, "")

    try:
        for d in data:
            signal = mongo_db.find_one({'_id': d['_id']})
            if not signal:
                mongo_db.insert_one(d)

    except Exception as e:
        logger.error(e)
        raise e
    


def check_closing_orders_db():
    try:
        # Vai fechar ordens lancadas no dia atual do sinal
        query = {
            "$and": [
                {
                    "$or": [
                        {"signal_type": "CLOSE"},
                        {"signal_type": "ALL_TAKE_PROFIT"}
                    ]
                },
                {"direction": "OPEN_ORDER"},
                # Adiciona o filtro para a data atual
                {"date": {"$regex": f"^{CURRENT_DAY}"}}
            ]
        }

        new_closing_orders = mongo_db.find_all( query)

        if new_closing_orders:
            return (True, new_closing_orders)

        return (False, "")

    except Exception as e:
        logger.error("check_position_closing", e)
        return (False, "")


def open_orders_db():
    query = {
        "signal_type": "NEW", 
        "status": {
            "$in": ["BUY", "SELL"]
            }, 
        "direction": {
            "$in": ["LONG", "SHORT"]
            }
        }
    
    # print(mongo_db.collection.count_documents(query))

    return mongo_db.find_all(query)



def new_buy_orders():
    query = {
        "signal_type": "NEW", 
        "status": ""
    }

    return mongo_db.find_all(query)



