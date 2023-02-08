from pymongo import MongoClient
from Variables.config import *


def connect_db():
    client = MongoClient(URI)

    db = client.SignalsDb
    try:
        client.admin.command('ping')
        print("Conexão bem-sucedida!")
        collections_list = db.list_collection_names()

    except Exception as e:
        print(f"Falha ao conectar!  {e}")

    cll = db["cll"]

    return cll


def insert_new_signal_db(collection, data):

    if data is None:
        return (False, "")

    signal = collection.find_one({'_id': data['_id']})

    try:
        if not signal:
            collection.insert_one(data)
            return (True, data)
    except:
        return (False, "Error")

    return (False, "")


def get_last_insert(collection):
    # acessando o primeiro elemento
    return collection.find().sort('_id', -1).limit(1)[0]


def update_one(collection, id_obj, data):
    # Executando a atualização do banco
    status = collection.update_one(id_obj, data, upsert=False)
    return status


def delete_one(collection, _id):
    collection.delete_one({"_id":_id})

