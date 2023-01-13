from pymongo import MongoClient
from Variables.config import *



def connect_db():
    client = MongoClient(STR_CONNECTION)
    db = client.test
    # cloud_points_db = client['cloud_points']
    # beacon_logs_db = client['beacon_logs']
    # bad_condition_log_db = client['bad_condition_log']
    # auto_alloc_logs_db = client['auto_alloc_logs']
    # tablet_info_db = client['tablet_info']
    db.test.insert_many([{"a": 1, "b": 2}])
    print(db)
    print(client)