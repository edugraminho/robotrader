from pymongo import MongoClient
from Variables.config import *
from Libraries.logger import get_logger

logger = get_logger(__name__)


def connect_db():
    client = MongoClient(URI)

    db = client.SignalsDb
    try:
        client.admin.command('ping')
        logger.info("Conexão bem-sucedida!")
        collections_list = db.list_collection_names()

    except Exception as e:
        logger.error(f"Falha ao conectar!  {e}")

    cll = db["cll"]

    return cll


def insert_new_signal_db(collection, data):

    if data is None:
        return (False, "")

    try:
        for d in data:
            signal = collection.find_one({'_id': d['_id']})
            if not signal:
                collection.insert_one(d)

    except Exception as e:
        logger.error(e)
        raise e


def get_last_insert(collection):
    # acessando o primeiro elemento
    return collection.find().sort('_id', -1).limit(1)[0]


def update_one(collection, id_obj, data):
    # Executando a atualização do banco
    return collection.update_one(id_obj, data, upsert=False)


def delete_one(collection, _id):
    collection.delete_one({"_id":_id})


def find_all(collection, query):
    return collection.find(query)