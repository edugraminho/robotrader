from pymongo import MongoClient
from Variables.config import *
from Libraries.logger import get_logger

logger = get_logger(__name__)


class MongoDb:
    def __init__(self):
        self.client = MongoClient(URI)
        self.db = self.client.SignalsDb
        self.collection = self.db["cll"]

    def test_connection_db(self):
        try:
            self.client.admin.command('ping')
            logger.info("Conexão bem-sucedida!")

        except Exception as e:
            logger.error(f"Falha ao conectar!  {e}")

    def update_one(self, id_obj, data):
        # Executando a atualização do banco
        return self.collection.update_one(id_obj, data, upsert=False)

    def delete_one(self, _id):
        self.collection.delete_one({"_id": _id})

    def find_all(self, query):
        return self.collection.find(query)

    def delete_old_date(self):
        "DROPA DADOS COM MAIS DE X DIAS DO BANCO"
        query = {
            "data": {
                "$lt": DATA_TO_DELETE_OLD_DATA_MONGODB
            }
        }
        status = self.collection.delete_many(query)


    def delete_all_db(self):
        self.collection.delete_many({})


    def find_one(self, query):
        return self.collection.find_one(query)
    
    def insert_one(self, query):
        return self.collection.insert_one(query)
